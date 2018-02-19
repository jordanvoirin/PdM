#%% Script to acquire images average over nbrImgAveraging images and save them into fits file

from ximea import xiapi
import datetime
import functionsXimea as fX
import winsound
import numpy as np

#%%instanciation --------------------------------------------------------------
#number of image to average
nbrImgAveraging = 5000
numberOfFinalImages = 1

#Cropping information
sizeImg = 256

#Parameter of camera and saving
folderPathCropped = 'C:/Users/Jojo/Desktop/LucPD/cropped/'
darkFolderPathCropped = 'C:/Users/Jojo/Desktop/LucPD/dark/cropped/'
folderPathFull = 'C:/Users/Jojo/Desktop/LucPD/full/'
darkFolderPathFull = 'C:/Users/Jojo/Desktop/LucPD/dark/full/'
nameCamera = 'Ximea'
focusPos = 11.55

#Sound
duration = 1000  # millisecond
freq = 2000  # Hz

#initial guess for the fit depending on the position of the beam in the CCD
initial_guess = [250, 679, 710, 3, 3]

#------------------------------------------------------------------------------
#%% data acquisition ----------------------------------------------------------

#Opening the connection to the camera
cam = xiapi.Camera()
cam.open_device()
cam.set_imgdataformat('XI_MONO8') #XIMEA format 8 bits per pixel
cam.set_gain(0)

img = xiapi.Image()
if cam.get_acquisition_status() == 'XI_OFF':
    cam.start_acquisition()
#%% exposition
cond = 1
while bool(cond):
    source = ''
    winsound.Beep(freq, duration)
    source = int(raw_input('Is the source turned on and at focus point (usually %5.3f mm) (yes = 1) ? '%focusPos))
    if source == 1:
        cond = 0
    else:
        print 'Please turn on the source and place the camera on the focus point (%5.3f mm)'%focusPos

if bool(source):
    #Set exposure time
    cam.set_exposure(fX.determineUnsaturatedExposureTime(cam,img,[1,10000],1))
    #get centroid
    centroid = fX.acquirePSFCentroid(cam,img,initial_guess)
    print 'centroid at (%d, %d)' %(centroid[0],centroid[1])

#%%Acquire images at different camera position

acquire = 1
while bool(acquire):
    cond = 1
    while bool(cond):
        dark = ''
        winsound.Beep(freq, duration)
        dark = int(raw_input('Is the source turned off (yes = 1) ? '))
        if dark == 1:
            cond = 0
        else:
            print 'Please shut down the source.'

    winsound.Beep(freq, duration)
    pos = float(raw_input('What is the position of the camera in mm focused (%5.3f mm) dephase 2Pi (pos+ = %5.3f mm, pos- = %5.3f) ? '%(focusPos,focusPos+3.19,focusPos-3.19)))

    if bool(dark):
        print 'Acquiring dark image...'
        # Acquire dark images
        [darkData,stdDarkData] = fX.acquireImg(cam,img,nbrImgAveraging)
        print 'Cropping'
        [darkdataCropped,stddarkDataCropped] = fX.cropAroundPSF(darkData,stdDarkData,centroid,sizeImg,sizeImg)
        print 'saving'        
        fX.saveImg2Fits(datetime.datetime.today(),darkFolderPathCropped,nameCamera,darkdataCropped,stddarkDataCropped,str(int(np.around(100*(focusPos-pos),0))),nbrImgAveraging)
        fX.saveImg2Fits(datetime.datetime.today(),darkFolderPathFull,nameCamera,darkData,stdDarkData,str(int(np.around(100*(focusPos-pos),0))),nbrImgAveraging)

    #Acquire images -------------------------
    cond = 1
    while bool(cond):
        source = ''
        winsound.Beep(freq, duration)
        source = int(raw_input('Is the source turned on (yes = 1) ? '))
        if source == 1:
            cond = 0
        else:
            print 'Please place turn on the camera'

    if bool(source):
        print 'Acquiring images...'
        # Acquire focused images
        for iImg in range(numberOfFinalImages):
            imgNumber = iImg+1
            print 'Acquiring Image %d'%imgNumber
            [data,stdData] = fX.acquireImg(cam,img,nbrImgAveraging)
            print 'Cropping'
            [dataCropped,stdDataCropped] = fX.cropAndCenterPSF(data-darkData,stdData+stdDarkData,sizeImg,initial_guess)
            print 'Saving'
            fX.saveImg2Fits(datetime.datetime.today(),folderPathCropped,nameCamera,dataCropped,stdDataCropped,str(int(np.around(100*(focusPos-pos),0))),nbrImgAveraging)
            fX.saveImg2Fits(datetime.datetime.today(),folderPathFull,nameCamera,data-darkData,stdData+stdDarkData,str(int(np.around(100*(focusPos-pos),0))),nbrImgAveraging)

    cond = 1
    while bool(cond):
        acquire = ''
        winsound.Beep(freq, duration)
        acquire = int(raw_input('Do you want to acquire at an other camera position (yes = 1, no = 0) ? '))
        if acquire == 1:
            cond = 0
        elif acquire == 0:
            cond = 0
        else:
             print 'please answer with 0 or 1 for no or yes, respectively'


##Stop the acquisition
cam.stop_acquisition()
cam.close_device()

print 'Acquisition finished'

#%% Script to acquire images average over nbrImgAveraging images and save them into fits file

from ximea import xiapi
import datetime
import functionsXimea as fX

#%%instanciation --------------------------------------------------------------
#number of image to average
nbrImgAveraging = 10000
numberOfFinalFocusedImages = 1
numberOfFinalDefocusedImages = 1

#Cropping information
sizeImgX = 256
sizeImgY = 256
initial_guess = (250,711,482,5,5)

#Parameter of camera and saving
folderPath = '../../data/PD/'

nameCamera = 'Ximea'


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

#Set exposure time
cam.set_exposure(fX.determineUnsaturatedExposureTime(cam,img,1))
#Acquire dark images for background correction---

cond = 1
while bool(cond):
    dark = ''
    dark = int(raw_input('Is the source turned off and the camera on the focus point (yes = 1) ? '))
    if dark == 1:
        cond = 0
    else:
        print 'Please shut down the source and/or place the camera on the focus point.'
    
if bool(dark):
    print 'Acquiring dark focused images...'
    # Acquire focused images
    [darkData,stdDarkData] = fX.acquireImg(cam,img,nbrImgAveraging)
    fX.saveImg2Fits(datetime.datetime.today(),folderPath,nameCamera,darkData,stdDarkData,'DarkDefocus','3.17',nbrImgAveraging)
    
#Acquire focused images -------------------------
cond = 1
while bool(cond):
    focus = ''
    focus = int(raw_input('Is the camera on the focus point (yes = 1)? '))
    if focus == 1:
        cond = 0
    else:
        print 'Please place the camera on the focus point (11.5 mm)'
    
if bool(focus):
    print 'Acquiring focused images...'
    # Acquire focused images
    for iImg in range(numberOfFinalFocusedImages):
        [data,stdData] = fX.acquireImg(cam,img,nbrImgAveraging)
        [data,stdData] = fX.cropAroundPSF(data-darkData,stdData+stdDarkData,sizeImgX,sizeImgY,initial_guess)
        fX.saveImg2Fits(datetime.datetime.today(),folderPath,nameCamera,data,stdData,'Focus','0',nbrImgAveraging)


#Acquire defocused images -----------------------

cond = 1
while bool(cond):
    dark = ''
    dark = int(raw_input('Is the source turned off and the camera on the defocus point (yes = 1) ? '))
    if dark == 1:
        cond = 0
    else:
        print 'Please shut down the source and/or place the camera on the defocus point.'
    
if bool(dark):
    print 'Acquiring dark defocused images...'
    # Acquire focused images
    [darkData,stdDarkData] = fX.acquireImg(cam,img,nbrImgAveraging)
    fX.saveImg2Fits(datetime.datetime.today(),folderPath,nameCamera,darkData,stdDarkData,'DarkDefocus','3.17',nbrImgAveraging)
    
cond = 1
while bool(cond):
    focus = ''
    focus = int(raw_input('Is the camera on the defocus point (yes = 1)? '))
    if focus==1:
        cond = 0
    else:
        print 'Please place the camera on the defocus point'
        
if focus == 1:
    focus = 0
else:
    focus = 1
        
if not bool(focus):
    print 'Acquiring defocused images background corrected...'
    for iImg in range(numberOfFinalDefocusedImages):
        [data,stdData] = fX.acquireImg(cam,img,nbrImgAveraging)
        [data,stdData] = fX.cropAroundPSF(data-darkData,stdData+stdDarkData,sizeImgX,sizeImgY,initial_guess)
        fX.saveImg2Fits(datetime.datetime.today(),folderPath,nameCamera,data,stdData,'Focus','0',nbrImgAveraging)

##Stop the acquisition
cam.stop_acquisition()
cam.close_device()


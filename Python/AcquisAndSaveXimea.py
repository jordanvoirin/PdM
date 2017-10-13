#%% Script to acquire images average over nbrImgAveraging images and save them into fits file

from ximea import xiapi
import datetime
import functionsXimea as fX
import winsound
import numpy as np
#%%instanciation --------------------------------------------------------------
#number of image to average
nbrImgAveraging = 5000
numberOfFinalFocusedImages = 10
numberOfFinalDefocusedImages = 10

#Cropping information
sizeImgX = 256
sizeImgY = 256
initial_guess = (250,708,481,3,3)

#Parameter of camera and saving
folderPath = '../../data/PD/'
darkFolderPath = '../../data/dark/'
nameCamera = 'Ximea'

#Sound
duration = 2000  # millisecond
freq = 2000  # Hz

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
cond = 1
while bool(cond):
    focus = ''
    winsound.Beep(freq, duration)
    focus = int(raw_input('Is the source turned on and the camera on the focus point (yes = 1) ? '))
    if focus == 1:
        cond = 0
    else:
        print 'Please place the camera on the focus point (11.5 mm)'
        
if bool(focus):        
    #Set exposure time
    cam.set_exposure(fX.determineUnsaturatedExposureTime(cam,img,1))
    #Acquire dark images for background correction---

cond = 1
while bool(cond):
    dark = ''
    winsound.Beep(freq, duration)
    dark = int(raw_input('Is the source turned off and the camera on the focus point (yes = 1) ? '))
    if dark == 1:
        cond = 0
    else:
        print 'Please shut down the source and/or place the camera on the focus point.'

pos = float(raw_input('What is the position of the camera in mm ? '))

if bool(dark):
    print 'Acquiring dark focused image...'
    # Acquire focused images
    [darkData,stdDarkData] = fX.acquireImg(cam,img,nbrImgAveraging)
    fX.saveImg2Fits(datetime.datetime.today(),darkFolderPath,nameCamera,darkData,stdDarkData,'DarkFocus',str(pos-11.5),nbrImgAveraging)
    
#Acquire focused images -------------------------
cond = 1
while bool(cond):
    focus = ''
    winsound.Beep(freq, duration)
    focus = int(raw_input('Is the source turned on and the camera on the focus point (yes = 1) ? '))
    if focus == 1:
        cond = 0
    else:
        print 'Please place the camera on the focus point (11.5 mm)'

pos = float(raw_input('What is the position of the camera in mm ? '))
    
if bool(focus):
    print 'Acquiring focused images...'
    # Acquire focused images
    for iImg in range(numberOfFinalFocusedImages):
        print 'Acquiring Image %d'%iImg
        [data,stdData] = fX.acquireImg(cam,img,nbrImgAveraging)
        print 'Cropping'
        [data,stdData] = fX.cropAroundPSF(data-darkData,stdData+stdDarkData,sizeImgX,sizeImgY,initial_guess)
        print 'Saving'
        fX.saveImg2Fits(datetime.datetime.today(),folderPath,nameCamera,data,stdData,'Focus',str(pos-11.5),nbrImgAveraging)


#Acquire defocused images -----------------------

cond = 1
while bool(cond):
    dark = ''
    winsound.Beep(freq, duration)
    dark = int(raw_input('Is the source turned off and the camera on the defocus point (yes = 1) ? '))
    if dark == 1:
        cond = 0
    else:
        print 'Please shut down the source and/or place the camera on the defocus point.'
        
pos = float(raw_input('What is the position of the camera in mm ? '))

if bool(dark):
    print 'Acquiring dark defocused images...'
    # Acquire focused images
    [darkData,stdDarkData] = fX.acquireImg(cam,img,nbrImgAveraging)
    fX.saveImg2Fits(datetime.datetime.today(),darkFolderPath,nameCamera,darkData,stdDarkData,'DarkDefocus',str(pos-11.5),nbrImgAveraging)
    
cond = 1
while bool(cond):
    focus = ''
    winsound.Beep(freq, duration)
    focus = int(raw_input('Is the source turned on and the camera on the defocus point (yes = 1) ? '))
    if focus==1:
        cond = 0
    else:
        print 'Please place the camera on the defocus point'

pos = float(raw_input('What is the position of the camera in mm ? '))
       
if focus == 1:
    focus = 0
else:
    focus = 1
        
if not bool(focus):
    print 'Acquiring defocused images background corrected...'
    for iImg in range(numberOfFinalDefocusedImages):
        print 'Acquiring Image %d'%iImg
        [data,stdData] = fX.acquireImg(cam,img,nbrImgAveraging)
        print 'Cropping'
        [data,stdData] = fX.cropAroundPSF(data-darkData,stdData+stdDarkData,sizeImgX,sizeImgY,initial_guess)
        print 'Saving'
        fX.saveImg2Fits(datetime.datetime.today(),folderPath,nameCamera,data,stdData,'Focus',str(pos-11.5),nbrImgAveraging)

##Stop the acquisition
cam.stop_acquisition()
cam.close_device()


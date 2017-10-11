
##Script to compute the FWHM of the beam on the camera averaging 
 #over "nbrImgAveraging" images and see which position minimizes it.

from ximea import xiapi
import numpy as np
from matplotlib import pyplot  as plt
import scipy.optimize as opt
import datetime
import functionsXimea as fX
#%% instanciation 

#create the matrix grid of the detector CCD
x = np.linspace(0,1280,1280)
y = np.linspace(0,1024,1024)
x, y = np.meshgrid(x, y)

#initial guess for the fit depending on the position of the beam in the CCD
initial_guess = (255,711,482,5,5)

#number of image to average
nbrImgAveraging = 10

#%%data acquisition and treatment

#create instance for first connected camera 
cam = xiapi.Camera()
#start communication
print('Opening camera...')
cam.open_device()
#settings
cam.set_imgdataformat('XI_MONO8') #XIMEA format 8 bits per pixel
cam.set_gain(0)
#create instance of Image to store image data and metadata
img = xiapi.Image()
#start data acquisition
print('Starting data acquisition...')
if cam.get_acquisition_status() == 'XI_OFF':
         cam.start_acquisition()
         
cam.set_exposure(fX.determineUnsaturatedExposureTime(cam,img,1))

#instanciation for the while loop
answer ='y'
i=0
relativePos = []
data = []
data_fitted = []
FWHMx = []
FWHMy = []
x0 = []
y0 = []
sigmaX0 = []
sigmaY0 = []

while answer == 'y':
    
    try:
        relativePos.append(float(raw_input('What is the position on the screw [mm] ? ')))
    except ValueError:
        print('Not a float number')
        
    #get data and pass them from camera to img
    cam.get_image(img)
    #create numpy array with data from camera. Dimensions of array are determined
    #by imgdataformat
    tmpData = [];
    for iImg in range(nbrImgAveraging) :
        cam.get_image(img)
        tmpData.append(img.get_image_data_numpy())
    
    tmpData = np.array(tmpData)
    
    data.append(np.nanmean(tmpData,0))

    #Fit the img data on the 2D Gaussian to compute the FWHM
    print('Fitting 2D Gaussian...')
    popt, pcov = opt.curve_fit(fX.TwoDGaussian, (x,y), data[i].ravel(), p0 = initial_guess)
    print('Fitting done')
    
    FWHMx.append(2*np.sqrt(2*np.log(2))*popt[3])
    FWHMy.append(2*np.sqrt(2*np.log(2))*popt[4])
    x0.append(popt[1])
    sigmaX0.append(popt[3])
    y0.append(popt[2])
    sigmaY0.append(popt[4])
    
    print 'Fig %d : FWHM x = %3.2f, FWHM y  = %3.2f' %(i,FWHMx[i],FWHMy[i])
    
    data_fitted.append(TwoDGaussian((x, y), *popt).reshape(1024, 1280))
    
    #plot the beamspot
    fig, ax = plt.subplots(1, 1)
    ax.imshow(data[i], cmap=plt.cm.jet,origin='bottom',
        extent=(x.min(), x.max(), y.min(), y.max()))
    ax.contour(x, y, data_fitted[i], 5, colors='w',linewidths=0.8)
    plt.xlim( (popt[1]-4*popt[3], popt[1]+4*popt[3]) )
    plt.ylim( (popt[2]-4*popt[4], popt[2]+4*popt[4]) )
    plt.show()
    
    #ask if the person wants to acquire a new image to improve the alignement
    pressedkey = raw_input('Do you want to acquire an other image [y (yes) or n (no)]: ')
    if (pressedkey =='n'):
        answer = pressedkey
    #increase i
    i+=1

#stop data acquisition
print('Stopping acquisition...')
cam.stop_acquisition()

#stop communication
cam.close_device()

#convert list to np.array
relativePos = np.array(relativePos)
data = np.array(data)
FWHMx = np.array(FWHMx)
FWHMy = np.array(FWHMy)
x0 = np.array(x0)
y0 = np.array(y0)
sigmaX0 = np.array(sigmaX0)
sigmaY0 = np.array(sigmaY0)

#plot the FWHM vs. relPos
fig, ax = plt.subplots(1,1)
ind = np.argsort(relativePos)
ax.plot(relativePos[ind],FWHMx[ind])
ax.set_xlabel('Position [mm]')
ax.set_ylabel('FWHM [px]')
ax.grid()

indOfMinFWHM = np.argmin(np.sqrt(FWHMx**2+FWHMy**2))

fig, axarr = plt.subplots(1,np.size(data,0))
#plot all the images besides each other
for iImg in ind:
    axarr[iImg].imshow(data[iImg], cmap=plt.cm.jet,origin='bottom',
        extent=(x.min(), x.max(), y.min(), y.max()))
#    axarr[iImg].contour(x, y, data_fitted[iImg], 5, colors='w',linewidths=0.8)
    axarr[iImg].set_xlim( (x0[iImg]-12, x0[iImg]+12) )
    axarr[iImg].set_ylim( (y0[iImg]-12, y0[iImg]+12) )
    axarr[iImg].set_yticklabels('',visible=False)
    axarr[iImg].set_xticklabels('',visible=False)
    axarr[iImg].set_title('%5.3f mm'%relativePos[iImg],fontsize=8)
    if iImg == indOfMinFWHM:
        axarr[iImg].set_frame_on(True)
        for pos in ['top', 'bottom', 'right', 'left']:
            axarr[iImg].spines[pos].set_edgecolor('r')
            axarr[iImg].spines[pos].set_linewidth(2)
    else:
        axarr[iImg].set_frame_on(False)
plt.show()

#save data
date = datetime.datetime.today()
np.save('../data/alignement/'+date.strftime('%Y%m%d%H%M%S')+'data.npy',data)
np.save('../data/alignement/'+date.strftime('%Y%m%d%H%M%S')+'relativePos.npy',relativePos)
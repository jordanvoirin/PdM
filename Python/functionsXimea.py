import numpy as np
import pyfits
import os
import scipy.optimize as opt
#%% Functions -----------------------------------------------------------------


#Create and save .fits from numpy array
def saveImg2Fits(date,folderPath,Detector,data,stdData,pos,nbrAveragingImg):
    
    #date : datetime at which the data where taken
    #folderPath : where to save the data$
    #Detector : name of detector (ex:Ximea)
    #data : np.array containing the image
    #stdData: np.array containing the error on each pixel
    #focusType : 1 (focused) or 0 (defocused)

    imgHdu = pyfits.PrimaryHDU(data)
    stdHdu = pyfits.ImageHDU(stdData,name = 'imgStdData')
    hdulist = pyfits.HDUList([imgHdu,stdHdu])
    
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath)
    
    hdulist.writeto(folderPath + date.strftime('%Y%m%d%H%M%S')+'_'+Detector+'_'+pos+'.fits')
        
def acquireImg(cam,img,nbrImgAveraging):
    imgData = np.zeros([1024,1280])
    stdData = np.zeros([1024,1280])
    for iImg in range(nbrImgAveraging) :
        #print iImg
        cam.get_image(img)
        imgTmpData = img.get_image_data_numpy()
        imgData[:,:] += imgTmpData
        stdData += imgTmpData*imgTmpData
    
    stdData = np.sqrt((stdData-imgData*imgData/nbrImgAveraging)/(nbrImgAveraging-1))/(np.sqrt(nbrImgAveraging))
    imgData = imgData/nbrImgAveraging
    
    return [imgData,stdData]
    
    
def determineUnsaturatedExposureTime(cam,img,precision):
     exposureTimes = [1,500]
     if cam.get_acquisition_status() == 'XI_OFF':
         cam.start_acquisition()
         
     while np.absolute(np.diff(exposureTimes))>precision:
         expTime2check = int(np.round(np.nanmean(exposureTimes)))
         print 'Try expTime : %d [us]' %expTime2check
         cam.set_exposure(expTime2check)
         data = acquireImg(cam,img,200)[0]
         
         if np.sum(data>250)>1:
             exposureTimes[1] = int(np.ceil(np.nanmean(exposureTimes)))
         else:
             exposureTimes[0] = int(np.floor(np.nanmean(exposureTimes)))
         print 'exposure time between %d and %d' %(exposureTimes[0],exposureTimes[1])
         
     return int(np.floor(np.nanmean(exposureTimes)))
 
def TwoDGaussian((x, y), A, yo, xo, sigma_y, sigma_x):
    g = A*np.exp( - ((x-xo)**2/(2*sigma_x**2) + ((y-yo)**2)/(2*sigma_y**2)))
    return g.ravel()
    
def getPSFCentroid(cam,img,initialGuessFit):
    #create the matrix grid of the detector CCD
    x = np.linspace(0,1280,1280)
    y = np.linspace(0,1024,1024)
    x, y = np.meshgrid(x, y)
    data = acquireImg(cam,img,200)[0]
    print('Fitting 2D Gaussian...')
    popt, pcov = opt.curve_fit(TwoDGaussian, (x,y), data.ravel(), p0 = initialGuessFit)
    print('Fitting done')
    return [popt[2],popt[1]]
 
def cropAroundPSF(data,stdData,centroid,sizeX,sizeY,):
    
    pxX = [int(np.floor(centroid[0])-np.ceil(sizeX/2)),int(np.floor(centroid[0])+np.ceil(sizeX/2))]
    pxY = [int(np.floor(centroid[1])-np.ceil(sizeY/2)),int(np.floor(centroid[1])+np.ceil(sizeY/2))]   
    
    dataCropped = data[pxY[0]:pxY[1],pxX[0]:pxX[1]]
    
    stdDataCropped = stdData[pxY[0]:pxY[1],pxX[0]:pxX[1]]
    
    return [dataCropped,stdDataCropped]
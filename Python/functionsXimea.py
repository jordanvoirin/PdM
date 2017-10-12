import numpy as np
import pyfits
import os
import scipy.optimize as opt
#%% Functions -----------------------------------------------------------------


#Create and save .fits from numpy array
def saveImg2Fits(date,folderPath,Detector,data,stdData,Type,pos,nbrAveragingImg):
    
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
    
    hdulist.writeto(folderPath + date.strftime('%Y%m%d%H%M%S')+'_'+Detector+'_'+Type+'_'+pos+'.fits')
        
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
 
def TwoDGaussian((x, y), A, xo, yo, sigma_x, sigma_y):
    g = A*np.exp( - ((x-xo)**2/(2*sigma_x**2) + ((y-yo)**2)/(2*sigma_y**2)))
    return g.ravel() 
 
def cropAroundPSF(data,stdData,sizeX,sizeY,initialGuessFit):
    
    x = np.linspace(0,np.size(data,1),np.size(data,1))
    y = np.linspace(0,np.size(data,0),np.size(data,0))
    x, y = np.meshgrid(x, y)
    
    print('Fitting 2D Gaussian...')
    popt, pcov = opt.curve_fit(TwoDGaussian, (x,y), data.ravel(), p0 = initialGuessFit)
    print('Fitting done')
    
    dataCropped = data[np.floor(popt[0])-np.ceil(sizeY/2):np.ceil(popt[0])+np.ceil(sizeY/2), \
                    np.floor(popt[1])-np.ceil(sizeX/2):np.ceil(popt[1])+np.ceil(sizeX/2)]
    
    stdDataCropped = stdData[np.floor(popt[0])-np.ceil(sizeY/2):np.floor(popt[0])+np.ceil(sizeY/2), \
                    np.floor(popt[1])-np.ceil(sizeX/2):np.floor(popt[1])+np.ceil(sizeX/2)]
    
    return [dataCropped,stdDataCropped]
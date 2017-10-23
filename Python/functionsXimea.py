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
    #pos : the position of the camera on the sliding holder in mm

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


def determineUnsaturatedExposureTime(cam,img,exposureLimit,precision):
     exposureTimes = exposureLimit
     if cam.get_acquisition_status() == 'XI_OFF':
         cam.start_acquisition()

     while np.absolute(np.diff(exposureTimes))>precision:
         expTime2check = int(np.round(np.nanmean(exposureTimes)))
         print 'Try expTime : %d [us]\n' %expTime2check
         cam.set_exposure(expTime2check)
         data = acquireImg(cam,img,10)[0]

         if np.sum(data>250)>1:
             exposureTimes[1] = int(np.ceil(np.nanmean(exposureTimes)))
         else:
             exposureTimes[0] = int(np.floor(np.nanmean(exposureTimes)))
         print 'exposure time between %d and %d \n' %(exposureTimes[0],exposureTimes[1])

     return int(np.floor(np.nanmean(exposureTimes)))

def TwoDGaussian((x, y), A, yo, xo, sigma_y, sigma_x):
    g = A*np.exp( - ((x-xo)**2/(2*sigma_x**2) + ((y-yo)**2)/(2*sigma_y**2)))
    return g.ravel()

def acquirePSFCentroid(cam,img):
    #create the matrix grid of the detector CCD
    x = np.linspace(0,1280,1280)
    y = np.linspace(0,1024,1024)
    x, y = np.meshgrid(x, y)
    data = acquireImg(cam,img,200)[0]
    centroid = getPSFCentroid(data)
    return centroid

def getPSFCentroid(data):
    xmean = 0
    ymean = 0
    for ix in range(np.size(data,1)):
        xmean += np.sum(data[:,ix])*ix
    xmean = int(np.around(xmean/np.sum(data)))
    for iy in range(np.size(data,0)):
        ymean += np.sum(data[iy,:])*iy
    ymean = int(np.around(ymean/np.sum(data)))

    return [xmean,ymean]


def cropAndCenterPSF(data,stdData,size):
    Xextent = np.size(data,1)-1
    Yextent = np.size(data,0)-1

    centroid = getPSFCentroid(data)

    minMarge = np.min([centroid[0],centroid[1],Xextent-centroid[0],Yextent-centroid[1]])

    if minMarge>size:
        return cropAroundPSF(data,stdData,centroid,size,size)
    elif minMarge<size:
        return cropAroundPSF(data,stdData, centroid,minMarge,minMarge)


def cropAroundPSF(data,stdData,centroid,sizeX,sizeY):

    pxX = [int(np.floor(centroid[0])-np.ceil(sizeX/2)),int(np.floor(centroid[0])+np.ceil(sizeX/2))]
    pxY = [int(np.floor(centroid[1])-np.ceil(sizeY/2)),int(np.floor(centroid[1])+np.ceil(sizeY/2))]

    dataCropped = data[pxY[0]:pxY[1],pxX[0]:pxX[1]]

    stdDataCropped = stdData[pxY[0]:pxY[1],pxX[0]:pxX[1]]

    return [dataCropped,stdDataCropped]

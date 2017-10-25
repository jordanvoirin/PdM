# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:38:36 2017

@author: Jojo
"""
import os
import pyfits
import functionsXimea as fX

imgSize = 256

initial_guess = [250,450,1135,3,3]

fullFolderPath = 'C:/Users/Jojo/Desktop/PdM-HEIG/Science/data/PD/astigmatism/angle_study/full/50/'
croppedFolderPath = 'C:/Users/Jojo/Desktop/PdM-HEIG/Science/data/PD/astigmatism/angle_study/cropped/50/'

files = os.listdir(fullFolderPath)

for f in files:
    hduList = pyfits.open(fullFolderPath+f)
    data = hduList[0].data
    stdData = hduList[1].data
    [dataCropped,stdDataCropped] = fX.cropAndCenterPSF(data,stdData,imgSize,initial_guess)
    
    imgHdu = pyfits.PrimaryHDU(dataCropped)
    stdHdu = pyfits.ImageHDU(stdDataCropped,name = 'imgStdData')
    hdulist = pyfits.HDUList([imgHdu,stdHdu])
    if not os.path.isdir(croppedFolderPath):
        os.makedirs(croppedFolderPath)
    hdulist.writeto(croppedFolderPath + f,clobber = True)
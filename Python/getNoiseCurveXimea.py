import os
import numpy as np
import pyfits
import matplotlib.pyplot as plt

sfolderPath = 'C:/Users/Jojo/Desktop/PdM-HEIG/Science/data/PD/noise_study/'

sFolderPaths = os.listdir(sfolderPath)

Nfolders =  np.size(sFolderPaths)

#get the vector of nbrImgAveraging-------------------------------------------------------------
nbrImgAveraging = np.zeros(Nfolders)
noiselevel = np.zeros(Nfolders)
for iFol in np.arange(Nfolders-1):
    nbrImgAveraging[iFol] = int(sFolderPaths[iFol])
    #get noise level on each image
    sFilePaths = os.listdir(sfolderPath+sFolderPaths[iFol])
    f = pyfits.open(sfolderPath+sFolderPaths[iFol]+'/'+sFilePaths[0])
    noiselevel[iFol] = np.nanmean(f[1].data)/np.nanmax(f[0].data)

indSorted = np.argsort(nbrImgAveraging)
nbrImgAveraging = nbrImgAveraging[indSorted]
noiselevel = noiselevel[indSorted]

plt.figure()
plt.plot(nbrImgAveraging,noiselevel)
plt.xlabel('# of averaging images')
plt.ylabel('Mean Noise / Max(PSF)')
plt.grid()


import phaseDiversity3PSFs as PD
import numpy as np
import PSF as psf
import matplotlib.pyplot as plt
import fs
import fsAnalyzePD as fsApd
import copy

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmin = 4
jmax = 30
rmsWFerror = 20.
noiseStdLevels = [1e-3,2e-3,5e-3,1e-2,2e-2,5e-2]

PSFinfoc = psf.PSF([1],[0],N,dxp,pupilRadius)


for i,noiseStdLevel in enumerate(noiseStdLevels):
    noiseMean = 0.
    noiseStd = np.max(PSFinfoc.PSF)*noiseStdLevel
    whiteNoise = fsApd.generateWhiteNoise((PSFinfoc.PSF).shape,noiseMean,noiseStd)
    
    

#import phaseDiversity3PSFs as PD
import numpy as np
import PSF as psf
import matplotlib.pyplot as plt
import fs
#import fsAnalyzePD as fsApd


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

jmin = 4
jmax = 30
oddjs = fs.getOddJs(jmin,jmax)
evenjs = fs.getEvenJs(jmin,jmax)


A1 = np.zeros((N**2,len(oddjs)))
for ij in np.arange(len(oddjs)):
    phiJ = fs.f1j(oddjs[ij],N,dxp,pupilRadius)
    A1[:,ij] = phiJ
M1 = np.linalg.pinv(A1)
stdErrorOddsAjs = np.sqrt(np.sum(M1**2,1))

deltaphi = fs.deltaPhi(N,deltaZ,F,2*pupilRadius,lbda,dxp) 
A2 = np.zeros((N**2,len(evenjs)))
for ij in np.arange(len(evenjs)):
    phiJ = fs.f2jeven(evenjs[ij],N,deltaphi,dxp,pupilRadius)
    A2[:,ij] = phiJ
M2 = np.linalg.pinv(A2)
stdErrorEvenAjs = np.sqrt(np.sum(M2**2,1))
    
js = np.append(oddjs,evenjs)
stdErrorAjs = np.append(stdErrorOddsAjs,stdErrorEvenAjs)
Ixjs = np.argsort(js)

plt.figure()
plt.plot(js[Ixjs],stdErrorAjs[Ixjs]*1e-3*1e9*lbda/2/np.pi)

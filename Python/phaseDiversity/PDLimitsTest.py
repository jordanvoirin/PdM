import fsAnalyzePD as fsApd
import phaseDiversity as PD
import numpy as np
import PSF as psf
import fs
import matplotlib.pyplot as plt

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmax = 15

P2Vdephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4.
a4dephasing = P2Vdephasing/2/np.sqrt(3)

rmsWFerrors = np.array([1,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100])
rmse = .0*rmsWFerrors
rmsWFerrorsRetrieved = .0*rmsWFerrors

js = np.linspace(4,jmax,num=jmax-3)

for i, rmsWFerror in enumerate(rmsWFerrors):
    ajstrue = fsApd.getRandomAjs(js,rmsWFerror)*1e-9/lbda*2*np.pi
    
    jswth4 = js
    ajswtha4 = ajstrue
    
    if 4 not in jswth4:
        jswth4 = np.append(4,js)
        ajswtha4 = np.append(a4dephasing,ajstrue)
    else:
        ajswtha4[jswth4==4] += a4dephasing
    
    PSFinfoc = psf.PSF(js,ajstrue,N,dxp,pupilRadius)
    
    PSFoutfoc = psf.PSF(jswth4,ajswtha4,N,dxp,pupilRadius)
    phaseDiv = PD.phaseDiversity(PSFinfoc.PSF,PSFoutfoc.PSF,deltaZ,lbda,pxsize,F,pupilRadius,jmax)
    
    jsretrieved = phaseDiv.result['js']
    ajsretrieved = phaseDiv.result['ajs']
    
    rmse[i] = fs.RMSE(ajsretrieved*1e9*lbda/2/np.pi,ajstrue*1e9*lbda/2/np.pi)
    rmsWFerrorsRetrieved[i] = fs.RMSwavefrontError(jsretrieved,ajsretrieved*1e9*lbda/2/np.pi)
    
    

plt.figure()
plt.plot(rmsWFerrors,rmsWFerrorsRetrieved)

plt.figure()
plt.plot(rmsWFerrors,rmse)

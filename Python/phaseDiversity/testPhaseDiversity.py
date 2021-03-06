import phaseDiversity as PD
import numpy as np
import PSF as psf
import matplotlib.pyplot as plt
import fs
import fsAnalyzePD as fsApd
import copy
#import seaborn as sns
#sns.set()

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmax = 15
rmsWFerror = 20.
noiseStdLevel = 0.001

P2Vdephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4.
a4dephasing = P2Vdephasing/2/np.sqrt(3)

js = np.linspace(4,jmax,num=jmax-3)

ajstrue = fsApd.getRandomAjs(js,rmsWFerror)*1e-9/lbda*2*np.pi
#print ajstrue*1e9*lbda/2/np.pi
#print fs.RMSwavefrontError(js,ajstrue*1e9*lbda/2/np.pi)

jswth4 = copy.deepcopy(js)
ajswtha4 = copy.deepcopy(ajstrue)

if 4 not in jswth4:
    jswth4 = np.append(4,js)
    ajswtha4 = np.append(a4dephasing,ajstrue)
else:
    ajswtha4[jswth4==4] += a4dephasing


PSFinfoc = psf.PSF(js,ajstrue,N,dxp,pupilRadius)
noiseMean = 0.
noiseStd = np.max(PSFinfoc.PSF)*noiseStdLevel
whiteNoise = fsApd.generateWhiteNoise((PSFinfoc.PSF).shape,noiseMean,noiseStd)
PSFinfocWthNoise = PSFinfoc.PSF+whiteNoise

PSFoutfoc = psf.PSF(jswth4,ajswtha4,N,dxp,pupilRadius)
noiseMean = 0.
noiseStd = np.max(PSFoutfoc.PSF)*noiseStdLevel
whiteNoise = fsApd.generateWhiteNoise((PSFoutfoc.PSF).shape,noiseMean,noiseStd)
PSFoutfocWthNoise = PSFoutfoc.PSF+whiteNoise

phaseDivWoutNoise = PD.phaseDiversity(PSFinfoc.PSF,PSFoutfoc.PSF,deltaZ,lbda,pxsize,F,pupilRadius,jmax)
phaseDivWthNoise = PD.phaseDiversity(PSFinfocWthNoise,PSFoutfocWthNoise,deltaZ,lbda,pxsize,F,pupilRadius,jmax)
#print phaseDiv.result['ajs']*1e9*lbda/2/np.pi
#print ajstrue*1e9*lbda/2/np.pi

plt.figure()
plt.hold(True)
plt.plot(js,ajstrue*1e9*lbda/2/np.pi,'b-',label='true, $\sigma_{WF,rms}$ = %5.3f nm' %(fs.RMSwavefrontError(js,ajstrue*1e9*lbda/2/np.pi)))
plt.xlim([js[0],js[-1]])
plt.hold(True)
plt.plot(phaseDivWoutNoise.result['js'],phaseDivWoutNoise.result['ajs']*1e9*lbda/2/np.pi
    ,'r-',label='retrieved wout noise, $\sigma_{WF,rms}$ = %5.3f nm, RMSE = %5.3f nm'
    %(fs.RMSwavefrontError(phaseDivWoutNoise.result['js'],phaseDivWoutNoise.result['ajs']*1e9*lbda/2/np.pi)
    ,fs.RMSE(phaseDivWoutNoise.result['ajs']*1e9*lbda/2/np.pi,ajstrue*1e9*lbda/2/np.pi)))
plt.plot(phaseDivWthNoise.result['js'],phaseDivWthNoise.result['ajs']*1e9*lbda/2/np.pi
    ,'g-',label='retrieved wth noise, $\sigma_{WF,rms}$ = %5.3f nm, RMSE = %5.3f nm'
    %(fs.RMSwavefrontError(phaseDivWthNoise.result['js'],phaseDivWthNoise.result['ajs']*1e9*lbda/2/np.pi)
    ,fs.RMSE(phaseDivWthNoise.result['ajs']*1e9*lbda/2/np.pi,ajstrue*1e9*lbda/2/np.pi)))
plt.xlabel('j')
plt.ylabel('aj [nm]')
plt.legend(loc='best')
plt.grid()


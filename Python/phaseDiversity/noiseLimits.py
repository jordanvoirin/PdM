import fsAnalyzePD as fsApd
import phaseDiversity as PD
import numpy as np
import PSF as psf
import fs
import copy
import matplotlib.pyplot as plt

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmax = 30
rmsWFerror=20

P2Vdephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4.
a4dephasing = P2Vdephasing/2/np.sqrt(3)

noiseStdLevels = np.array([1,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,115,130,150,175,200])*1e-4
NnStdL = noiseStdLevels.size
rmse = .0*noiseStdLevels
rmsWFerrorsTrue = np.ones(NnStdL)*rmsWFerror
rmsWFerrorsRetrieved = .0*noiseStdLevels

js = np.linspace(4,jmax,num=jmax-3)

ajsretrieveds = np.zeros([NnStdL,js.size])
ajstrues = np.zeros([NnStdL,js.size])

for i, noiseStdLevel in enumerate(noiseStdLevels):
    ajstrues[i,:] = fsApd.getRandomAjs(js,rmsWFerror)*1e-9/lbda*2*np.pi
    
    jswth4 = copy.deepcopy(js)
    ajswtha4 = copy.deepcopy(ajstrues[i,:])
    
    if 4 not in jswth4:
        jswth4 = np.append(4,js)
        ajswtha4 = np.append(a4dephasing,ajstrues[i,:])
    else:
        ajswtha4[jswth4==4] += a4dephasing
    
    PSFinfoc = psf.PSF(js,ajstrues[i,:],N,dxp,pupilRadius)
    noiseMean = 0.
    noiseStd = np.max(PSFinfoc.PSF)*noiseStdLevel
    whiteNoise = fsApd.generateWhiteNoise((PSFinfoc.PSF).shape,noiseMean,noiseStd)
    PSFinfocWthNoise = PSFinfoc.PSF+whiteNoise
    
    PSFoutfoc = psf.PSF(jswth4,ajswtha4,N,dxp,pupilRadius)
    whiteNoise = fsApd.generateWhiteNoise((PSFoutfoc.PSF).shape,noiseMean,noiseStd)
    PSFoutfocWthNoise = PSFoutfoc.PSF+whiteNoise
    
    phaseDivWthNoise = PD.phaseDiversity(PSFinfocWthNoise,PSFoutfocWthNoise,deltaZ,lbda,pxsize,F,pupilRadius,jmax)
    
    jsretrieved = phaseDivWthNoise.result['js']
    ajsretrieveds[i,:] = phaseDivWthNoise.result['ajs']
    
    rmse[i] = fs.RMSE(ajsretrieveds[i,:]*1e9*lbda/2/np.pi,ajstrues[i,:]*1e9*lbda/2/np.pi)
    rmsWFerrorsRetrieved[i] = fs.RMSwavefrontError(jsretrieved,ajsretrieveds[i,:]*1e9*lbda/2/np.pi)


plt.figure()
plt.hold(True)
plt.plot(noiseStdLevels,rmsWFerrorsRetrieved,label='$\sigma_{WF,rms}$ retrieved')
plt.plot(noiseStdLevels,rmsWFerrorsTrue,linewidth=2,c='grey',label='$\sigma_{WF,rms}$ true')
plt.xlabel('noise Std level of PSF/PSF max')
plt.ylabel('$\sigma_{WF,rms}$ retrieved [nm]')
plt.grid()

plt.figure()
plt.plot(noiseStdLevels,rmse)
plt.xlabel('noise Std level of PSF/PSF max')
plt.ylabel('RMSE [nm]')
plt.grid()

plt.figure()
for instd in np.arange(NnStdL):
    plt.subplot(NnStdL,1,instd+1)
    plt.title('Noise Std Level = %4.3f'%(noiseStdLevels[instd]))
    plt.hold(True)
    plt.plot(js,ajstrues[instd,:],label='true')
    plt.plot(js,ajsretrieveds[instd,:],label = 'retrieved')
    plt.legend(loc='best')
    plt.grid()
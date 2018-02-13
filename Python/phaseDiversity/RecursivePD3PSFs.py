import phaseDiversity3PSFs as PD
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
jmin = 4
jmax = 30
rmsWFerrors = np.array([5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,115,130,150,175,200,250])
noiseStdLevel = 0.001

P2Vdephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4.
a4dephasing = P2Vdephasing/2/np.sqrt(3)

js = np.linspace(jmin,jmax,num=jmax-3)

ajscomplete = js*.0

for rmsWFerror in rmsWFerrors:
    
    ajstrue = fsApd.getRandomAjs(js,rmsWFerror)*1e-9/lbda*2*np.pi
    ajstrueWthNoise = copy.deepcopy(ajstrue)
    for ij,j in enumerate(js):
        ajscomplete[j-jmin]=copy.deepcopy(ajstrue[ij])
        
    ajsresultWthNoise = js*.0
    ajsresultWoutNoise = js*.0
    jswth4 = copy.deepcopy(js)
    
    rmsWFerrorprevious = fs.RMSwavefrontError(js,ajstrue)*1e9*lbda/2/np.pi    
    
    while(fs.RMSwavefrontError(js,ajstrue)*1e9*lbda/2/np.pi > 2.):
        print fs.RMSwavefrontError(js,ajstrue)*1e9*lbda/2/np.pi
        ajswtha4pos = copy.deepcopy(ajstrue)
        ajswtha4neg = copy.deepcopy(ajstrue)
        
        if 4 not in jswth4:
            jswth4 = np.append(4,js)
            ajswtha4pos = np.append(a4dephasing,ajstrue)
            ajswtha4neg = np.append(-a4dephasing,ajstrue)
        else:
            ajswtha4pos[jswth4==4] += a4dephasing
            ajswtha4neg[jswth4==4] -= a4dephasing
    
        PSFinfoc = psf.PSF(js,ajstrue,N,dxp,pupilRadius)
        noiseMean = 0.
        noiseStd = np.max(PSFinfoc.PSF)*noiseStdLevel
        whiteNoise = fsApd.generateWhiteNoise((PSFinfoc.PSF).shape,noiseMean,noiseStd)
        PSFinfocWthNoise = PSFinfoc.PSF+whiteNoise
        
        PSFoutfocpos = psf.PSF(jswth4,ajswtha4pos,N,dxp,pupilRadius)
        noiseMean = 0.
        noiseStd = np.max(PSFoutfocpos.PSF)*noiseStdLevel
        whiteNoise = fsApd.generateWhiteNoise((PSFoutfocpos.PSF).shape,noiseMean,noiseStd)
        PSFoutfocposWthNoise = PSFoutfocpos.PSF+whiteNoise
        
        PSFoutfocneg = psf.PSF(jswth4,ajswtha4neg,N,dxp,pupilRadius)
        noiseMean = 0.
        noiseStd = np.max(PSFoutfocneg.PSF)*noiseStdLevel
        whiteNoise = fsApd.generateWhiteNoise((PSFoutfocneg.PSF).shape,noiseMean,noiseStd)
        PSFoutfocnegWthNoise = PSFoutfocneg.PSF+whiteNoise
        
        phaseDivWoutNoise = PD.phaseDiversity3PSFs(PSFinfoc.PSF,PSFoutfocpos.PSF,PSFoutfocneg.PSF,deltaZ,lbda,pxsize,F,pupilRadius,jmin,jmax)
        
        ajsresultWoutNoise = ajsresultWoutNoise + phaseDivWoutNoise.result['ajs']
        ajstrue = ajstrue-phaseDivWoutNoise.result['ajs']
        
        if fs.RMSwavefrontError(js,ajstrueWthNoise)*1e9*lbda/2/np.pi > rmsWFerrorprevious:
            print 'do not converge'
            break
    #    plt.figure()
    #    plt.plot(js,ajscomplete*1e9*lbda/2/np.pi,'b-',label='true, $\sigma_{WF,rms}$ = %5.3f nm' %(fs.RMSwavefrontError(js,ajscomplete*1e9*lbda/2/np.pi)))
    #    plt.plot(js,ajsresultWoutNoise*1e9*lbda/2/np.pi,color = 'red',lineStyle='-',label='retrieved wout noise, $\sigma_{WF,rms}$ = %5.3f nm, RMSE = %5.3f nm'
    #        %(fs.RMSwavefrontError(js,ajsresultWoutNoise*1e9*lbda/2/np.pi)
    #        ,fs.RMSE(ajsresultWoutNoise*1e9*lbda/2/np.pi,ajscomplete*1e9*lbda/2/np.pi)))
    #    plt.xlabel('j')
    #    plt.ylabel('aj [nm]')
    #    plt.xlim([js[0],js[-1]])
    #    plt.legend(loc='best')
    #    plt.grid()
    
    plt.figure()
    plt.plot(js,ajscomplete*1e9*lbda/2/np.pi,'b-',label='true, $\sigma_{WF,rms}$ = %5.3f nm' %(fs.RMSwavefrontError(js,ajscomplete*1e9*lbda/2/np.pi)))
    plt.plot(js,ajsresultWoutNoise*1e9*lbda/2/np.pi,color = 'red',lineStyle='-',label='retrieved wout noise, $\sigma_{WF,rms}$ = %5.3f nm, RMSE = %5.3f nm'
        %(fs.RMSwavefrontError(js,ajsresultWoutNoise*1e9*lbda/2/np.pi)
        ,fs.RMSE(ajsresultWoutNoise*1e9*lbda/2/np.pi,ajscomplete*1e9*lbda/2/np.pi)))
    plt.xlabel('j')
    plt.ylabel('aj [nm]')
    plt.xlim([js[0],js[-1]])
    plt.legend(loc='best')
    plt.grid()
    
    rmsWFerrorprevious = fs.RMSwavefrontError(js,ajstrueWthNoise)*1e9*lbda/2/np.pi
    
    while(fs.RMSwavefrontError(js,ajstrueWthNoise)*1e9*lbda/2/np.pi > 2.):
        print fs.RMSwavefrontError(js,ajstrueWthNoise)*1e9*lbda/2/np.pi
        
        ajswtha4pos = copy.deepcopy(ajstrueWthNoise)
        ajswtha4neg = copy.deepcopy(ajstrueWthNoise)
        
        if 4 not in jswth4:
            jswth4 = np.append(4,js)
            ajswtha4pos = np.append(a4dephasing,ajstrueWthNoise)
            ajswtha4neg = np.append(-a4dephasing,ajstrueWthNoise)
        else:
            ajswtha4pos[jswth4==4] += a4dephasing
            ajswtha4neg[jswth4==4] -= a4dephasing
    
        PSFinfoc = psf.PSF(js,ajstrueWthNoise,N,dxp,pupilRadius)
        noiseMean = 0.
        noiseStd = np.max(PSFinfoc.PSF)*noiseStdLevel
        whiteNoise = fsApd.generateWhiteNoise((PSFinfoc.PSF).shape,noiseMean,noiseStd)
        PSFinfocWthNoise = PSFinfoc.PSF+whiteNoise
        
        PSFoutfocpos = psf.PSF(jswth4,ajswtha4pos,N,dxp,pupilRadius)
        noiseMean = 0.
        noiseStd = np.max(PSFoutfocpos.PSF)*noiseStdLevel
        whiteNoise = fsApd.generateWhiteNoise((PSFoutfocpos.PSF).shape,noiseMean,noiseStd)
        PSFoutfocposWthNoise = PSFoutfocpos.PSF+whiteNoise
        
        PSFoutfocneg = psf.PSF(jswth4,ajswtha4neg,N,dxp,pupilRadius)
        noiseMean = 0.
        noiseStd = np.max(PSFoutfocneg.PSF)*noiseStdLevel
        whiteNoise = fsApd.generateWhiteNoise((PSFoutfocneg.PSF).shape,noiseMean,noiseStd)
        PSFoutfocnegWthNoise = PSFoutfocneg.PSF+whiteNoise
        
        phaseDivWthNoise = PD.phaseDiversity3PSFs(PSFinfocWthNoise,PSFoutfocposWthNoise,PSFoutfocnegWthNoise,deltaZ,lbda,pxsize,F,pupilRadius,jmin,jmax)
        
        ajsresultWthNoise = ajsresultWthNoise + phaseDivWthNoise.result['ajs']
        ajstrueWthNoise = ajstrueWthNoise-phaseDivWthNoise.result['ajs']
        
        if fs.RMSwavefrontError(js,ajstrueWthNoise)*1e9*lbda/2/np.pi > rmsWFerrorprevious:
            print 'do not converge'
            break
        
    #    plt.figure()
    #    plt.plot(js,ajscomplete*1e9*lbda/2/np.pi,'b-',label='true, $\sigma_{WF,rms}$ = %5.3f nm' %(fs.RMSwavefrontError(js,ajscomplete*1e9*lbda/2/np.pi)))
    #    plt.plot(js,ajsresultWthNoise*1e9*lbda/2/np.pi,color = 'red',lineStyle='-',label='retrieved wth noise, $\sigma_{WF,rms}$ = %5.3f nm, RMSE = %5.3f nm'
    #        %(fs.RMSwavefrontError(js,ajsresultWthNoise*1e9*lbda/2/np.pi)
    #        ,fs.RMSE(ajsresultWthNoise*1e9*lbda/2/np.pi,ajscomplete*1e9*lbda/2/np.pi)))
    #    plt.xlabel('j')
    #    plt.ylabel('aj [nm]')
    #    plt.xlim([js[0],js[-1]])
    #    plt.legend(loc='best')
    #    plt.grid()
    
    plt.figure()
    plt.plot(js,ajscomplete*1e9*lbda/2/np.pi,'b-',label='true, $\sigma_{WF,rms}$ = %5.3f nm' %(fs.RMSwavefrontError(js,ajscomplete*1e9*lbda/2/np.pi)))
    plt.plot(js,ajsresultWthNoise*1e9*lbda/2/np.pi,color = 'red',lineStyle='-',label='retrieved wth noise, $\sigma_{WF,rms}$ = %5.3f nm, RMSE = %5.3f nm'
        %(fs.RMSwavefrontError(js,ajsresultWthNoise*1e9*lbda/2/np.pi)
        ,fs.RMSE(ajsresultWthNoise*1e9*lbda/2/np.pi,ajscomplete*1e9*lbda/2/np.pi)))
    plt.xlabel('j')
    plt.ylabel('aj [nm]')
    plt.xlim([js[0],js[-1]])
    plt.legend(loc='best')
    plt.grid()

#phaseDivWthNoise = PD.phaseDiversity3PSFs(PSFinfocWthNoise,PSFoutfocposWthNoise,PSFoutfocnegWthNoise,deltaZ,lbda,pxsize,F,pupilRadius,jmin,jmax)

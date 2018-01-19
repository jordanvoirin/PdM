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
jmax = 15
rmsWFerrors = np.array([5,10,15,20,25,30])
Nretrieve = 100
noiseStdLevel = 0.001

P2Vdephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4.
a4dephasing = P2Vdephasing/2/np.sqrt(3)

js = np.linspace(jmin,jmax,num=jmax-3)

jscomplete = np.linspace(jmin,jmax,num=jmax-3)
ajscomplete = np.zeros([rmsWFerrors.size,js.size])

results = np.zeros([rmsWFerrors.size,Nretrieve,js.size])

for irmsWFe,rmsWFerror in enumerate(rmsWFerrors):
    print 'rmsWFerror = %3.1f'%(rmsWFerror)
    ajstrue = fsApd.getRandomAjs(js,rmsWFerror)*1e-9/lbda*2*np.pi
    for ij,j in enumerate(js):
        ajscomplete[irmsWFe,j-jmin]=ajstrue[ij]
    
    #print ajstrue*1e9*lbda/2/np.pi
    #print fs.RMSwavefrontError(js,ajstrue*1e9*lbda/2/np.pi)
    
    jswth4 = copy.deepcopy(js)
    ajswtha4pos = copy.deepcopy(ajstrue)
    ajswtha4neg = copy.deepcopy(ajstrue)
    
    if 4 not in jswth4:
        jswth4 = np.append(4,js)
        ajswtha4pos = np.append(a4dephasing,ajstrue)
        ajswtha4neg = np.append(-a4dephasing,ajstrue)
    else:
        ajswtha4pos[jswth4==4] += a4dephasing
        ajswtha4neg[jswth4==4] -= a4dephasing
        
    for iNretrieve in np.arange(Nretrieve):
        print 'retrieve %d'%(iNretrieve+1)
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
        
#        phaseDivWoutNoise = PD.phaseDiversity3PSFs(PSFinfoc.PSF,PSFoutfocpos.PSF,PSFoutfocneg.PSF,deltaZ,lbda,pxsize,F,pupilRadius,jmax)
        phaseDivWthNoise = PD.phaseDiversity3PSFs(PSFinfocWthNoise,PSFoutfocposWthNoise,PSFoutfocnegWthNoise,deltaZ,lbda,pxsize,F,pupilRadius,jmin,jmax)
        
        results[irmsWFe,iNretrieve,:] = phaseDivWthNoise.result['ajs']



#plt.figure()
#plt.hold(True)
#plt.plot(jscomplete,ajscomplete*1e9*lbda/2/np.pi,'b-',label='true, $\sigma_{WF,rms}$ = %5.3f nm' %(fs.RMSwavefrontError(js,ajstrue*1e9*lbda/2/np.pi)))
#plt.xlim([jscomplete[0],jscomplete[-1]])
#plt.hold(True)
#plt.plot(phaseDivWoutNoise.result['js'],phaseDivWoutNoise.result['ajs']*1e9*lbda/2/np.pi
#    ,'r-',label='retrieved wout noise, $\sigma_{WF,rms}$ = %5.3f nm, RMSE = %5.3f nm'
#    %(fs.RMSwavefrontError(phaseDivWoutNoise.result['js'],phaseDivWoutNoise.result['ajs']*1e9*lbda/2/np.pi)
#    ,fs.RMSE(phaseDivWoutNoise.result['ajs']*1e9*lbda/2/np.pi,ajscomplete*1e9*lbda/2/np.pi)))
#plt.plot(phaseDivWthNoise.result['js'],phaseDivWthNoise.result['ajs']*1e9*lbda/2/np.pi
#    ,'g-',label='retrieved wth noise, $\sigma_{WF,rms}$ = %5.3f nm, RMSE = %5.3f nm'
#    %(fs.RMSwavefrontError(phaseDivWthNoise.result['js'],phaseDivWthNoise.result['ajs']*1e9*lbda/2/np.pi)
#    ,fs.RMSE(phaseDivWthNoise.result['ajs']*1e9*lbda/2/np.pi,ajscomplete*1e9*lbda/2/np.pi)))
#plt.xlabel('j')
#plt.ylabel('aj [nm]')
#plt.legend(loc='best')
#plt.grid()
fnameajsjs = '../../../fig/PDDev/test/newPD_ajs_js_rmsWFe_%d%s'
fnamebxpajsjs = '../../../fig/PDDev/test/newPD_bxp_ajs_js_rmsWFe_%d%s'

for irmsWFe,rmsWFerror in enumerate(rmsWFerrors):
    meanAjsRetrieved = np.mean(results[irmsWFe,:,:],0)*1e9*lbda/2/np.pi
    meanrmsWFerror = fs.RMSwavefrontError(jscomplete,meanAjsRetrieved)
    meanRMSE = fs.RMSE(meanAjsRetrieved,ajscomplete*1e9*lbda/2/np.pi)
    #Plot all the result
    plt.figure()
    plt.title('$\sigma_{wf,rms}$ = %3.1fnm, noiseStdLevel = %4.3f [maxPSF]'%(rmsWFerror,noiseStdLevel))
    plt.hold(True)
    for iNretrieve in np.arange(Nretrieve-1):
        plt.plot(jscomplete,results[irmsWFe,iNretrieve,:]*1e9*lbda/2/np.pi,linewidth = 0.5,color='red')
    plt.plot(jscomplete,results[irmsWFe,Nretrieve-1,:]*1e9*lbda/2/np.pi,linewidth = 0.5,color='red',label='Retrieved, $\overline{\sigma_{wf,rms}}$ = %5.3fnm, $\overline{RMSE}$ = %5.3fnm'%(meanrmsWFerror,meanRMSE))
    plt.plot(jscomplete,ajscomplete[irmsWFe,:]*1e9*lbda/2/np.pi,linewidth = 2, color='blue',label='True')
    plt.grid(True)
    plt.xlim([jscomplete[0],jscomplete[-1]])
    plt.xlabel('js')
    plt.ylabel('ajs [nm]')
    plt.legend(loc='best')
    plt.savefig(fnameajsjs % (rmsWFerror,'png'), dpi=300)
    plt.savefig(fnameajsjs % (rmsWFerror,'pdf'), dpi=300)
    
    #Plot boxplot to have a better view of the statistics
    plt.figure()    
    plt.title('$\sigma_{wf,rms}$ = %3.1fnm, noiseStdLevel = %4.3f [maxPSF]'%(rmsWFerror,noiseStdLevel))
    plt.hold(True)
    plt.boxplot(results[irmsWFe,:,:]*1e9*lbda/2/np.pi,positions=jscomplete)    
    plt.plot(jscomplete,ajscomplete[irmsWFe,:]*1e9*lbda/2/np.pi,'b-',linewidth=1.5,label='true, $\overline{\sigma_{wf,rms}}$ = %5.3fnm, $\overline{RMSE}$ = %5.3fnm'%(meanrmsWFerror,meanRMSE))
    plt.xlabel('js')
    plt.ylabel('ajs [nm]')
    plt.legend(loc='best')
    plt.xlim([jscomplete[0],jscomplete[-1]])
    plt.grid(True)
    plt.savefig(fnamebxpajsjs % (rmsWFerror,'.png'), dpi=300)
    plt.savefig(fnamebxpajsjs % (rmsWFerror,'.pdf'), dpi=300)
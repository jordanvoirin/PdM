import fsAnalyzePD as fsApd
import phaseDiversity3PSFs as PD
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
jmin = 4

P2Vdephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4.
a4dephasing = P2Vdephasing/2/np.sqrt(3)

rmsWFerrors = np.array([1,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,115,130,150,175,200])
rmse = .0*rmsWFerrors
rmsWFerrorsRetrieved = .0*rmsWFerrors

js = np.linspace(jmin,jmax,num=jmax-3)

for i, rmsWFerror in enumerate(rmsWFerrors):
    ajstrue = fsApd.getRandomAjs(js,rmsWFerror)*1e-9/lbda*2*np.pi
    
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
    
    PSFinfoc = psf.PSF(js,ajstrue,N,dxp,pupilRadius)
    PSFoutfocpos = psf.PSF(jswth4,ajswtha4pos,N,dxp,pupilRadius)
    PSFoutfocneg = psf.PSF(jswth4,ajswtha4neg,N,dxp,pupilRadius)
    
    phaseDiv = PD.phaseDiversity3PSFs(PSFinfoc.PSF,PSFoutfocpos.PSF,PSFoutfocneg.PSF,deltaZ,lbda,pxsize,F,pupilRadius,jmin,jmax)
    
    jsretrieved = phaseDiv.result['js']
    ajsretrieved = phaseDiv.result['ajs']
    
    rmse[i] = fs.RMSE(ajsretrieved*1e9*lbda/2/np.pi,ajstrue*1e9*lbda/2/np.pi)
    rmsWFerrorsRetrieved[i] = fs.RMSwavefrontError(jsretrieved,ajsretrieved*1e9*lbda/2/np.pi)
    
    
rmsWFerrorMax = np.max(np.append(rmsWFerrors,rmsWFerrorsRetrieved))
rmsWFerrorMin = np.min(np.append(rmsWFerrors,rmsWFerrorsRetrieved))

fnamerms = '../../../fig/PDDev/test/rmsWFerrorsretrieved_rmsWFe%s'
fnamermse = '../../../fig/PDDev/test/rmse_rmsWFe%s'

fig = plt.figure()
plt.hold(True)
plt.plot(rmsWFerrors,rmsWFerrorsRetrieved)
plt.plot([rmsWFerrorMin,rmsWFerrorMax],[rmsWFerrorMin,rmsWFerrorMax],linewidth=2,c='grey')
plt.xlim([rmsWFerrorMin,rmsWFerrorMax])
plt.ylim([rmsWFerrorMin,rmsWFerrorMax])
plt.xlabel('$\sigma_{WF,rms}$ true [nm]')
plt.ylabel('$\sigma_{WF,rms}$ retrieved [nm]')
plt.grid()
plt.savefig(fnamerms % ('.png'), dpi=300)
plt.savefig(fnamerms % ('.pdf'), dpi=300)
plt.close(fig)

fig = plt.figure()
plt.plot(rmsWFerrors,rmse)
plt.xlim([rmsWFerrorMin,rmsWFerrorMax])
plt.xlabel('$\sigma_{WF,rms}$ true [nm]')
plt.ylabel('RMSE [nm]')
plt.grid()
plt.savefig(fnamermse % ('.png'), dpi=300)
plt.savefig(fnamermse % ('.pdf'), dpi=300)
plt.close(fig)
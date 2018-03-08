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
rmsWFerror = 30.
noiseStdLevel = 0.001

P2Vdephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4.
a4dephasing = P2Vdephasing/2/np.sqrt(3)

js = np.linspace(jmin,jmax,num=jmax-3)

jscomplete = np.linspace(jmin,jmax,num=jmax-3)
ajscomplete = jscomplete*.0

ajstrue = fsApd.getRandomAjs(js,rmsWFerror)*1e-9/lbda*2*np.pi
for ij,j in enumerate(js):
    ajscomplete[j-jmin]=ajstrue[ij]

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


PSFinfoc = psf.PSF(js,ajstrue,N,dxp,pupilRadius)
#noiseMean = 0.
#noiseStd = np.max(PSFinfoc.PSF)*noiseStdLevel
#whiteNoise = fsApd.generateWhiteNoise((PSFinfoc.PSF).shape,noiseMean,noiseStd)
#PSFinfocWthNoise = PSFinfoc.PSF+whiteNoise

PSFoutfocpos = psf.PSF(jswth4,ajswtha4pos,N,dxp,pupilRadius)
#noiseMean = 0.
#noiseStd = np.max(PSFoutfocpos.PSF)*noiseStdLevel
#whiteNoise = fsApd.generateWhiteNoise((PSFoutfocpos.PSF).shape,noiseMean,noiseStd)
#PSFoutfocposWthNoise = PSFoutfocpos.PSF+whiteNoise

PSFoutfocneg = psf.PSF(jswth4,ajswtha4neg,N,dxp,pupilRadius)
#noiseMean = 0.
#noiseStd = np.max(PSFoutfocneg.PSF)*noiseStdLevel
#whiteNoise = fsApd.generateWhiteNoise((PSFoutfocneg.PSF).shape,noiseMean,noiseStd)
#PSFoutfocnegWthNoise = PSFoutfocneg.PSF+whiteNoise

phaseDivWoutNoise = PD.phaseDiversity3PSFs(PSFinfoc.PSF,PSFoutfocpos.PSF,PSFoutfocneg.PSF,deltaZ,lbda,pxsize,F,pupilRadius,jmin,jmax)
#phaseDivWthNoise = PD.phaseDiversity3PSFs(PSFinfocWthNoise,PSFoutfocposWthNoise,PSFoutfocnegWthNoise,deltaZ,lbda,pxsize,F,pupilRadius,jmin,jmax)
#print phaseDiv.result['ajs']*1e9*lbda/2/np.pi
#print ajstrue*1e9*lbda/2/np.pi

plt.figure()
plt.hold(True)
plt.plot(jscomplete,ajscomplete*1e9*lbda/2/np.pi,'b-',label='true, $\sigma_{WF,rms}$ = %5.3f nm' %(fs.RMSwavefrontError(js,ajstrue*1e9*lbda/2/np.pi)))
plt.errorbar(phaseDivWoutNoise.result['js'],phaseDivWoutNoise.result['ajs']*1e9*lbda/2/np.pi,yerr=phaseDivWoutNoise.result['ajsSte']*1e9*lbda/2/np.pi
    ,color = 'red',lineStyle='-',label='retrieved wout noise, $\sigma_{WF,rms}$ = %5.3f nm, RMSE = %5.3f nm'
    %(fs.RMSwavefrontError(phaseDivWoutNoise.result['js'],phaseDivWoutNoise.result['ajs']*1e9*lbda/2/np.pi)
    ,fs.RMSE(phaseDivWoutNoise.result['ajs']*1e9*lbda/2/np.pi,ajscomplete*1e9*lbda/2/np.pi)))
#plt.errorbar(phaseDivWthNoise.result['js'],phaseDivWthNoise.result['ajs']*1e9*lbda/2/np.pi,yerr=phaseDivWthNoise.result['ajsSte']*1e9*lbda/2/np.pi
#    ,color = 'green',lineStyle='-',label='retrieved wth noise, $\sigma_{WF,rms}$ = %5.3f nm, RMSE = %5.3f nm'
#    %(fs.RMSwavefrontError(phaseDivWthNoise.result['js'],phaseDivWthNoise.result['ajs']*1e9*lbda/2/np.pi)
#    ,fs.RMSE(phaseDivWthNoise.result['ajs']*1e9*lbda/2/np.pi,ajscomplete*1e9*lbda/2/np.pi)))
plt.xlabel('j')
plt.ylabel('aj [nm]')
plt.xlim([jscomplete[0],jscomplete[-1]])
plt.legend(loc='upper center')
plt.grid()

fnameajsjs = '../../../fig/PDDev/test/ajs_js_jmax_%d_WoutN_rmsWFe_%d%s'
plt.savefig(fnameajsjs % (jmax,rmsWFerror,'.png'), dpi=300)
plt.savefig(fnameajsjs % (jmax,rmsWFerror,'.pdf'), dpi=300)

plt.figure()
plt.subplot(2,3,4)
plt.imshow(PSFoutfocneg.PSF)
plt.xlim([180,220])
plt.ylim([180,220])
plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labeltop='off',
    labelright='off',
    labelleft='off')
plt.subplot(2,3,5)
plt.imshow(PSFinfoc.PSF)
plt.xlim([180,220])
plt.ylim([180,220])
plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labeltop='off',
    labelright='off',
    labelleft='off')
plt.subplot(2,3,6)
plt.imshow(PSFoutfocpos.PSF)
plt.xlim([180,220])
plt.ylim([180,220])
plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labeltop='off',
    labelright='off',
    labelleft='off')
plt.subplot(2,3,1)
plt.imshow(PSFoutfocneg.phasor.phase)
plt.xlim([132,268])
plt.ylim([132,268])
plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labeltop='off',
    labelright='off',
    labelleft='off')
plt.subplot(2,3,2)
plt.imshow(PSFinfoc.phasor.phase)
plt.xlim([132,268])
plt.ylim([132,268])
plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labeltop='off',
    labelright='off',
    labelleft='off')
plt.subplot(2,3,3)
plt.imshow(PSFoutfocpos.phasor.phase)
plt.xlim([132,268])
plt.ylim([132,268])
plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labeltop='off',
    labelright='off',
    labelleft='off')
plt.show()
fnameajsjs = '../../../fig/PDDev/test/PhasesAndPSFs_jmax_%d_WoutN_rmsWFe_%d%s'
plt.savefig(fnameajsjs % (jmax,rmsWFerror,'.png'), dpi=300)
plt.savefig(fnameajsjs % (jmax,rmsWFerror,'.pdf'), dpi=300)
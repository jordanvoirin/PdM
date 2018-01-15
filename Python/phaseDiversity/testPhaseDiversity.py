import phaseDiversity as PD
import numpy as np
import PSF as psf
import matplotlib.pyplot as plt
import fs
import seaborn as sns
sns.set()

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmax = 15

jspresent = np.array([6,7,9])
ajspresent = np.array([10e-9/lbda*2*np.pi,10e-9/lbda*2*np.pi,10e-9/lbda*2*np.pi])

js = np.linspace(1,jmax,num=jmax)
ajs = js*0.

for ij,j in enumerate(jspresent):
    ajs[js==jspresent[ij]]=ajspresent[ij]

P2Vdephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4.
a4dephasing = P2Vdephasing/2/np.sqrt(3)

jswth4 = jspresent
ajswtha4 = ajspresent

if 4 not in jswth4:
    jswth4 = np.append(4,jspresent)
    ajswtha4 = np.append(a4dephasing,ajspresent)
else:
    ajswtha4[jswth4==4] += a4dephasing

PSFinfoc = psf.PSF(jspresent,ajspresent,N,dxp,pupilRadius)

PSFoutfoc = psf.PSF(jswth4,ajswtha4,N,dxp,pupilRadius)

phaseDiv = PD.phaseDiversity(PSFinfoc.PSF,PSFoutfoc.PSF,deltaZ,lbda,pxsize,F,pupilRadius,jmax)

print phaseDiv.result['ajs']

plt.figure()
plt.hold(True)
plt.plot(js,ajs*1e9*lbda/2/np.pi,'b-',label='true, $\sigma_{WF,rms}$ = %5.3f nm' %(fs.RMSwavefrontError(js,ajs*1e9*lbda/2/np.pi)))
plt.xlim([js[0],js[-1]])
plt.hold(True)
plt.plot(phaseDiv.result['js'],phaseDiv.result['ajs']*1e9*lbda/2/np.pi,'r-',label='retrieved, $\sigma_{WF,rms}$ = %5.3f nm, RMSE = %5.3f nm'%(fs.RMSwavefrontError(phaseDiv.result['js'],phaseDiv.result['ajs']*1e9),fs.RMSE(phaseDiv.result['ajs']*1e9,ajs*1e9*lbda/2/np.pi)))
plt.xlabel('j')
plt.ylabel('aj [nm]')
plt.legend(loc='best')


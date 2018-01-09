import phaseDiversity as PD
import numpy as np
import PSF as psf
import matplotlib.pyplot as plt

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmax = 15

jspresent = np.array([7])
ajspresent = np.array([75e-9/lbda*2*np.pi])


P2Vdephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4.
a4dephasing = P2Vdephasing/2/np.sqrt(6)

if 4 not in jspresent:
    jswth4 = np.append(4,jspresent)
    ajswtha4 = np.append(a4dephasing,ajspresent)
else:
    ajspresent[jspresent==4] += a4dephasing

PSFinfoc = psf.PSF(jspresent,ajspresent,N,dxp,pupilRadius)

PSFoutfoc = psf.PSF(jswth4,ajswtha4,N,dxp,pupilRadius)

phaseDiv = PD.phaseDiversity(PSFinfoc.PSF,PSFoutfoc.PSF,deltaZ,lbda,pxsize,F,pupilRadius,jmax)

print phaseDiv.result['ajs']

plt.figure()
plt.plot(jspresent,ajspresent*1e9*lbda/2/np.pi,'bo')
plt.hold()
plt.plot(phaseDiv.result['js'],phaseDiv.result['ajs']*1e9,'ro')


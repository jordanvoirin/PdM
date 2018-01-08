import phaseDiversity as PD
import numpy as np
import PSF as psf

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmax = 15

a4dephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4./2.

PSFinfoc = psf.PSF([6,7],[1e-9/lbda*2*np.pi,1e-9/lbda*2*np.pi],N,dxp,pupilRadius)

PSFoutfoc = psf.PSF([4,6,7],[a4dephasing,1e-9/lbda*2*np.pi,1e-9/lbda*2*np.pi],N,dxp,pupilRadius)

phaseDiv = PD.phaseDiversity(PSFinfoc.PSF,PSFoutfoc.PSF,deltaZ,lbda,pxsize,F,pupilRadius,jmax)

print phaseDiv.result['ajs']

PSFinfoc = psf.PSF([6],[0],N,dxp,pupilRadius)

PSFoutfoc = psf.PSF([4],[a4dephasing],N,dxp,pupilRadius)

phaseDiv = PD.phaseDiversity(PSFinfoc.PSF,PSFoutfoc.PSF,deltaZ,lbda,pxsize,F,pupilRadius,jmax)

print phaseDiv.result['ajs']
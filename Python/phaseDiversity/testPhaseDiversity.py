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
jmax = 30

a4dephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4./2.

rad = int(np.ceil(pupilRadius/dxp))

PSFinfoc = psf.PSF([7],[10e-9/lbda],N,rad,dxp)

PSFoutfoc = psf.PSF([4,7],[a4dephasing,10e-9/lbda],N,rad,dxp)

phaseDiv = PD.phaseDiversity(PSFinfoc.PSF,PSFoutfoc.PSF,deltaZ,lbda,pxsize,F,pupilRadius,jmax)

print phaseDiv.result['ajs']

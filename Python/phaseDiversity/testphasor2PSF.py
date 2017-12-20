import numpy as np
import matplotlib.pyplot as plt
import PSF as psf
#%matplotlib inline
#%config InlineBackend.figure_format = 'svg'

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)

rad = int(np.ceil(pupilRadius/dxp))
PSF = psf.PSF([8],[2000e-9/lbda],N,rad,dxp)


plt.figure()
plt.imshow(np.real(PSF.phasor.phasor),vmax = np.max(np.real(PSF.phasor.phasor)), vmin = np.min(np.real(PSF.phasor.phasor)))
plt.figure()
plt.imshow(PSF.PSF,vmax=np.max(PSF.PSF),vmin=np.min(PSF.PSF))
plt.figure()
plt.imshow(PSF.phasor.phase)
plt.figure()
plt.imshow(PSF.phasor.pupil)

import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
import phasor as ph
#%matplotlib inline
#%config InlineBackend.figure_format = 'svg'

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)

rad = int(np.ceil(pupilRadius/dxp))
phasor = ph.phasor([8],[2000e-9/lbda],N,rad)
matphasor = phasor.phasor
FFTPupil = np.fft.fftshift(np.fft.fft2(matphasor))
NFFTPupil = np.abs(FFTPupil)**2/np.sum(phasor.pupil)**2
NFFTPupilnormalized = NFFTPupil/np.max(NFFTPupil)

plt.figure()
plt.imshow(np.real(matphasor),vmax = np.max(np.real(matphasor)), vmin = np.min(np.real(matphasor)))
plt.figure()
plt.imshow(NFFTPupil,vmax=np.max(NFFTPupil),vmin=0.)
plt.figure()
plt.imshow(phasor.phase)
plt.figure()
plt.imshow(phasor.pupil)

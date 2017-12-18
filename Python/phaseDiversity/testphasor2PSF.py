import numpy as np
import matplotlib.pyplot as plt
import libtim.im as im
import phasor as ph
import myExceptions
%matplotlib inline
%config InlineBackend.figure_format = 'svg'

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)

rad = int(np.ceil(pupilRadius/dxp))
phasor = ph.phasor([1],[0],N,rad)
matphasor = phasor.phasor
FFTPupil = np.fft.fftshift(np.fft.fft2(matphasor))
NFFTPupil = np.abs(FFTPupil)**2/np.sum(phasor.pupil)**2
NFFTPupilnormalized = NFFTPupil/np.max(NFFTPupil)

plt.imshow(np.real(matphasor),vmax = np.max(np.real(matphasor)), vmin = np.min(np.real(matphasor)))

plt.imshow(NFFTPupil,vmax=np.max(NFFTPupil),vmin=0.)

plt.imshow(phasor.phase)

plt.imshow(phasor.pupil)


a = []

a

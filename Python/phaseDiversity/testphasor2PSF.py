import numpy as np
import matplotlib.pyplot as plt
import libtim.im as im
%matplotlib inline
%config InlineBackend.figure_format = 'svg'

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)

rad = int(np.ceil(pupilRadius/dxp))
print rad
grid_mask = (im.mk_rad_mask(2*rad)) <= 1
pupil = np.ones((2*rad,2*rad))*grid_mask
matpupil = np.zeros((4*rad,4*rad))
matpupil[rad:3*rad,rad:3*rad] = pupil
FFTPupil = np.fft.fftshift(np.fft.fft2(matpupil))

NFFTPupil = np.abs(FFTPupil)**2/np.sum(pupil)

plt.imshow(matpupil)

plt.imshow(NFFTPupil,vmax=2.,vmin=0.)

import numpy as np
import matplotlib.pyplot as plt
from libtim import all

%matplotlib inline
%config 

rad = int(np.ceil(pupilRadius/dxp))
grid_mask = (im.mk_rad_mask(2*rad)) <= 1
pupil = np.ones((2*rad,2*rad))*grid_mask
matpupil = np.zeros((4*rad,4*rad))
matpupil[rad:3*rad,rad:3*rad] = pupil
FFTPupil = np.fft.fftshift(np.fft.fft2(matpupil))

NFFTPupil = np.abs(FFTPupil)**2/np.sum(pupil)

plt.figure()
plt.imshow(matpupil)

plt.figure()
plt.imshow(NFFTpupil,vmax=0.,vmin=2.)

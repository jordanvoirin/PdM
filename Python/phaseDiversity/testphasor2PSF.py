import numpy as np
import matplotlib.pyplot as plt
from libtim import all

rad = int(np.ceil(pupilRadius/dxp))
grid_mask = (im.mk_rad_mask(2*rad)) <= 1
pupil = np.ones((2*rad,2*rad))*grid_mask
FFTPupil = np.fft.fftshift(np.fft.fft2(pupil))

import numpy as np
import matplotlib.pyplot as plt
import phasor as ph
import zernike as Z
lbda = 0.6375e-6
pxsize = 5.3e-6
F = 80e-3
pupilRadius = 1.6e-3
N = 400
dxp = F*lbda/(N*pxsize)


Lp = N*dxp

xp = np.arange(-Lp/2,Lp/2,dxp)
yp = xp

[Xp,Yp]=np.meshgrid(xp,yp)

r = np.sqrt(Xp**2+Yp**2)
r = r*(r<=pupilRadius)/pupilRadius
theta = np.arctan2(Yp,Xp)

plt.figure
plt.subplot(2,1,1)
plt.imshow(r)
plt.subplot(2,1,2)
plt.imshow(theta)

pup = np.float64(np.sqrt(Xp**2+Yp**2)<=pupilRadius)
rad = int(np.ceil(pupilRadius/dxp))
phasor = ph.phasor([1],[0],N,rad)

plt.figure()
plt.imshow(pup)
plt.figure()
plt.imshow(pup-phasor.pupil)

fftpup = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(pup)))
fftpupil = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(phasor.pupil)))

plt.figure()
plt.subplot(2,1,1)
plt.imshow(np.real(fftpup)-np.real(fftpupil))
plt.subplot(2,1,2)
plt.imshow(np.imag(fftpup)-np.imag(fftpupil))

Zj = Z.calc_zern_j(4,N,dxp,pupilRadius)

plt.figure()
plt.imshow(Zj)

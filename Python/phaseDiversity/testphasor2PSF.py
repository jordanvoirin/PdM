import numpy as np
import matplotlib.pyplot as plt
import PSF as psf
import pyfits

#%matplotlib inline
#%config InlineBackend.figure_format = 'svg'

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
rad = int(np.ceil(pupilRadius/dxp))

PSF = psf.PSF([1],[0],N,dxp,pupilRadius)
PSFwthAb = psf.PSF([4,10],[1,1],N,dxp,pupilRadius)

hdulist = pyfits.open('C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\devPD\psfnAb.fits')
psfLJo = hdulist[0].data
phaseLJo = hdulist[1].data

hdulist = pyfits.open('C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\devPD\psf4_10__1_1.fits')
psfLJo_wthAb = hdulist[0].data
phaseLJo_wthAb = hdulist[1].data

#FFTpupil = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(PSF.phasor.pupil)))
#plt.figure()
#plt.imshow(np.real(PSF.phasor.phasor),vmax = np.max(np.real(PSF.phasor.phasor)), vmin = np.min(np.real(PSF.phasor.phasor)))
plt.figure()
plt.subplot(1,3,1)
plt.imshow(PSF.PSF,vmax=np.max(PSF.PSF),vmin=np.min(PSF.PSF))
plt.colorbar()
plt.subplot(1,3,2)
plt.imshow(psfLJo,vmax=np.max(PSF.PSF),vmin=np.min(PSF.PSF))
plt.colorbar()
plt.subplot(1,3,3)
plt.imshow((PSF.PSF-psfLJo),vmax=np.max((PSF.PSF-psfLJo)),vmin=np.min((PSF.PSF-psfLJo)))
plt.colorbar()

plt.figure()
plt.subplot(1,3,1)
plt.imshow(PSFwthAb.PSF,vmax=np.max(PSFwthAb.PSF),vmin=np.min(PSFwthAb.PSF))
plt.colorbar()
plt.subplot(1,3,2)
plt.imshow(psfLJo_wthAb,vmax=np.max(PSFwthAb.PSF),vmin=np.min(PSFwthAb.PSF))
plt.colorbar()
plt.subplot(1,3,3)
plt.imshow(PSFwthAb.PSF-psfLJo_wthAb,vmax=np.max(PSFwthAb.PSF-psfLJo_wthAb),vmin=np.min(PSFwthAb.PSF-psfLJo_wthAb))
#plt.imshow((PSFwthAb.PSF-psfLJo_wthAb)/PSFwthAb.PSF*100.,vmax=np.max((PSFwthAb.PSF-psfLJo_wthAb)/PSFwthAb.PSF*100.),vmin=np.min((PSFwthAb.PSF-psfLJo_wthAb)/PSFwthAb.PSF*100.))
plt.colorbar()

#plt.figure()
#plt.imshow(PSF.phasor.phase)
#plt.figure()
#plt.imshow(np.real(FFTpupil))
#plt.figure()
#plt.imshow(np.imag(FFTpupil))

#Compare phase

#plt.figure()
#plt.subplot(1,3,1)
#plt.imshow(PSF.phasor.pupil,vmax=np.max(PSF.phasor.pupil),vmin=np.min(PSF.phasor.pupil))
#plt.colorbar()
#plt.subplot(1,3,2)
#plt.imshow(phaseLJo,vmax=np.max(PSF.phasor.pupil),vmin=np.min(PSF.phasor.pupil))
#plt.colorbar()
#plt.subplot(1,3,3)
#plt.imshow(PSF.phasor.pupil-phaseLJo,vmax=np.max(PSF.phasor.pupil-phaseLJo),vmin=np.min(PSF.phasor.pupil-phaseLJo))

plt.figure()
plt.subplot(1,3,1)
plt.imshow(PSFwthAb.phasor.phase,vmax=np.max(PSFwthAb.phasor.phase),vmin=np.min(PSFwthAb.phasor.phase))
plt.colorbar()
plt.subplot(1,3,2)
plt.imshow(phaseLJo_wthAb,vmax=np.max(PSFwthAb.phasor.phase),vmin=np.min(PSFwthAb.phasor.phase))
plt.colorbar()
plt.subplot(1,3,3)
plt.imshow(PSFwthAb.phasor.phase-phaseLJo_wthAb,vmax=np.max(PSFwthAb.phasor.phase-phaseLJo_wthAb),vmin=np.min(PSFwthAb.phasor.phase-phaseLJo_wthAb))
plt.colorbar()

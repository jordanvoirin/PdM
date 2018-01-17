import numpy as np
import matplotlib.pyplot as plt
import PSF as psf
import pyfits
import fs
import fsAnalyzePD as fsApd

#%matplotlib inline
#%config InlineBackend.figure_format = 'svg'

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)

noiseStdLevel = 0.01

PSF = psf.PSF([1],[0],N,dxp,pupilRadius)
PSFwthAb = psf.PSF([5,6,13],[1,1,1],N,dxp,pupilRadius)
noiseMean = 0.
noiseStd = np.max(PSFwthAb.PSF)*noiseStdLevel
whiteNoise = fsApd.generateWhiteNoise((PSFwthAb.PSF).shape,noiseMean,noiseStd)
PSFwthAbWthNoise = PSFwthAb.PSF+whiteNoise

hdulist = pyfits.open('C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\devPD\psfnAb.fits')
psfLJo = hdulist[0].data
phaseLJo = hdulist[1].data

hdulist = pyfits.open('C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\devPD\psf4__1.fits')
psfLJo_wthAb = hdulist[0].data
phaseLJo_wthAb = hdulist[1].data
pupLJo_wthAb = hdulist[2].data

#FFTpupil = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(PSF.phasor.pupil)))
#plt.figure()
#plt.imshow(np.real(PSF.phasor.phasor),vmax = np.max(np.real(PSF.phasor.phasor)), vmin = np.min(np.real(PSF.phasor.phasor)))

#plt.figure()
#plt.subplot(1,3,1)
#plt.imshow(PSF.PSF,vmax=np.max(PSF.PSF),vmin=np.min(PSF.PSF))
#plt.colorbar(fraction=0.046, pad=0.04)
#plt.subplot(1,3,2)
#plt.imshow(psfLJo,vmax=np.max(PSF.PSF),vmin=np.min(PSF.PSF))
#plt.colorbar(fraction=0.046, pad=0.04)
#plt.subplot(1,3,3)
#plt.imshow((PSF.PSF-psfLJo),vmax=np.max((PSF.PSF-psfLJo)),vmin=np.min((PSF.PSF-psfLJo)))
#plt.colorbar(fraction=0.046, pad=0.04)
#
#plt.figure()
#plt.hist((psfLJo/PSF.PSF))
#
#plt.figure()
#plt.subplot(1,3,1)
#plt.imshow(PSFwthAb.PSF,vmax=np.max(PSFwthAb.PSF),vmin=np.min(PSFwthAb.PSF))
#plt.colorbar(fraction=0.046, pad=0.04)
#plt.subplot(1,3,2)
#plt.imshow(psfLJo_wthAb,vmax=np.max(PSFwthAb.PSF),vmin=np.min(PSFwthAb.PSF))
#plt.colorbar(fraction=0.046, pad=0.04)
#plt.subplot(1,3,3)
#plt.imshow(PSFwthAb.PSF-psfLJo_wthAb,vmax=np.max(PSFwthAb.PSF-psfLJo_wthAb),vmin=np.min(PSFwthAb.PSF-psfLJo_wthAb))
##plt.imshow((PSFwthAb.PSF-psfLJo_wthAb)/PSFwthAb.PSF*100.,vmax=np.max((PSFwthAb.PSF-psfLJo_wthAb)/PSFwthAb.PSF*100.),vmin=np.min((PSFwthAb.PSF-psfLJo_wthAb)/PSFwthAb.PSF*100.))
#plt.colorbar(fraction=0.046, pad=0.04)
#
##plt.figure()
##plt.imshow(PSF.phasor.phase)
##plt.figure()
##plt.imshow(np.real(FFTpupil))
##plt.figure()
##plt.imshow(np.imag(FFTpupil))
#
#
##compare pupil
#plt.figure()
#plt.subplot(1,3,1)
#plt.imshow(PSF.phasor.pupil,vmax=np.max(PSF.phasor.pupil),vmin=np.min(PSF.phasor.pupil))
#plt.colorbar(fraction=0.046, pad=0.04)
#plt.subplot(1,3,2)
#plt.imshow(pupLJo_wthAb,vmax=np.max(PSF.phasor.pupil),vmin=np.min(PSF.phasor.pupil))
#plt.colorbar(fraction=0.046, pad=0.04)
#plt.subplot(1,3,3)
#plt.imshow(PSF.phasor.pupil-pupLJo_wthAb,vmax=np.max(PSF.phasor.pupil-pupLJo_wthAb),vmin=np.min(PSF.phasor.pupil-pupLJo_wthAb))
#
##Compare phase
#plt.figure()
#plt.subplot(1,3,1)
#plt.imshow(PSFwthAb.phasor.phase,vmax=np.max(PSFwthAb.phasor.phase),vmin=np.min(PSFwthAb.phasor.phase))
#plt.colorbar(fraction=0.046, pad=0.04)
#plt.subplot(1,3,2)
#plt.imshow(phaseLJo_wthAb,vmax=np.max(PSFwthAb.phasor.phase),vmin=np.min(PSFwthAb.phasor.phase))
#plt.colorbar(fraction=0.046, pad=0.04)
#plt.subplot(1,3,3)
#plt.imshow(PSFwthAb.phasor.phase-phaseLJo_wthAb,vmax=np.max(PSFwthAb.phasor.phase-phaseLJo_wthAb),vmin=np.min(PSFwthAb.phasor.phase-phaseLJo_wthAb))
#plt.colorbar(fraction=0.046, pad=0.04)

plt.figure()
plt.subplot(2,3,1)
plt.title('Even Part Even aberrations PSF wout noise')
plt.imshow(fs.getEvenPart(PSFwthAb.PSF))
plt.colorbar(fraction=0.046, pad=0.04)
plt.subplot(2,3,2)
plt.title('Odd Part Even aberrations PSF wout noise')
plt.imshow(fs.getOddPart(PSFwthAb.PSF))
plt.colorbar(fraction=0.046, pad=0.04)
plt.subplot(2,3,3)
plt.title('Odd Part Even aberrations PSF wth noise')
plt.imshow(fs.getOddPart(PSFwthAbWthNoise))
plt.colorbar(fraction=0.046, pad=0.04)
plt.subplot(2,3,4)
plt.title('Even Part Even aberrations PSF wout noise hist')
plt.hist(fs.getEvenPart(PSFwthAb.PSF))
plt.subplot(2,3,5)
plt.title('Odd Part Even aberrations PSF wout noise hist')
plt.hist(fs.getOddPart(PSFwthAb.PSF))
plt.subplot(2,3,6)
plt.title('Odd Part Even aberrations PSF wth noise hist')
plt.hist(fs.getOddPart(PSFwthAbWthNoise))


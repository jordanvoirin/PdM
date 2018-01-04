import numpy as np
import matplotlib.pyplot as plt
import PSF as psf
import scipy.special as scispe
import pyfits

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)

dfx = 1/(N*dxp)
Lf = 1./dxp
fx = np.arange(-Lf/2,Lf/2,dfx)
fy = fx
[Fx,Fy]=np.meshgrid(fx,fy) 
x = 2*np.pi*pupilRadius*np.sqrt(Fx**2+Fy**2)


def analyticalTFpupil(x):
    return pupilRadius**2*scispe.jv(1,x)/x*2*np.pi

PSF = psf.PSF([1],[0],N,dxp,pupilRadius)
PSFAnalytical = np.abs(analyticalTFpupil(x))**2/PSF.Sp**2

hdulist = pyfits.open('C:\Users\Jojo\Desktop\PdM-HEIG\Science\data\devPD\psfnAb.fits')
psfLJo = hdulist[0].data
phaseLJo = hdulist[1].data

plt.figure()
plt.subplot(2,3,1)
plt.imshow(PSF.PSF,vmax=np.max(PSF.PSF),vmin=np.min(PSF.PSF))
plt.title('PSF python')
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,3)
plt.imshow(PSFAnalytical,vmax=np.max(PSF.PSF),vmin=np.min(PSF.PSF))
plt.title('PSF analytical')
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,5)
plt.imshow(PSF.PSF-PSFAnalytical,vmax=np.max(PSF.PSF-PSFAnalytical),vmin=np.min(PSF.PSF-PSFAnalytical))
plt.title('PSF python - PSF analytical')
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,2)
plt.imshow(psfLJo,vmax=np.max(PSF.PSF),vmin=np.min(PSF.PSF))
plt.title('PSF IDL')
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,6)
plt.imshow(psfLJo-PSFAnalytical,vmax=np.max(psfLJo-PSFAnalytical),vmin=np.min(psfLJo-PSFAnalytical))
plt.title('PSF IDL - PSF analytical')
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,4)
plt.imshow((PSF.PSF-psfLJo),vmax=np.max((PSF.PSF-psfLJo)),vmin=np.min((PSF.PSF-psfLJo)))
plt.title('PSF python - PSF IDL')
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()


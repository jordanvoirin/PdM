import numpy as np
import matplotlib.pyplot as plt
import PSF as psf
import fs

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
a4dephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4./2./np.sqrt(6)

PSF = psf.PSF([1],[0],N,dxp,pupilRadius)
PSFwthAb = psf.PSF([7],[1e-9/lbda*2*np.pi],N,dxp,pupilRadius)

DeltaPSF = PSFwthAb.Sp**2*PSFwthAb.PSF - PSF.Sp**2*PSF.PSF
oddDeltaPSF = fs.getOddPart(DeltaPSF)
evenDeltaPSF = fs.getEvenPart(DeltaPSF)


plt.figure()
plt.subplot(1,3,1)
plt.title('PSF without Abs')
plt.imshow(PSF.PSF,vmin = np.min(PSF.PSF), vmax=np.max(PSF.PSF))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar(fraction=0.046, pad=0.04)
plt.subplot(1,3,2)
plt.title('PSF with Abs')
plt.imshow(PSFwthAb.PSF,vmin = np.min(PSFwthAb.PSF), vmax=np.max(PSFwthAb.PSF))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar(fraction=0.046, pad=0.04)
plt.subplot(1,3,3)
plt.title('Delta PSF Delta(Sp^2*PSF)')
plt.imshow(DeltaPSF,vmin = np.min(DeltaPSF), vmax=np.max(DeltaPSF))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar(fraction=0.046, pad=0.04)

plt.figure()
plt.subplot(1,3,1)
plt.title('Delta PSF')
plt.imshow(DeltaPSF,vmin = np.min(DeltaPSF), vmax=np.max(DeltaPSF))
#plt.xlim([180,220])
#plt.ylim([180,220])
plt.colorbar(fraction=0.046, pad=0.04)
plt.subplot(1,3,2)
plt.title('Odd Part Delta PSF')
plt.imshow(oddDeltaPSF,vmin = np.min(oddDeltaPSF), vmax=np.max(oddDeltaPSF))
#plt.xlim([180,220])
#plt.ylim([180,220])
plt.colorbar(fraction=0.046, pad=0.04)
plt.subplot(1,3,3)
plt.title('Even Part Delta PSF')
plt.imshow(evenDeltaPSF,vmin = np.min(evenDeltaPSF), vmax=np.max(evenDeltaPSF))
#plt.xlim([180,220])
#plt.ylim([180,220])
plt.colorbar(fraction=0.046, pad=0.04)
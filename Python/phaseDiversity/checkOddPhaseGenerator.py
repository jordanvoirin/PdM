#Check odd part generator

import numpy as np
import PSF as psf
import fs
import matplotlib.pyplot as plt
import scipy.special as scispe

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmax = 6

dfx = 1/(N*dxp)
Lf = 1./dxp
fx = np.arange(-Lf/2,Lf/2,dfx)
fy = fx
[Fx,Fy]=np.meshgrid(fx,fy) 
x = 2*np.pi*pupilRadius*np.sqrt(Fx**2+Fy**2)


def analyticalTFpupil(x):
    return pupilRadius**2*scispe.jv(1,x)/x*2*np.pi



a4dephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4./2.

PSFinfoc = psf.PSF([6],[1e-9/lbda*2*np.pi],N,dxp,pupilRadius)
PSFAnalytical = np.abs(analyticalTFpupil(x))**2/PSFinfoc.Sp**2



PSFoutfoc = psf.PSF([4,6],[a4dephasing,1e-9/lbda*2*np.pi],N,dxp,pupilRadius)
PSFoufocperfect = psf.PSF([4],[a4dephasing],N,dxp,pupilRadius)

DeltaPSFinfoc = PSFinfoc.Sp**2*PSFinfoc.PSF - PSFinfoc.Sp**2*PSFinfoc.perfectPSF
DeltaPSFoutfoc = PSFoutfoc.Sp**2*PSFoutfoc.PSF - PSFoutfoc.Sp**2*PSFoufocperfect.PSF

oddDeltaPSFinfoc = fs.getOddPart(DeltaPSFinfoc)
oddDeltaPSFoutfoc = fs.getOddPart(DeltaPSFoutfoc)
evenDeltaPSFinfoc = fs.getEvenPart(DeltaPSFinfoc)
evenDeltaPSFoutfoc = fs.getEvenPart(DeltaPSFoutfoc)

plt.figure()
plt.subplot(2,3,1)
plt.title('infoc')
plt.imshow(DeltaPSFinfoc,vmax=np.max(DeltaPSFinfoc),vmin=np.min(DeltaPSFinfoc))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,2)
plt.title('Odd infoc')
plt.imshow(oddDeltaPSFinfoc,vmax=np.max(oddDeltaPSFinfoc),vmin=np.min(oddDeltaPSFinfoc))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,3)
plt.title('Even infoc')
plt.imshow(evenDeltaPSFinfoc,vmax=np.max(evenDeltaPSFinfoc),vmin=np.min(evenDeltaPSFinfoc))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,4)
plt.title('outfoc')
plt.imshow(DeltaPSFoutfoc,vmax=np.max(DeltaPSFoutfoc),vmin=np.min(DeltaPSFoutfoc))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,5)
plt.title('Odd outfoc')
plt.imshow(oddDeltaPSFoutfoc,vmax=np.max(oddDeltaPSFoutfoc),vmin=np.min(oddDeltaPSFoutfoc))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,6)
plt.title('Even outfoc')
plt.imshow(evenDeltaPSFoutfoc,vmax=np.max(evenDeltaPSFoutfoc),vmin=np.min(evenDeltaPSFoutfoc))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()

A = [[1,3,2],[2,1,2],[2,3,1]]
oddA = fs.getOddPart(A)
evenA = fs.getEvenPart(A)

#PSFs odd and even part
PSF = psf.PSF([1],[0],N,dxp,pupilRadius)
oddPSF = fs.getOddPart(PSF.PSF)
evenPSF = fs.getEvenPart(PSF.PSF)
PSFAnalytical = np.abs(analyticalTFpupil(x))**2/PSFinfoc.Sp**2
oddPSFAnalytical = fs.getOddPart(PSFAnalytical)
evenPSFAnalytical = fs.getEvenPart(PSFAnalytical)

plt.figure()
plt.subplot(2,3,1)
plt.title('PSF')
plt.imshow(PSF.PSF,vmax=np.max(PSF.PSF),vmin=np.min(PSF.PSF))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,2)
plt.title('Odd PSF')
plt.imshow(oddPSF,vmax=np.max(oddPSF),vmin=np.min(oddPSF))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,3)
plt.title('Even PSf')
plt.imshow(evenPSF,vmax=np.max(evenPSF),vmin=np.min(evenPSF))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,4)
plt.title('PSF analytical')
plt.imshow(PSFAnalytical,vmax=np.max(PSFAnalytical),vmin=np.min(PSFAnalytical))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,5)
plt.title('Odd PSF analytical')
plt.imshow(oddPSFAnalytical,vmax=np.max(oddPSFAnalytical),vmin=np.min(oddPSFAnalytical))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()
plt.subplot(2,3,6)
plt.title('Even PSF analytical')
plt.imshow(evenPSFAnalytical,vmax=np.max(evenPSFAnalytical),vmin=np.min(evenPSFAnalytical))
plt.xlim([180,220])
plt.ylim([180,220])
plt.colorbar()

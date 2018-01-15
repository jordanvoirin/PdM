#test y2 and f2j in the absence of even aberrations so deltaPSFoutfoc should be equal to 2*im{PC*PCE+PS*PSE}

import numpy as np
import fs
import matplotlib.pyplot as plt
import phasor as ph
import PSF as psf

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmax = 15
deltaphi = fs.deltaPhi(N,deltaZ,F,2*pupilRadius,lbda,dxp)

j=4

jspresent = np.array([7])
ajspresent = np.array([10e-9/lbda*2*np.pi])

js = np.linspace(1,jmax,num=jmax)
ajs = js*0.

for ij,j in enumerate(jspresent):
    ajs[js==jspresent[ij]]=ajspresent[ij]

P2Vdephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4.
a4dephasing = P2Vdephasing/2/np.sqrt(3)

jswth4 = jspresent
ajswtha4 = ajspresent

if 4 not in jswth4:
    jswth4 = np.append(4,jspresent)
    ajswtha4 = np.append(a4dephasing,ajspresent)
else:
    ajswtha4[jswth4==4] += a4dephasing

PSFinfoc = psf.PSF(jspresent,ajspresent,N,dxp,pupilRadius)

PSFoutfoc = psf.PSF(jswth4,ajswtha4,N,dxp,pupilRadius)
PSFoutfocPerf = psf.PSF([4],[a4dephasing],N,dxp,pupilRadius)

deltaPSFinFoc = PSFinfoc.Sp**2*PSFinfoc.PSF - PSFinfoc.Sp**2*PSFinfoc.perfectPSF
deltaPSFoutFoc = PSFoutfoc.Sp**2*PSFoutfoc.PSF - PSFoutfocPerf.Sp**2*PSFoutfocPerf.PSF

oddjs = fs.getOddJs(1,jmax)
ajsodd = .0*oddjs
ajsodd[oddjs==7]=10e-9/lbda*2*np.pi

f2j = fs.f2j(j,N,oddjs,ajsodd,deltaphi,dxp,pupilRadius)
y2 = (fs.y2(deltaPSFoutFoc,N,oddjs,ajsodd,deltaphi,dxp,pupilRadius)).reshape([400,400])

oddDeltaPSF = fs.getOddPart(deltaPSFoutFoc)
oddPhasor = ph.phasor(oddjs,ajsodd,N,dxp,pupilRadius)
oddPhase = oddPhasor.phase

pupilSin = oddPhasor.pupil*np.sin(deltaphi)
pupilCos = oddPhasor.pupil*np.cos(deltaphi)
FFTPupilSin =  fs.scaledfft2(pupilSin,dxp)
FFTPupilCos =  fs.scaledfft2(pupilCos,dxp)
cosOddPhase = np.cos(deltaphi)*oddPhase
sinOddPhase = np.sin(deltaphi)*oddPhase
FFTcosOddPhase = fs.scaledfft2(cosOddPhase,dxp)
FFTsinOddPhase =  fs.scaledfft2(sinOddPhase,dxp)

B = 2*np.real(np.conj(FFTPupilCos))*np.imag(FFTcosOddPhase) + 2*np.real(np.conj(FFTPupilSin))*np.imag(FFTsinOddPhase)

plt.figure()
plt.subplot(1,3,1)
plt.title('oddDeltaPSFoutfoc')
plt.imshow(oddDeltaPSF)
plt.colorbar(fraction=0.046, pad=0.04)
plt.xlim([180,220])
plt.ylim([180,220])
plt.subplot(1,3,2)
plt.title('2*im{PC*PCE+PS*PSE}')
plt.imshow(B)
plt.colorbar(fraction=0.046, pad=0.04)
plt.xlim([180,220])
plt.ylim([180,220])
plt.subplot(1,3,3)
plt.title('y2')
plt.imshow(y2)
plt.colorbar(fraction=0.046, pad=0.04)
plt.xlim([180,220])
plt.ylim([180,220])



oddDeltaPSFinfoc = fs.getOddPart(deltaPSFinFoc)
oddPhasor = ph.phasor(jspresent,ajspresent,N,dxp,pupilRadius)
pupil = oddPhasor.pupil
FFTpupil = fs.scaledfft2(pupil,dxp)
pupOddPhase = pupil*oddPhasor.phase
FFTpupOddPhase = fs.scaledfft2(pupOddPhase,dxp)

B = 2*np.imag(np.conj(FFTpupil)*FFTpupOddPhase)

plt.figure()
plt.subplot(1,3,1)
plt.title('oddDeltaPSFinfoc')
plt.imshow(oddDeltaPSFinfoc)
plt.colorbar(fraction=0.046, pad=0.04)
plt.xlim([180,220])
plt.ylim([180,220])
plt.subplot(1,3,2)
plt.title('2*im{P*PE}')
plt.imshow(B)
plt.colorbar(fraction=0.046, pad=0.04)
plt.xlim([180,220])
plt.ylim([180,220])
plt.subplot(1,3,3)
plt.title('oddDeltaPSFinfoc-2*im{P*PE}')
plt.imshow(oddDeltaPSFinfoc-B)
plt.colorbar(fraction=0.046, pad=0.04)
plt.xlim([180,220])
plt.ylim([180,220])
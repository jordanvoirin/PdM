#test f2j

import numpy as np
import fs
import matplotlib.pyplot as plt
import zernike as Z
import phasor as ph

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmax = 15
oddjs = fs.getOddJs(1,jmax)
evenjs = fs.getEvenJs(1,jmax)
ajsodd = np.zeros(jmax)
ajsodd[oddjs==7]=10e-9/lbda*2*np.pi     
deltaphi = fs.deltaPhi(N,deltaZ,F,2*pupilRadius,lbda,dxp)

j=4

Zj = Z.calc_zern_j(j,N,dxp,pupilRadius)

#compute the different 2Dfft given in the equations of deltaPSF
cosZj = np.cos(deltaphi)*Zj
sinZj = np.sin(deltaphi)*Zj
FFTcosZj =  fs.scaledfft2(cosZj,dxp)
FFTsinZj =  fs.scaledfft2(sinZj,dxp)

#odd phase
oddPhasor = ph.phasor(oddjs,ajsodd,N,dxp,pupilRadius)
oddPhase = oddPhasor.phase
pupil = oddPhasor.pupil
cosOddPhase = np.cos(deltaphi)*oddPhase
sinOddPhase = np.sin(deltaphi)*oddPhase
FFTcosOddPhase =  fs.scaledfft2(cosOddPhase,dxp)
FFTsinOddPhase =  fs.scaledfft2(sinOddPhase,dxp)

#2Dfft of pupil function times sin(deltaPhi) and cos(deltaPhi)
pupilSin = pupil*np.sin(deltaphi)
pupilCos = pupil*np.cos(deltaphi)
FFTPupilSin =  fs.scaledfft2(pupilSin,dxp)
FFTPupilCos =  fs.scaledfft2(pupilCos,dxp)

FFTsinZjOddPhase = fs.scaledfft2(sinZj*oddPhase,dxp)
FFTcosZjOddPhase = fs.scaledfft2(cosZj*oddPhase,dxp)

f2jrealimag = 2*(np.real(np.conj(FFTcosZj))*np.imag(FFTsinOddPhase)+np.real(FFTsinZj)*np.imag(np.conj(FFTcosOddPhase))
        - np.real(np.conj(FFTPupilCos))*np.imag(FFTsinZjOddPhase)+np.real(np.conj(FFTPupilSin))*np.imag(FFTcosZjOddPhase))
f2jimag = 2*np.imag(np.conj(FFTcosZj)*FFTsinOddPhase+FFTsinZj*np.conj(FFTcosOddPhase)
            - np.conj(FFTPupilCos)*FFTsinZjOddPhase+np.conj(FFTPupilSin)*FFTcosZjOddPhase)

plt.subplot(1,3,1)
plt.title('f2jimag j= %d'%(j))
plt.imshow(f2jimag,vmin= np.min(f2jimag),vmax = np.max(f2jimag))
plt.colorbar(fraction=0.046, pad=0.04)
plt.xlim([180,220])
plt.ylim([180,220])
plt.subplot(1,3,2)
plt.title('f2jrealimag j= %d'%(j))
plt.imshow(f2jrealimag,vmin= np.min(f2jrealimag),vmax = np.max(f2jrealimag))
plt.colorbar(fraction=0.046, pad=0.04)
plt.xlim([180,220])
plt.ylim([180,220])
plt.subplot(1,3,3)
plt.title('f2jimag-f2jrealimag j= %d'%(j))
plt.imshow(f2jimag-f2jrealimag,vmin= np.min(f2jimag-f2jrealimag),vmax = np.max(f2jimag-f2jrealimag))
plt.colorbar(fraction=0.046, pad=0.04)
plt.xlim([180,220])
plt.ylim([180,220])

#plt.figure()
#for ij,j in enumerate(evenjs):
#
#     # 2: phij's of matrix A to find a_j even
#    #Get the jth zernike polynomials values on a circular pupil of radius rad
#    Zj = Z.calc_zern_j(j,N,dxp,pupilRadius)
#    
#    #compute the different 2Dfft given in the equations of deltaPSF
#    cosZj = np.cos(deltaphi)*Zj
#    sinZj = np.sin(deltaphi)*Zj
#    FFTcosZj =  fs.scaledfft2(cosZj,dxp)
#    FFTsinZj =  fs.scaledfft2(sinZj,dxp)
#    
#    #odd phase
#    oddPhasor = ph.phasor(oddjs,ajsodd,N,dxp,pupilRadius)
#    oddPhase = oddPhasor.phase
#    pupil = oddPhasor.pupil
#    cosOddPhase = np.cos(deltaphi)*oddPhase
#    sinOddPhase = np.sin(deltaphi)*oddPhase
#    FFTcosOddPhase =  fs.scaledfft2(cosOddPhase,dxp)
#    FFTsinOddPhase =  fs.scaledfft2(sinOddPhase,dxp)
#    
#    #2Dfft of pupil function times sin(deltaPhi) and cos(deltaPhi)
#    pupilSin = pupil*np.sin(deltaphi)
#    pupilCos = pupil*np.cos(deltaphi)
#    FFTPupilSin =  fs.scaledfft2(pupilSin,dxp)
#    FFTPupilCos =  fs.scaledfft2(pupilCos,dxp)
#    
#    FFTsinZjOddPhase = fs.scaledfft2(sinZj*oddPhase,dxp)
#    FFTcosZjOddPhase = fs.scaledfft2(cosZj*oddPhase,dxp)
#    
#    f2jrealimag = 2*(np.real(FFTcosZj)*np.imag(np.conj(FFTsinOddPhase))+np.real(FFTsinZj)*np.imag(np.conj(FFTcosOddPhase))
#            - np.real(np.conj(FFTPupilCos))*np.imag(FFTsinZjOddPhase)+np.real(np.conj(FFTPupilSin))*np.imag(FFTcosZjOddPhase))
#    f2jimag = -2*np.imag(FFTcosZj*np.conj(FFTsinOddPhase)-FFTsinZj*np.conj(FFTcosOddPhase)
#                + np.conj(FFTPupilCos)*FFTsinZjOddPhase-np.conj(FFTPupilSin)*FFTcosZjOddPhase)
#                
#    
#    plt.subplot((np.shape(evenjs))[0],3,(ij+1)*2+(ij+1)-2)
#    plt.title('f2jimag j= %d'%(j))
#    plt.imshow(f2jimag,vmin= np.min(f2jimag),vmax = np.max(f2jimag))
#    plt.colorbar(fraction=0.046, pad=0.04)
#    plt.xlim([180,220])
#    plt.ylim([180,220])
#    plt.subplot((np.shape(evenjs))[0],3,(ij+1)*2+(ij+1)-1)
#    plt.title('f2jrealimag j= %d'%(j))
#    plt.imshow(f2jrealimag,vmin= np.min(f2jrealimag),vmax = np.max(f2jrealimag))
#    plt.colorbar(fraction=0.046, pad=0.04)
#    plt.xlim([180,220])
#    plt.ylim([180,220])
#    plt.subplot((np.shape(evenjs))[0],3,(ij+1)*2+(ij+1))
#    plt.title('f2jimag-f2jrealimag j= %d'%(j))
#    plt.imshow(f2jimag-f2jrealimag,vmin= np.min(f2jimag-f2jrealimag),vmax = np.max(f2jimag-f2jrealimag))
#    plt.colorbar(fraction=0.046, pad=0.04)
#    plt.xlim([180,220])
#    plt.ylim([180,220])
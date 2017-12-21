#functions to compute the matrix element of the system of equations Ax = b
import zernike as Z
import phasor as ph
import numpy as np

def f1j(j,N,dxp,pupilRadius): # 1: phij's of matrix A to find a_j odd
    Zj = Z.calc_zern_j(j,N,dxp,pupilRadius)
    FFTZj = scaledfft2(Zj,dxp)

    Lp = N*dxp
    xp = np.arange(-Lp/2,Lp/2,dxp)
    yp = xp

    [Xp,Yp]=np.meshgrid(xp,yp) 
    
    pupil = np.float64(np.sqrt(Xp**2+Yp**2)<=pupilRadius)
    FFTPupil = scaledfft2(pupil,dxp)

    return np.ravel(2 * np.real(FFTPupil) * np.imag(FFTZj))

def f2j(j,N,jsodd,ajsodd,deltaphi,pupilRadius,dxp): # 2: phij's of matrix A to find a_j even
    #Get the jth zernike polynomials values on a circular pupil of radius rad
    Zj = Z.calc_zern_j(j,N,dxp,pupilRadius)

    #compute the different 2Dfft given in the equations of deltaPSF
    cosZj = np.cos(deltaphi)*Zj
    sinZj = np.sin(deltaphi)*Zj
    FFTcosZj =  scaledfft2(cosZj,dxp)
    FFTsinZj =  scaledfft2(sinZj,dxp)

    #odd phase
    oddPhasor = ph.phasor(jsodd,ajsodd,N,dxp,pupilRadius)
    oddPhase = oddPhasor.phase
    pupil = oddPhasor.pupil
    cosOddPhase = np.cos(deltaphi)*oddPhase
    sinOddPhase = np.sin(deltaphi)*oddPhase
    FFTcosOddPhase =  scaledfft2(cosOddPhase,dxp)
    FFTsinOddPhase =  scaledfft2(sinOddPhase,dxp)

    #2Dfft of pupil function times sin(deltaPhi) and cos(deltaPhi)
    pupilSin = pupil*np.sin(deltaphi)
    pupilCos = pupil*np.cos(deltaphi)
    FFTPupilSin =  scaledfft2(pupilSin,dxp)
    FFTPupilCos =  scaledfft2(pupilCos,dxp)

    FFTsinZjOddPhase = scaledfft2(sinZj*oddPhase,dxp)
    FFTcosZjOddPhase = scaledfft2(cosZj*oddPhase,dxp)

    return np.ravel(-2*np.imag(FFTcosZj*np.conj(FFTsinOddPhase)-FFTsinZj*np.conj(FFTcosOddPhase)
            + np.conj(FFTPupilCos)*FFTsinZjOddPhase-np.conj(FFTPupilSin)*FFTcosZjOddPhase))

def y1(deltaPSFinFoc): #1: yi's of y to find a_j odd
    #compute the odd part of delta PSF
    oddDeltaPSF = getOddPart(deltaPSFinFoc)
    return np.ravel(oddDeltaPSF)

def y2(deltaPSFoutFoc,N,jsodd,ajsodd,deltaphi,dxp,pupilRadius): # 2: yi's of y to find a_j even
    oddDeltaPSF = getOddPart(deltaPSFoutFoc)
    oddPhasor = ph.phasor(jsodd,ajsodd,N,dxp,pupilRadius)
    oddPhase = oddPhasor.phase

    pupilSin = np.sin(deltaphi)
    pupilCos = np.cos(deltaphi)
    FFTPupilSin =  scaledfft2(pupilSin,dxp)
    FFTPupilCos =  scaledfft2(pupilCos,dxp)
    cosOddPhase = np.cos(deltaphi)*oddPhase
    sinOddPhase = np.sin(deltaphi)*oddPhase
    FFTcosOddPhase = scaledfft2(cosOddPhase,dxp)
    FFTsinOddPhase =  scaledfft2(sinOddPhase,dxp)

    return np.ravel(oddDeltaPSF - 2*np.imag(np.conj(FFTPupilCos)*FFTcosOddPhase
            +np.conj(FFTPupilSin)*FFTsinOddPhase))

#Other functions----------------------------------------------------------------------

def flipMatrix(M):
    #flip 2D matrix along x and y
    Mflipped = np.flipud(np.fliplr(M))
    return Mflipped
def getOddPart(F):
    oddF = (F - flipMatrix(F))/2.
    return oddF
def getEvenPart(F):
    evenF = (F + flipMatrix(F))/2.
    return evenF
def getOddJs(jmin,jmax):
    js = []
    for j in np.arange(jmin,jmax+1):
        [n,m] = Z.noll_to_zern(j)
        if np.mod(m,2) == 1:
            js.append(j)
        else:
            continue
    return js
def getEvenJs(jmin,jmax):
    js = []
    for j in np.arange(jmin,jmax+1):
        [n,m] = Z.noll_to_zern(j)
        if np.mod(m,2) == 0:
            js.append(j)
        else:
            continue
    return js
def deltaPhi(N,deltaZ,F,D,wavelength,dxp):
    Zj = Z.calc_zern_j(4,N,dxp,D/2.)

    P2Vdephasing = np.pi*deltaZ/wavelength*(D/F)**2/4.

    return Zj*P2Vdephasing/2
def cleanZeros(A,threshold):
    A[np.abs(A) < threshold] = 0.
    return A

def scaledfft2(A,dxp):
    return np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(A)))*dxp**2

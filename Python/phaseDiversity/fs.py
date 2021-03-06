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

def f2j(j,N,jsodd,ajsodd,deltaphi,dxp,pupilRadius): # 2: phij's of matrix A to find a_j even
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
    cosOddPhase = pupil*np.cos(deltaphi)*oddPhase
    sinOddPhase = pupil*np.sin(deltaphi)*oddPhase
    FFTcosOddPhase =  scaledfft2(cosOddPhase,dxp)
    FFTsinOddPhase =  scaledfft2(sinOddPhase,dxp)

    #2Dfft of pupil function times sin(deltaPhi) and cos(deltaPhi)
    pupilSin = pupil*np.sin(deltaphi)
    pupilCos = pupil*np.cos(deltaphi)
    FFTPupilSin =  scaledfft2(pupilSin,dxp)
    FFTPupilCos =  scaledfft2(pupilCos,dxp)

    FFTsinZjOddPhase = scaledfft2(sinZj*oddPhase,dxp)
    FFTcosZjOddPhase = scaledfft2(cosZj*oddPhase,dxp)

    return np.ravel(2*np.imag(np.conj(FFTcosZj) * FFTsinOddPhase + FFTsinZj * np.conj(FFTcosOddPhase)
            - np.conj(FFTPupilCos) * FFTsinZjOddPhase + np.conj(FFTPupilSin) * FFTcosZjOddPhase))
            
def f2jeven(j,N,deltaphi,dxp,pupilRadius): # 2: phij's of matrix A to find a_j even
    #Get the jth zernike polynomials values on a circular pupil of radius rad
    Zj = Z.calc_zern_j(j,N,dxp,pupilRadius)
    Phasor = ph.phasor([1],[0],N,dxp,pupilRadius)
    pupil = Phasor.pupil
    #compute the different 2Dfft given in the equations of deltaPSF
    cosZj = pupil*np.cos(deltaphi)*Zj
    sinZj = pupil*np.sin(deltaphi)*Zj
    FFTcosZj =  scaledfft2(cosZj,dxp)
    FFTsinZj =  scaledfft2(sinZj,dxp)
    #2Dfft of pupil function times sin(deltaPhi) and cos(deltaPhi)
    pupilSin = pupil*np.sin(deltaphi)
    pupilCos = pupil*np.cos(deltaphi)
    FFTPupilSin =  scaledfft2(pupilSin,dxp)
    FFTPupilCos =  scaledfft2(pupilCos,dxp)

    return np.ravel(-4*np.real(np.conj(FFTPupilCos)*FFTsinZj-np.conj(FFTPupilSin)*FFTcosZj))

def y1(deltaPSFinFoc): #1: yi's of y to find a_j odd
    #compute the odd part of delta PSF
    oddDeltaPSF = getOddPart(deltaPSFinFoc)
    return np.ravel(oddDeltaPSF)

def y2(deltaPSFoutFoc,N,jsodd,ajsodd,deltaphi,dxp,pupilRadius): # 2: yi's of y to find a_j even
    oddDeltaPSF = getOddPart(deltaPSFoutFoc)
    oddPhasor = ph.phasor(jsodd,ajsodd,N,dxp,pupilRadius)
    oddPhase = oddPhasor.phase

    pupilSin = oddPhasor.pupil*np.sin(deltaphi)
    pupilCos = oddPhasor.pupil*np.cos(deltaphi)
    FFTPupilSin =  scaledfft2(pupilSin,dxp)
    FFTPupilCos =  scaledfft2(pupilCos,dxp)
    cosOddPhase = oddPhasor.pupil*np.cos(deltaphi)*oddPhase
    sinOddPhase = oddPhasor.pupil*np.sin(deltaphi)*oddPhase
    FFTcosOddPhase = scaledfft2(cosOddPhase,dxp)
    FFTsinOddPhase =  scaledfft2(sinOddPhase,dxp)

    return np.ravel(oddDeltaPSF - 2*np.real(np.conj(FFTPupilCos))*np.imag(FFTcosOddPhase)
            - 2*np.real(np.conj(FFTPupilSin))*np.imag(FFTsinOddPhase))
            
def y2even(deltaPSFoutFocpos,deltaPSFoutfocneg): #3: yi's of y to find a_j even
    return np.ravel(deltaPSFoutFocpos-deltaPSFoutfocneg)
    
#Other functions----------------------------------------------------------------------
def flipMatrix(M):
    #flip 2D matrix along x and y
    dimM = (np.shape(M))[0]
    Mflipped = np.flipud(np.fliplr(M))
    if np.mod(dimM,2)==0:
        Mflipped = np.roll(Mflipped,1,axis=0)
        Mflipped = np.roll(Mflipped,1,axis=1)
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
    return np.array(js)
def getEvenJs(jmin,jmax):
    js = []
    for j in np.arange(jmin,jmax+1):
        [n,m] = Z.noll_to_zern(j)
        if np.mod(m,2) == 0:
            js.append(j)
        else:
            continue
    return np.array(js)
def deltaPhi(N,deltaZ,F,D,wavelength,dxp):
    Zj = Z.calc_zern_j(4,N,dxp,D/2.)
    P2Vdephasing = np.pi*deltaZ/wavelength*(D/F)**2/4.
    a4defocus = P2Vdephasing/2/np.sqrt(3)
    return a4defocus*Zj
def cleanZeros(A,threshold):
    A[np.abs(A) < threshold] = 0.
    return A
def scaledfft2(f,dxp):
    return np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(f)))*dxp**2
def RMSE(estimator,target):
    return np.sqrt(np.mean((estimator-target)**2))
def BIAS(estimator,target):
    return np.mean((estimator-target))
    
def RMSwavefrontError(js,ajs):
    if 1 in js:
        return np.sqrt(np.sum(ajs**2)-ajs[js==1]**2)
    else:
        return np.sqrt(np.sum(ajs**2))

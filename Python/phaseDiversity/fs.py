#functions to compute the matrix element of the system of equations Ax = b
import libtim.zern as Z
import libtim.im as im
import phasor as ph
import numpy as np

def f1j(j,N,rad): # 1: phij's of matrix A to find a_j odd
    zernike = Z.calc_zern_basis(1,rad,j)
    Zj = np.zeros((N,N))
    Zj[N/2-1-rad:N/2-1+rad,N/2-1-rad:N/2-1+rad] = zernike['modes'][0]/(Z.zern_normalisation(nmodes=j))[-1]
    FFTZj = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(Zj),norm='ortho'))

    grid_mask = (im.mk_rad_mask(2*rad)) <= 1
    pupil = np.zeros((N,N))
    pupil[N/2-1-rad:N/2-1+rad,N/2-1-rad:N/2-1+rad] = np.ones((2*rad,2*rad))*grid_mask
    FFTPupil = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(pupil),norm='ortho'))

    return np.ravel(2 * np.real(FFTPupil) * np.imag(FFTZj))

def f2j(j,N,rad,jsodd,ajsodd,deltaphi): # 2: phij's of matrix A to find a_j even
    #Get the jth zernike polynomials values on a circular pupil of radius rad
    zernike = Z.calc_zern_basis(1,rad,j)
    Zj = np.zeros((N,N))
    Zj[N/2-1-rad:N/2-1+rad,N/2-1-rad:N/2-1+rad] = zernike['modes'][0]/(Z.zern_normalisation(nmodes=j))[-1]

    #compute the different 2Dfft given in the equations of deltaPSF
    cosZj = np.cos(deltaphi)*Zj
    sinZj = np.sin(deltaphi)*Zj
    FFTcosZj =  np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(cosZj),norm='ortho'))
    FFTsinZj =  np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(sinZj),norm='ortho'))

    #odd phase
    oddPhasor = ph.phasor(jsodd,ajsodd,N,rad)
    oddPhase = oddPhasor.phase
    pupil = oddPhasor.pupil
    cosOddPhase = np.cos(deltaphi)*oddPhase
    sinOddPhase = np.sin(deltaphi)*oddPhase
    FFTcosOddPhase =  np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(cosOddPhase),norm='ortho'))
    FFTsinOddPhase =  np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(sinOddPhase),norm='ortho'))

    #2Dfft of pupil function times sin(deltaPhi) and cos(deltaPhi)
    pupilSin = pupil*np.sin(deltaphi)
    pupilCos = pupil*np.cos(deltaphi)
    FFTPupilSin =  np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(pupilSin),norm='ortho'))
    FFTPupilCos =  np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(pupilCos),norm='ortho'))

    FFTsinZjOddPhase = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(sinZj*oddPhase),norm='ortho'))
    FFTcosZjOddPhase = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(cosZj*oddPhase),norm='ortho'))

    return np.ravel(-2*np.imag(FFTcosZj*np.conj(FFTsinOddPhase)-FFTsinZj*np.conj(FFTcosOddPhase)
            + np.conj(FFTPupilCos)*FFTsinZjOddPhase-np.conj(FFTPupilSin)*FFTcosZjOddPhase))

def y1(deltaPSFinFoc): #1: yi's of y to find a_j odd
    #compute the
    oddDeltaPSF = getOddPart(deltaPSFinFoc)
    return np.ravel(oddDeltaPSF)

def y2(deltaPSFoutFoc,N,rad,jsodd,ajsodd,deltaphi): # 2: yi's of y to find 8b_j odd
    oddDeltaPSF = getOddPart(deltaPSFoutFoc)
    oddPhasor = ph.phasor(jsodd,ajsodd,N,rad)
    oddPhase = oddPhasor.phase
    #pupil = oddPhasor.pupil

    pupilSin = np.sin(deltaphi)
    pupilCos = np.cos(deltaphi)
    FFTPupilSin =  np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(pupilSin),norm='ortho'))
    FFTPupilCos =  np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(pupilCos),norm='ortho'))
    cosOddPhase = np.cos(deltaphi)*oddPhase
    sinOddPhase = np.sin(deltaphi)*oddPhase
    FFTcosOddPhase = np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(cosOddPhase),norm='ortho'))
    FFTsinOddPhase =  np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(sinOddPhase),norm='ortho'))

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
        if (-1)**m == -1:
            js.append(j)
        else:
            continue
    return js
def getEvenJs(jmin,jmax):
    js = []
    for j in np.arange(jmin,jmax+1):
        [n,m] = Z.noll_to_zern(j)
        if (-1)**m == 1:
            js.append(j)
        else:
            continue
    return js
def deltaPhi(N,rad,deltaZ,F,D,wavelength):
    zernike = Z.calc_zern_basis(1,rad,4)
    Zj = np.zeros((N,N))
    Zj[N/2-1-rad:N/2-1+rad,N/2-1-rad:N/2-1+rad] = zernike['modes'][0]/(Z.zern_normalisation(nmodes=4))[-1]

    P2Vdephasing = np.pi*deltaZ/wavelength*(D/F)**2/4

    return Zj*P2Vdephasing/2
def cleanZeros(A,threshold):
    A[np.abs(A) < threshold] = 0.
    return A

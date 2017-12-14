#function to compute the matrix of P~*(PZkodd)~ for a given j
import numpy as np
import libtim.zern as Z
import libtim.im as im
import phasor

def f1j(j,N,rad): # 1: phij's of matrix A to find a_j odd
    zernike = Z.calc_zern_basis(1,rad,j)
    Zj = np.zeros((N,N))
    Zj[(N-2*rad)/2:(N-2*rad)/2+2*rad,(N-2*rad)/2:(N-2*rad)/2+2*rad] = zernike['modes'][0]/(Z.zern_normalisation(nmodes=j))[-1]
    FFTZj = np.fft.fftshift(np.fft.fft2(Zj))

    grid_mask = (im.mk_rad_mask(2*rad)) <= 1
    pupil = np.zeros((N,N))
    pupil[(N-2*rad)/2:(N-2*rad)/2+2*rad,(N-2*rad)/2:(N-2*rad)/2+2*rad] = np.ones((2*rad,2*rad))*grid_mask
    FFTPupil = np.fft.fftshift(np.fft.fft2(pupil))

    return 2 * np.real(FFTPupil) * np.imag(FFTZj)

def f2j(j,N,rad): # 2: phij's of matrix A to find b_j=a_j^2 even
    #Get the jth zernike polynomials values on a circular pupil of radius rad
    zernike = Z.calc_zern_basis(1,rad,j)
    Zj = np.zeros((N,N))
    Zj[(N-2*rad)/2:(N-2*rad)/2+2*rad,(N-2*rad)/2:(N-2*rad)/2+2*rad] = zernike['modes'][0]/(Z.zern_normalisation(nmodes=j))[-1]
    #compute the different 2Dfft given in the equations of deltaPSF
    ZjNorm = np.abs(Zj)**2
    FFTZjNorm =  np.fft.fftshift(np.fft.fft2(ZjNorm))
    FFTZjsquare =  np.fft.fftshift(np.fft.fft2(Zj*Zj))

    #2Dfft of pupil function
    grid_mask = (im.mk_rad_mask(2*rad)) <= 1
    pupil = np.zeros((N,N))
    pupil[(N-2*rad)/2:(N-2*rad)/2+2*rad,(N-2*rad)/2:(N-2*rad)/2+2*rad] = np.ones((2*rad,2*rad))*grid_mask
    FFTPupil =  np.fft.fftshift(np.fft.fft2(pupil))

    return FFTZjNorm - np.real(FFTPupil)*np.real(FFTZjsquare)

def f3j(j,N,rad,deltaPhi): # 3: phij's of matrix A to find a_j even
    #Get the jth zernike polynomials values on a circular pupil of radius rad
    zernike = Z.calc_zern_basis(1,rad,j)
    Zj = np.zeros((N,N))
    Zj[(N-2*rad)/2:(N-2*rad)/2+2*rad,(N-2*rad)/2:(N-2*rad)/2+2*rad] = zernike['modes'][0]/(Z.zern_normalisation(nmodes=j))[-1]
    #compute the different 2Dfft given in the equations of deltaPSF
    cosZj = np.cos(deltaPhi)*Zj
    sinZj = np.sin(deltaPhi)*Zj
    FFTcosZj =  np.fft.fftshift(np.fft.fft2(cosZj))
    FFTsinZj =  np.fft.fftshift(np.fft.fft2(sinZj))

    #2Dfft of pupil function times sin(deltaPhi)
    grid_mask = (im.mk_rad_mask(2*rad)) <= 1
    pupilSin = np.zeros((N,N))
    pupilSin[(N-2*rad)/2:(N-2*rad)/2+2*rad,(N-2*rad)/2:(N-2*rad)/2+2*rad] = np.ones((2*rad,2*rad))*grid_mask*np.sin(deltaPhi)
    pupilCos = np.zeros((N,N))
    pupilCos[(N-2*rad)/2:(N-2*rad)/2+2*rad,(N-2*rad)/2:(N-2*rad)/2+2*rad] = np.ones((2*rad,2*rad))*grid_mask*np.cos(deltaPhi)
    FFTPupilSin =  np.fft.fftshift(np.fft.fft2(pupilSin))
    FFTPupilCos =  np.fft.fftshift(np.fft.fft2(pupilCos))

    return 2*(np.real(np.conj(FFTPupilSin))*np.real(FFTcosZj)+np.real(np.conj(FFTPupilCos))*np.real(FFTsinZj))

def y1(deltaPSFinFoc): #1: yi's of y to find a_j odd
    #compute the
    oddDeltaPSF = getOddPart(deltaPSFinFoc)
    return np.ravel(oddDeltaPSF)

def y2(deltaPSFinFoc,N,rad,jsodd,ajsodd): # 2: yi's of y to find b_j odd
    evenPSF = getPSFEvenPart(deltaPSFinFoc)
    phasor = phasor(jsodd,ajsodd,rad)
    phase = phasor.phase

    return

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
    for j in np.arange(jmin,jmax+1)
        [n,m] = Z.noll_to_zern(j)
        if (-1)**m == -1:
            js.append(j)
        else:
            continue
    return js
def getEvenJs(jmin,jmax):
    js = []
    for j in np.arange(jmin,jmax+1)
        [n,m] = Z.noll_to_zern(j)
        if (-1)**m == 1:
            js.append(j)
        else:
            continue
    return js
def deltaPhi(N,rad,deltaZ,F,D,wavelength):
    zernike = zern.calc_zern_basis(1,rad,4)
    Zj = np.zeros((N,N))
    Zj[(N-2*rad)/2:(N-2*rad)/2+2*rad,(N-2*rad)/2:(N-2*rad)/2+2*rad] = zernike['modes'][0]/(Z.zern_normalisation(nmodes=j))[-1]

    P2Vdephasing = np.pi*deltaZ/wavelength*(D/F)**2

    return Zj*P2Vdephasing

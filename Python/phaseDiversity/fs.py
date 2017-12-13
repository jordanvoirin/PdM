#function to compute the matrix of P~*(PZkodd)~ for a given j
import numpy as np
from libtim import all

def f1j(j,pupilRadius,dxp): #phij of matrix A to find a_j odd
    rad = int(np.ceil(pupilRadius/dxp))
    zernike = zern.calc_zern_basis(1,rad,j)
    Zj = zernike['modes'][0]/(zern_normalisation(nmodes=j))[-1]
    FFTZj = np.fft.fftshift(np.fft.fft2(Zj))

    grid_mask = (im.mk_rad_mask(2*rad)) <= 1
    pupil = np.ones((2*rad,2*rad))*grid_mask
    FFTPupil = np.fft.fftshift(np.fft.fft2(pupil))

    return 2 * np.real(FFTPupil) .* np.imag(FFTZj)

def f2j(j,pupilRadius,dxp): #phij of matrix A to find b_j=a_j^2 even
    rad = int(np.ceil(pupilRadius/dxp))
    #Get the jth zernike polynomials values on a circular pupil of radius rad
    zernike = zern.calc_zern_basis(1,rad,j)
    Zj = zernike['modes'][0]/(zern_normalisation(nmodes=j))[-1]
    #compute the different 2Dfft given in the equations of deltaPSF
    ZjNorm = np.abs(Zj)**2
    FFTZjNorm =  np.fft.fftshift(np.fft.fft2(ZjNorm))
    FFTZjsquare =  np.fft.fftshift(np.fft.fft2(Zj.*Zj))

    #2Dfft of pupil function
    grid_mask = (im.mk_rad_mask(2*rad)) <= 1
    pupil = np.ones((2*rad,2*rad))*grid_mask
    FFTPupil =  np.fft.fftshift(np.fft.fft2(pupil))

    return FFTZjNorm - np.real(FFTPupil).*np.real(FFTZjsquare)

def f3j(j,pupilRadius,dxp,deltaPhi): #phij of matrix A to find a_j even
    rad = int(np.ceil(pupilRadius/dxp))
    #Get the jth zernike polynomials values on a circular pupil of radius rad
    zernike = zern.calc_zern_basis(1,rad,j)
    Zj = zernike['modes'][0]/(zern_normalisation(nmodes=j))[-1]
    #compute the different 2Dfft given in the equations of deltaPSF
    cosZj = np.cos(deltaPhi).*Zj
    sinZj = np.sin(deltaPhi).*Zj
    FFTcosZj =  np.fft.fftshift(np.fft.fft2(cosZj))
    FFTsinZj =  np.fft.fftshift(np.fft.fft2(sinZj))

    #2Dfft of pupil function times sin(deltaPhi)
    grid_mask = (im.mk_rad_mask(2*rad)) <= 1
    pupilSin = np.ones((2*rad,2*rad)).*grid_mask.*np.sin(deltaPhi)
    pupilCos = np.ones((2*rad,2*rad)).*grid_mask.*np.cos(deltaPhi)
    FFTPupilSin =  np.fft.fftshift(np.fft.fft2(pupilSin))
    FFTPupilCos =  np.fft.fftshift(np.fft.fft2(pupilCos))

    return 2*(np.real(np.conj(FFTPupilSin)).*np.real(FFTcosZj)+np.real(np.conj(FFTPupilCos)).*np.real(FFTsinZj))

def getPSFOddPart(PSF):

    


def y1(inFoc)

    oddPSF = getPSFOddPart

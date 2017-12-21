import numpy as np
import phasor as ph
import fs

class PSF(object):

    def __init__(self,js=[1],ajs=[0],N=800,dxp=1.,pupilRadius = 200.):
        self.phasor = ph.phasor(js,ajs,N,dxp,pupilRadius) #phasor in the pupil
        self.Sp = np.sum(self.phasor.pupil)*dxp**2 #pupil surface
        self.FFTphasor = fs.scaledfft2(self.phasor.phasor,dxp) #fourier transform of the phasor
        self.PSF = np.abs(self.FFTphasor)**2/self.Sp**2 #PSF on the focal plane
        self.FFTpupil = fs.scaledfft2(self.phasor.pupil,dxp) #fourier transform of the pupil function which gives the perfect PSF
        self.perfectPSF = np.abs(self.FFTpupil)**2/self.Sp**2 #perfect PSF
        self.deltaPSF = self.Sp**2*self.PSF-self.Sp**2*self.perfectPSF #deltaPSF

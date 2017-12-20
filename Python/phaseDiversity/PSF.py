import numpy as np
import phasor as ph
import fs

class PSF(object):
    
    def __init__(self,js=[1],ajs=[0],N=800,rad=200,dxp=1.):
        self.phasor = ph.phasor(js,ajs,N,rad)
        self.FFTphasor = fs.scaledfft2(self.phasor.phasor,dxp) 
        self.PSF = np.abs(self.FFTphasor)**2/(np.sum(self.phasor.pupil)*dxp**2)**2
        self.FFTpupil = fs.scaledfft2(self.phasor.pupil,dxp) 
        self.perfectPSF = np.abs(self.FFTpupil)**2/(np.sum(self.phasor.pupil)*dxp**2)**2
        self.deltaPSF = self.PSF-self.perfectPSF
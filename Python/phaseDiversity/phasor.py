#class phasor
import numpy as np
import libtim.zern as zern
import libtim.im as im

class phasor(object):

    def __init__(self,js=[1],ajs=[0],pupilRadius=1.6e-3,dxp=2.405660377358491e-05):
        self.js = js
        self.ajs = ajs
        self.pupilRadius = pupilRadius
        self.dxp = dxp
        self.rad = int(np.ceil(pupilRadius/dxp))
        self.grid_mask = (im.mk_rad_mask(2*self.rad)) <= 1
        self.pupil = np.ones((2*self.rad,2*self.rad))*self.grid_mask
        self.phase = self.constructPhase()
        self.phasor = self.pupil*np.exp(-1j*self.phase)

    def constructPhase(self):
        phase = np.zeros((2*self.rad,2*self.rad))
        for ij, j in enumerate(self.js):
            zernike = zern.calc_zern_basis(1,self.rad,j)
            Zj = zernike['modes'][0]/(zern.zern_normalisation(nmodes=j))[-1]
            phase += self.ajs[ij]*Zj
        return phase

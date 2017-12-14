#class phasor
import numpy as np
import libtim.zern as zern
import libtim.im as im

class phasor(object):

    def __init__(self,js=[1],ajs=[0],N=800,rad=200):
        self.js = js
        self.ajs = ajs
        self.rad = rad
        self.grid_mask = (im.mk_rad_mask(2*self.rad)) <= 1
        self.pupil = np.zeros((N,N))
        self.pupil[(N-2*self.rad)/2:(N-2*self.rad)/2+2*self.rad,(N-2*self.rad)/2:(N-2*self.rad)/2+2*self.rad] = np.ones((2*self.rad,2*self.rad))*self.grid_mask
        self.phase = np.zeros((N,N))
        self.phase[(N-2*rad)/2:(N-2*rad)/2+2*rad,(N-2*rad)/2:(N-2*rad)/2+2*rad] = self.constructPhase()
        self.phasor = self.pupil*np.exp(-1j*self.phase)

    def constructPhase(self):
        phase = np.zeros((2*self.rad,2*self.rad))
        for ij, j in enumerate(self.js):
            zernike = zern.calc_zern_basis(1,self.rad,j)
            Zj = zernike['modes'][0]/(zern.zern_normalisation(nmodes=j))[-1]
            phase += self.ajs[ij]*Zj
        return phase

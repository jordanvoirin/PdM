#class phasor
import numpy as np
import zernike as Z



class phasor(object):

    def __init__(self,js=[1],ajs=[0],N=800,dxp=1,pupilRadius = 200):
        self.js = js
        self.ajs = ajs
        self.N = N
        self.dxp = dxp
        self.pupilRadius = pupilRadius
        
        self.pupil = self.constructPupil()
        
        self.phase = self.constructPhase()
        self.phasor = self.pupil*np.exp(-1j*self.phase)

    def constructPhase(self):
        phase = np.zeros((self.N,self.N))
        for ij, j in enumerate(self.js):
            Zj = Z.calc_zern_j(j,self.N,self.dxp,self.pupilRadius)
            phase += self.ajs[ij]*Zj
        return phase
        
    def constructPupil(self):
        Lp = self.N*self.dxp

        xp = np.arange(-Lp/2,Lp/2,self.dxp)
        yp = xp

        [Xp,Yp]=np.meshgrid(xp,yp)
        
        pup = np.float64(np.sqrt(Xp**2+Yp**2)<=self.pupilRadius)
        return pup

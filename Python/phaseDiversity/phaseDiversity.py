#Class phaseDiversity object to retrieve the phase in the pupil from two psfs in/out of focus

import libtim.zern as Z
import numpy as np
import fs

class phaseDiversity(object):

    def __init__(self,inFoc,outFoc,deltaZ,lbda,pxsize,F,pupilRadius,Nj):
        self.inFoc = inFoc
        self.outFoc = outFoc
        self.N = np.shape(inFoc,0)
        self.deltaZ = deltaZ
        self.lbda = lbda
        self.pxsize = pxsize
        self.F = F
        self.pupilRadius = pupilRadius
        self.dxp = self.F*self.lbda/(self.N*self.pxsize)
        self.Nj = Nj

    def instanciateMatrices():
        fs.f1j

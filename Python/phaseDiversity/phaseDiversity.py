#Class phaseDiversity object to retrieve the phase in the pupil from two psfs in/out of focus

import libtim.zern as Z
import numpy as np
import fs
import myExceptions

class phaseDiversity(object):

    def __init__(self,inFoc,outFoc,deltaZ,lbda,pxsize,F,pupilRadius,Nj):

        self.inFoc = inFoc
        self.outFoc = outFoc
        shapeinFoc = np.shape(self.inFoc)
        shapeoutFoc = np.shape(self.outFoc)
        if shapeinFoc == shapeoutFoc:
            self.shape = shapeinFoc
        else:
            raise PSFssizeError('the shape of the in/out PSFs is not the same',[shapeinFoc,shapeoutFoc])
        if shapeinFoc[0]==shapeinFoc[1] and np.mod(shapeinFoc[0],2)==0:
            self.N = shapeinFoc[0]
        else:
            raise PSFssizeError('Either PSF is not square or mod(N,2) != 0',shapeinFoc)
        self.deltaZ = deltaZ
        self.lbda = lbda
        self.pxsize = pxsize
        self.F = F
        self.pupilRadius = pupilRadius
        self.dxp = self.F*self.lbda/(self.N*self.pxsize)
        self.rad = int(np.ceil(self.pupilRadius/self.dxp))
        if 2*self.rad > self.N/2:
            raise myExceptions.PupilSizeError('Npupil (2*rad) is bigger than N/2 which is not correct for the fft computation',[])
        self.NyquistCriterion()
        self.Nj = Nj

    def NyquistCriterion(self):
        deltaXfnyq = 0.5*self.lbda/(2*self.pupilRadius)
        deltaXf = self.pxsize/self.F
        if deltaXfnyq < deltaXf : raise NyquistError('the system properties do not respect the nyquist criterion',[])

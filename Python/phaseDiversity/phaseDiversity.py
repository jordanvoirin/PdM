#Class phaseDiversity object to retrieve the phase in the pupil from two psfs in/out of focus

import numpy as np
import fs
import myExceptions
import PSF as psf

class phaseDiversity(object):

    def __init__(self,inFoc,outFoc,deltaZ,lbda,pxsize,F,pupilRadius,jmax):
        
        #PSF
        self.inFoc = inFoc
        self.outFoc = outFoc
        shapeinFoc = np.shape(self.inFoc)
        shapeoutFoc = np.shape(self.outFoc)
        if shapeinFoc == shapeoutFoc:
            self.shape = shapeinFoc
        else:
            raise myExceptions.PSFssizeError('the shape of the in/out PSFs is not the same',[shapeinFoc,shapeoutFoc])
        if shapeinFoc[0]==shapeinFoc[1] and np.mod(shapeinFoc[0],2)==0:
            self.N = shapeinFoc[0]
        else:
            raise myExceptions.PSFssizeError('Either PSF is not square or mod(N,2) != 0',shapeinFoc)
            
        # properties   
        self.deltaZ = deltaZ
        self.lbda = lbda
        self.pxsize = pxsize
        self.F = F
        self.pupilRadius = pupilRadius
        self.dxp = self.F*self.lbda/(self.N*self.pxsize)
        self.rad = int(np.ceil(self.pupilRadius/self.dxp))
        if 2*self.rad > self.N/2.:
            raise myExceptions.PupilSizeError('Npupil (2*rad) is bigger than N/2 which is not correct for the fft computation',[])
        self.NyquistCriterion()
        self.jmax = jmax
        self.oddjs = fs.getOddJs(1,self.jmax)
        self.evenjs = fs.getEvenJs(1,self.jmax)
        
        # result computation
        self.result = self.retrievePhase()

    def NyquistCriterion(self):
        deltaXfnyq = 0.5*self.lbda/(2*self.pupilRadius)
        deltaXf = self.pxsize/self.F
        if deltaXfnyq < deltaXf : raise myExceptions.NyquistError('the system properties do not respect the nyquist criterion',[])

    def retrievePhase(self):
        y1,A1 = self.initiateMatrix1()
        results1 = np.linalg.lstsq(A1,y1)
        ajsodd = results1[0]
        deltaphi = fs.deltaPhi(self.N,self.deltaZ,self.F,2*self.pupilRadius,self.lbda,self.dxp)
        y2,A2 = self.initiateMatrix2(ajsodd,deltaphi)
        results2 = np.linalg.lstsq(A2,y2)
        ajseven = results2[0]

        js = np.append(self.oddjs,self.evenjs)
        ajs = np.append(ajsodd,ajseven)

        Ixjs = np.argsort(js)
        result = {'js': js[Ixjs], 'ajs': ajs[Ixjs]*self.lbda/2/np.pi} #,'wavefront':phase}
        return result

    def initiateMatrix1(self):
        deltaPSFinFoc = self.CMPTEdeltaPSF()
        y1 = fs.y1(deltaPSFinFoc)
        A1 = np.zeros((self.N**2,len(self.oddjs)))
        for ij in np.arange(len(self.oddjs)):
            phiJ = fs.f1j(self.oddjs[ij],self.N,self.dxp,self.pupilRadius)
            A1[:,ij] = phiJ
        return y1,A1

    def initiateMatrix2(self,ajsodd,deltaphi):
        
        deltaPSFoutFoc = self.CMPTEdeltaPSF(self.deltaZ)
        y2 = fs.y2(deltaPSFoutFoc,self.N,self.oddjs,ajsodd,deltaphi,self.dxp,self.pupilRadius)
        A2 = np.zeros((self.N**2,len(self.evenjs)))
        for ij in np.arange(len(self.evenjs)):
            phiJ = fs.f2j(self.evenjs[ij],self.N,self.oddjs,ajsodd,deltaphi,self.dxp,self.pupilRadius)
            A2[:,ij] = phiJ
        return y2,A2

    def CMPTEdeltaPSF(self,deltaZ=[]):
        if not deltaZ:
            PSF = psf.PSF([1],[0],self.N,self.dxp,self.pupilRadius)
            return PSF.Sp**2*self.inFoc - PSF.Sp**2*PSF.PSF
        else:
            P2Vdephasing = np.pi*self.deltaZ/self.lbda*(2*self.pupilRadius/self.F)**2/4.
            a4 = P2Vdephasing/2./np.sqrt(6)
            PSF = psf.PSF([4],[a4],self.N,self.dxp,self.pupilRadius)
            return PSF.Sp**2*self.outFoc - PSF.Sp**2*PSF.PSF

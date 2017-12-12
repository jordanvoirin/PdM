import numpy as np
from libtim import *


def deltaPhi(pupilRadius,dxp,deltaZ,F,D,wavelength):
    rad = np.ceil(pupilRadius/dxp)
    zernike = zern.calc_zern_basis(1,rad,4)
    Zj = zernike['modes'][0]/(zern_normalisation(nmodes=j))[-1]

    P2Vdephasing = np.pi*deltaZ/wavelength*(D/F)**2

    return Zj*P2Vdephasing

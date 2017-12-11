import numpy as np
from libtim import All


def deltaPhi(j,pupilRadius,size,pixelSize,deltaZ,F,D,wavelength):
    dxp = 1./pixelSize
    rad = np.ceil(pupilRadius/dxp)
    zernike = zern.calc_zern_basis(1,rad,j)
    Zj = zernike['modes'][0]/(zern_normalisation(nmodes=j))[-1]

    P2Vdephasing = np.pi*deltaZ/wavelength*(D/F)**2

    return Zj*P2Vdephasing

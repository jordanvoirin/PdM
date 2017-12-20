import numpy as np


def calc_zern_j(j, N, dxp, pupilRadius):

    Lp = N*dxp

    if (j <= 0):
		return {'modes':[], 'modesmat':[], 'covmat':0, 'covmat_in':0, 'mask':[[0]]}
	if (N <= 0):
		raise ValueError("N should be > 0")
    if (dxp <= 0 or dxp >= N):
		raise ValueError("dxp should be > 0 or < N")
	if (modestart <= 0):
		raise ValueError("**modestart** Noll index should be > 0")

    xp = np.arange(-Lp/2,Lp/2,dxp)
    yp = xp

    [Xp,Yp]=np.meshgrid(xp,yp)

    r = np.sqrt(Xp**2+Yp**2)
    r = r[r<=pupilRadius]/r
    theta = np.arctan2(Yp,Xp)

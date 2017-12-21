import numpy as np


def calc_zern_j(j, N, dxp, pupilRadius):

    Lp = N*dxp
    
    if (j <= 0):
    		return {'modes':[], 'modesmat':[], 'covmat':0, 'covmat_in':0, 'mask':[[0]]}
    if (N <= 0):
    		raise ValueError("N should be > 0")
    if (dxp <= 0 or dxp >= N):
    		raise ValueError("dxp should be > 0 or < N")
    
    xp = np.arange(-Lp/2,Lp/2,dxp)
    yp = xp

    [Xp,Yp]=np.meshgrid(xp,yp) 
    r = np.sqrt(Xp**2+Yp**2)
    r = r*(r<=pupilRadius)/pupilRadius
    pup = np.float64(np.sqrt(Xp**2+Yp**2)<=pupilRadius)
    theta = np.arctan2(Yp,Xp)

    Zj = zernike(j,r,theta)*pup
    return Zj

def zernike(j,r,theta):
    n,m = noll_to_zern(j)
    nc = 1.0
    #nc = (2*(n+1)/(1+(m==0)))**0.5
    if (m > 0): return nc*zernike_rad(m, n, r) * np.cos(m * theta)
    if (m < 0): return nc*zernike_rad(-m, n, r) * np.sin(-m * theta)
    return nc*zernike_rad(0, n, r)

def zernike_rad(m, n, r):
    if (np.mod(n-m, 2) == 1):
        return r*0.0
    wf = r*0.0
    for k in range((n-m)/2+1):
        wf += r**(n-2.0*k) * (-1.0)**k * fac(n-k) / ( fac(k) * fac( (n+m)/2.0 - k ) * fac( (n-m)/2.0 - k ) )
    return wf

def noll_to_zern(j):
    if (j == 0):
        raise ValueError("Noll indices start at 1, 0 is invalid.")
    n = 0
    j1 = j-1
    while (j1 > n):
        n += 1
        j1 -= n
    m = (-1)**j * ((n % 2) + 2 * int((j1+((n+1)%2)) / 2.0 ))
    return (n, m)
def fac(n):
    if n == 0:
        return 1
    else:
        return n * fac(n-1)
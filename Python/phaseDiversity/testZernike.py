#test zernike 
import numpy as np
import zernike as Z
import matplotlib.pyplot as plt
import fs

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
j=4

Zj = Z.calc_zern_j(j,N,dxp,pupilRadius)

plt.figure()
plt.imshow(Zj)

deltaZ = 3.19e-3
deltaphi = fs.deltaPhi(N,deltaZ,F,2*pupilRadius,lbda,dxp)

plt.figure()
plt.title('DeltaPhi')
plt.imshow(deltaphi,vmin = np.min(deltaphi), vmax = np.max(deltaphi))
plt.colorbar(fraction=0.046, pad=0.04)
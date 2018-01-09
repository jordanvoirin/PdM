#test zernike 
import numpy as np
import zernike as Z
import matplotlib.pyplot as plt

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
j=9

Zj = Z.calc_zern_j(j,N,dxp,pupilRadius)

plt.figure()
plt.imshow(Zj)
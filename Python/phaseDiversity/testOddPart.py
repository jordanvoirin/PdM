import fs
import numpy as np
import libtim.zern as Z
import matplotlib.pyplot as plt

zernike = Z.calc_zern_basis(1,200,8)
Zj = zernike['modes'][0]/(Z.zern_normalisation(nmodes=8))[-1]

plt.figure()
plt.subplot(3,2,1)
plt.imshow(Zj)
plt.subplot(3,2,2)
plt.imshow(fs.flipMatrix(Zj))
plt.subplot(3,2,3)
plt.imshow((Zj+fs.flipMatrix(Zj))/2.)
plt.subplot(3,2,4)
plt.imshow((Zj-fs.flipMatrix(Zj))/2.)
plt.subplot(3,2,5)
plt.imshow(Zj-((Zj+fs.flipMatrix(Zj))/2.+(Zj-fs.flipMatrix(Zj))/2.),vmin=1e-6,vmax=1.)


C = np.array([[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20]])

M = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])

print (M+fs.flipMatrix(M))/2.+(M-fs.flipMatrix(M))/2.
print fs.flipMatrix(C)
import fs
import numpy as np
import zernike as Z
import matplotlib.pyplot as plt
#%matplotlib inline
#%config InlineBackend.figure_format = 'svg'

Zj = Z.calc_zern_j(8,400,1)

plt.figure()
plt.subplot(3,2,1)
plt.imshow(Zj)
plt.subplot(3,2,2)
plt.imshow(fs.flipMatrix(Zj))
plt.subplot(3,2,3)
plt.imshow(fs.cleanZeros((Zj+fs.flipMatrix(Zj))/2.,1e-2))
plt.subplot(3,2,4)
plt.imshow(fs.cleanZeros((Zj-fs.flipMatrix(Zj))/2.,1e-2))
plt.subplot(3,2,5)
plt.imshow(fs.cleanZeros(Zj-((Zj+fs.flipMatrix(Zj))/2.+(Zj-fs.flipMatrix(Zj))/2.),1e-13),vmin=1e-16,vmax=1e-12)


C = np.array([[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20]])

M = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])

print (M+fs.flipMatrix(M))/2.+(M-fs.flipMatrix(M))/2.
print fs.flipMatrix(C)

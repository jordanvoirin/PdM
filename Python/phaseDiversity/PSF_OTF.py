import numpy as np
import matplotlib.pyplot as plt
import PSF as psf
import fs
from mpl_toolkits.mplot3d.axes3d import Axes3D

def OTF(PSF,dxp):
    return fs.scaledfft2(PSF,dxp)

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)

Lp = N*dxp

xp = np.arange(-Lp/2,Lp/2,dxp)
yp = xp
[Xp,Yp]=np.meshgrid(xp,yp) 


PSF = psf.PSF([6,11],np.array([0,0])*1e-9/lbda*2*np.pi,N,dxp,pupilRadius)
PSFdef = psf.PSF([4,6,11],np.array([637.5,50,50])*1e-9/lbda*2*np.pi,N,dxp,pupilRadius)

otf = OTF(PSF.PSF,dxp)

plt.figure()
plt.imshow(PSF.phasor.phase)
plt.xlim([132,268])
plt.ylim([132,268])
plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labeltop='off',
    labelright='off',
    labelleft='off')
plt.show()

plt.figure()
plt.imshow(PSF.PSF)
plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labeltop='off',
    labelright='off',
    labelleft='off')
plt.show()

plt.figure()
plt.imshow(PSF.PSF)
plt.xlim([180,220])
plt.ylim([180,220])
plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labeltop='off',
    labelright='off',
    labelleft='off')
plt.show()

plt.figure()
plt.imshow(PSFdef.PSF)
plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labeltop='off',
    labelright='off',
    labelleft='off')
plt.show()

plt.figure()
plt.imshow(PSFdef.PSF)
plt.xlim([180,220])
plt.ylim([180,220])
plt.tick_params(
    axis='both',       # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off',
    labeltop='off',
    labelright='off',
    labelleft='off')
plt.show()

fig = plt.figure()
ax3d = Axes3D(fig)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(Xp/np.max(Xp), Yp/np.max(Yp), otf/np.max(otf))
plt.xlim([-1,1])
plt.ylim([-1,1])

plt.show(fig)
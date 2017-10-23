import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


angles = np.array([0., 5., 10., 15., 20., 25., 30., 35., 40., 45., 50., 55.])
anglesRad = angles/180*np.pi

nAir = 1.000293
nPlexi = 1.49

d = 0.01 #[m]

ds = d/np.cos(anglesRad)

OPD = ds*nPlexi-d*nAir

plt.figure()
plt.plot(angles, OPD*1000)
plt.xlabel('Angle [$^{\circ}$]')
plt.ylabel('OPD [mm]')
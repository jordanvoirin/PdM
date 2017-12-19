import phaseDiversity as PD
import numpy as np
import phasor as ph

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmax = 30

a4dephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4./2.

rad = int(np.ceil(pupilRadius/dxp))

phasorinFoc = ph.phasor([7],[10e-9/lbda],N,rad)
FFTPupilinFoc = np.fft.fftshift(np.fft.fft2(phasorinFoc.phasor))
PSFinFoc = np.abs(FFTPupilinFoc)**2/np.sum(phasorinFoc.pupil)**2

phasoroutFoc = ph.phasor([4,7],[a4dephasing,10e-9/lbda],N,rad)
FFTPupiloutFoc = np.fft.fftshift(np.fft.fft2(phasoroutFoc.phasor))
PSFoutFoc = np.abs(FFTPupiloutFoc)**2/np.sum(phasoroutFoc.pupil)**2

phaseDiv = PD.phaseDiversity(PSFinFoc,PSFoutFoc,deltaZ,lbda,pxsize,F,pupilRadius,jmax)

print phaseDiv.result['ajsodd']

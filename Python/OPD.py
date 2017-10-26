# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import numpy as np
import matplotlib.pyplot as plt

def abberationAstigmatism(n,e,up,N):
    return (n**2-1)*e*up**2/(2*n**3*N)
    
n = 1.49
e = 1.4e-2
phi = np.linspace(0,60,13)
theta = 90-phi
beta = 90-theta
pup = 3.2e-3
f = 200e-3
N = f/pup
alphamax = np.arctan(pup/f)
alphamin = np.arctan(-pup/f)
upmax = (beta+alphamax)*np.pi/180
upmin = (beta+alphamin)*np.pi/180

OPDmaxmin = abberationAstigmatism(n,e,upmax,N)-abberationAstigmatism(n,e,upmin,N)

plt.figure()
plt.plot(phi,OPDmaxmin*1e9,'b-2')
plt.xlabel('Plane Parallel Plate Angle [$^{\circ}$]')
plt.ylabel('P2V OPD [nm]')
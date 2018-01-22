import fsAnalyzePD as fsApd
import numpy as np
import PSF as psf
import copy
import os
import pyfits

def savePSFasFits(folderPath,data,rmsWFe,jmax,pos):
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath)   
    
    imgHdu = pyfits.PrimaryHDU(data)
    hdulist = pyfits.HDUList([imgHdu])
    hdulist.writeto(folderPath +'PSFtheoretical_rmsWFe_'+str(int(rmsWFe))+'_jmax_'+str(int(jmax))+'_'+str(pos)+'.fits', clobber=True)

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmax = 30
jmin = 4

P2Vdephasing = np.pi*deltaZ/lbda*(2*pupilRadius/F)**2/4.
a4dephasing = P2Vdephasing/2/np.sqrt(3)

rmsWFerrors = np.array([1,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,115,130,150,175,200])

js = np.linspace(jmin,jmax,num=jmax-3)
for i, rmsWFerror in enumerate(rmsWFerrors):
    folderPath='../../../data/devPD/PSFforIDLtreatment/PSFs/rmsWFerror_'+str(int(rmsWFerror))+'/'
    ajsFilePath = '../../../data/devPD/PSFforIDLtreatment/ajsTrue/ajstrue_rmsWFe_'+str(int(rmsWFerror))+'.txt'
    ajstrue = fsApd.getRandomAjs(js,rmsWFerror)*1e-9/lbda*2*np.pi
    jaj = np.vstack((js,ajstrue))
    np.savetxt(ajsFilePath,jaj)
    
    jswth4 = copy.deepcopy(js)
    ajswtha4pos = copy.deepcopy(ajstrue)
    ajswtha4neg = copy.deepcopy(ajstrue)
    
    if 4 not in jswth4:
        jswth4 = np.append(4,js)
        ajswtha4pos = np.append(a4dephasing,ajstrue)
        ajswtha4neg = np.append(-a4dephasing,ajstrue)
    else:
        ajswtha4pos[jswth4==4] += a4dephasing
        ajswtha4neg[jswth4==4] -= a4dephasing
    
    PSFinfoc = psf.PSF(js,ajstrue,N,dxp,pupilRadius)
    savePSFasFits(folderPath,PSFinfoc.PSF,rmsWFerror,jmax,0)    
    
    PSFoutfocpos = psf.PSF(jswth4,ajswtha4pos,N,dxp,pupilRadius)
    savePSFasFits(folderPath,PSFoutfocpos.PSF,rmsWFerror,jmax,319)
    
    PSFoutfocneg = psf.PSF(jswth4,ajswtha4neg,N,dxp,pupilRadius)
    savePSFasFits(folderPath,PSFoutfocneg.PSF,rmsWFerror,jmax,-319)
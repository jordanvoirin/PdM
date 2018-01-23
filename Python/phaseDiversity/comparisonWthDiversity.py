import phaseDiversity3PSFs as PD
import numpy as np
import matplotlib.pyplot as plt
import fs
import os
import pyfits
#import seaborn as sns
#sns.set()

pupilRadius = 1.6e-3
lbda = 0.6375e-6
F = 80e-3
pxsize = 5.3e-6
N = 400
dxp = lbda*F/(N*pxsize)
deltaZ = 3.19e-3
jmin = 4
jmax = 30

#retrieve ajsIDL and ajsTrue

ajsTrueFolderPath = 'C:\\Users\\Jojo\\Desktop\\PdM-HEIG\\Science\\data\\devPD\\PSFforIDLtreatment\\ajsTrue'
ajsTrueFile = os.listdir(ajsTrueFolderPath)
ajsIDLFolderPath = 'C:\\Users\\Jojo\\Desktop\\PdM-HEIG\\Science\\data\\devPD\\PSFforIDLtreatment\\IDLajs'
ajsIDLFile = os.listdir(ajsIDLFolderPath)

ajsTrue = np.zeros([len(ajsIDLFile),jmax-jmin+1])
rmsWFeTrue = np.zeros(len(ajsIDLFile))

ajsIDLmodal = ([len(ajsIDLFile),jmax-jmin+1])
rmsWFeIDLmodalretrieved = np.zeros(len(ajsIDLFile))
rmsemodal = np.zeros(len(ajsIDLFile))

ajsIDLzonal = ([len(ajsIDLFile),jmax-jmin+1])
rmsWFeIDLzonalretrieved = np.zeros(len(ajsIDLFile))
rmsezonal = np.zeros(len(ajsIDLFile))

rmsWFeIDLtrue = np.zeros(len(ajsIDLFile))

for i in np.arange(len(ajsIDLFile)):
    rmsWFeTrue[i] = (((ajsTrueFile[i]).replace('.','_')).split('_'))[-2]
    rmsWFeIDLtrue[i] = (((ajsIDLFile[i]).replace('.','_')).split('_'))[-2]
    
    jsajsTrue = np.loadtxt(ajsTrueFolderPath+'\\'+ajsTrueFile[i])
    jsTrue = jsajsTrue[0,:]
    ajsTrue[i,:] = jsajsTrue[1,:]*1e9*lbda/2/np.pi
    
    jsajsIDL = np.loadtxt(ajsIDLFolderPath+'\\'+ajsIDLFile[i],delimiter=',',skiprows=1)
    jsIDL = jsajsIDL[:,0]
    ajsIDLmodal = jsajsIDL[:,1]*1000
    ajsIDLzonal = jsajsIDL[:,2]*1000
    
    rmsWFeIDLmodalretrieved[i] = fs.RMSwavefrontError(jsIDL,ajsIDLmodal)
    rmsemodal[i] = fs.RMSE(ajsIDLmodal,ajsTrue)
    rmsWFeIDLzonalretrieved[i] = fs.RMSwavefrontError(jsIDL,ajsIDLzonal)
    rmsezonal[i] = fs.RMSE(ajsIDLzonal,ajsTrue)


rmsWFefolderPath = 'C:\\Users\\Jojo\\Desktop\\PdM-HEIG\\Science\\data\\devPD\\PSFforIDLtreatment\\PSFs'
rmsWFerrorFolderPaths = os.listdir(rmsWFefolderPath)

NrmsWFe = len(rmsWFerrorFolderPaths)
rmsePy = np.zeros(NrmsWFe)
rmsWFerrorsPyRetrieved = np.zeros(NrmsWFe)
rmsWFeTruePy = np.zeros(NrmsWFe)

for irms,rmsWFdir in enumerate(rmsWFerrorFolderPaths):
    PSFfolderPaths = rmsWFefolderPath+'\\' + rmsWFdir
    sPSFfiles = os.listdir(PSFfolderPaths)
    rmsWFeTruePy[irms] = (rmsWFdir.split('_'))[-1]
    
    PSFs = np.zeros([3,400,400])
    deltaZs = np.array([])
    for ipsf,sPSFfile in enumerate(sPSFfiles):
        PSFfilePath = rmsWFefolderPath+ '\\' + rmsWFdir + '\\' + sPSFfile
        hdulist = pyfits.open(PSFfilePath)
        PSFs[ipsf,:,:] = hdulist[0].data
        deltaZs = np.append(deltaZs,int(((sPSFfile.replace('.','_')).split('_'))[-2]))
    
    IxdeltaZ =np.argsort(deltaZs)
    
    phaseDiv = PD.phaseDiversity3PSFs(PSFs[IxdeltaZ[1],:,:],PSFs[IxdeltaZ[2],:,:],PSFs[IxdeltaZ[0],:,:],deltaZ,lbda,pxsize,F,pupilRadius,jmin,jmax)
    
    jsretrieved = phaseDiv.result['js']
    ajsretrieved = phaseDiv.result['ajs']
    
    a = np.where(rmsWFeTrue==rmsWFeTruePy[irms])
    
    rmsePy[irms] = fs.RMSE(ajsretrieved*1e9*lbda/2/np.pi,ajsTrue[a,:])
    rmsWFerrorsPyRetrieved[irms] = fs.RMSwavefrontError(jsretrieved,ajsretrieved*1e9*lbda/2/np.pi)



rmsWFerrorMax = np.max(np.append(rmsWFerrorsPyRetrieved,rmsWFeTrue))
rmsWFerrorMin = np.min(np.append(rmsWFerrorsPyRetrieved,rmsWFeTrue))

fnamerms = '../../../fig/PDDev/test/rmsWFerrorsretrieved_rmsWFeWthIDL %s'
fnamermse = '../../../fig/PDDev/test/rmse_rmsWFeWthIDL%s'
IxsortIDl = np.argsort(rmsWFeIDLtrue)
IxsortPy = np.argsort(rmsWFeTruePy)
fig = plt.figure()
plt.hold(True)
plt.plot(rmsWFeTruePy[IxsortPy],rmsWFerrorsPyRetrieved[IxsortPy],label='python')
plt.plot(rmsWFeIDLtrue[IxsortIDl],rmsWFeIDLmodalretrieved[IxsortIDl],label='IDL modal')
plt.plot(rmsWFeIDLtrue[IxsortIDl],rmsWFeIDLzonalretrieved[IxsortIDl],label='IDL zonal')
plt.plot([rmsWFerrorMin,rmsWFerrorMax],[rmsWFerrorMin,rmsWFerrorMax],linewidth=2,c='grey')
plt.xlim([rmsWFerrorMin,rmsWFerrorMax])
plt.ylim([rmsWFerrorMin,rmsWFerrorMax])
plt.xlabel('$\sigma_{WF,rms}$ true [nm]')
plt.ylabel('$\sigma_{WF,rms}$ retrieved [nm]')
plt.legend(loc='best')
plt.grid()
plt.savefig(fnamerms % ('.png'), dpi=300)
plt.savefig(fnamerms % ('.pdf'), dpi=300)
#plt.close(fig)

fig = plt.figure()
plt.plot(rmsWFeTruePy[IxsortPy],rmsePy[IxsortPy],label='python')
plt.plot(rmsWFeIDLtrue[IxsortIDl],rmsemodal[IxsortIDl],label='IDL modal')
plt.plot(rmsWFeIDLtrue[IxsortIDl],rmsezonal[IxsortIDl],label='IDL zonal')
plt.xlim([rmsWFerrorMin,rmsWFerrorMax])
plt.xlabel('$\sigma_{WF,rms}$ true [nm]')
plt.ylabel('RMSE [nm]')
plt.legend(loc='best')
plt.grid()
plt.savefig(fnamermse % ('.png'), dpi=300)
plt.savefig(fnamermse % ('.pdf'), dpi=300)
#plt.close(fig)
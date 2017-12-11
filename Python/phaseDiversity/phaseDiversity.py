import libtim.zern as Z
import numpy as np

def retrievePhase(InFoc,OutFoc,DeltaZ,dx):

    if np.shape(InFoc) == np.shape(OutFoc) and np.shape(InFoc)[0] == np.shape(InFoc)[1]:
        size = (np.shape(Infoc))[0]
    else:
        print 'the InFoc and outFoc must be squared arrays of the same size'
        return

    

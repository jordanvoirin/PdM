import numpy as np
import random

def getRandomAjs(js,rmsWFerror):
    Najs = js.__len__()
    ajssq = np.zeros(Najs)
    for ij, j in enumerate(js):
        ajssq[ij] = random.random()
    ajssq = ajssq /np.sum(ajssq)*rmsWFerror**2
    ajs = np.zeros(Najs)
    for iaj, ajsq in enumerate(ajssq):
        ajs[iaj] = random.choice([-1,1])*np.sqrt(ajsq)
    return ajs                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
import numpy as np
#import fs

def getRandomAjs(js,rmsWFerror):
    Najs = js.__len__()
    ajssq = np.random.random(Najs)
    ajssq = ajssq /np.sum(ajssq)*rmsWFerror**2
    ajs = np.zeros(Najs)
    for iaj, ajsq in enumerate(ajssq):
        ajs[iaj] = np.random.choice([-1,1])*np.sqrt(ajsq)
    return ajs


def generateWhiteNoise(shape,mean,std):
    imDim = shape
    num_samples = imDim[0]*imDim[1]
    noise = np.random.normal(mean, std, size=num_samples)
    noise = np.reshape(noise,[imDim[0],imDim[1]])
    return noise
#js = np.linspace(4,15,num=15-3)
#
#ajs = getRandomAjs(js,70)
#
#rmsWFerror = fs.RMSwavefrontError(js,ajs)
#
#print js
#print ajs
#print rmsWFerror
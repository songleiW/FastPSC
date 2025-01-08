import numpy as np
from util import DOMAIN
from util import p


MAC_key1=np.random.randint(0, p)
MAC_key2=np.random.randint(0, p)



def PSI(encSets,M,N):
    encPSI1=np.sum(encSets, axis=0)
    encPSI2=np.sum(encSets, axis=0)



    randomSet=np.random.randint(0, p, DOMAIN)

    encPSI=(M/3-encPSI1)*randomSet %p
    encPSI=(M/3-encPSI2)*randomSet % p





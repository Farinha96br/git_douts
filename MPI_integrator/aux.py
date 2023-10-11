# Arquivo em python com funçoes auxiliares
import random as rng
import numpy as np
from scipy.optimize import curve_fit

def label_hue2(labels):
    # recebe uma img rotulada e aplica cores aleatorias nelas
    rng.seed(11121996)
    shape = labels.shape
    new = np.zeros((shape[0],shape[1],3))
    for k in range(1,np.max(labels)+1):
        new[labels == k] = [rng.randint(10,255),rng.randint(10,255),rng.randint(10,255)]
        #print(k)
    return np.uint8(new)


def plaw(t,gamma):
    return t**gamma

def getExp(x,t):
    if len(x) != len(t):
        return 99999
    # function to extract the expoent gamma from the time series
    xsquared = (x-x[0])**2
    popt, pcov = curve_fit(plaw,t,xsquared)
    perr = np.sqrt(np.diag(pcov))
    gamma = popt[0]
    return gamma, perr[0]
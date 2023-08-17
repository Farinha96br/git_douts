# Arquivo em python com funçoes auxiliares
import random as rng
import numpy as np

def label_hue2(labels):
    # recebe uma img rotulada e aplica cores aleatorias nelas
    rng.seed(11121996)
    shape = labels.shape
    new = np.zeros((shape[0],shape[1],3))
    for k in range(1,np.max(labels)+1):
        new[labels == k] = [rng.randint(10,255),rng.randint(10,255),rng.randint(10,255)]
        #print(k)
    return np.uint8(new)
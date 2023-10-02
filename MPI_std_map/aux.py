# Arquivo em python com funçoes auxiliares
import random as rng
import numpy as np
from skimage import morphology as mm


def label_hue2(labels):
    # recebe uma img rotulada e aplica cores aleatorias nelas
    rng.seed(11121996)
    shape = labels.shape
    new = np.zeros((shape[0],shape[1],3))
    for k in range(1,np.max(labels)+1):
        new[labels == k] = [rng.randint(10,255),rng.randint(10,255),rng.randint(10,255)]
        #print(k)
    return np.uint8(new)


def recmatrix2D(x,y,eps):
    xx1,xx2 = np.meshgrid(x,x)
    xx = np.abs(xx1 - xx2)
    xx = xx**2

    yy1,yy2 = np.meshgrid(y,y)
    yy = np.abs(yy1 -yy2)
    yy = yy**2

    M = np.sqrt(xx + yy)
    M = M < eps
    return M


def perisim(x,lim):
    return (x-lim)%(2*lim)


def mm_filter(img_gr,radius):
    SE = mm.disk(radius)
    SEconnec = mm.diamond(1) # 4-conectividade na reconstrucao
    ero = mm.erosion(img_gr,SE)
    opening = mm.reconstruction(ero,img_gr,"dilation",SEconnec)
    dil = mm.dilation(opening,SE)
    close = mm.reconstruction(dil,opening,"erosion",SEconnec)
    return close

def isAcc(x):
    # checa se a particula tem um modo acelerado
    d = np.diff(x)
    ret = False
    if np.all(d > 0) or np.all(d < 0):
        ret = True
    return ret


def H2d(x,y,xedges,yedges):
    hist , xedges, yedges = np.histogram2d(x,y,bins = (xedges,yedges))
    hist = hist[hist != 0]
    hist = hist/np.sum(hist)

    entropy = -1*np.sum(hist*np.log(hist))
    return entropy



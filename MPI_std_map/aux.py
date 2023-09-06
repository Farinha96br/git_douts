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


def tiptxt(x):
    # 0X = Periodico
    # 1X = Caotico
    # X0 = Sem transporte
    # X1 = Transp Horizontal
    # X2 = Transp vertical
    # X3 = Tranp geral
    txt = ["A","B"] # periodico sem transporte
    if x >= 10:
        txt[0] = "C"
    if x < 10:
        txt[0] = "P"
    if x%10 == 0:
        txt[1] = "T"
    if x%10 == 1:
        txt[1] = "H"
    if x%10 == 2:
        txt[1] = "V"
    if x%10 == 3:
        txt[1] = "G"
    return "".join(txt)

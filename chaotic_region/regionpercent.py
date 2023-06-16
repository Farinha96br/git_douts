import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import os
import sys



folders = sorted(os.listdir())


area = []
vars = []

for f in folders:
    if f.startswith("data-cregion_A2"):
    
        ######## De fato a plotagem
        data = np.loadtxt(f + "/" + f + "xyz.dat")

        L = 250
        x0 = np.reshape(data[:,0],(L,L))
        y0 = np.reshape(data[:,1],(L,L))
        z = np.reshape(data[:,2],(L,L))
        var = f[-5:]
        print(var,np.sum(z)/(L*L))
        #print(np.sum(z))








#print(np.sum(z)/(L*L))

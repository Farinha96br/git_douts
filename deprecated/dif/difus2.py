import numpy as np
import os
import sys
import matplotlib.pyplot as plt







data_folder = sys.argv[1]
datax = np.load(data_folder + "/datax.npy")
#formato: datax[id,t_index]


print(datax.shape)
t = np.load(data_folder + "/datat.npy")
print(t.shape)

#dif_file = sys.argv[1] + "/D_" +  sys.argv[1]  +".dat"

Dxs = np.array([])
msds = np.array([])
#f = open(dif_file, "w")

for i in range(1,len(t)):
    deltax = datax[:,i] - datax[:,0]

    # This part does the diffusion stuff
    squaresx = deltax**2
    msd = np.sum(squaresx)/len(datax[:,0])
    msds = np.append(msds,msd)
    Dx = msd/2*t[i]
    Dxs = np.append(Dxs,Dx)

print("sep arr\n",msds,"\n",Dxs)
arr = np.vstack((msds,Dxs))
print("arr stack\n",arr)

np.save(data_folder + "/msd_D.npy",arr)

print("reload check\n",np.load(data_folder + "/msd_D.npy"))




















#

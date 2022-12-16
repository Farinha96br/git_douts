import numpy as np
import matplotlib.pyplot as plt
import sys
import os

folder = sys.argv[1] # pasta com os dados
data_folder = sys.argv[1] + "/traj/"

N = 750
c = 0
data_full = np.zeros((N*N,3))
for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        data = np.loadtxt(data_folder + filename)
        data_full[c,:] += data
        #print(data_full)
        c += 1
for i in range(0,data_full.shape[0]):
    print(data_full[i,0],data_full[i,1],data_full[i,2],)

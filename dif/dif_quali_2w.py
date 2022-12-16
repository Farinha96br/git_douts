import numpy as np
import matplotlib.pyplot as plt
import sys
import os



Folders = os.listdir("U_espectro/")
print(Folders)
F = np.zeros(Folders.shape)
for i in range(0,len(Folders)):
    Folders[i] = Folders[i].replace("neg","-")
    Folders[i] = np.float(Folders[i])
F = sorted(Folders)






#fig, ax = plt.subplots()
#plt.tight_layout()
#fig.set_size_inches(10, 5)
#ax.set_yscale("log")
#ax.set_ylabel("$<D_x(500)>$")
#ax.set_xlabel("U")
#ax.set_xlim(-1.5,1.5)
#ax.plot(all3[:,0],all3[:,1],marker = "o",linewidth = 1,markersize = 4, c = "firebrick", label = "$A_2 = 0.5A_1$")
#ax.plot(all2[:,0],all2[:,1],marker = "^",linewidth = 1,markersize = 4, c = "limegreen", label = "$A_2 = 0.3A_1$")
#ax.plot(all1[:,0],all1[:,1],marker = "s",linewidth = 1,markersize = 4, c = "steelblue", label = "$A_2 = 0.1A_1$")
#ax.legend()
#
#
#plt.savefig("U_dif.png", dpi = 600)

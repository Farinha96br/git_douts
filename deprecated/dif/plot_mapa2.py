import numpy as np
import matplotlib.pyplot as plt
import sys
import os


plt.rc('text', usetex=False)
plt.rc('font', family='serif')
plt.rcParams["mathtext.fontset"] = "cm" # isso é pra salvar as coisa em png com a fonte do latex


k = 3
cell = np.pi/k
folder = sys.argv[1] # pasta com os dados
data_folder = sys.argv[1] + "/traj/"

#title = sys.argv[2]


fig, ax = plt.subplots()
#plt.title(title)
fig.set_size_inches(7*0.393, 7*0.393)
ax.set_ylim([0,2*cell])
ax.set_xlim([0,2*cell])
ax.set_xticks([0,cell,2*cell])
ax.set_xticklabels([r"0",r"$\frac{\pi}{k}$",r"$2\frac{\pi}{k}$"])
ax.set_yticks([0,cell,2*cell])
ax.set_yticklabels([r"0",r"$\frac{\pi}{k}$",r"$2\frac{\pi}{k}$"])
ax.set_ylabel(r"$x$")
ax.set_xlabel(r"$y$")

sx = []
sy = []

for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        data = np.loadtxt(data_folder + filename)
        sx.append(data[0,1])
        sy.append(data[0,2])
        print(data.shape)
        x = data[:,1]
        x = x%(2*cell)
        y = data[:,2]
        y = y%(2*cell)
        #ax.plot(x,y,marker=".",ls="",c = "black",markersize = 0.5,linewidth=0)
        ax.scatter(y,x, s=0.5,marker='.', c = "black", alpha = 1,linewidths=0)





#plt.tight_layout()


#ax.axhline(1,color = "#333333", linestyle = "--", a)

ax.scatter(sy,sx,s = 0.25,marker='o', c = "firebrick",zorder = 3)
savepath = folder + "/map2_" + folder + ".png"
plt.savefig(savepath, bbox_inches='tight', dpi = 300)
os.system("cp " + savepath + " maps/" )

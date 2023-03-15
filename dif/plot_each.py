import numpy as np
import matplotlib.pyplot as plt
import sys
import os

plt.rc('text', usetex=False)
plt.rc('font', family='serif')

folder = sys.argv[1] # pasta com os dados
data_folder = sys.argv[1] + "/traj/"
os.makedirs(sys.argv[1] + "/graphs_traj",exist_ok=True)
Nplots = int(sys.argv[2])
counter = 0
for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        if counter < Nplots:
            data = np.loadtxt(data_folder + filename)
            print(filename)
            sx = data[0,1]
            sy = data[0,2]
            x = data[:,1]
            y = data[:,2]
            colors = data[:,0]

            fig, ax = plt.subplots()

            #plt.title(filename)
            plt.set_cmap("jet")
            plt.tight_layout()
            fig.set_size_inches(9*0.393, 7*0.393)
            ax.set_xlim([-3.1415,3.1415])
            if np.max(x) <= 1:
                ax.set_ylim(0,1.05)
            else:
                ax.set_ylim(0,np.max(x)*1.05)
            ax.set_xticks([-3.14,0,3.14],[r"$-\pi$","0",r"$+\pi$"])
            #ax.axhline(1,color = "#333333", linestyle = "--", a)
            ax.set_ylabel("$x$")
            ax.set_xlabel("$y$")
            #p = ax_plot = ax.scatter(y,x, s=0.1, c = colors,edgecolors=None,alpha = 1,zorder = 0)
            p = ax_plot = ax.scatter(y,x,s=0.15,marker = "o", c = colors,lw = 0,zorder = 0)
            fig.colorbar(p,label="$t$", orientation="vertical")

            ax.plot(sy,sx, c = "black", marker = "s",markersize=3,lw = 1,zorder = 1)
            ax.plot(sy,sx, c = "white", marker = "s",markersize=1,lw = 1,zorder = 2)

            plt.savefig(sys.argv[1] + "/graphs_traj/" + filename[0:-4] + ".png", bbox_inches='tight',dpi =300)
            plt.close()
            counter += 1

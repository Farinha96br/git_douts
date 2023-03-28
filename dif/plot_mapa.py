import numpy as np
import matplotlib.pyplot as plt
import sys

folder = sys.argv[1] # pasta com os dados
start = np.loadtxt(sys.argv[2])
print(start.shape)
sx = start[:,0]
sy = start[:,1]
data = np.loadtxt(folder + "/all_traj.dat")
print(data.shape)
print(data[:,0])
x = data[:,1]
y = data[:,2]
#colors = data[:,3]



plt.rc('text', usetex=False)
plt.rc('font', family='serif')
plt.rcParams["mathtext.fontset"] = "cm" # isso é pra salvar as coisa em png com a fonte do latex


fig, ax = plt.subplots()
#plt.title(sys.argv[3])
#plt.tight_layout()
fig.set_size_inches(7*0.393, 7*0.393)
ax.set_ylim([0.0,1.1])
ax.set_xlim([-3.1415,3.1415])
ax.set_xticks([-3.14,0,3.14])
ax.set_xticklabels([r"$-\pi$",r"0",r"$+\pi$"])

#ax.axhline(1,color = "#333333", linestyle = "--", a)
ax.set_ylabel(r"$x$")
ax.set_xlabel(r"$y$")
ax.scatter(y,x, s=0.2,marker='.', c = "black", alpha = 1,linewidths=0)
ax.scatter(sy,sx,s = 0.25,marker='o', c = "firebrick")
plt.savefig(folder + "/map_" + folder + ".png", bbox_inches='tight', dpi = 300)

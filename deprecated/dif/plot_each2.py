import numpy as np
import matplotlib.pyplot as plt
import sys
import os

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
plt.rcParams["mathtext.fontset"] = "cm" # isso é pra salvar as coisa em png com a fonte do latex

# Algumas paletas de cor p serem usadas (VSCode recomendado pra mostar as cores no editor de texto)
rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_darker = ['#007a96','#b39700','#b04bb0']

folder = sys.argv[1] # pasta com os dados

os.makedirs(sys.argv[1] + "/graphs_traj",exist_ok=True)
Nplots = int(sys.argv[2])

k = 3
cell = np.pi/k
counter = 0

datax = np.load(folder + "/datax.npy")
datay = np.load(folder + "/datay.npy")
t = np.load(folder + "/datat.npy")
print("shp x:",datax.shape)
print("shp y:",datay.shape)
print("shp t:",t.shape)

print(t)

for i in range(0,Nplots):
    sx = datax[i,0]
    sy = datay[i,0]
    x = datax[i,:]
    y = datay[i,:]

    #x = x%(2*np.pi)
    #y = y%(2*np.pi)
    colors = t/np.max(t)

    fig, ax = plt.subplots()

    #plt.title(filename)
    plt.set_cmap("jet")
    plt.tight_layout()
    fig.set_size_inches(10*0.393, 8*0.393)
    #ax.set_ylim([0,2*3.1415])
    #ax.set_xlim([0,2*3.1415])
    ax.set_xticks([0,3.1415,2*3.1415])
    ax.set_xticklabels([r"0",r"$\pi$",r"$2\pi$"])
    ax.set_yticks([0,3.1415,2*3.1415])
    ax.set_yticklabels([r"0",r"$\pi$",r"$2\pi$"])
    ax.set_ylabel("$x$")
    ax.set_xlabel("$y$")
    #p = ax_plot = ax.scatter(y,x, s=0.1, c = colors,edgecolors=None,alpha = 1,zorder = 0)
    p = ax.scatter(y,x,s=0.15,marker = "o", c = colors,lw = 0,zorder = 0)
    fig.colorbar(p,label="$t$", orientation="vertical")
    ax.plot(sy,sx, c = "black", marker = "s",markersize=3,lw = 1,zorder = 1)
    ax.plot(sy,sx, c = "white", marker = "s",markersize=1,lw = 1,zorder = 2)
    plt.savefig(sys.argv[1] + "/graphs_traj/" + str(i).zfill(6) + "_map.png", bbox_inches='tight',dpi =300)
    plt.close()

    counter += 1

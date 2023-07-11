import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors

# Algumas paletas de cor p serem usadas (VSCode recomendado pra mostar as cores no editor de texto)
rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_pallet = ['#007a96','#b39700','#b04bb0']

## modelo de como criar um colormap linear usando cores predefinidas:
cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("", [rgb_pallet[2],"black",rgb_pallet[0]])


######
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######

folder = sys.argv[1]
os.makedirs(folder + "/trajs",exist_ok=True)
x = np.loadtxt(folder + "/x.dat")
y = np.loadtxt(folder + "/y.dat")




for i in np.arange(0,len(x[:,0])):
    print(i)
    fig, ax = plt.subplots(2,1,sharex=True)
    fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm
    ax[0].plot(x[i,:],ls= "",marker="o",markersize=0.5,color = rgb_pallet[2])
    ax[0].set_ylabel(r"$x(\tau)$")
    ax[0].set_ylim(-100,100)
    ax[1].plot(y[i,:],ls= "",marker="o",markersize=0.5,color = rgb_pallet[1])
    ax[1].set_ylabel(r"$y(\tau)$")
    ax[1].set_ylim(-100,100)
    ax[1].set_xlabel(r"$\tau$")
    plt.savefig(folder + "/trajs/" + str(i) + ".png",bbox_inches='tight',dpi = 300) # salva em png
    plt.close()




#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf

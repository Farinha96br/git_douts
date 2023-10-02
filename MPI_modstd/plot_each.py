import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors
import aux

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
x = np.loadtxt(folder + "/theta.dat")%(2*np.pi)
y = np.loadtxt(folder + "/p.dat")

tmax = 5000
for i in np.arange(81,len(x[:,0])):
    print(i)
    
    xbins = np.linspace(0,2*np.pi,1024)
    ybins = np.linspace(-np.pi,np.pi,1024)
    H = aux.H2d(x[i,:]%(2*np.pi),aux.perisim(y[i,:],np.pi),xbins,ybins)
    print(H)
    t = np.arange(len(x[0,0:tmax]))
    fig, ax = plt.subplots(2,1,sharex=True)
    fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm
    ax[0].set_title(str(H))
    ax[0].scatter(t,x[i,:tmax],s=0.75,edgecolors='none', color = rgb_pallet[2],zorder = 1)
    ax[0].set_ylabel(r"$\theta/2\pi$")
    #ax[0].set_ylim(-100,100)
    ax[1].scatter(t,y[i,:tmax],s=0.75,edgecolors='none', color = rgb_pallet[1],zorder = 1)
    ax[1].set_ylabel(r"$p$")
    #ax[1].set_ylim(-100,100)
    ax[1].set_xlabel(r"$t$")
    plt.savefig(folder + "/trajs/" + str(i-81) + ".png",bbox_inches='tight',dpi = 300) # salva em png
    plt.close()




#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf

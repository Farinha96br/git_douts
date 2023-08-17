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

k = 3
folder = sys.argv[1]
os.makedirs(folder + "/trajs",exist_ok=True)
x = np.loadtxt(folder + "/x.dat")


fig, ax = plt.subplots()
fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm
ax.set_ylabel(r"$\Delta x(\tau)$")
#ax.set_ylim(-110,110)
ax.set_xlabel(r"$\tau$")
ax.set_xlim(0,100)

N_prefilter = len(x[:,0])
N = len(x[:,0]) # quantidade de cond. inicias que tem transporte
its = len(x[0,:])
print("Total\tWith transport")
print("Doing math...")

kx = 3

deltax1 = x - np.tile(x[:,0],(its,1)).T
index = np.abs(deltax1) < 2*np.pi*2/kx
index = np.all(index,axis=1)
index = np.invert(index)
deltax1 = deltax1[index,:]

print(N_prefilter,"\t",N)

for i in np.arange(0,len(deltax1[:,0])):
    print(i)
    if i == 0:
        ax.plot(deltax1[i,:],lw = 0.1,color = rgb_pallet[2],alpha = 0.5, label = "Trajectory")
    else:
        ax.plot(deltax1[i,:],lw = 0.1,color = rgb_pallet[2],alpha = 0.5)

for i in range(0,100):
    ax.axhline(i*np.pi/kx,ls="ls")



msd = np.sum(deltax1**2,axis=0)/N

ax.plot(msd,lw = 0.5,color = rgb_pallet[0],label = "MSD")
ax.plot(-msd,lw = 0.5,color = rgb_pallet[0])
ax.legend(frameon = False)
plt.savefig(folder + "/all_x" + str(i) + ".png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()




#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf

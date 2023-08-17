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

folder1 = sys.argv[1]
folder2 = sys.argv[2]

os.makedirs(folder1 + "/displacement",exist_ok=True)
print("loading x...")
x1 = np.loadtxt(folder1 + "/x.dat")
x2 = np.loadtxt(folder2 + "/x.dat")
kx = 3

its = len(x1[0,:])
deltax1 = x1 - np.tile(x1[:,0],(its,1)).T
index = np.abs(deltax1) < 2*np.pi*2/kx
index = np.all(index,axis=1)
index = np.invert(index)
deltax1 = deltax1[index,:]

deltax2 = x2 - np.tile(x2[:,0],(its,1)).T
index = np.abs(deltax2) < 2*np.pi*2/kx
index = np.all(index,axis=1)
index = np.invert(index)
deltax2 = deltax2[index,:]
print(np.std())


fig, ax = plt.subplots()
fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

bins = np.linspace(-120,120,61)
ax.hist(deltax2[:,-1],bins = bins, color = rgb_pallet[0],histtype='stepfilled',edgecolor=rgb_darker[2], linewidth=0.25,label=r"$A_2 = 0.20$",alpha = 0.5)
ax.hist(deltax1[:,-1],bins = bins, color = rgb_pallet[2],histtype='stepfilled',edgecolor=rgb_darker[2], linewidth=0.25,label=r"$A_2 = 0.16$",alpha = 0.5)


ax.legend(frameon = False)
plt.savefig(folder1 + "histogram.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()




#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf

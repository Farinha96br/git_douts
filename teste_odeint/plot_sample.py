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
fig, ax = plt.subplots()
fig.set_size_inches(14*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm




# plot normal
file = "odeint.dat"
data = np.loadtxt(file)
ax.plot(data[:,0],data[:,2],lw=0.5, color = rgb_pallet[2],label = file,alpha = 0.7)

file = "while.dat"
data = np.loadtxt(file)
ax.plot(data[:,0],data[:,2],lw=0.5, color = rgb_pallet[0],label = file,alpha = 0.7)
ax.set_ylabel("y")
ax.set_xlabel("t")
# plot com histograma:
#w = 0.1 # largura dos bins
#b = np.arange(0, Ncell*cellx + w, w) + w/2 # bins em si
#ax.hist(x,bins = b, color = rgb_pallet[2] , alpha = 0.5, label = r"$A_2 = 0.1A_1$",histtype='stepfilled',edgecolor=rgb_darker[2], linewidth=0.25)



ax.legend()
plt.savefig("graph.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()
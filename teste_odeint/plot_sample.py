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
fig.set_size_inches(7*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

file = "teste.dat"
data = np.loadtxt(file)
k = 3
x = data[:,1]%(2*np.pi/k)
y = data[:,2]%(2*np.pi/k)

##  Título do plot
#ax.set_title(filename)
k = 3
cell = np.pi/k
##  Limites e ticklabels em x e y:
ax.set_ylim([0,2*cell])
ax.set_xlim([0,2*cell])
ax.set_xticks([0,cell,2*cell])
ax.set_xticklabels([r"0",r"$\frac{\pi}{k}$",r"$2\frac{\pi}{k}$"])
ax.set_yticks([0,cell,2*cell])
ax.set_yticklabels([r"0",r"$\frac{\pi}{k}$",r"$2\frac{\pi}{k}$"])




# plot normal
ax.plot(x,y,ls ="",marker=",",markersize = 10, color = rgb_pallet[2],label = "data1")
ax.scatter(x[0],y[0],s=0.5,color = "black")

# plot com histograma:
#w = 0.1 # largura dos bins
#b = np.arange(0, Ncell*cellx + w, w) + w/2 # bins em si
#ax.hist(x,bins = b, color = rgb_pallet[2] , alpha = 0.5, label = r"$A_2 = 0.1A_1$",histtype='stepfilled',edgecolor=rgb_darker[2], linewidth=0.25)




plt.savefig("graph.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()
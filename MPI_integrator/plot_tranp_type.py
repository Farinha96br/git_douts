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
fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

file = "tranp_frac.dat"
data = np.loadtxt(file)

##  Limites e ticklabels em x e y:
ax.set_xlim([0,1])
ax.set_xlabel(r'$A_2$')
ax.set_ylim([0,1])
ax.set_ylabel("fractional area")

cum = np.sum(data[:,1:],axis=1)

ax.stackplot(data[:,0],data[:,1]/cum,data[:,3]/cum,data[:,2]/cum, labels = ["trapped","balistic","difusive"], colors = [rgb_light[2],"black",rgb_light[0]])
ax.legend(frameon=True) # Caixinha d legenda sem borda
#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf
plt.savefig("regime_areas.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()

fig, ax = plt.subplots()
fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

##  Limites e ticklabels em x e y:
ax.set_xlim([0.1,0.2])
ax.set_xlabel(r'$A_2$')
ax.set_ylim([0.2,0.5])
ax.set_ylabel("fractional area")

cum = np.sum(data[:,1:],axis=1)

ax.stackplot(data[:,0],data[:,1]/cum,data[:,3]/cum,data[:,2]/cum, labels = ["trapped","balistic","difusive"], colors = [rgb_light[2],"black",rgb_light[0]])
ax.legend(frameon=True) # Caixinha d legenda sem borda
#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf
plt.savefig("regime_areas_zoom.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()
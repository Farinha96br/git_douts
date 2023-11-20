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
fig.set_size_inches(8*0.393, 4*0.393) # o valor multiplicando é o tamanho em cm



x = np.linspace(1,1000,100)

ax.plot(x,x**2,linewidth = 0.5, color = rgb_pallet[0],label = r"Superdiffusion $\gamma < 1$")
ax.plot(x,x,linewidth = 0.5, color = rgb_pallet[2],label = r"Normal $\gamma = 1$")
ax.plot(x,x**0.5,linewidth = 0.5, color = rgb_pallet[1],label = r"Subdiffusion $\gamma > 1$")

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$\langle \sigma^2(t) \rangle$")
ax.set_xscale("log")
ax.set_yscale("log")
ax.grid(which='major', color='#DDDDDD', linewidth=0.8)
ax.grid(which='minor', color='#EEEEEE', linewidth=0.5)
ax.set_xlim(1,1000)
ax.set_ylim(1,1000)


ax.legend(frameon=False,loc='center left', bbox_to_anchor=(1, 0.5)) # Caixinha d legenda sem borda
#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf
plt.savefig("graph.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()
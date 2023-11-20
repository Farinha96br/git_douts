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
plt.rc('text', usetex=True) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######
fig, ax = plt.subplots()
fig.set_size_inches(10*0.393, 5*0.393) # o valor multiplicando é o tamanho em cm

file = "gamma_dif.dat"
data = np.loadtxt(file)


#  Limites e ticklabels em x e y:
ax.set_xlabel(r"$K$")
ax.set_xlim([0,9])
ax.set_xticks(np.arange(0,9))

ax.set_ylim([0,2.1])
ax.set_yticks([0,1,2])
ax.set_ylabel(r"$\gamma$")






# plot normal
ax.plot(data[:,0],data[:,1],linewidth = 0.6, color = rgb_pallet[2],zorder = 1)
ax.axhline(1,color = "#777777",ls = "--", linewidth = 0.5,zorder = 0)
ax.axhline(2,color = "#777777",ls = "--", linewidth = 0.5,zorder = 0)



plt.savefig("gamma.pdf",bbox_inches='tight') # salva em png
plt.close()
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



xa = np.loadtxt("logistic_map_0.1000.dat")
xb = np.loadtxt("logistic_map_0.1001.dat")

r = xa[:,0]
xa = xa[:,1:]
xb = xb[:,1:]

dx = np.abs(xb - xa)

print(dx.shape)
print(xa)

lyaps = []

for i in range(0,len(r)):
    lyaps.append(np.sum(np.log(dx[i,500:]))/len(dx[0,500:]))
    print(i,lyaps[i])


fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

ax.plot(r,lyaps, color = "black", lw = 0.5)
ax.imshow(dx.T)

ax.axhline(0,ls="--",color = "#555555",lw = 0.5)
ax.set_ylabel(r"$\lambda$")
ax.set_xlabel(r"$r$")

#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf
plt.savefig("lyap.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()
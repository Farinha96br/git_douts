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
x = np.loadtxt(folder + "/x.dat")
y = np.loadtxt(folder + "/y.dat")

x0 = x[:,0]
y0 = y[:,0]
#x = np.ravel(x)%(2*np.pi/3)
#y = np.ravel(y)%(2*np.pi/3)

k = 3

fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393)
ax.set_xlabel(r"$y$")
#ax.set_xlim([0,2*np.pi/k])
ax.set_xticks([0,np.pi/k,2*np.pi/k])
#ax.set_xticklabels([r"0",r"$\pi$",r"$2\pi$"])

ax.set_ylabel(r"$x$")
#ax.set_ylim([0,2*np.pi/k])
ax.set_yticks([0,np.pi/k,2*np.pi/k])
#ax.set_yticklabels([r"0",r"$\pi$",r"$2\pi$"])
for i in range(0,len(x[:,0])):
    ax.plot(y[i,:]%(2*np.pi/3),x[i,:]%(2*np.pi/3),ls="",marker = ",",zorder = 0)
ax.scatter(y0,x0,marker = "o",s = 0.1, color = rgb_pallet[0],zorder = 1)
plt.savefig(folder + "/map.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()



#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf

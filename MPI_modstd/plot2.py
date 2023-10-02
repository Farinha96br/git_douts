import numpy as np
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
fig, ax = plt.subplots(2,1,sharex=True)
fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

file = sys.argv[1]
data = np.loadtxt(file)


ax[0].set_xlim([0,9])

ax[0].set_ylim([0,0.05])
ax[0].set_ylabel(r"%area")

# plot normal
ax[0].plot(data[:,0],data[:,2],linewidth = 0.5)



file = sys.argv[2]
data = np.loadtxt(file)


ax[1].set_xlim([0,9])
ax[1].set_xlabel(r"$K$")
ax[1].set_xticks(np.linspace(0,9,10))

ax[1].set_ylabel(r"$\gamma$")

# plot normal
ax[1].plot(data[:,0],data[:,1],linewidth = 0.5)







ax[0].legend(frameon=False) # Caixinha d legenda sem borda
#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf
plt.savefig("double.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()
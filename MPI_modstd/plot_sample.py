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
cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("", ["#9ef27b","#FF6645","#FF59D7","#8FAAFF"])


######
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######
fig, ax = plt.subplots()
fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

file = sys.argv[1]
data = np.loadtxt(file)

##  Título do plot
Kc = 0.9716

ax.set_xlim([0,9])
ax.set_xlabel(r"$K$")
ax.set_xticks([0,Kc,2,3,4,5,6,7,8,9])
ax.set_xticklabels([0,r"$K_c$",2,3,4,5,6,7,8,9])


ax.set_ylim([0,1])
ax.set_ylabel(r"%area")


cmap2(0)
# plot normal
a = np.linspace(0,1,4)
ax.plot(data[:,0],data[:,1],linewidth = 0.5, color = "#4dd315", label = "periodic conf.")
ax.plot(data[:,0],data[:,2],linewidth = 0.5, color = "#FF6645", label = "periodic acc.")
ax.plot(data[:,0],data[:,3],linewidth = 0.5, color = "#FF59D7", label = "chaotic conf.")
ax.plot(data[:,0],data[:,4],linewidth = 0.5, color = "#507AFF", label = "chaotic transp.")

ax.axvline(Kc,ls="--",lw=0.5,c="Grey")


ax.legend(frameon=False) # Caixinha d legenda sem borda
#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf
plt.savefig("graph.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()
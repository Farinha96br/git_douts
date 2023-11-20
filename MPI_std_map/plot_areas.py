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
plt.rc('text', usetex=True) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######
fig, ax = plt.subplots(2,1,sharex=True)
fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

data = np.loadtxt("areas.dat")

##  Título do plot
Kc = 0.9716

ax[0].set_xlim([0,9])
ax[1].set_xlabel(r"$K$")
ax[0].set_xticks([0,Kc,2,3,4,5,6,7,8,9])
ax[0].set_xticklabels([0,r"$K_c$",2,3,4,5,6,7,8,9])


cs = ["#22b04f","#f514e2","#ffb81f","#512eff"]

ax[0].set_ylim([0,1])
ax[0].set_ylabel(r"area")
ax[1].set_ylabel(r"area",color = cs[1])
ax[1].tick_params(axis='y', colors=cs[1])




# plot normal
ax[0].plot(data[:,0],data[:,1],linewidth = 0.5, color = cs[0], label = "PC")
ax[0].plot(data[:,0],data[:,2],linewidth = 0.5, color = cs[1], label = "PA")
ax[0].plot(data[:,0],data[:,3],linewidth = 0.5, color = cs[2], label = "BC")
ax[0].plot(data[:,0],data[:,4],linewidth = 0.5, color = cs[3], label = "UC")
ax[0].axvline(Kc,ls="--",lw=0.5,c="Grey")



ax[1].plot(data[:,0],data[:,2],linewidth = 0.5, color = cs[1])



data = np.loadtxt("gamma.dat")

ax2 = ax[1].twinx()
ax2.plot(data[:,0],data[:,1],linewidth = 0.5,c = '#010203',label = r"$\gamma$")
#ax2.legend(frameon=False)
ax2.set_ylabel(r"$\gamma$")
ax2.spines['left'].set_color(cs[1])


ax[0].legend(frameon=False,loc = 'upper center',bbox_to_anchor=(0.5, 1.3),ncol = 4) # Caixinha d legenda sem borda
ax[1].legend(frameon=False) # Caixinha d legenda sem borda

plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf
#plt.savefig("graph.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()
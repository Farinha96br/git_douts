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
p = np.loadtxt(folder + "/p.dat")
q = np.loadtxt(folder + "/q.dat")%(2*np.pi)

p0 = p[:,0]
q0 = q[:,0]




# Plota sem periodicidade 

fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393)
ax.set_xlabel(r"$q$")
ax.set_xlim([0,2*np.pi])
#ax.set_xticks([0,np.pi/k,2*np.pi/k])
#ax.set_xticklabels([r"0",r"$\pi$",r"$2\pi$"])

ax.set_ylabel(r"$p$")
#ax.set_ylim([-4*np.pi,4*np.pi])
#ax.set_yticks([0,np.pi/k,2*np.pi/k])
#ax.set_yticklabels([r"0",r"$\pi$",r"$2\pi$"])
M = float(folder[-8:])
#M = int(M)
#M = 2*M +1
ax.set_title("K = " + str(M))
for i in range(0,len(p[:,0])):
    ax.plot(q[i,:],p[i,:],ls="",marker = ",",zorder = 0)

ax.axvline(0,ls="--",color = "Gray", lw = 0.5)
ax.axvline(2*np.pi,ls="--",color = "Gray", lw = 0.5)
#ax.axhline(-np.pi,ls="--",color = "Gray", lw = 0.5)
#ax.axhline(np.pi,ls="--",color = "Gray", lw = 0.5)
os.makedirs("map_chaos0",exist_ok=True)

ax.scatter(q0,p0,marker = "o",s = 0.5, color = "black",zorder = 1)
plt.savefig(folder + "/map_0_" + folder[-8:] + ".png",bbox_inches='tight',dpi = 300) # salva em png
plt.savefig("map_chaos0/" + folder[-8:] + "_0.png",bbox_inches='tight',dpi = 300) # salva em png

plt.close()


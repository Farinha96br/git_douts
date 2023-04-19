import numpy as np
import matplotlib.pyplot as plt
import sys
import os

rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_darker = ['#007a96','#b39700','#b04bb0']

import matplotlib.colors
cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("", [rgb_pallet[2],"black",rgb_pallet[0]])
cmap3 = matplotlib.colors.LinearSegmentedColormap.from_list("", [cym_pallet[0],cym_pallet[2]])

######

plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=True) # esse vc deixa True e for salvar em pdf e False se for p salvar png




#figdif, axdif = plt.subplots()

#figdif.set_size_inches(7*0.393, 5*0.393) # esse fatir 0.393 é p converter polegadas p cm
#axdif.set_ylabel(r"$\langle D_x(t_f) \rangle$") # Legenda, p renderizar direito precisa do r"$blablabla$"
#axdif.set_xlabel(r"$t$")
#axdif.set_title(r"$\omega2=32$")
#axdif.set_ylim(0,0.006)
#axdif.set_xlim(0,1000)


files = ["phasex_D_0.1.dat","phasex_D_0.2.dat"]
labels = [r"$A_2 = 0.1$",r"$A_2 = 0.2$"]
fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 5*0.393) # esse fatir 0.393 é p converter polegadas p cm
ax.set_ylabel(r"$\langle D_x(t_f) \rangle$") # Legenda, p renderizar direito precisa do r"$blablabla$"
ax.set_xlabel(r"$\phi_x$")
ax.set_xticks(np.arange(0,2*np.pi + np.pi/4,np.pi/4))
ax.set_xticklabels(["0",r"$\frac{\pi}{4}$",r"$\frac{\pi}{2}$",r"$\frac{3\pi}{4}$",r"$\pi$",r"$\frac{5\pi}{4}$",r"$\frac{3\pi}{2}$",r"$\frac{7\pi}{4}$",r"$2\pi$"])
ax.set_xlim(0.000,2*3.1415)
#ax.set_yscale("log")
#ax.axvline(np.pi/4, color = '#888888', linestyle = "--", linewidth = 0.7, zorder = 2)

for i in range(0,len(files)):
    data = np.loadtxt(files[i])
    print(data.shape)
    ax.plot(data[:,0],data[:,1],linewidth = 0.5,marker = ",",markersize = 0.5, c = rgb_pallet[i], label = labels[i])

#ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0)) # coloca em notação científica
ax.legend(frameon=False)

plt.savefig("var_D.pdf",bbox_inches='tight',dpi=300) ## salva como pdf

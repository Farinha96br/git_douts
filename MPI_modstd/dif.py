import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors
from scipy.optimize import curve_fit

def plaw(t,gamma,c):
    return c*(t**gamma)

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
var = folder[-6:]
print("loading p...")
x = np.loadtxt(folder + "/p.dat")





N = len(x[:,0]) # quantidade de cond. inicias que tem transporte
its = len(x[0,:])


deltax1 = x - np.tile(x[:,0],(its,1)).T
#index = np.any(deltax1 > 2*np,pi,axis=0)


msd = np.sum(deltax1**2,axis=0)/N
t = np.arange(0,its)
popt, pcov = curve_fit(plaw,t,msd)
gamma = popt[0]
gamma_file = open("gamma.dat","a")
gamma_file.write(var + "\t" +  str(gamma) + "\n")




fig, ax = plt.subplots()
fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm
ax.set_ylabel(r"$\Delta p(\tau)$")
#ax.set_ylim(-110,110)
ax.set_xlabel(r"$\tau$")
#ax.set_xlim(0,100)
ax.plot(msd,lw = 0.5,color = rgb_pallet[2],label = "MSD")
ax.set_title(r"$\gamma = " + str(gamma) + "$")
plt.savefig("data-msd_batch/msd_" + var +  ".png",bbox_inches='tight',dpi = 300) # salva em pdf
plt.close()



import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors
from scipy.optimize import curve_fit


# Algumas paletas de cor p serem usadas (VSCode recomendado pra mostar as cores no editor de texto)
rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_pallet = ['#007a96','#b39700','#b04bb0']

## modelo de como criar um colormap linear usando cores predefinidas:
cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("", [rgb_pallet[2],"black",rgb_pallet[0]])

def plaw(t,gamma,c):
    return c*(t**gamma)

######
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######

folder = sys.argv[1]
os.makedirs(folder + "/displacement",exist_ok=True)
print("loading x...")
x = np.loadtxt(folder + "/x.dat")
k = 3

#filtragem das cond. iniciais que trem transporte:
print("filtering...")
#index = (np.abs(x[:,-1]) > np.pi*2/k)
#N_prefilter = len(x[:,0])
#x = x[index,:]
#N = len(x[:,0]) # quantidade de cond. inicias que tem transporte
#its = len(x[0,:])
#print("Total\tWith transport")
#print(N_prefilter,"\t",N)
#print("Doing math...")
its = len(x[0,:])
t = np.arange(0,its)
x = x - np.tile(x[:,0],(its,1)).T
x = x**2
msd = np.sum(x,axis=0)/len(x[:,0])
popt, pcov = curve_fit(plaw,t,msd)
gamma = popt[0]
Dx = popt[1]/2
print("gamma:",gamma,"Dx",Dx)
print("--err--")
perr = np.sqrt(np.diag(pcov))
print("gamma:",perr[0],"Dx",perr[1])


print("Plotting...")
fig, ax = plt.subplots()
fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm
ax.plot(t,msd,lw = 0.75, color = rgb_pallet[2],label = "numerical")
ax.plot(t,plaw(t,popt[0],popt[1]),lw = 0.75,color = rgb_pallet[0],label = "fit")
ax.set_xlabel(r"$\tau$")
ax.set_ylabel(r"$\sigma^2(\tau)$")
ax.set_xlim(0,its)
ax.legend(frameon = False)
plt.savefig("msd.pdf",bbox_inches='tight') # salva em pdf

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


######
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######

def plaw(t,gamma,c):
    return c*(t**gamma)

folder = sys.argv[1]
print("loading x...")
x = np.loadtxt(folder + "/x.dat")
k = 3


N_plot = np.array([])
its_plot = np.array([])
gamma_plot = np.array([])



N_list = range(100,10000,100)
its_list = range(10,1000,10)

len_N = len(N_list)
len_its = len(its_list)

for N in N_list:
    for its in its_list:
        print(N,its)
        x_temp = x[:N,:its]
        x_temp = x_temp - np.tile(x_temp[:,0],(its,1)).T
        x_temp = x_temp**2
        msd = np.sum(x_temp,axis=0)/N
        t = np.arange(0,its)
        popt, pcov = curve_fit(plaw,t,msd,maxfev = 1200)
        gamma = popt[0]
        gamma_plot = np.append(gamma_plot,gamma)
        N_plot = np.append(N_plot,N)
        its_plot = np.append(its_plot,its)

print(gamma_plot.shape)
print(its_plot.shape)
print(N_plot.shape)


N_plot = np.reshape(N_plot,(len_N,len_its))      
its_plot = np.reshape(its_plot,(len_N,len_its))        
gamma_plot = np.reshape(gamma_plot,(len_N,len_its))        

print(N_plot.shape)
print(its_plot.shape)
print(gamma_plot.shape)
print(N_plot)
print(its_plot)
print(gamma_plot)



print("Plotting...")
fig, ax = plt.subplots()
fig.set_size_inches(9*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

a = ax.pcolormesh(N_plot,its_plot,gamma_plot,cmap="jet")
ax.set_ylabel(r"$\tau$")
ax.set_xlabel(r"$N$")

fig.colorbar(a,label = r"$\gamma$")
plt.savefig(folder + "/gamma_precision.png",bbox_inches='tight',dpi = 300) # salva em pdf

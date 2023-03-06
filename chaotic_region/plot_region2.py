import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import os
import sys

# Algumas paletas de cor p serem usadas (VSCode recomendado pra mostar as cores no editor de texto)
rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_pallet = ['#007a96','#b39700','#b04bb0']

cmapblues = matplotlib.colors.LinearSegmentedColormap.from_list("", ["#ffffff00",rgb_light[2],rgb_pallet[2],rgb_darker[2]])

######
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png


folders = sys.argv
labels = ["$A_2 = 0.5$","$A_2 = 0.3$","$A_2 = 0.1$"]



fig, ax = plt.subplots()
fig.set_size_inches(18*0.393, 14*0.393) # diminuir na metade p 
ax.set_ylabel("$x$")
ax.set_xlabel("$y$")

L = 2000



z0 = np.zeros((L,L))


for i in range(1,len(folders)):
    print(i)
    data = np.loadtxt(folders[i] + "/" + folders[i] + "xyz.dat")
    
    z0 += np.reshape(data[:,2],(L,L))

x = np.reshape(data[:,0],(L,L))
y = np.reshape(data[:,1],(L,L))
ax.pcolormesh(y, x,z0,cmap=cmapblues)

#ax.legend()
plt.savefig("all_region.png", bbox_inches='tight', dpi = 300)

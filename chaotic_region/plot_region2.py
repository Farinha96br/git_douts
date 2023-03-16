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

cmapblues = matplotlib.colors.LinearSegmentedColormap.from_list("", ["#ffffff",rgb_darker[2]])

######
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png



fig, ax = plt.subplots()
fig.set_size_inches(18*0.393, 14*0.393) # diminuir na metade p 
ax.set_ylabel("$x$")
ax.set_xlabel("$y$")

rootname = sys.argv[1] #nome raiz dos experimentos
L = int(sys.argv[2]) #tamanho da rede quadrada dos dados


z = np.zeros((L,L))
c = 0
for folder in sorted(os.listdir("./")):
    if folder.startswith(rootname):
        print(folder + "/" + rootname + "xyz.dat")
        data = np.loadtxt(folder + "/" + folder + "xyz.dat")
        x = np.reshape(data[:,0],(L,L))
        y = np.reshape(data[:,1],(L,L))
        z += np.reshape(data[:,2],(L,L))
        c+=1

z = z/c
axis = ax.pcolormesh(y, x,z,cmap=cmapblues)
plt.colorbar(axis, label = r"$A_2$")
ax.set_title(r"$\w_1 = 3$ $\w_2 = 4$ $k_{y1} = k_{y2} = 3$  k_{x1} = 3 \pi k_{x1} = 3 \pi A_1 = 1")
plt.savefig("all_region2.png", bbox_inches='tight', dpi = 300)

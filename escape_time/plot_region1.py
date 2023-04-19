import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import cm
import os
import sys


plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png

rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_pallet = ['#007a96','#b39700','#b04bb0']

cmap = LinearSegmentedColormap.from_list("", [rgb_pallet[2],"white"])
cmap2 = LinearSegmentedColormap.from_list("", [rgb_pallet[2],"black",rgb_pallet[0]])

jet = cm.get_cmap('jet', 256)
newcolors = jet(np.linspace(0, 1, 256))
newcolors[-1,:] = [0,0,0,0]
newcmap = ListedColormap(newcolors)

folder = sys.argv[1]
######## De fato a plotagem
data = np.loadtxt(folder + "/" + folder + "xyz.dat")
fig, ax = plt.subplots()
ax.set_title(r"$A_2=0.5$")
fig.set_size_inches(7*0.393, 7*0.393) # diminuir na metade p 
ax.set_ylabel("$x$")
ax.set_xlabel("$y$")
print(data.shape)

L = 0
val0 = data[0,0]
for i in range(0,len(data[:,0])):
    if data[i,0] == val0:
        L +=1
        print(L)
    else:
        break
x = np.reshape(data[:,0],(L,L))
y = np.reshape(data[:,1],(L,L))
z = np.reshape(data[:,2],(L,L))


z = np.log(z)
fig.colorbar(ax.pcolormesh(y, x,z,cmap=newcmap),label = r"$\log(t)$")
plt.savefig(folder + "/escape.png", bbox_inches='tight', dpi = 300)

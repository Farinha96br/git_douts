import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
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

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white",rgb_darker[2]])
cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("", [rgb_pallet[2],"white",rgb_pallet[0]])

folder = sys.argv[1]

######## De fato a plotagem
data = np.loadtxt(folder + "/" + folder + "xyz.dat")
fig, ax = plt.subplots()
fig.set_size_inches(18*0.393, 14*0.393) # diminuir na metade p 
ax.set_ylabel("$x$")
ax.set_xlabel("$y$")
print(data.shape)
L = 500
x = np.reshape(data[:,0],(L,L))
y = np.reshape(data[:,1],(L,L))
z = np.reshape(data[:,2],(L,L))

d = np.abs(z-x)



ax1 = ax.pcolormesh(y, x,d,cmap=cmap)
fig.colorbar(ax1,label = r"|\Delta x|")
plt.savefig(folder + "/region.png", bbox_inches='tight', dpi = 300)

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
os.makedirs(folder + "/displacement",exist_ok=True)
print("loading x...")
x = np.loadtxt(folder + "/theta.dat")
print("loading y...")
y = np.loadtxt(folder + "/p.dat")


shape = (1024,1024)
x0 = np.reshape(x[:,0],shape)
y0 = np.reshape(y[:,0],shape)



yf = y0 - np.reshape(y[:,-1],shape)
fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$p$")

a = ax.pcolormesh(x0,y0,yf,cmap="bwr")
fig.colorbar(a,label = r"$\Delta p$")
plt.savefig(folder + "/disp" + ".png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()




#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf

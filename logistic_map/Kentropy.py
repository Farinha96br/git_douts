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

def KSentropy(x_t,min,max,n):
    bins = np.linspace(min,max,n)
    #print(bins)
    hist, edges = np.histogram(x_t,bins,density=True)
    hist = hist[hist != 0]
    H = np.sum(np.multiply(-1*np.log(hist),hist))
    return H

######
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######
fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

file = "logistic_map_0.5001.dat"
data = np.loadtxt(file)








##  Título do plot
ax.set_title("Shannon Entropy")




# plot normal
ax.plot(r,H,linewidth = 0.5, color = rgb_pallet[2],label = "H(r)")





#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf
plt.savefig("Entropy.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()
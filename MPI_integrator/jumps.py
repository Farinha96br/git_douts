import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors
import scipy.signal as scipy

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
fig, ax = plt.subplots()
fig.set_size_inches(10*0.393, 5*0.393) # o valor multiplicando é o tamanho em cm

folder = sys.argv[1]
x = np.loadtxt(folder + "/x.dat")
y = np.loadtxt(folder + "/y.dat")

kx = 3
ky = 3
cellx = np.pi/(2*kx)

os.makedirs(folder + "/jumps",exist_ok=True)
jumpdata = open(folder + "/datajumps.dat","w")

cell = np.pi/kx
for i in range(0,len(x[:,0])):
    ax.set_xlabel(r"$\tau$")
    ax.set_xlim(0,400)
    ax.set_ylim(-5,20)
    ax.set_ylabel(r"$x(\tau)$")
    for l in range(-10,10):
        ax.axhline(l*cell,lw = 0.5, ls = "--", color = "#cccccc")

    print("---",i,"---")
    jumps_index = np.array([])
    x_t= np.array(x[i,:])
    t = np.arange(0,len(x_t),1)
    #print(t)
    #peaks, _ = scipy.find_peaks(x_t)
    #valleys, _ = scipy.find_peaks(-1*x_t)
    #extrema = np.hstack((peaks,valleys)) # indices dos pontos extremas
    #extrema = sorted(extrema) # organiza os pontos extremos
    #extrema = np.array(extrema)
    x_cell = np.floor((x_t/cell))



    
    
        
                

        
        

    ax.plot(t,x_t, linewidth = 0.25,color = rgb_pallet[2],label = r"$x(t)$")
    ax.plot(t,x_cell, linewidth = 0.25,color = rgb_pallet[0],label = r"$cell$")

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(folder + "/jumps/"+ str(i) + ".png",bbox_inches='tight',dpi = 300) # salva em png
    ax.cla()













#ax.legend(frameon=False) # Caixinha d legenda sem borda
#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf
plt.close()
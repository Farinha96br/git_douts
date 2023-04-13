import numpy as np
import os
import sys
import matplotlib.pyplot as plt

# Algumas paletas de cor p serem usadas (VSCode recomendado pra mostar as cores no editor de texto)
rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_darker = ['#007a96','#b39700','#b04bb0']


#####
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######
# Parametros dos ks
kx =    3
ky =    3
kx2 = 3
ky2 = 3

a = 1

# define e printa o tamanho da céula
cellx = 3.14159265359/(kx*a)
cellx2 = 3.14159265359/(kx2*a)
print("cellx:",cellx)


print("file1")
data = np.loadtxt(sys.argv[1] + "/jumps_data.dat")
print("file2")
data2 = np.loadtxt(sys.argv[2] + "/jumps_data.dat")
print("file3")
data3 = np.loadtxt(sys.argv[3] + "/jumps_data.dat")

hist_data = data[:]
hist_data2 = data2[:]
hist_data3 = data3[:]

fig, ax = plt.subplots()
plt.tight_layout()
fig.set_size_inches(10*0.393, 5*0.393)




#ax.set_ylim(0,10000)
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

Ncell = 11
for i in range(0,Ncell):
    ax.axvline(cellx*i, linewidth = 0.25, linestyle = "--", color = "#cccccc",zorder = 0)
    #ax.axvline(cellx2*i, linewidth = 0.25, linestyle = "--", color = "#ff98ff",zorder = 0)



ax.set_xlabel(r"$ \frac{\pi}{k_{x}}$")


w = cellx*0.02
ax.set_xlim(cellx*4,Ncell*cellx)
ax.set_xticks(np.arange(cellx*4,cellx*Ncell+1,cellx))
ax.set_xticklabels(np.arange(4,Ncell+1,1))
b= np.arange(0, Ncell*cellx + w, w) + w/2
ax.set_ylim(0,10)
ax.set_ylabel("\# Saltos")
ax.hist(hist_data,bins = b, color = rgb_pallet[0] , alpha = 0.5, label = r"$A_2 = 0.1A_1$",histtype='stepfilled',edgecolor=rgb_darker[0], linewidth=0.25)
ax.hist(hist_data2,bins = b, color = rgb_pallet[1] ,alpha = 0.5, label = r"$A_2 = 0.2A_1$",histtype='stepfilled',edgecolor=rgb_darker[1], linewidth=0.25)
ax.hist(hist_data3,bins = b, color = rgb_pallet[2] ,alpha = 0.5, label = r"$A_2 = 0.4A_1$",histtype='stepfilled',edgecolor=rgb_darker[2], linewidth=0.25)
ax.legend(frameon = False, loc ="upper right")
plt.savefig("jumps_varios.png",bbox_inches='tight',dpi=300)
plt.close()


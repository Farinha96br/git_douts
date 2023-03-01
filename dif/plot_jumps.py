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
plt.rc('text', usetex=True) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######

# Parametros dos ks
kx =    12*3.1415
ky =    6
kx2 = 12*np.sqrt(7)
ky2 = 6

a = 1
 
# define e printa o tamanho da céula
cellx = 3.14159265359/(kx*a)
cellx2 = 3.14159265359/(kx2*a)
print("cellx:",cellx)


data = np.loadtxt(sys.argv[1] + "/jumps_data.dat")
print(data.shape)
hist_data = data[:]
fig, ax = plt.subplots()
plt.tight_layout()
fig.set_size_inches(10*0.393, 5*0.393)

Celllim = 8

#ax.set_xlim(0,Celllim*cellx)
#ax.set_ylim(0,600000)

for i in range(0,Celllim):
    ax.axvline(cellx*i, linewidth = 0.25, linestyle = "--", color = "#cccccc",zorder = 0)
    ax.axvline(cellx2*i, linewidth = 0.25, linestyle = "--", color = "#ff98ff",zorder = 0)

#ax.set_xticks(np.arange(cellx,cellx*Celllim,cellx))
#ax.set_xticklabels(np.arange(1,Celllim,1))

ax.set_xlabel(r"$\Delta \frac{N\pi}{k_{x0}}$")


ax.set_ylabel("\# Pulos")

w = 0.01
b= np.arange(0, Ncell*cellx + w, w)
ax.hist(hist_data,bins = b, color = "royalblue",zorder = 1)
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.savefig(sys.argv[1] + "/jump_hist.pdf",bbox_inches='tight')

plt.close()

#print("agora fazendo varios num só")
#print("file2")
#data2 = np.loadtxt(sys.argv[2] + "/jumps_data.dat")
#print("file3")
#data3 = np.loadtxt(sys.argv[3] + "/jumps_data.dat")
#
#
#hist_data2 = data2[:]
#hist_data3 = data3[:]
#
#fig, ax = plt.subplots()
#plt.tight_layout()
#fig.set_size_inches(10*0.393, 5*0.393)
#
#ax.set_xlim(cellx,8*cellx)
#ax.set_ylim(0,600000)
#
#
#for i in range(0,8):
#    ax.axvline(cellx*i, linewidth = 0.25, linestyle = "--", color = "#cccccc",zorder = 0)
#    ax.axvline(cellx2*i, linewidth = 0.25, linestyle = "--", color = "#ff98ff",zorder = 0)
#
#ax.set_xticks(np.arange(cellx,cellx*8,cellx))
#ax.set_xticklabels(np.arange(1,8,1))
#
#ax.set_xlabel(r"$\Delta \frac{N\pi}{k_{x0}}$")
#
#
#ax.set_ylabel("\# Pulos")
#ax.hist(hist_data,bins = 200, color = rgb_pallet[0] ,alpha = 0.6, label = r"$A_2 = 0.1$")
#ax.hist(hist_data2,bins = 200, color = rgb_pallet[1] ,alpha = 0.6, label = r"$A_2 = 0.4$")
#ax.hist(hist_data3,bins = 200, color = rgb_pallet[2] ,alpha = 0.6, label = r"$A_2 = 0.8$")
#
#ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#
#ax.legend(frameon = False)
#plt.savefig("jumps_varios.pdf",bbox_inches='tight')
#
#plt.close()





import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import scipy.signal as scipy

# Coisas d plotagem
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=True) # esse vc deixa True e for salvar em pdf e False se for p salvar png



data = []

# Faz o arquiv com as coisas dos pulos
data_folder = sys.argv[1] + "/traj/"
out_folder = sys.argv[1] + "/jumps/"
os.makedirs(out_folder,exist_ok=True)


# Parametros dos ks
kx =    12*3.1415
ky =    6
a = 1

# define e printa o tamanho da céula
cellx = 3.14159265359/(kx*a)
print("cellx:",cellx)

# Quantas vezes maior que uma celula o salto tem que ser
fac = 1.5

# arrays vazios onde os saltos entram
jumps_x = np.array([]) # todos saltos todos em x


c = 0
for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        print(filename)
        # inicializa arrays pra cada particula
        jumps_temp = np.array([])
        jumps_index = np.array([])

        # carrega e organiza os dados
        data = np.loadtxt(data_folder + filename)
        t= data[:,0]
        x= data[:,1]
        y= data[:,2]
        dt = data[1,0] - data[1,0]

        # identifica os indices dos pontos extremos
        peaks, _ = scipy.find_peaks(x)
        valleys, _ = scipy.find_peaks(-1*x)
        extrema = np.hstack((peaks,valleys))
        extrema = sorted(extrema) # organiza os pontos extremos

        
        # Procura os saltos
        for i in range(0,len(extrema)-1):
            d = abs(x[extrema[i]] - x[extrema[i+1]])
            if d >= cellx*fac: # checa se teve salto
                jumps_temp = np.append(jumps_temp,d) # anexa tamanho do pulo da particula
                jumps_index = np.append(jumps_index,extrema[i]) # anexa indice dos pulos da particula
                jumps_x = np.append(jumps_x,x[i]) # anexa o pulo no role dos pulos totais

            
        jumps_index = jumps_index.astype(int)

        # Plota as trajetorias com identificaçao dos saltos p conferências
        if c < 15:
            fig, ax = plt.subplots()
            plt.tight_layout()
            fig.set_size_inches(10*0.393, 5*0.393)
            #ax.set_title(filename)
            ax.set_xlim(0,20)
            ax.set_xlabel(r"$t$")

            NCELL = 10
            for j in range(0,NCELL):
                ax.axhline(cellx*j, linewidth = 0.25, linestyle = "--", color = "#cccccc",zorder = 0)
            #ax.axhline(1, linewidth = 0.5, linestyle = "--", color = "#555555",zorder = 0)

            ax.set_ylim(-0.05,cellx*NCELL)
            ax.set_ylabel(r"$x$")
            ticksy = np.arange(0,cellx*NCELL,2*cellx)
            ax.set_yticks(ticksy)
            ax.set_yticklabels(np.arange(0,NCELL,2))
            ax.set_ylabel(r"$\frac{N\pi}{k_{x0}}$")
            ax.plot(t,x,linewidth = 0.5, color = "royalblue",zorder = 1)
            ax.plot(t[extrema],x[extrema],ls = " ", marker = ",",markersize = 0.5, color = "firebrick",zorder = 2)
            ax.plot(t[jumps_index],x[jumps_index],ls = " ",markersize = 1, marker = "s", color = "forestgreen",zorder = 3)
            plt.savefig(out_folder + filename[:-4] + ".pdf",bbox_inches='tight')
            plt.close()
            c+=1




print("escrevendo arquivo")
f = open(sys.argv[1] + "/jumps_data.dat","w")
for i in range(0,len(jumps_x)):
    f.write(str(jumps_x[i]) + "\n")
f.close()


# Plotagem do histograma de saltos

data = np.loadtxt(sys.argv[1] + "/jumps_data.dat")
print(data.shape)
hist_data = data[:]
fig, ax = plt.subplots()

plt.tight_layout()
fig.set_size_inches(10*0.393, 5*0.393)

ax.set_xlim(cellx,cellx*9)

for i in range(0,9):
    ax.axvline(cellx*i, linewidth = 0.25, linestyle = "--", color = "#cccccc",zorder = 0)
ax.set_xticks(np.arange(cellx,cellx*9,cellx*2))
ax.set_xticklabels(np.arange(1,9,2))

ax.set_xlabel(r"$\Delta \frac{N\pi}{k_{x0}}$")


ax.set_ylabel("\# Pulos")
ax.hist(hist_data,bins = 200, color = "royalblue",zorder = 1)
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.savefig(sys.argv[1] + "/jump_hist.pdf",bbox_inches='tight')

plt.close()








#

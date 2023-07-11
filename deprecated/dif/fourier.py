
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_pallet = ['#007a96','#b39700','#b04bb0']

#cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [rgb_pallet[2],"white",rgb_pallet[0]])
#cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("", [rgb_pallet[2],"black",rgb_pallet[0]])

plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png




data = []
data_folder = sys.argv[1] + "/traj/"
out_folder = sys.argv[1] + "/fourier/"
os.makedirs(out_folder,exist_ok=True)
norm = 1
for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        print(filename)
        #data.append(np.loadtxt(data_folder + filename))
        data = np.loadtxt(data_folder + filename)
        t = data[:,0]
        if  filename == sorted(os.listdir(data_folder))[0]:
            Fcum = np.zeros(t.shape)
        N = len(t)
        x = data[:,1] # todas posições x da 1a particula
        xf = np.fft.fft(x) # faz a transformada
        xf = np.abs(xf)/len(t) # usa a magnitude e normalizada
        Fcum += xf

        freq = np.fft.fftfreq(N,d=(t[1]-t[0])) # Sabe la deus oq rola mas ajeita as frequencias

        #plota as coisa
        fig, ax = plt.subplots()
        fig.set_size_inches(16*0.393, 8*0.393)
        #ax[0].set_xlabel(r"$t$")
        #ax[0].set_ylabel(r"$x(t)$")
        #ax[0].set_xlim(0,200)
        #ax[0].set_ylim(0,5)
        #ax[0].plot(t[::2],x[::2],color = rgb_pallet[2], lw = 0.25)

        ax.set_xlabel(r"$f$")
        ax.set_ylabel(r"$A(f)$")
        ax.set_xlim(0,8)
        ax.set_ylim(0,0.06)
        ax.plot(freq,2*Fcum/norm,color = rgb_pallet[2], lw = 0.25)
        plt.savefig(out_folder + "/" + filename[:-4] + "_fouier.png",bbox_inches='tight', dpi = 300)
        plt.close()
        norm+=1



data = np.array(data)
print(data.shape)   #data[partícula,linha,coluna de dados]
                    # coluna de dados
                    # data[1,:,0] pega todos
#print(data[0,:,1])
#print(data[0,0,1]) # pos inicial
#print(data[0,-1,1]) # pos final






plt.show()










N = data.shape[0] # Número de partículas





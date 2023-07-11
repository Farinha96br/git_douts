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
os.makedirs(folder + "/recurrence",exist_ok=True)
x = np.loadtxt(folder + "/x.dat")
y = np.loadtxt(folder + "/y.dat")




for i in np.arange(0,100000,1):
    print(i)
    x_temp = x[i,:]
    y_temp = y[i,:]
    if np.abs(x_temp[-1] - x_temp[0]) > 70:
        t = np.arange(0,len(x[i,:]))

        tt, tt2 = np.meshgrid(t,t)
        tt2 = np.flip(tt2,axis=1)

        xx,xx2 = np.meshgrid(x_temp,x_temp)
        xx2 = np.flip(xx2,axis=1)

        yy,yy2 = np.meshgrid(y_temp,y_temp)
        yy2 = np.flip(yy2,axis=1)

        D = np.sqrt((xx - xx2)**2 + (yy - yy2)**2)

        fig, ax = plt.subplots()
        fig.set_size_inches(7*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm
        a = ax.pcolormesh(tt,tt2,D,cmap="jet")
        ax.set_xlabel(r"$\tau$")
        ax.set_ylabel(r"$\tau'$")

        fig.colorbar(a,label = r"$\Delta x$")
        plt.savefig(folder + "/recurrence/" + str(i) + ".png",bbox_inches='tight',dpi = 300) # salva em png
        plt.close()




#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf

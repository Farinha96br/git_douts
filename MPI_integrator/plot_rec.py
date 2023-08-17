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

its = len(x[0,:])
N = len(x[:,0])
kx = 3
ky = 3



for i in np.arange(0,len(x[:,0])):
    print(i+1,"/",N)
    fig, ax = plt.subplots()
    fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm
    x_t = x[i,:]
    y_t = y[i,:]

    xx1,xx2 = np.meshgrid(x_t,x_t)
    xx = np.abs(xx1 - xx2)
    xx = xx**2

    yy1,yy2 = np.meshgrid(y_t,y_t)
    yy = np.abs(yy1 -yy2)
    yy = yy**2


    M = np.sqrt(xx + yy)
    M = M < 0.01*np.sqrt((np.pi/kx)**2 + (np.pi/ky)**2)


    ts = np.arange(0,its,1)
    tt1,tt2 = np.meshgrid(ts,ts)


    
    ax1 = ax.pcolormesh(tt1,tt2,M,cmap="Greys")

    ax.set_ylabel(r"$x(\tau)$")
    ax.set_ylabel(r"$x(\tau')$")
    #fig.colorbar(ax1,label=r"$\Delta S$")

    plt.savefig(folder + "/recurrence/" + str(i) + ".png",bbox_inches='tight',dpi = 300) # salva em png
    plt.close()
    
    





#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf

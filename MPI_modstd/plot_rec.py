import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors
import aux
import skimage.feature as ft
import skimage.morphology as mm

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
x = np.loadtxt(folder + "/theta.dat")%(2*np.pi)
y = np.loadtxt(folder + "/p.dat")
y = aux.perisim(y,np.pi)


its = len(x[0,:])
N = len(x[:,0])



reclim = 500
for i in np.arange(0,len(x[:,0])):
    
    fig, ax = plt.subplots()
    fig.set_size_inches(10*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm
    x_t = x[i,:reclim]
    y_t = y[i,:reclim]

    #xx1,xx2 = np.meshgrid(x_t,x_t)
    #xx = np.abs(xx1 - xx2)%(2*np.pi)
    #xx = xx**2
#
    #yy1,yy2 = np.meshgrid(y_t,y_t)
    #yy = np.abs(yy1 - yy2)%(np.pi)
    #yy = yy**2

    M = aux.recmatrix2D(x_t,y_t,0.01*np.sqrt(np.pi**2))
    #print(np.flip(np.identity(25),axis=1))

    #Cx, Cy = aux.center_mass(M)
    #Dcenter = np.sqrt((Cx-reclim/2)**2+(Cx-reclim/2)**2)

    #glcm = ft.greycomatrix(M,levels=2,distances=[1],angles = [np.pi/4])
    print(i,np.sum(M)-reclim)
    param = np.sum(M)-reclim
    if param > 2*reclim:
        title = "periodic"
    if param < 2*reclim:
        title = "chaos"
    
    #print(i,"/",Cx, Cy,Dcenter, title)   

    

    ts = np.arange(0,reclim,1)
    tt1,tt2 = np.meshgrid(ts,ts)


    
    ax1 = ax.pcolormesh(tt1,tt2,M)
    ax.set_title(title)
    ax.set_ylabel(r"$x(\tau)$")
    ax.set_ylabel(r"$x(\tau')$")
    #fig.colorbar(ax1,label=r"$\Delta S$")

    plt.savefig(folder + "/recurrence/" + str(i) + ".png",bbox_inches='tight',dpi = 300) # salva em png
    plt.close()
    
    





#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf

import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.colors
from skimage import morphology as mm
from skimage import measure as med
import aux

# Algumas paletas de cor p serem usadas (VSCode recomendado pra mostar as cores no editor de texto)
rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_darker = ['#007a96','#b39700','#b04bb0']

## modelo de como criar um colormap linear usando cores predefinidas:
cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("", ["#9ef27b","#FF6645","#FF59D7","#8FAAFF"])



######
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######

fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm
ax.set_xlabel(r"$y$")
ax.set_ylabel(r"$x$")

folder = sys.argv[1]
Nskip = int(sys.argv[2])

label = np.load(folder + "/label.npy")


print("loading x...")
x = np.loadtxt(folder + "/theta.dat")
x = x[Nskip:,:]

print("loading y...")
y = np.loadtxt(folder + "/p.dat")
y = y[Nskip:,:]

#y = y%(2*np.pi/ky)

print("testpoints")


# 0X = Periodico
# 1X = Caotico
# X0 = Sem transporte
# X1 = Transp Horizontal
# X2 = Transp vertical
# X3 = Tranp geral


tipo = np.zeros(len(x[:,0]))


for i in range(0,len(x[:,0])):
    #print(i,":",x[i,0],y[i,0])

    # classifica sobre caos ou periotico
    x_t = x[i,:]%(2*np.pi)
    y_t = aux.perisim(y[i,:],np.pi)
    xbins = np.linspace(0,2*np.pi,1024)
    ybins = np.linspace(-np.pi,np.pi,1024)
    H = aux.H2d(x_t%(2*np.pi),aux.perisim(y_t,np.pi),xbins,ybins)
    txt = ""
    if H > 7:
        # traj caótica

        txt += "chaotic "
        if np.any(np.abs(y[i,:] - y[i,0]) > 2.5*np.pi):
            tipo[i] = 3
            txt += "with transport"
        else:
            txt += "no transport"
            tipo[i] = 2

    
    else:
        txt += "periodic "
        if aux.isAcc(y[i,:]):
            tipo[i] = 1
            txt += "accelerated"
        else:
            txt += "confined"
            tipo[i] = 0


    

    print(i,"\t",txt)
    
        
    
    #print(i,x[i,0],y[i,0],H,tipo[i])
    







# Bota os dados num grid (ainda com elementos repitidos)
Lx = 2*np.pi
Nx = 1024
Lpxx = Lx/Nx
#xpx = np.trunc(x/Lpxx).astype("int32")
#xpx = np.ravel(xpx)
#
Ly = 2*np.pi
Ny = 1024
Lpxy = Ly/Ny
#ypx = np.trunc(y/Lpxy).astype("int32")
#ypx = np.ravel(ypx)
#print("with duplicates:",xpx.shape)
#
#
#all = xpx + Ny*ypx
#all = np.ravel(all)
#all = np.unique(all)
#
#xpx = all%Ny
#ypx = (all/Ny).astype("int32")
#print("No duplicates:",xpx.shape)
#
#
#img = np.zeros(Nx*Ny)
#img[all] = 1
#img = np.reshape(img,(Nx,Ny)).astype("uint8") ## IMAGEM DO MAPA
#print(img)

print(x.shape)

print(x)

px0 = x[:,0]
py0 = y[:,0]


aa, bb = np.meshgrid(np.linspace(0,2*np.pi,Nx),np.linspace(-np.pi,np.pi,Ny))

#fig, ax = plt.subplots()
#fig.set_size_inches(7*0.393, 7*0.393)
#ax.set_xlabel(r"$\theta$")
#ax.set_ylabel(r"$p$")
#ax.set_title("Recheck label")
#ax.pcolormesh(aa, bb, label, cmap = "rainbow")
#ax.scatter(px0,py0,s = 0.5,c = "black")
#for i in range(0,len(x[:,0])):
#    ax.text(px0[i],py0[i],str(i),c = "black",size="small")
#
#plt.savefig(folder + "/mm_7_tests",bbox_inches='tight',dpi = 300) # salva em png
#plt.close()



label_type = np.zeros(label.shape)
print("#N",np.max(label))


for i in range(0,len(tipo)):

    print(i,tipo[i])
    mask_region = np.zeros(label.shape)
    mask_region[label == i] = 1
    label_type[mask_region == 1] = tipo[i]




    
fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393)
ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$p$")
plotson = ax.pcolormesh(aa, bb, label_type, cmap = cmap2,vmin=0,vmax=3)
ax.set_xlim(0,2*np.pi)
ax.set_ylim(-np.pi,np.pi)

#ax.scatter(px0,py0,s = 0.5,c = "black")


#fig.colorbar(plotson)

plt.savefig(folder + "/mm_8_tests",bbox_inches='tight',dpi = 300) # salva em png
plt.savefig("transp_type/K_" + folder[-6:] +".png",bbox_inches='tight',dpi = 300) # salva em png

plt.close()


file = open("areas.dat","a")

norm = label.shape[0]*label.shape[1]

norm = np.sum(norm)
#file.write("#var    periodic-conf periodic-acc chaos-trapped chaos-transport")
file.write(folder[-6:] + "\t")
print(norm,label.shape)


for i in range(0,4):
    mask = label_type == i
    
    mask = np.sum(mask)/norm
    file.write(str(mask) + "\t")

file.write(str(np.max(label)) + "\t")
file.write("\n")
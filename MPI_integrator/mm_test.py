import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.patches as mpatches
import aux

# Algumas paletas de cor p serem usadas (VSCode recomendado pra mostar as cores no editor de texto)
rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_pallet = ['#007a96','#b39700','#b04bb0']

## modelo de como criar um colormap linear usando cores predefinidas:
cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("", ["#ffffff","#4E6CFF","#FF4E6C"])


######
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######



kx = 3
ky = 3

folder = sys.argv[1]
Nskip = int(sys.argv[2])

label = np.load(folder + "/label.npy")


print("loading x...")
x = np.loadtxt(folder + "/x.dat")
x = x[Nskip:,:]

print("loading y...")
y = np.loadtxt(folder + "/y.dat")
y = y[Nskip:,:]



tipo = [None]*(len(x[:,0]))
# 0 = confinada
# 1 = transporte normal
# 2 = balistica


for i in range(0,len(x[:,0])):
    #print(i,":",x[i,0],y[i,0])
    x_t = x[i,:]
    t = np.arange(0,len(x_t))
    txt = ""
    gamma, erro = aux.getExp(x_t,t)

    if gamma < 0.5:
        tipo[i] = 0
    
    if gamma >= 0.7 and gamma < 1.7:
        tipo[i] = 1

    if gamma >= 1.7:
        tipo[i] = 2
    
    


    tipo[i] = gamma

     
    print(i,"{:05.4f}".format(gamma),"{:05.4f}".format(erro))


# Bota os dados num grid (ainda com elementos repitidos)
kx = 3
Lx = 2*np.pi/kx
Nx = 1024
Lpxx = Lx/Nx
#xpx = np.trunc(x/Lpxx).astype("int32")
#xpx = np.ravel(xpx)
#
ky = 3 
Ly = 2*np.pi/ky
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


aa, bb = np.meshgrid(np.linspace(0,Lx,Nx),np.linspace(0,Ly,Ny))

label_type = np.zeros(label.shape)
print("#N",np.max(label))


for i in range(0,len(tipo)):

    print(i,tipo[i])
    mask_region = np.zeros(label.shape)
    mask_region[label == i] = 1
    label_type[mask_region == 1] = tipo[i]




fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

ax.set_xlim(0,2*np.pi/3)
ax.set_xticks([0,2*np.pi/6,2*np.pi/3])
ax.set_xticklabels([r"$0$",r"$2\pi/2k_y$",r"$2\pi/k_y$"])
ax.set_ylim(0,2*np.pi/3)
ax.set_yticks([0,2*np.pi/6,2*np.pi/3])
ax.set_yticklabels([r"$0$",r"$2\pi/2k_x$",r"$2\pi/k_x$"])
plotson = ax.pcolormesh(bb, aa, label_type, cmap = cmap2,vmin = 0, vmax = 2)

# Ajeita os labels
patch0 = mpatches.Patch(color="#ffffff", label='trapped')
patch1 = mpatches.Patch(color="#4E6CFF", label='diffusive')
patch2 = mpatches.Patch(color="#FF4E6C", label='ballistic')

ax.legend(handles=[patch0,patch1,patch2],)



#ax.scatter(py0,px0,s = 0.5,c = "black")
#for i in range(0,len(px0)):
#    ax.text(py0[i],px0[i],str(i),c = "black",size="small")

#plt.colorbar(plotson)
ax.set_xlim(0,2*np.pi/3)
ax.set_ylim(0,2*np.pi/3)

plt.savefig(folder + "/mm_type",bbox_inches='tight',dpi = 300) # salva em png

plt.close()


file = open("areas.dat","a")

norm = label.shape[0]*label.shape[1]

norm = np.sum(norm)
#file.write("#var    periodic-conf periodic-acc chaos-trapped chaos-transport")
file.write(folder[-8:] + "\t")
print(norm,label.shape)


for i in range(0,2):
    mask = label_type == i
    mask = np.sum(mask)/norm
    file.write(str(mask) + "\t")

file.write(str(np.max(label)) + "\t")
file.write("\n")
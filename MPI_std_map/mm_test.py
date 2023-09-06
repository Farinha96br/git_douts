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
cym_pallet = ['#007a96','#b39700','#b04bb0']

## modelo de como criar um colormap linear usando cores predefinidas:
cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("", [rgb_pallet[2],"black",rgb_pallet[0]])



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

Nrec = 1000
for i in range(0,len(x[:,0])):
    print(i,":",x[i,0],y[i,0])

    # classifica sobre ter transporte ou não
    #if np.any(x[i,:]) > 3*np.pi:
    #    tipo[i] += 1
    #if np.any(y[i,:]) > 3*np.pi:
    #    tipo[i] += 2
   
    # classifica sobre caos ou periotico
    x_t = x[i,:Nrec]%(2*np.pi)
    y_t = aux.perisim(y[i,:Nrec],np.pi)
    M = aux.recmatrix2D(x_t,y_t,0.01*np.sqrt(np.pi**2))

    fracarea = np.sum(M)/(Nrec*Nrec)
    #print(i,count)
    if fracarea > 0.01:
        tipo[i] = 1
    if fracarea <= 0.01:
        tipo[i] = 2
    
    print(i,x[i,0],x[i,0],fracarea,tipo[i])
    







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
plotson = ax.pcolormesh(aa, bb, label_type, cmap = "rainbow",vmin=0,vmax=2)
ax.scatter(px0,py0,s = 0.5,c = "black")
for i in range(0,len(x[:,0])):
    txt = ""
    if tipo[i] == 1:
        txt = "P"
    if tipo[i] == 2:
        txt = "C"
    ax.text(px0[i],py0[i],txt,c = "black",size="small")

fig.colorbar(plotson)

plt.savefig(folder + "/mm_8_tests",bbox_inches='tight',dpi = 300) # salva em png
plt.close()


file = open("areas.dat","a")

norm = label != 0

norm = np.sum(norm)
#file.write("#var    periodic    chaos\n")
file.write(folder[-6:] + "\t")
print(norm,label.shape)

for i in range(0,2):
    mask = label_type == (i+1)
    
    mask = np.sum(mask)/norm
    file.write(str(mask) + "\t")

file.write(str(np.max(label)) + "\t")
file.write("\n")
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

kx = 3
ky = 3

folder = sys.argv[1]
Nskip = int(sys.argv[2])

label = np.load(folder + "/label.npy")


print("loading x...")
x = np.loadtxt(folder + "/x.dat")
x = x[Nskip:,:]
#x = x%(2*np.pi/kx)
print("loading y...")
y = np.loadtxt(folder + "/y.dat")
y = y[Nskip:,:]
#y = y%(2*np.pi/ky)



tipo = [None]*(np.max(label))
# 0 = confinada
# 1 = transporte
# 2 = balistica
i = 0
while i < len(x[:,0]):
    dev = np.std(x[i,:])

    if dev > 500:
        tipo[i] = 3
    
    if dev < 500:
        tipo[i] = 2

    if np.all(np.abs(x[i,:]) < 2*np.pi/kx):
        tipo[i] = 1
    
    i += 1

# Bota os dados num grid (ainda com elementos repitidos)
kx = 3
Lx = 2*np.pi/kx
Nx = 512
Lpxx = Lx/Nx
#xpx = np.trunc(x/Lpxx).astype("int32")
#xpx = np.ravel(xpx)
#
ky = 3 
Ly = 2*np.pi/ky
Ny = 512
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

px0 = np.array((x[:,0]*Nx/Lx).astype("int"))
py0 = np.array((y[:,0]*Ny/Ly).astype("int"))






aa, bb = np.meshgrid(np.arange(Nx),np.arange(Ny))

fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393)
ax.set_xlabel(r"$y$")
ax.set_ylabel(r"$x$")
ax.pcolormesh(bb, aa, label, cmap = "rainbow")
for i in range(0,len(tipo)):
    ax.text(py0[i],px0[i],tipo[i],c= "white")
    print(py0[i],px0[i],tipo[i])
ax.scatter(py0[i],px0[i],s = 0.5,c= "black")

plt.savefig(folder + "/mm_7_tests",bbox_inches='tight',dpi = 300) # salva em png
plt.close()


label_type = np.zeros(label.shape)

print("#N",np.max(label))


for i in range(1,np.max(label)+1):
    mask_region = np.zeros(label.shape)
    mask_region[label == i] = 1
    label_type[mask_region == 1] = tipo[i-1]
    



fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393)
ax.set_xlabel(r"$y$")
ax.set_ylabel(r"$x$")
ax.pcolormesh(bb, aa, label_type, cmap = "rainbow")

for i in range(0,len(tipo)):
    if tipo[i] == 1:
        ax.text(py0[i],px0[i],"c",c= "white")
    if tipo[i] == 2:
        ax.text(py0[i],px0[i],"d",c= "white")
    if tipo[i] == 3:
        ax.text(py0[i],px0[i],"b",c= "white")

#ax.scatter(py0[i],px0[i],s = 0.5,c= "black")
plt.savefig(folder + "/mm_8_tests",bbox_inches='tight',dpi = 300) # salva em png
plt.close()


var = folder[-5:]

file = open("tranp_frac","a")
#file.write("# var confined difusive balistic\n")
file.write(var + " ")

for i in range(1,4):
    mask = np.zeros(label.shape)
    mask = label_type[label_type == i]
    sum = np.sum(mask)
    file.write(str(sum) + " ")

file.write(str(sum) + "\n")



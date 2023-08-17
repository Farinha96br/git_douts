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
print("loading x...")
x = np.loadtxt(folder + "/x.dat")
x = x%(2*np.pi/kx)
print("loading y...")
y = np.loadtxt(folder + "/y.dat")
y = y%(2*np.pi/ky)


# Bota os dados num grid (ainda com elementos repitidos)
kx = 3
Lx = 2*np.pi/kx
Nx = 512
Lpxx = Lx/Nx
xpx = np.trunc(x/Lpxx).astype("int32")
xpx = np.ravel(xpx)

ky = 3 
Ly = 2*np.pi/ky
Ny = 512
Lpxy = Ly/Ny
ypx = np.trunc(y/Lpxy).astype("int32")
ypx = np.ravel(ypx)
print("with duplicates:",xpx.shape)


all = xpx + Ny*ypx
all = np.ravel(all)
all = np.unique(all)

xpx = all%Ny
ypx = (all/Ny).astype("int32")
print("No duplicates:",xpx.shape)


img = np.zeros(Nx*Ny)+1
img[all] = 0
img = np.reshape(img,(Nx,Ny)).astype("uint8") ## IMAGEM DO MAPA
print(img)

aa, bb = np.meshgrid(np.arange(Nx),np.arange(Ny))

#ax.imshow(img.astype("uint8"),cmap = "Greys")
ax.pcolormesh(bb, aa, img, cmap = "Greys_r")
plt.savefig(folder + "/mm_raw.png",bbox_inches='tight',dpi = 300) # salva em png

# Tratamento morfologico
radius = 2
SE = mm.disk(radius)
SEconnec = mm.diamond(3) # 4-conectividade na reconstrucao

print(SE)

op = mm.binary_opening(img,SE)
ax.pcolormesh(bb, aa, op, cmap = "Greys_r")
plt.savefig(folder + "/mm_op.png",bbox_inches='tight',dpi = 300) # salva em png

cls = mm.binary_closing(op,SE)
ax.pcolormesh(bb, aa, cls, cmap = "Greys_r")
plt.savefig(folder + "/mm_cls.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()


fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393)
ax.set_xlabel(r"$y$")
ax.set_ylabel(r"$x$")

label = med.label(np.flip(np.rot90(cls,3),axis=1))

if np.max(label) >= 1:
    cx = []
    cy = []
    props = med.regionprops(label) # imagem rotulada
    for i in range(0,len(props)): # pega as centroides
        cx.append(props[i].centroid[0])
        cy.append(props[i].centroid[1])


color_label = aux.label_hue2(label)
print(color_label.shape)
ax.imshow(color_label,interpolation='none',origin="lower",zorder = 0)
ax.scatter(cy,cx,c = "white",marker="x")

plt.savefig(folder + "/mm_labeled.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()









#plt.savefig("graph.pdf",bbox_inches='tight') # salva em pdf






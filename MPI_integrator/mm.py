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

fig, ax = plt.subplots(2,3,sharex=True,sharey=True)
fig.set_size_inches(12*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm
ax[1,1].set_xlabel(r"$y$")
ax[1,0].set_ylabel(r"$x$")
for i in range(0,2):
    for j in range(0,3):
        ax[i,j].set_xlim(0,2*np.pi/3)
        ax[i,j].set_xticks([0,2*np.pi/6,2*np.pi/3])
        ax[i,j].set_xticklabels([r"$0$",r"$2\pi/2k_y$",r"$2\pi/k_y$"])
        
        ax[i,j].set_ylim(0,2*np.pi/3)
        ax[i,j].set_yticks([0,2*np.pi/6,2*np.pi/3])
        ax[i,j].set_yticklabels([r"$0$",r"$2\pi/2k_x$",r"$2\pi/k_x$"])



kx = 3
ky = 3

folder = sys.argv[1]
print("loading x...")
x = np.loadtxt(folder + "/x.dat")
x = x%(2*np.pi/kx)
print("loading y...")
y = np.loadtxt(folder + "/y.dat")
y = y%(2*np.pi/ky)

saveSteps = True

# Bota os dados num grid (ainda com elementos repitidos)
kx = 3
Lx = 2*np.pi/kx
Nx = 1024
Lpxx = Lx/Nx
xpx = np.trunc(x/Lpxx).astype("int32")
xpx = np.ravel(xpx)

ky = 3 
Ly = 2*np.pi/ky
Ny = 1024
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


img = np.zeros(Nx*Ny)
img[all] = 1
img = np.reshape(img,(Nx,Ny)).astype("uint8") ## IMAGEM DO MAPA
print(img)

aa, bb = np.meshgrid(np.linspace(0,2*np.pi/kx,Nx),np.linspace(0,2*np.pi/ky,Ny))
step = 0
if saveSteps:
    #ax.imshow(img.astype("uint8"),cmap = "Greys")
    ax[0,0].pcolormesh(bb, aa, img, cmap = "Greys_r")
    #ax.set_title("Raw")

radius = 2
SE = mm.disk(radius)
ero = mm.erosion(img,SE)
op = mm.reconstruction(ero,img,"dilation",np.ones((3,3)))

if saveSteps:
    #ax.imshow(img.astype("uint8"),cmap = "Greys")
    ax[0,1].pcolormesh(bb, aa, ero, cmap = "Greys_r")
    #ax.set_title("Erosion")

if saveSteps:
    #ax.imshow(img.astype("uint8"),cmap = "Greys")
    ax[0,2].pcolormesh(bb, aa, op, cmap = "Greys_r")
    #ax.set_title("Op. Rec.")


radius = 3
SE = mm.disk(radius)
dil = mm.dilation(op,SE)
cls = mm.erosion(dil,SE)


if saveSteps:
    #ax.imshow(img.astype("uint8"),cmap = "Greys")
    ax[1,0].pcolormesh(bb, aa, dil, cmap = "Greys_r")
    #ax.set_title("Dilation")


if saveSteps:
    #ax.imshow(img.astype("uint8"),cmap = "Greys")
    ax[1,1].pcolormesh(bb, aa, cls, cmap = "Greys_r")
    #ax.set_title("Closing")


to_label = cls



label1 = mm.label(to_label,connectivity=1)
print("#region1",np.max(label1))
label2 = mm.label(1-to_label,connectivity=1)
print("#region2",np.max(label2))
label2[label2 != 0] += np.max(label1)
label = label1 + label2 - 1
np.save(folder + "/label.npy",label)
print("#region3",np.max(label)+1)

#print(label)

cx = []
cy = []

if np.all(label == label[0,0]):
    cx.append(0.1)
    cy.append(0.1)
else:
    for i in range(0,np.max(label)+1):
        mask = np.zeros(label.shape)
        mask[label == i] = 1
        tempmask1 = np.array(mask)
        # bota as bordas da mascara como 0 p nao dar problema com exigoes mt extensas como o mapa padrao com K pequeno
        tempmask1[:,0] = 0
        tempmask1[:,-1] = 0
        tempmask1[0,:] = 0
        tempmask1[-1,:] = 0


        # This method is using morphology and randon choice to pick the "center point"
        while np.sum(tempmask1 > 0):
            #print(c)
            tempmask2 = tempmask1   
            tempmask1 = mm.binary_erosion(tempmask1, mm.disk(1))

            
        #print(i,np.max(tempmask2))
        tempmask2 = tempmask2.astype("bool")
        tempmask2[tempmask2] = 1

        ycand = np.ravel(bb[tempmask2])
        xcand = np.ravel(aa[tempmask2])
        if len(xcand) != len(ycand):
            print("ERRO CARAIO")
        a = int(len(xcand)/2)
        cx.append(xcand[a])
        cy.append(ycand[a])


#label = np.flip(np.rot90(label,3),axis=1)
#color_label = aux.label_hue2(label)
#print(color_label.shape)

#ax.imshow(color_label,interpolation='none',origin="lower",zorder = 0)
ax[1,2].pcolormesh(bb,aa,label,cmap="rainbow")


pointfile = open(folder + "/testpoints.dat","w")
for i in range(0,len(cx)):
    
    ax[1,2].text(cy[i],cx[i],str(i),c = "black",size="small")
    pointfile.write(str(cx[i]) + "\t" + str(cy[i]) + "\n")

ax[1,2].scatter(cy,cx,s = 0.5,c = "black")

plt.savefig(folder + "/mm_steps",bbox_inches='tight',dpi = 900) # salva em png
#plt.savefig("data-seg_batch/K_" + folder[-8:] +".png",bbox_inches='tight',dpi = 900) # salva em png

plt.close()
print("regions:",len(np.ravel(np.unique(label))))
pointfile.close()
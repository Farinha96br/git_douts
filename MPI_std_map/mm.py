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
ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$p$")

folder = sys.argv[1]
print("loading x...")
x = np.loadtxt(folder + "/theta.dat")
x = x%(2*np.pi)

print("loading y...")
y = np.loadtxt(folder + "/p.dat")
y = (y-np.p)%(2*np.pi)

# Bota os dados num grid (ainda com elementos repitidos)

SaveSteps = True

Lx = 2*np.pi
Nx = 1024
Lpxx = Lx/Nx
xpx = np.trunc(x/Lpxx).astype("int32")
xpx = np.ravel(xpx)

Ly = 2*np.pi
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
#print(img)

aa, bb = np.meshgrid(np.linspace(0,2*np.pi,Nx),np.linspace(-np.pi,np.pi,Nx))

if SaveSteps:
    #ax.imshow(img.astype("uint8"),cmap = "Greys")
    ax.pcolormesh(aa, bb, img, cmap = "Greys_r")
    ax.set_title("Raw")
    plt.savefig(folder + "/mm_0.png",bbox_inches='tight',dpi = 300) # salva em png

# Tratamento morfologico
radius = 4
SE = mm.disk(radius)

#print(SE)

cls = mm.binary_closing(img,SE)
if SaveSteps:
    ax.pcolormesh(aa, bb, cls, cmap = "Greys_r")
    ax.set_title("Closing")
    plt.savefig(folder + "/mm_1.png",bbox_inches='tight',dpi = 300) # salva em png


#op = np.array(cls)
radius = 1
SE = mm.disk(radius)
op = mm.binary_opening(cls,SE)
#op = mm.area_opening(cls,64)
if SaveSteps:
    ax.pcolormesh(aa, bb, op, cmap = "Greys_r")
    ax.set_title("Opening")
    plt.savefig(folder + "/mm_2.png",bbox_inches='tight',dpi = 300) # salva em png



#radius = 1
#SE = mm.disk(radius)
#grad =  op.astype("uint8") - mm.erosion(op,SE).astype("uint8") 
#if SaveSteps:
#    ax.pcolormesh(aa, bb, grad, cmap = "Greys_r")
#    ax.set_title("Gradient")
#    plt.savefig(folder + "/mm_3.png",bbox_inches='tight',dpi = 300) # salva em png
#
##print("grad1",grad)
#
#grad = 1 - grad
#if SaveSteps:
#    ax.pcolormesh(aa, bb, grad, cmap = "Greys_r")
#    ax.set_title("Gradient inverse (opt)")
#    plt.savefig(folder + "/mm_4.png",bbox_inches='tight',dpi = 300) # salva em png
#    plt.close()
##print("grad2",grad)



label1 = mm.label(op,connectivity=1)
print("#region1",np.max(label1))
label2 = mm.label(1-op,connectivity=1)
print("#region2",np.max(label2))
label2[label2 != 0] += np.max(label1)
label = label1 + label2 - 1
np.save(folder + "/label.npy",label)
print("#region3",np.max(label)+1)

print(label)

cx = []
cy = []

#if np.all(grad == 0) or np.all(grad == 1):
#    cx.append(0.1)
#    cy.append(0.1)

for i in range(0,np.max(label)+1):
    mask = np.zeros(label.shape)
    mask[label == i] = 1
    tempmask1 = mask
    # bota as bordas da mascara como 0 p nao dar problema com exigoes mt extensas como o mapa padrao com K pequeno
    if np.all(tempmask1[:,0] == 1):
        tempmask1[:,0] = 0
    if np.all(tempmask1[:,-1] == 1):
        tempmask1[:,-1] = 0
    if np.all(tempmask1[0,:] == 1):
        tempmask1[0,:] = 0
    if np.all(tempmask1[-1,:] == 1):
        tempmask1[-1,:] = 0


    while np.sum(tempmask1 > 0):
        #print(c)
        tempmask2 = tempmask1   
        tempmask1 = mm.binary_erosion(tempmask1, mm.disk(1))
    #print(i,np.max(tempmask2))
    tempmask2 = tempmask2.astype("bool")
    tempmask2[tempmask2] = 1
    #ax.pcolormesh(bb, aa, tempmask2, cmap = "Greys_r")
    #ax.set_title("mask" + str(i))
    #plt.savefig(folder + "/mm_5_" + str(i) + "_.png",bbox_inches='tight',dpi = 300) # salva em png
    #tempmask2 = tempmask2.astype("uint8")
    #print(tempmask2)
    ##props = med.regionprops(tempmask2)
    ##c_temp = props[0]['centroid']
    ##cx.append(c_temp[1])
    ##cy.append(c_temp[0])
    ycand = np.ravel(bb[tempmask2])
    xcand = np.ravel(aa[tempmask2])
    cx.append(np.random.choice(xcand))
    cy.append(np.random.choice(ycand))



plt.close()


fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393)
ax.set_xlabel(r"$\theta$")
ax.set_ylabel(r"$p$")
#label = np.flip(np.rot90(label,3),axis=1)
#color_label = aux.label_hue2(label)
#print(color_label.shape)
ax.set_title("Labeled")
#ax.imshow(color_label,interpolation='none',origin="lower",zorder = 0)
ax.pcolormesh(aa,bb,label,cmap="rainbow")

pointfile = open(folder + "/testpoints.dat","w")
for i in range(0,len(cx)):
    ax.text(cx[i],cy[i],str(i),c = "black",size="small")
    pointfile.write(str(cx[i]) + "\t" + str(cy[i]) + "\n")
ax.scatter(cx,cy,s = 0.5,c = "black")
plt.savefig(folder + "/mm_6",bbox_inches='tight',dpi = 300) # salva em png
plt.savefig("seg_batch/K_" + folder[-6:] +".png",bbox_inches='tight',dpi = 300) # salva em png

plt.close()
print("regions:",len(np.ravel(np.unique(label))))
pointfile.close()




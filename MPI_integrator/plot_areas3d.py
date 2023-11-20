import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource
from matplotlib import cbook, cm

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
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
fig.set_size_inches(21*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm


data = np.loadtxt("areas.dat")
print(data.shape)
##  Limites e ticklabels em x e y:
ax.set_xlabel(r'$A_2$')
ax.set_ylabel(r"$\theta_x$")
ax.set_xlim(0,1)
ax.set_ylim(0,np.pi)

ax.set_xticks(np.linspace(0,1,5))
ax.set_yticks([0,np.pi/4,np.pi/2,np.pi/4+np.pi/2,np.pi])
ax.set_yticklabels([r"$0$",r"$\frac{\pi}{4}$",r"$\frac{\pi}{2}$",r"$\frac{3\pi}{4}$",r"$\pi$"])



L_all = len(data[:,0])
sort_1 = np.argsort(data[:,0])
data = data[sort_1,:]
#np.savetxt("areas2.dat",data)

V0 = data[0,1]
L1 = 0
keepTrying = True
while keepTrying:
    if data[L1,0] == V0:
        L1 += 1
    else:
        keepTrying = False

L2 = int(L_all/L1)
print("L1",L1)
print("L2",L2)


for i in range(0,L2):
    print(i,i*L1,i*L1+L1)
    temp = data[i*L1:i*L1+L1,:]
    print(temp.shape)
    index = np.argsort(temp[:,1])
    temp = temp[index,:]
    data[i*L1:i*L1+L1,:] = temp

np.savetxt
print(data)

titles = ["periodic","chaotic","balistic"]

AA =   np.reshape(data[:,0],(L2,L1))
thth = np.reshape(data[:,1],(L2,L1))
peri = np.reshape(data[:,2],(L2,L1))
chao = np.reshape(data[:,3],(L2,L1))
bali = np.reshape(data[:,4],(L2,L1))
#bali[bali != 0] = 1

#AA, thth = np.meshgrid(np.linspace(0,1,201),np.linspace(0,3.1415,201)[:30])
ls = LightSource(270, 45)
rgb = ls.shade(chao, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
surf = ax.plot_surface(AA, thth, chao,rstride=1, cstride=1, facecolors=rgb, linewidth=0, antialiased=False, shade=False)

plt.show()
#plt.savefig("paramspace.png",bbox_inches='tight',dpi = 300) # salva em png
plt.close()
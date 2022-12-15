import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mp_img
from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting

data = np.loadtxt("log.txt")

A = data[:,1]
f = data[:,2]/1000
k = data[:,4]
print(A.shape)


fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(projection='3d')
ax.set_xlim(-200,400)   #   Limite em x
ax.set_ylim(0,100)   #   Limite em y
ax.set_zlim(0,32)
ax.set_xlabel("$k_y (m^{-1})$") #   Nome do eixo y
ax.set_ylabel("$f (kHz)$") #   Nome do eixo y
ax.set_zlabel("$A (V)$") #   Nome do eixo y
ax.scatter(k[0:3], f[0:3], A[0:3], c = "black",alpha = 1,zorder = 1000)
ax.scatter(k[3], f[3], A[3], c = "red",alpha = 1,zorder = 1000)
ax.scatter(k[4:], f[4:], A[4:], c = "black",alpha = 1,zorder = 1000)

for i in range(0,len(A)):
    if i!= 3:
        c = "#555555"
    if i == 3:
        c = "#FF2222"
    ax.plot([k[i],k[i]],[f[i],f[i]],[0,A[i]-0.05], color = c,zorder = 300)

img = mp_img.imread("Espectro2.png")
img = np.rot90(img)
img = np.rot90(img)
img = np.rot90(img)
img = img[:,:,0:3]
print(np.max(img))


xx, yy = np.mgrid[0:img.shape[0], 0:img.shape[1]]

xx = xx*600/img.shape[0] - 200
yy = yy*100/img.shape[1]

zz = np.zeros((img.shape[0],img.shape[1]))


ax.plot_surface(xx, yy, zz ,rstride=2, cstride=2, facecolors=img,
        linewidth=0,zorder = 0, alpha = 1)


plt.show()
plt.close()





















#

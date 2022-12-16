import numpy as np
import matplotlib.pyplot as plt
import sys
import os

folder = sys.argv[1] # pasta com os dados
data_folder = sys.argv[1] + "/"



data = np.loadtxt(folder + "/" + folder + "_escape2.dat")
N = 1000
x = data[:,0]
y = data[:,1]
t = data[:,2]

xn = np.reshape(x,(N,N))
yn = np.reshape(y,(N,N))
tn = np.reshape(t,(N,N))


#x = xn[:,0]
#y = yn[0,:]
#yy, xx = np.meshgrid(y,x)


#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')
plt.rcParams["mathtext.fontset"] = "cm"

fig, ax = plt.subplots()
fig.set_size_inches(15*0.393, 6.5*0.393)
ax.set_xlim([-3.1415,3.1415])
ax.set_xlabel(r"$y$")
ax.set_xticks([-3.14,0,3.14])
ax.set_xticklabels([r'$-\pi$',r'0',r'$\pi$'])


ax.set_ylim([0.0,1.0])
ax.set_yticks([0,0.25,0.5,0.75,1.0])
#ax.set_xticklabels([r'$-\pi$',r'0',r'$\pi$'])
ax.set_ylabel(r"$x$")
plt.set_cmap("jet")
print("plotting")
p = ax.pcolormesh(yn,xn,np.log10(tn), shading = "nearest", vmin = 0,vmax = np.log10(500))

cbar_ax = fig.add_axes([0.92, 0.105, 0.025, 0.775])
fig.colorbar(p,label=r"$log_{10} (t)$", orientation="vertical", cax=cbar_ax)



plt.savefig(data_folder + folder + "_escape.png", bbox_inches = 'tight',dpi = 300)
plt.close()

os.system("pdftoppm -png -rx 600 -ry 600" + data_folder + folder + "_escape.pdf" + data_folder  + folder + "_escape")











plt.close()

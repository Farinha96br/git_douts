import numpy as np
import os
import sys
import matplotlib.pyplot as plt

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
plt.rcParams["mathtext.fontset"] = "cm" # isso é pra salvar as coisa em png com a fonte do latex

# Algumas paletas de cor p serem usadas (VSCode recomendado pra mostar as cores no editor de texto)
rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_darker = ['#007a96','#b39700','#b04bb0']




data_folder = sys.argv[1] + "/traj/"


data = []
for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        print(filename)
        #print(data_folder + filename)
        data.append(np.loadtxt(data_folder + filename))
data = np.array(data)
print(data.shape)   #data[partícula,linha,coluna de dados]





deltax = data[:,-1,1] - data[:,0,1] # all starting condition position o x
print("antes do corte: ",len(deltax))

deltax = deltax[np.abs(deltax) > np.pi/3]
print("depois do corte: ",len(deltax))

bins = np.linspace(0,200,100)

fig, ax = plt.subplots()
plt.tight_layout()
fig.set_size_inches(10*0.393, 5*0.393)
#ax.set_xlim(-25,25)
ax.set_xlabel(r"$\Delta x$")
ax.set_ylabel(r"$\#$")
#ax.set_yscale("log")

ax.hist(np.abs(deltax),bins = bins, color = rgb_pallet[2],histtype='stepfilled',edgecolor=rgb_darker[2], linewidth=0.25)
plt.savefig(sys.argv[1] + "/hist_all.png",bbox_inches='tight',dpi=300)
plt.close()






























#

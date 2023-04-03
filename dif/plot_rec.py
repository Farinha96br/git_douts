import numpy as np
import matplotlib.pyplot as plt
import sys
import os

rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_darker = ['#007a96','#b39700','#b04bb0']

import matplotlib.colors
cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("", [rgb_pallet[2],"black",rgb_pallet[0]])
cmap3 = matplotlib.colors.LinearSegmentedColormap.from_list("", ["#ffffff",rgb_darker[2]])

######

plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png

folder = sys.argv[1] # pasta com os dados
data_folder = sys.argv[1] + "/traj/"
os.makedirs(sys.argv[1] + "/rec",exist_ok=True)
eps = float(sys.argv[2])
Nplots = int(sys.argv[3])
counter = 0

for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        if counter < Nplots:
            fig, ax = plt.subplots()
            fig.set_size_inches(7*0.393, 7*0.393)
            ax.cla()
            data = np.loadtxt(data_folder + filename)
            print(filename)
            t = data[:,0]
            x = data[:,1]
            y = data[:,2]
            colors = data[:,0]

            xx1,xx2 = np.meshgrid(x,x)
            xx = (xx1 -xx2)**2

            yy1,yy2 = np.meshgrid(y,y)
            yy = yy1 -yy2
            yy = np.fmod(yy,3.1415)
            yy = yy**2


            M = np.sqrt(xx + yy)


            ts = np.arange(0,len(t),1)
            tt1,tt2 = np.meshgrid(t,t)
            
            #plt.title(filename)
            
            

            ax1 = ax.pcolormesh(tt1,tt2,M,cmap=cmap3)
            plt.colorbar(ax1,label = r"$d$")
            ax.set_xlabel(r"$\tau$")
            ax.set_ylabel(r"$\tau'$")


            plt.savefig(sys.argv[1] + "/rec/rec_" + filename[0:-4] + ".png", bbox_inches='tight',dpi =300)
            counter += 1
            plt.close()

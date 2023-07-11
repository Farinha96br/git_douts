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



folder = sys.argv[1] # pasta com todas as pastas
vars = np.array([])

folders = sorted(os.listdir(folder))
rootname = sys.argv[2] # nome comum a todos ATE O p0.000 ou n0.0000 como data-coisoA2_


bins = np.linspace(0,200,100)
hist = np.zeros(len(bins)-1)
hists = []


vars = np.array([])
# loop das pastas
for f in folders:
    if f.startswith(rootname):
        # loop dos arquivos
        var = f
        print(var)
        var = var.replace(rootname,"")
        print(var)
        var = var.replace("p","+")
        print(var)
        var = var.replace("n","-")
        print(var)

        trajfolder = f + "/traj/"
        data = []
        vars = np.append(vars,float(var))
        c = 0
        if c < 30:
            for filename in sorted(os.listdir(trajfolder)):
                if filename.endswith(".dat"):
                    print("pasta:",f,"arquivo:",filename)
                    #print(data_folder + filename)
                    data.append(np.loadtxt(trajfolder + filename))
                    #print(data.shape)
                    c +=1
        data = np.array(data)
        print("whole traj data shape",data.shape)

        #data tem o formato data[particula,tempo,coluna de dados]
        deltax = np.abs(data[:,-1,1] - data[:,0,1]) # all starting condition position o x
        
        #print("antes do corte: ",len(deltax))
        #deltax = deltax[np.abs(deltax) > np.pi/3]
        #print("depois do corte: ",len(deltax))

        hist, _ = np.histogram(deltax,bins=bins)

        hists.append(hist)
        print("bins shape",bins.shape)
        print("histogram shape",hist.shape)
        print("histograms shape",np.array(hists).shape)
        # formato do hists hists[var,counts]

        #temp_hist = np.histogram(deltax,bins = bins) 
        #hists = np.append(hists,temp_hist)
print("---  ALL LOADED  ---")

hists = np.array(hists)
print("vars shape",vars.shape)
print("bins shape",bins.shape)
print("histogram shape",hist.shape)
print("histograms shape",hists.shape)

bins2,vars2 = np.meshgrid(bins,vars)

print("bins2 shp",bins2.shape)
print("vars2 shp",vars2.shape)

fig, ax = plt.subplots()
plt.tight_layout()
fig.set_size_inches(10*0.393, 10*0.393)
#ax.set_xlim(-25,25)
ax.set_xlabel(r"$\Delta x$")
ax.set_ylabel(r"$A_2$")
#ax.set_yscale("log")

ax.pcolormesh(bins2,vars2,hists,cmap = "jet")
plt.show()
plt.close()

































#

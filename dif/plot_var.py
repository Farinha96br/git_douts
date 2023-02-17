import numpy as np
import matplotlib.pyplot as plt
import sys
import os

plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=True) # esse vc deixa True e for salvar em pdf e False se for p salvar png


folder = sys.argv[1] # pasta com os dados

D = np.array([])
vars = np.array([])

folders = sorted(os.listdir(sys.argv[1]))

for f in folders:
    if f.startswith("data-dif_w2_"):
        for file in sorted(os.listdir(f)):
            if file.startswith("D_"):
                var = file
                var = var.replace("D_data-dif_A2_","").replace("p","+").replace(".dat","")
                var = var.replace("D_data-dif_A2_","").replace("n","-").replace(".dat","")
                var = float(var)
                vars = np.append(vars,var)
                print(file,var)

                temp_data = np.loadtxt(f + "/" + file)
                D = np.append(D,temp_data[-1,1])




rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_pallet = ['#007a96','#b39700','#b04bb0']
######


fig, ax = plt.subplots()
plt.tight_layout() # isso aq nsei bem qq faz mas ajuda a deixar menos espaço em branco
fig.set_size_inches(6*0.393, 4*0.393) # esse fatir 0.393 é p converter polegadas p cm
ax.set_ylabel(r"$\langle D_x(t_f) \rangle$") # Legenda, p renderizar direito precisa do r"$blablabla$"
ax.set_xlabel(r"\omega_2")
ax.set_xlim(-1.2,1.2)
ax.set_yscale("log")

cores = ["royalblue","firebrick","forestgreen"] # alguma cores q eu gosto, RGB nao tao saturadao
ax.plot(vars,D,linewidth = 0.0,marker = ",",markersize = 0.5, c = rgb_pallet[2])

#ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0)) # coloca em notação científica
ax.legend(frameon=False)

plt.savefig("w_D.pdf",bbox_inches='tight') ## salva como pdf

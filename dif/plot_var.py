import numpy as np
import matplotlib.pyplot as plt
import sys
import os

rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_pallet = ['#007a96','#b39700','#b04bb0']
######

plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=True) # esse vc deixa True e for salvar em pdf e False se for p salvar png




figdif, axdif = plt.subplots()

figdif.set_size_inches(6*0.393, 4*0.393) # esse fatir 0.393 é p converter polegadas p cm
axdif.set_ylabel(r"$\langle D_x(t_f) \rangle$") # Legenda, p renderizar direito precisa do r"$blablabla$"
axdif.set_xlabel(r"$t$")
axdif.set_title(r"All $D_x(t)$")
axdif.set_ylim(0,0.01)


folder = sys.argv[1] # pasta com os dados
D = np.array([])
vars = np.array([])

folders = sorted(os.listdir(sys.argv[1]))

colors = plt.cm.jet(np.linspace(0,1,120))
i = 0
for f in folders:
    if f.startswith("data-diflong_w2_"):
        for file in sorted(os.listdir(f)):
            if file.startswith("D_"):
                var = file
                temp_data = np.loadtxt(f + "/" + file)
                D = np.append(D,temp_data[-1,1])

                p = axdif.plot(temp_data[:,0],temp_data[:,1],linewidth = 0.2,alpha = 0.5, color = colors[i])
                var = var.replace("D_data-dif_w2_","").replace("p","+").replace(".dat","")
                var = var.replace("D_data-dif_w2_","").replace("n","-").replace(".dat","")
                var = float(var)
                vars = np.append(vars,var)
                print(file,var)
                i += 1

figdif.colorbar(colors)

plt.savefig("t_Ds.pdf",bbox_inches='tight') ## salva como pdf
plt.close()



#sorted_index = vars.argsort()
#print(sorted_index)
#D = D[sorted_index]
#vars = vars[sorted_index]

print(vars)
print(D)




fig, ax = plt.subplots()
fig.set_size_inches(6*0.393, 4*0.393) # esse fatir 0.393 é p converter polegadas p cm
ax.set_ylabel(r"$\langle D_x(t_f) \rangle$") # Legenda, p renderizar direito precisa do r"$blablabla$"
ax.set_xlabel(r"$\omega_2$")
ax.set_title(r"$\omega_1=6$")
ax.set_xticks(np.arange(6,32,3))
#ax.set_xlim(-1.2,1.2)
#ax.set_yscale("log")

cores = ["royalblue","firebrick","forestgreen"] # alguma cores q eu gosto, RGB nao tao saturadao
ax.plot(vars,D,linewidth = 1,marker = ",",markersize = 0.5, c = rgb_pallet[2])

#ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0)) # coloca em notação científica
ax.legend(frameon=False)

plt.savefig("w_D.pdf",bbox_inches='tight') ## salva como pdf

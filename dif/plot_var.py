import numpy as np
import matplotlib.pyplot as plt
import sys
import os

plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=True) # esse vc deixa True e for salvar em pdf e False se for p salvar png


folder = sys.argv[1] # pasta com os dados

data_all = np.array([])
vars = np.array([])
for filename in sorted(os.listdir(folder)):
    if filename.endswith(".dat"):
        print(filename[11:-4])
        var = filename[11:-4]
        vars = np.append(vars,float(var))
        data = np.loadtxt(folder + "/" + filename)
        data_all = np.append(data_all,data[-1,1])


print(data_all)
fig, ax = plt.subplots()
plt.tight_layout() # isso aq nsei bem qq faz mas ajuda a deixar menos espaço em branco
fig.set_size_inches(6*0.393, 4*0.393) # esse fatir 0.393 é p converter polegadas p cm
ax.set_ylabel(r"$\langle D_x(t_f) \rangle$") # Legenda, p renderizar direito precisa do r"$blablabla$"
ax.set_xlabel(r"factor")
#ax.set_xlim(-1.5,1.5)

cores = ["royalblue","firebrick","forestgreen"] # alguma cores q eu gosto, RGB nao tao saturadao
ax.plot(vars,data_all,linewidth = 0.5,marker = ",",markersize = 0.5, c = "royalblue")

ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0)) # coloca em notação científica
ax.legend(frameon=False)

plt.savefig("A3.pdf",bbox_inches='tight') ## salva como pdf

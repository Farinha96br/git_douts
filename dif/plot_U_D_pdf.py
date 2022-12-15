import numpy as np
import matplotlib.pyplot as plt
import sys




all1 = np.loadtxt("U_D_exp_0.dat")
all2 = np.loadtxt("U_D_exp_r.dat")

# Coisos pra salvar a figura usando latex
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

fig, ax = plt.subplots()
plt.tight_layout()
fig.set_size_inches(1*0.393, 1*0.393)
ax.set_yscale("log")
ax.set_ylim(0.0001,0.1)
ax.set_ylabel(r"$\langle D_x(t_f) \rangle$")
ax.set_xlabel("U")
ax.set_xlim(-1.5,1.5)
ax.plot(all1[:,0],all1[:,1],marker = "o",linewidth = 1,markersize = 1.5, c = "firebrick", label = "Em fase")
ax.plot(all2[:,0],all2[:,1],marker = "^",linewidth = 1,markersize = 1.5, c = "limegreen", label = "Fases aleatórias")
ax.legend(frameon=False)


#plt.savefig("exp_U_D.pgf",format='pgf')
plt.savefig("exp_U_D.pdf",bbox_inches='tight')

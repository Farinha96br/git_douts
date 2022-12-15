import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit

def plaw(t,gamma,c):
    return c*(t**gamma)


folder = sys.argv[1] # pasta com os dados

data = np.loadtxt(folder + "/D_" + folder + ".dat")

t = data[:,0]
D = data[:,1]
C = data[:,2]
Cov = data[:,3]

# plotando a difusão
fig, ax = plt.subplots()
fig.set_size_inches(10*0.393, 5*0.393)
#ax.set_yscale("log")
#ax.set_ylim(0,0.2)
ax.set_ylabel(r"$\langle D_x(t) \rangle$")
ax.set_xlabel("$t$")
#ax.set_xlim(0,1000)
ax.plot(t,D,linewidth = 1, c = "royalblue")
#ax.plot(all2[:,0],all2[:,1],linewidth = 1, c = "firebrick", label = "Fases aleatórias")
#ax.legend(frameon=False)
#plt.savefig("exp_U_D.pgf",format='pgf')
plt.savefig(folder + "/" + folder + "_t_D.pdf",bbox_inches='tight')
plt.close()

popt, pcov = curve_fit(plaw,t,C)

print("fit da funcao C*(t**gamma)")
print("gamma","C")
print(popt[0],popt[1])

fig, ax = plt.subplots()
fig.set_size_inches(10*0.393, 5*0.393)
#ax.set_yscale("log")
#ax.set_xscale("log")
#ax.set_title(r"$A^{\gamma t}$, $A = " + strpopt[0] +   " $, $ \gamma = " + strgamma1  + " $" )
ax.set_ylabel(r"$\langle \sigma_x (t) \rangle$")
ax.set_xlabel(r"$t$")
#ax.set_xlim(0,1000)
#ax.set_ylim(0,120)
ax.plot(t,C, c = "royalblue", linewidth = 1)
ax.plot(t,plaw(t,popt[0],popt[1]), c = "firebrick", linewidth = 1)
plt.savefig(folder + "/" + folder + "_t_sigma.pdf",bbox_inches='tight')
plt.close()

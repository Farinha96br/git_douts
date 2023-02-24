import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit

rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_darker = ['#007a96','#b39700','#b04bb0']

def plaw(t,gamma,c):
    return c*(t**gamma)


folder = sys.argv[1] # pasta com os dados

data = np.loadtxt(folder + "/D_" + folder + ".dat")

t = data[:,0]
D = data[:,1]

# plotando a difusão
fig, ax = plt.subplots()
fig.set_size_inches(10*0.393, 5*0.393)
#ax.set_yscale("log")
#ax.set_ylim(0,D[-1]*10)
ax.set_ylabel(r"$\langle D_x(t) \rangle$")
ax.set_xlabel("$t$")
ax.set_ylim(0,0.01)
ax.plot(t,D,linewidth = 0.5, c = rgb_pallet[2])
ax.axhline(0,color = "gray", ls="--", lw = 0.25)
#ax.plot(all2[:,0],all2[:,1],linewidth = 1, c = "firebrick", label = "Fases aleatórias")
#ax.legend(frameon=False)
#plt.savefig("exp_U_D.pgf",format='pgf')
ax.set_title(r"$D_x(t_f) = $" + str(D[-1]))
plt.savefig(folder + "/" + folder + "_t_D.pdf",bbox_inches='tight')
plt.close()


C = data[:,2]
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
ax.plot(t,plaw(t,popt[0],popt[1]), c = "firebrick", linewidth = 0.5)
plt.savefig(folder + "/" + folder + "_t_sigma.pdf",bbox_inches='tight')
plt.close()

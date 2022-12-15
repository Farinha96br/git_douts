import numpy as np
import matplotlib.pyplot as plt
import sys

folder = sys.argv[1] # pasta com os dados

data = np.loadtxt(folder + "/D_" + folder + ".dat")

t = data[:,0]
D = data[:,1]
C = data[:,2]
Cov = data[:,3]

# plotando a difusão
fig, ax = plt.subplots()
#ax.set_yscale('log')
#plt.title("Coef. de difusão")
fig.set_size_inches(10, 5)
ax.set_ylim([0,D[-1]*6])
ax.set_ylabel("$<D_x>$")
ax.set_xlabel("Normalized time")
ax.plot(t,D, c = "black", linewidth = 1)
plt.savefig(sys.argv[1] + "/Dif.png", dpi = 600)
plt.close()

# plotando o desvio quadrático
alpha, beta = np.polyfit(t, C, 1)

fig, ax = plt.subplots()
#plt.title("<σ²> \n" + "β = " + str(beta) + "\n α = " + str(alpha))
plt.tight_layout()
fig.set_size_inches(10, 5)
ax.set_yscale("log")
ax.set_ylabel("<σ²>")
ax.set_xlabel("Normalized time")
#ax.set_xlim(0,1000)
ax.plot(t,C, c = "black", linewidth = 0.7, label = "Numerical data")
#ax.plot(t,alpha*beta, c = "red", linewidth = 1.2, ls = "--",label = "Linear regression")

props = dict(boxstyle='square', facecolor='white', alpha=0.5)

ax.text(0.8, 0.2, "a = " + str(round(beta,4)) + "\n b = " + str(round(alpha,4)), transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)
ax.legend()

plt.savefig(sys.argv[1] + "/Dev.png", dpi = 600)
plt.close()

import numpy as np
import os
import sys
import matplotlib.pyplot as plt

rgb_light =  ['#ce5825','#2e9a60','#6182e2']
rgb_pallet = ['#cd4100','#007148','#4169E1']
rgb_darker = ['#9e3000','#005738','#304ea6']

cym_light =  ['#82e7ff','#fde974','#ff98ff']
cym_pallet = ['#00ceff','#ffd700','#ff6dff']
cym_pallet = ['#007a96','#b39700','#b04bb0']



#####
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=True) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######
fig, ax = plt.subplots(2,2)
fig.set_size_inches(20*0.393, 10*0.393) # o valor multiplicando é o tamanho em cm
plt.subplots_adjust(hspace=0.5)

#ax.set_title(filename)





def pdf(x,a):
    return a*np.exp(-1*a*x)

def cdf(x,a):
    return 1 - np.exp(-1*a*x)

def icdf(x,a):
    return -1*np.log(1-x)/a


x1 = np.linspace(0.0001,0.99999999,500)
x10 = np.linspace(0.0001,9.9999999,500)



# PDF
ax[0,0].set_xlim(0,10)
ax[0,0].set_ylim(0,3)
ax[0,0].set_title("PDF")
ax[0,0].set_xlabel(r"$x$",labelpad = -3)
ax[0,0].set_ylabel(r"$P(x)$")
ax[0,0].plot(x10,pdf(x10,0.5),linewidth = 1, color = rgb_pallet[0], label = "a=0.5")
ax[0,0].plot(x10,pdf(x10,1),linewidth = 1, color = rgb_pallet[1], label = "a=1.5")
ax[0,0].plot(x10,pdf(x10,3),linewidth = 1, color = rgb_pallet[2], label = "a=3.0")
ax[0,0].legend(frameon=False)
#plt.savefig("pdf.pdf",bbox_inches='tight')


# CDF
ax[0,1].set_title("CDF")
ax[0,1].set_xlabel(r"$x$",labelpad = -3)
ax[0,1].set_ylabel(r"$C(x)$")
ax[0,1].plot(x10,cdf(x10,0.5),linewidth = 1, color = rgb_pallet[0], label = "a=0.5")
ax[0,1].plot(x10,cdf(x10,1),linewidth = 1, color = rgb_pallet[1], label = "a=1.5")
ax[0,1].plot(x10,cdf(x10,3),linewidth = 1, color = rgb_pallet[2], label = "a=3.0")
ax[0,1].legend(frameon=False)
#plt.savefig("cdf.pdf",bbox_inches='tight')
#ax.cla()


# ICDF
ax[1,0].set_title("ICDF")
ax[1,0].set_xlabel(r"$x$",labelpad = -2)
ax[1,0].set_ylabel(r"$P^{-1}(x)$")
ax[1,0].set_xlim(0,1)
ax[1,0].set_ylim(0,3)
ax[1,0].plot(x1,icdf(x1,0.5),linewidth = 1, color = rgb_pallet[0], label = "a=0.5")
ax[1,0].plot(x1,icdf(x1,1),linewidth = 1, color = rgb_pallet[1], label = "a=1.5")
ax[1,0].plot(x1,icdf(x1,3),linewidth = 1, color = rgb_pallet[2], label = "a=3.0")
ax[1,0].legend(frameon=False)
#plt.savefig("icdf.pdf",bbox_inches='tight')
#ax.cla()

ax[1,1].set_title("Comparison")
ax[1,1].set_xlabel(r"$x$",labelpad = -2)
ax[1,1].set_ylabel(r"$f(x)$")
ax[1,1].set_xlim(0,3)
ax[1,1].set_ylim(0,3)
ax[1,1].plot(x10,cdf(x10,3),linewidth = 1, color = rgb_pallet[2], label = "CDF")
ax[1,1].plot(x1,icdf(x1,3),linewidth = 1, color = rgb_pallet[0], label = r"CDF$^{-1}$")
ax[1,1].plot(np.linspace(-3,3,2),np.linspace(-3,3,2),linewidth = 1, color = '#999999',alpha = 0.5)
ax[1,1].legend(frameon=False)
plt.savefig("ICDF_test.pdf",bbox_inches='tight')










plt.close()

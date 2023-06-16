import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.colors


######
plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=False) # esse vc deixa True e for salvar em pdf e False se for p salvar png
######
fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm



files = os.listdir("data/")

for f in files:
    data = np.loadtxt("data/" + f)
    ax.pcolormesh(data,cmap = "plasma", vmax=1)
    plt.savefig("plots/" + f[:-4] + ".png",bbox_inches='tight',dpi = 300) # salva em png
    ax.cla()

plt.close()
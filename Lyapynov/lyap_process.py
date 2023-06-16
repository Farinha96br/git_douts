import numpy as np
import matplotlib.pyplot as plt
import sys
import os

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

folder = sys.argv[1] # pasta com os dados
data_folder = sys.argv[1] + "/traj/"


fig, ax = plt.subplots()
fig.set_size_inches(7*0.393, 5*0.393)

ls = []
As = []
for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        data = np.loadtxt(data_folder + filename)
        print(filename)
        ls.append(data[-1,5])
        As.append(0.1)

            

print(ls)
print(np.sum(ls)/len(ls))
ax.plot(As,ls, marker = ",", ls="", color = rgb_pallet[2])
plt.savefig(sys.argv[1] + "/" + sys.argv[1] + "_lyap.png", bbox_inches='tight',dpi =300)
plt.close()


import numpy as np
import matplotlib.pyplot as plt
import sys
import os

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
plt.rcParams["mathtext.fontset"] = "cm" # isso é pra salvar as coisa em png com a fonte do latex


folder = sys.argv[1] # pasta com os dados
data_folder = sys.argv[1] + "/traj/"
os.makedirs(sys.argv[1] + "/cell_pos",exist_ok=True)
Nplots = int(sys.argv[2])
k = 3
cell = np.pi/k
counter = 0

def get_cell(x,y,cellx,celly):
    cell_i = np.zeros(len(x))

    
    cell_1 = (x <= cellx and y <= celly)
    cell_2 = (x <= cellx and y > celly)
    cell_3 = (x > cellx and y > celly)
    cell_4 = (x > cellx and y <= celly)
    cell_i[cell_1] = 1
    cell_i[cell_2] = 2
    cell_i[cell_3] = 3
    cell_i[cell_4] = 4
    return cell_i
    




for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        if counter < Nplots:
            data = np.loadtxt(data_folder + filename)
            print(filename)
            t = data[:0]
            x = data[:,1]
            x = x%(2*np.pi/k)
            y = data[:,2]
            y = y%(2*np.pi/k)
            cell_i = get_cell(x,y,cell,cell)

            fig, ax = plt.subplots()
            plt.tight_layout()
            fig.set_size_inches(8*0.393, 5*0.393)
          
            ax.set_ylabel("cell index")
            ax.set_xlabel("$t$")
            for i in range(0,4):
                ax.axhline(i,color = "#999999",ls = "--",zorder = 0)

            p = ax.plot(t,cell_i,linewidth = 0.5, zorder = 1)

            plt.savefig(sys.argv[1] + "/cell_pos/" + filename[0:-4] + ".png", bbox_inches='tight',dpi =300)
            plt.close()
            counter += 1
        else:
            break

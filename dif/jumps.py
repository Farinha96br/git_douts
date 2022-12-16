import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import scipy.signal as scipy

plt.rcParams["mathtext.fontset"] = "cm" # Fonte matemática pro latex
plt.rc('font', family='serif') # fonte tipo serif, p fica paredico com latex msm
plt.rc('text', usetex=True) # esse vc deixa True e for salvar em pdf e False se for p salvar png



data = []

data_folder = sys.argv[1] + "/traj/"
out_folder = sys.argv[1] + "/jumps/"

os.makedirs(out_folder,exist_ok=True)

#ky = 55.555
#kx = 104.719 # duas ondas
#kx = 86.4225 # experimental
#a = 0.18

ky = 6
kx = 12
a = 1

cellx = 3.14159265359/(kx*a)

print("cellx:",cellx)

jumps_x = np.array([])
jumps_y = np.array([])

jumps_all = np.array([])
c = 0
for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        print(filename)
        jumps = np.array([])
        jumps_index = np.array([])

        data = np.loadtxt(data_folder + filename)
        t= data[:,0]
        x= data[:,1]
        y= data[:,2]
        dt = data[1,0] - data[1,0]

        peaks, _ = scipy.find_peaks(x)
        valleys, _ = scipy.find_peaks(-1*x)
        extrema = np.hstack((peaks,valleys)) # indices dos pontos extremas
        extrema = sorted(extrema) # organiza os pontos extremos
        #jumps = np.diff(x[extrema]) # extremos de x em cada indica extrema

        for i in range(0,len(extrema)-1):
            d = abs(x[extrema[i]] - x[extrema[i+1]])
            if d >= cellx*2.5:
                index = extrema[i]
                jumps = np.append(jumps,d)
                jumps_index = np.append(jumps_index,index)

                jumps_x = np.append(jumps_x,x[i])
                jumps_y = np.append(jumps_y,y[i])


                

        jumps_index = jumps_index.astype(int)
        jumps_all = np.append(jumps_all,jumps)


        # Plotting some trajectories to see if the detection works
        if c < 30:
            fig, ax = plt.subplots()
            plt.tight_layout()
            fig.set_size_inches(10*0.393, 5*0.393)
            #ax.set_title(filename)
            ax.set_xlim(0,100)
            ax.set_xlabel(r"$t$")

            NCELL = 16
            for j in range(0,NCELL):
                ax.axhline(cellx*j, linewidth = 0.25, linestyle = "--", color = "#cccccc",zorder = 0)
            #ax.axhline(1, linewidth = 0.5, linestyle = "--", color = "#555555",zorder = 0)

            ax.set_ylim(-0.05,cellx*NCELL)
            ax.set_ylabel(r"$x$")
            ticksy = np.arange(0,cellx*NCELL,2*cellx)
            ax.set_yticks(ticksy)
            ax.set_yticklabels(np.arange(0,NCELL,2))
            ax.set_ylabel(r"$\frac{N\pi}{k_{x4}}$")
            ax.plot(t,x,linewidth = 0.5, color = "royalblue",zorder = 1)
            ax.plot(t[extrema],x[extrema],ls = " ", marker = ",",markersize = 0.5, color = "firebrick",zorder = 2)
            ax.plot(t[jumps_index],x[jumps_index],ls = " ",markersize = 1, marker = "s", color = "forestgreen",zorder = 3)
            plt.savefig(out_folder + filename[:-4] + ".pdf",bbox_inches='tight')
            plt.close()
            c+=1




print("escrevendo arquivo")
f = open(sys.argv[1] + "/jumps_data.dat","w")
for i in range(0,len(jumps_all)):
    f.write(str(jumps_x[i]) + "\t" + str(jumps_y[i]) + "\t" + str(jumps_all[i]) + "\n")
f.close()


# Plotting the jump histogram

data = np.loadtxt(sys.argv[1] + "/jumps_data.dat")
hist_data = data[:,2]

fig, ax = plt.subplots()
plt.tight_layout()
fig.set_size_inches(10*0.393, 5*0.393)

ax.set_xlim(cellx,cellx*16)

for i in range(0,16):
    ax.axvline(cellx*i, linewidth = 0.25, linestyle = "--", color = "#cccccc",zorder = 0)

ax.set_xticks(np.arange(cellx,cellx*16,cellx*2))
ax.set_xticklabels(np.arange(1,16,2))
ax.set_xlabel(r"$\Delta \frac{N\pi}{k_{x0}}$")


ax.set_ylabel("\# Pulos")
ax.hist(hist_data,bins = 200, color = "royalblue",zorder = 1)
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.savefig(sys.argv[1] + "/jump_hist.pdf",bbox_inches='tight')

plt.close()

# Plotting the places where the jumps happen

fig, ax = plt.subplots()
plt.tight_layout()
fig.set_size_inches(6*0.393, 6*0.393)
#ax.set_ylim(-3.1415,3.1415)
#ax.set_xlim(0,3)
ax.axhline(1, linewidth = 0.35, linestyle = "--", color = "#cccccc",zorder = 0)

ax.scatter(data[:,1],data[:,0],data[:,2],alpha=0.5)
plt.savefig(sys.argv[1] + "/jump_pos.pdf",bbox_inches='tight')









#

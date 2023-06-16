import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def plaw(t,gamma,c):
    return c*(t**gamma)



data = []
data_folder = sys.argv[1] + "/traj/"
c = 0
for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        print(filename)
        #print(data_folder + filename)
        data.append(np.loadtxt(data_folder + filename))
        c+= 1
data = np.array(data)

print("Raw data",data.shape)   #data[partícula,linha,coluna de dados]
                    # coluna de dados
                    # data[1,:,0] pega todos
#print(data[0,:,1])
#print(data[0,0,1]) # pos inicial
#print(data[0,-1,1]) # pos final
x0 = data[0,:,1] # todas posições x da 1a particula
tf = data[0,-1,0]



folder = sys.argv[1]

f = open(folder + "/convergence.dat", "w")
f.write("Ntau   N   gamma   errorgamma\n" )




for Nlim in range(50,5000,50):
    for tlim in range(50,5000,50):
        ts = data[0,:tlim,0]
        xs = data[0:Nlim,0:tlim,1]
        #print(xs.shape)
        msd = np.sum(xs**2,axis=0)/Nlim
        #print(msd.shape)

        popt, pcov = curve_fit(plaw,ts,msd) #popt[0] é gamma 
        perr = np.diag(pcov)[0] # pcov eh a matrix covariancia, com os erros na diagonal

        f.write(str(tlim) + "\t" + str(Nlim) + "\t" + str(popt[0]) + "\t" + str(perr)  + "\n")
        print(str(tlim) + "\t" + str(Nlim) + "\t" + str(popt[0]) + "\t" + str(perr)  + "\n" )

f.close()
print(data_folder)


















#

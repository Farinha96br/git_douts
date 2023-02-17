import numpy as np
import os
import sys
import matplotlib.pyplot as plt

def linfit(X,Y):
    N = len(X)
    Sx = np.sum(X)
    Sy = np.sum(Y)
    Sxx = np.sum(X*X)
    Syy = np.sum(Y*Y)
    Sxy = np.sum(X*Y)
    beta = (N*Sxy - Sx*Sy)/(N*Sxx-Sx*Sx)
    alpha = Sy/N - beta*Sx/N
    return beta, alpha




data = []
data_folder = sys.argv[1] + "/traj/"
for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".dat"):
        print(filename)
        data.append(np.loadtxt(data_folder + filename))
data = np.array(data)
print(data.shape)   #data[partícula,linha,coluna de dados]
                    # coluna de dados
                    # data[1,:,0] pega todos
#print(data[0,:,1])
#print(data[0,0,1]) # pos inicial
#print(data[0,-1,1]) # pos final
x0 = data[0,:,1] # todas posições x da 1a particula
tf = data[0,-1,0]

N = data.shape[0] # Número de partículas

dif_file = sys.argv[1] + "/D_" +  sys.argv[1]  +".dat"

f = open(dif_file, "w")
for t in range(1,data.shape[1]):
    D = 0
    x0s = data[:,0,1]
    xfs = data[:,t,1]
    D = np.sum((xfs-x0s)**2)

    C = D/N
    D = D/(2*N*data[0,t,0])

    # covariancia
    C1 = np.sum((xfs-x0s)*(xfs-x0s))/N
    C2 = (np.sum((xfs-x0s)/N))**2
    Cov = C1 - C2
    f.write(str(data[0,t,0]) + "\t" + str(D) + "\t" + str(C) + "\t" + str(Cov) + "\n")

f.close()
print(sys.argv[1].replace("-","n"),D)
data = None
# Regressão e plotagens:


















#

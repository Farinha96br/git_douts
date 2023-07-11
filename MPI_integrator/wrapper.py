import numpy as np
import matplotlib.pyplot as plt
import os
import time


#os.system("rm  x.dat")
#os.system("rm  y.dat")

program = "integrator_mpi2.cpp"                    # Nome de programa
os.system("mpic++ -lm " + program)        # Compila
its = 100                              # Numero de iteracoes
var = 0.16                               # variavel que estou mexendo
folder = "data-teste"                        # nome da pasta de saida
Npar = 8                               # Numero de runs paralelas
Nstarts = 128*128                       # Numero de cond. iniciais (Conferir no programa em sí!!!)
# faz a pasta onde vai ter os roles
os.makedirs(folder,exist_ok=True)

Nfull = int(Nstarts/Npar)
print("Nfull",Nfull)
Nleft = Nstarts - Nfull*Npar 
print("Nleft",Nleft)

times = np.array([])
for i in range(0,Nfull):
    s0 = time.time()
    L0 = i*Npar
    print()
    runstring = "mpirun -np " + str(Npar)  + " ./a.out " + str(L0) + " " + str(its) + " " + str(var) + " " + folder
    print(runstring)
    os.system(runstring)
    times = np.append(times,time.time() - s0)
    avg = np.sum(times/len(times))
    print(i,"/",Nfull,"expected runtime:" , avg*(Nfull+Nleft)/(60*60)," h")
if Nstarts%Npar != 0:
    L0 = Nfull*Npar
    runstring = "mpirun -np " + str(Nleft) + " ./a.out " + str(L0) + " " + str(its) + " " + str(var) + " " + folder
    print(runstring)
    os.system(runstring)




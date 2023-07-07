import numpy as np
import matplotlib.pyplot as plt
import os



#os.system("rm  x.dat")
#os.system("rm  y.dat")

program = "mpi7.cpp"                    # Nome de programa
os.system("mpic++ -lm mpi7.cpp")        # Compila
its = 100                              # Numero de iteracoes
var = 0.16                               # variavel que estou mexendo
folder = "data-teste2"                        # nome da pasta de saida
Npar = 8                               # Numero de runs paralelas
Nstarts = 128*128                       # Numero de cond. iniciais (Conferir no programa em sí)


os.makedirs(folder,exist_ok=True)

Nfull = int(Nstarts/Npar)
print("Nfull",Nfull)
Nleft = Nstarts - Nfull*Npar 
print("Nleft",Nleft)
for i in range(0,Nfull):
    L0 = i*Npar
    print(i,"/",Nfull)
    runstring = "mpirun -np " + str(Npar)  + " ./a.out " + str(L0) + " " + str(its) + " " + str(var) + " " + folder
    print(runstring)
    os.system(runstring)
if Nstarts%Npar != 0:
    L0 = Nfull*Npar
    runstring = "mpirun -np " + str(Nleft) + " ./a.out " + str(L0) + " " + str(its) + " " + str(var) + " " + folder
    print(runstring)
    os.system(runstring)




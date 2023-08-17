import numpy as np
import matplotlib.pyplot as plt
import os
import time




program = "integrator_mpi.cpp"                    # Nome de programa
os.system("mpic++ -O3 " + program + " -lm -lgsl")        # Compila
rootname = "data-mm_pi4_A2"
its = 5000                              # Numero de iteracoes
Npar = 8                               # Numero de runs paralelas
Nstarts = 8*8                      # Numero de cond. iniciais (Conferir no programa em sí!!!)
scase = 0 # 1 => pontos aleatorios, 2 => grid definido do programa, 2 => le um arquivo especificado
sfile = "start.dat"
# faz a pasta onde vai ter os roles


Nfull = int(Nstarts/Npar)
Nleft = Nstarts - Nfull*Npar 

print("Nleft:",Nleft,"Nfull",Nfull)
vars = [0.16]
for var_i in range(0,len(vars)):
    svar = "{:.3f}".format(vars[var_i])
    folder = rootname + "_" + svar
    os.makedirs(folder,exist_ok=True)
    times = np.array([])
    for i in range(0,Nfull):
        s0 = time.time()
        L0 = i*Npar
        print()
        runstring = "mpirun -np " + str(Npar)  + " ./a.out " + str(scase) + " " +  str(L0) + " " + str(its) + " " + str(vars[var_i]) + " " + sfile + " " + folder
        #print(runstring)
        os.system(runstring)
        times = np.append(times,time.time() - s0)
        avg = np.sum(times/len(times))
        print(i,"/",Nfull,"expected runtime:" , avg*(Nfull+Nleft)/(60*60)," h")

    if Nstarts%Npar != 0:
        L0 = Nfull*Npar
        runstring = "mpirun -np " + str(Nleft) + " ./a.out " + str(scase) + " " +  str(L0) + " " + str(its) + " " + str(vars[var_i]) + " " + sfile + " " + folder
        #print(runstring)
        os.system(runstring)




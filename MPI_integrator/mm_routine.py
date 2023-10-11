import numpy as np
import matplotlib.pyplot as plt
import os
import time




program = "integrator_mpi.cpp"                    # Nome de programa
os.system("mpic++ -O3 " + program + " -lm -lgsl")        # Compila
rootname = "data-paramspace/phas_A2"
its = 10000                              # Numero de iteracoes
Npar = 8                               # Numero de runs paralelas

scase = 0 # 0 => grid definido (configurar no program), 1 => pontos aleatorios, 2 => le um arquivo especificado
Nstarts = 9*9                      # Numero de cond. iniciais (Conferir no programa em sí!!!)
sfile = "dummy.dat"

if scase == 2:
    Nstarts = len(np.loadtxt(sfile)[:,0])
    print(Nstarts)

# Roda pra obter o mapa em sí
Nfull = int(Nstarts/Npar)
Nleft = Nstarts - Nfull*Npar 

print("Nleft:",Nleft,"Nfull",Nfull)
vars = [np.pi/4,np.pi/2]
vars2 = [0.16,0.2]

for var_i in range(0,len(vars)):
    for var2_i in range(0,len(var2_i))
        svar = "{:07.5f}".format(vars[var_i])
        svar2 = "{:07.5f}".format(vars[var_i])
        folder = rootname + "_" + svar + "_" + svar2
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
        
        os.system("python3 mm.py " + folder)
        #os.system("python3 plot_disp.py " + folder)
        
    #os.system("shutdown")
    #roda p testar os pontos


scase = 2

for var_i in range(0,len(vars)):
    svar = "{:07.5f}".format(vars[var_i])
    svar2 = "{:07.5f}".format(vars[var_i])
    folder = rootname + "_" + svar + "_" + svar2
    os.makedirs(folder,exist_ok=True)
    sfile = folder + "/testpoints.dat"
    starts = np.loadtxt(sfile)
    if starts.shape == (2,):
        Nstarts = 1
    else:
        Nstarts = len(starts[:,0])
  
    print(folder)

    Nfull = int(Nstarts/Npar)
    Nleft = Nstarts - Nfull*Npar 
    print("Nleft:",Nleft,"Nfull",Nfull)
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

    os.system("python3 mm_test.py " + folder + " 81")


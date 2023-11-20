import numpy as np
import matplotlib.pyplot as plt
import os
import time




program = "integrator_mpi.cpp"                    # Nome de programa
#os.system("mpic++ -O3 " + program + " -lm -lgsl")        # Compila
rootname = "data-101w/K"
its = 5000                              # Numero de iteracoes
Npar = 8                               # Numero de runs paralelas

scase = 0 # 0 => grid definido (configurar no program), 1 => pontos aleatorios, 2 => le um arquivo especificado
                 # Numero de cond. iniciais (Conferir no programa em sí!!!)
sfile = "dummy.dat"
mm_anal = False

if scase == 2:
    Nstarts = len(np.loadtxt(sfile)[:,0])
    print(Nstarts)

# Roda pra obter o mapa em sí

vars = [50] # N waves
vars2 = [0.1,0.5,1,2,5] # fase

for var_i in range(0,len(vars)):
    for var_i2 in range(0,len(vars2)):

        Nstarts = 8*8     
        Nfull = int(Nstarts/Npar)
        Nleft = Nstarts - Nfull*Npar 

        print("Nleft:",Nleft,"Nfull",Nfull)

        svar = "{:08.4f}".format(vars[var_i])
        svar2 = "{:08.4f}".format(vars2[var_i2])
        folder = rootname + "_" + svar + "_" + svar2
        os.makedirs(folder,exist_ok=True)
        times = np.array([])
        for i in range(0,Nfull):
            s0 = time.time()
            L0 = i*Npar
            print()
            runstring = "mpirun -np " + str(Npar)  + " ./a.out " + str(scase) \
            + " " +  str(L0) + " " + str(its) \
            + " " + str(vars[var_i]) + " " + str(vars2[var_i2]) \
            + " " + sfile + " " + folder
            print(runstring)
            os.system(runstring)
            times = np.append(times,time.time() - s0)
            avg = np.sum(times/len(times))
            print(i,"/",Nfull,"expected runtime:" , avg*(Nfull+Nleft)/(60*60)," h")

        if Nstarts%Npar != 0:
            L0 = Nfull*Npar
            runstring = "mpirun -np " + str(Nleft)  + " ./a.out " + str(scase) \
            + " " +  str(L0) + " " + str(its) \
            + " " + str(vars[var_i]) + " " + str(vars2[var_i2]) \
            + " " + sfile + " " + folder
            print(runstring)
            os.system(runstring)

        if mm_anal:
            os.system("python3 mm2.py " + folder)
            
            #agora roda os pontos pra testar
            times = np.array([])
            sfile = folder + "/testpoints.dat"
            starts = np.loadtxt(sfile)
            if starts.shape == (2,):
                Nstarts = 1
            else:
                Nstarts = len(starts[:,0])

            Nfull = int(Nstarts/Npar)
            Nleft = Nstarts - Nfull*Npar 
            print("Nleft:",Nleft,"Nfull",Nfull)

            for i in range(0,Nfull):
                s0 = time.time()
                L0 = i*Npar
                print()
                runstring = "mpirun -np " + str(Npar)  + " ./a.out " + str(2) \
                + " " +  str(L0) + " " + str(its) \
                + " " + str(vars[var_i]) + " " + str(vars2[var_i2]) \
                + " " + sfile + " " + folder
                #print(runstring)
                os.system(runstring)
                times = np.append(times,time.time() - s0)
                avg = np.sum(times/len(times))
                print(i,"/",Nfull,"expected runtime:" , avg*(Nfull+Nleft)/(60*60)," h")

            if Nstarts%Npar != 0:
                L0 = Nfull*Npar
                runstring = "mpirun -np " + str(Nleft)  + " ./a.out " + str(2) \
                + " " +  str(L0) + " " + str(its) \
                + " " + str(vars[var_i]) + " " + str(vars2[var_i2]) \
                + " " + sfile + " " + folder
                #print(runstring)
                os.system(runstring)
            os.system("python3 mm_test.py " + folder  + " " + str(8*8))

        os.system("python3 plot_map.py " + folder)
    
                

    

#    
#
#
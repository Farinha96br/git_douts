import numpy as np
import os
import time



## Setup dos paramteros
os.system("rm  a.out")
program = "integrator_mpi.cpp"                    # Nome de programa
os.system("mpic++ " + program + " -lm -lgsl")        # Compila
rootname = "data-meso_mm"
                            # Numero de iteracoes
Ntasks = 32                               # Numero de runs paralelas
Nnode = 1
Npar = Ntasks*Nnode


scase = 0 # 0 => grid definido (configurar no program), 1 => pontos aleatorios, 2 => le um arquivo especificado
its = 250  
Nstarts = 1024*1024                      # Numero de cond. iniciais (Conferir no programa em sí!!!)
sfile = "dummy.dat"

if scase == 2:
    Nstarts = len(np.loadtxt(sfile)[:,0])
    print(Nstarts)
                          # Numero de cond. iniciais (Conferir no programa em sí!!!)
vars = [0.82, 1.2, 6.5]
# faz a pasta onde vai ter os roles


Nfull = int(Nstarts/Npar)
Nleft = Nstarts - Nfull*Npar 
print("Nleft:",Nleft,"Nfull",Nfull)

folder_batch = "meso_mm"
os.makedirs(folder_batch,exist_ok=True)
os.system("cp head.sh " + folder_batch)

meso_all = open(folder_batch + "/head.sh", "a")
meso_all.write("\n mkdir data-seg_batch \n")
for var_i in range(0,len(vars)):
    print(var_i)
    svar = "{:08.4f}".format(vars[var_i])
    folder = rootname + "_" + svar

    meso_all.write("mkdir -p " + folder + "\n")
    os.system("cp " + program + " " +  folder_batch)

    times = np.array([])
    for i in range(0,Nfull):
        s0 = time.time()
        L0 = i*Npar
        runstring = "mpirun -np " + str(Npar)  + " ./a.out " + str(scase) + " " +  str(L0) + " " + str(its) + " " + str(vars[var_i]) + " " + sfile + " " + folder

        meso_all.write(runstring + "\n")
        #print(runstring)
        #os.system(runstring)
        times = np.append(times,time.time() - s0)
        avg = np.sum(times/len(times))
        #print(i,"/",Nfull,"expected runtime:" , avg*(Nfull+Nleft)/(60*60)," h")

    if Nstarts%Npar != 0:
        L0 = Nfull*Npar
        runstring = "mpirun -np " + str(Nleft) + " ./a.out " + str(scase) + " " +  str(L0) + " " + str(its) + " " + str(vars[var_i]) + " " + sfile + " " + folder
        meso_all.write(runstring + "\n")
        #print(runstring)
        #os.system(runstring)
    
    #meso_all.write("python3 mm.py " + folder + "\n")
    meso_all.write("python3 plot_disp.py " + folder + "\n")




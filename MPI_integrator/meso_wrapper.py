import numpy as np
import matplotlib.pyplot as plt
import os
import time



## Setup dos paramteros
os.system("rm  a.out")
program = "integrator_mpi.cpp"                    # Nome de programa
os.system("mpic++ " + program + " -lm -lgsl")        # Compila
rootname = "data-maps"
its = 10000                              # Numero de iteracoes
Ntasks = 32                               # Numero de runs paralelas
Nnode = 2
Npar = Ntasks*Nnode
Nstarts = 8*8                       # Numero de cond. iniciais (Conferir no programa em sí!!!)
vars = [0.16,0.2]
# faz a pasta onde vai ter os roles


Nfull = int(Nstarts/Npar)
Nleft = Nstarts - Nfull*Npar 
print("Nleft:",Nleft,"Nfull",Nfull)

folder_batch = "meso_maps"
os.makedirs(folder_batch)

# arquivo que compila e chama os outros arquivos
meso_all = open(folder_batch + "/meso_all.sh", "w")
meso_all.write("#!/bin/sh \n")
meso_all.write("module purge all\n\
purge environment modules\n\
module load userspace/all\n\
module load mpich/gcc72/psm2/3.2.1\n\
module load boost/gcc72/openmpi/1.65.1\n")
meso_all.write("mpic++ " + program + " -lm -lgsl \n \n")

for var_i in range(0,len(vars)):
    svar = "{:.3f}".format(vars[var_i])
    folder = rootname + "_" + svar
    # de fato chama os arquivos
    #meso_all.write("jid" + str(rn) + "=$(sbatch --parsable --dependency=afterany:$jid" + str(rn-1) + " meso_" + out_folder + ".sh) \n")
    # "{folder}.sh" é o programa do batch
    meso_all.write("jid" + str(var_i) + "=$(sbatch " + folder + ".sh) \n")
    meso_all.write("echo " + "jid" + str(var_i) + "\n")
    mesorun = open(folder_batch + "/" + folder + ".sh","w")
    mesorun.write("#!/bin/sh \n")
    mesorun.write("\
#SBATCH -J " + folder + "\n\
#SBATCH -p skylake \n\
#SBATCH -A b336 \n\
#SBATCH -N " + str(Nnode) + " \n\
#SBATCH -n " + str(Ntasks) +  " \n\
#SBATCH -t 03:00:00 \n\
#SBATCH --mail-type=END \n\
#SBATCH --mail-user=farinha96br@gmail.com \n \n")

    mesorun.write("\n")
    
                  
    mesorun.write("mkdir -p " + folder + "\n")
    os.system("cp " + program + " " +  folder_batch)

    times = np.array([])
    for i in range(0,Nfull):
        s0 = time.time()
        L0 = i*Npar
        runstring = "mpirun ./a.out " + str(L0) + " " + str(its) + " " + str(vars[var_i]) + " " + folder
        mesorun.write(runstring + "\n")
        #print(runstring)
        #os.system(runstring)
        times = np.append(times,time.time() - s0)
        avg = np.sum(times/len(times))
        #print(i,"/",Nfull,"expected runtime:" , avg*(Nfull+Nleft)/(60*60)," h")

    if Nstarts%Npar != 0:
        L0 = Nfull*Npar
        runstring = "mpirun ./a.out " + str(L0) + " " + str(its) + " " + str(vars[var_i]) + " " + folder
        mesorun.write(runstring + "\n")
        #print(runstring)
        #os.system(runstring)




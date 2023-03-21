import numpy as np
import os
import time
 
# compilação
t_all = time.time()
programscript = "arrumado2.cpp"
program =  "program2.out" # nome do programa
os.system("g++ " + programscript + " -lm -lgsl -o " + program)
 # tempo p cancelar caso de probelma na compilaca
#os.system("g++ arrumado.cpp -lm -lgsl -o " + program)

 # carrega as cond. inicias num array
Nrun = 30 # numero máximo de programas simultanios
iterations = 1000# Número de pontos no arquivo final
#vars = np.hstack((np.linspace(-1,-0.25,25),np.linspace(-0.25,0.25,301),np.linspace(0.25,1,25))) # array do parametro a ser variavel
vars = np.linspace(3,16,50)
lenvar = len(vars)
startfiles = ["sep_1k_6pi_3.dat"] # arquivo de cond. iniciais
rootname = "data-Dx_w2" # Nome principal da rodada de experimentos
############################

# this flag indicates if we are doing a large batch of simulations and the results should be
# transfered to another folder. 1 = True, 0 = False
batch_bool = 0  # Basicamente separar os resultados
mesoBool = True
mesoH = 5 # quantidade de horas esperadas para rodar no mesocentre
mesomin = 0 # quantidade de horas esperadas para rodar no mesocentre

############################

if mesoBool: ## Caso para script do mesocentre
    mesofolder = "meso_" + rootname
    os.makedirs(mesofolder, exist_ok = True)
    mesoall = open(mesofolder + "/meso_all.sh","w")
    mesoall.write("#!/bin/sh \n")
    mesoall.write("g++ " + programscript + " -lm -o " + program + "\n \n") # sem o lgsl
else:
    print("Certeza que é pra rodar?")
    time.sleep(5)




for rn in range(0,len(vars)): # loop pelos parametros var
    
    var = vars[rn]
    varstring = "{:05.4f}".format(var)
    startfile = startfiles[0] # arquivo com as cond. inicias

    start = np.loadtxt(startfile) # carrega oarquivo

    ## Algumas maracutais pro processamento paralelo funcionar direito
    Nsim = len(start[:,0])  # numero de simulaçoes
    Nfull = int(Nsim/Nrun) # Numero de rodadas cheias
    Nfinal = Nsim-Nfull*Nrun # Quantidade de programas paralelos caso Nsim n seja multiplo de Nrun

    # printa umas groselhas sobre o numero de simulações
    print("Nrun,Nsim,Nfull,Nfinal")
    print(Nrun,Nsim,Nfull,Nfinal)

    # Renomeia as coisas positivas e negativas
    if var >= 0:
        out_folder = rootname + "_" + "p" + varstring
    if var < 0:
        out_folder = rootname + "_" + "n" + varstring

    # Oraganiza as pastas do experimento, e cria a pasta com as trajetorias

    
    if mesoBool: ## Caso para script do mesocentre
        if rn == 0:
            mesoall.write("jid" + str(rn) + "=$(sbatch --parsable meso_" + out_folder + ".sh) \n")
        else:
            mesoall.write("jid" + str(rn) + "=$(sbatch --parsable --dependency=afterany:$jid" + str(rn-1) + " meso_" + out_folder + ".sh) \n")
        mesoall.write("echo " + "jid" + str(rn) + "\n")
        mesorun = open(mesofolder + "/meso_" + out_folder + ".sh","w")
        mesorun.write("#!/bin/sh \n")
        mesorun.write("#SBATCH -J " + out_folder + "\n\
#SBATCH -p skylake \n\
#SBATCH --ntasks=" + str(Nrun) + "\n\
#SBATCH --cpus-per-task=1  ## the number of threads allocated to each task \n\
#SBATCH --mem-per-cpu=100M   # memory per CPU core\n\
#SBATCH -A b336 \n\
#SBATCH -t " + str(mesoH).zfill(2) + ":" + str(mesomin).zfill(2) + ":00 \n\
#SBATCH --mail-type=BEGIN,END \n\
#SBATCH --mail-user=farinha96br@gmail.com \n \n")
        mesorun.write("\n")
        mesorun.write("mkdir -p " + out_folder + "\n")
        mesorun.write("mkdir -p " + out_folder + "/traj" + "\n \n")
        os.system("cp " + programscript + " " +  mesofolder)
        os.system("cp run2.py " +  mesofolder)
    else:
        os.makedirs(out_folder,exist_ok=True)
        os.makedirs(out_folder + "/traj",exist_ok=True)

        # Arquivo com os registros do tempo de simulação (Talvez tirar isso aq)
        timefile = open(out_folder + "/timelog.dat","w")
        timefile.write("# #sim_paralela \t parametro \t tempo(s) \n")

    # Coisas pra dar certo o paralelismp
    # n_f é p garantir que caso seja um inteiro, o loop n rode a parte final 2x
    n_f = 1
    if Nfinal == 0:
        n_f = 0
    Npar = Nrun
    #
    t = []
    ## Numero de vezes q vai ter q rodar o role completo, N rodadas cheias + 1 finall
    for i in range(0,Nfull+n_f): 
        if i == Nfull:
            Npar = Nfinal
        t0 = time.time()
        run_string = ""
        
        for j in range(0,Npar): # executa em rodadas de 5
            index = Nrun*i+j
            #print(index,start[index,0],start[index,1],rn)
            if mesoBool: ## Caso para script do mesocentre
                head = "time srun --ntasks=1 --cpus-per-task=$SLURM_CPUS_PER_TASK "
                run_string += head
            
            run_string += "./"+ program \
            + " " + str(index) \
            + " " + str(start[index,0]) \
            + " " + str(start[index,1]) \
            + " " + str(iterations) \
            + " " + str(out_folder) \
            + " " + str(var) \
            + " &"
            if mesoBool:
                run_string += "\n"
        run_string += "wait"
        # de fato roda o os prgramas
        if mesoBool: ## Caso para script do mesocentre
            mesorun.write(run_string + "\n \n")
        else:
            os.system(run_string)
        # Informações a respeito do tempo de computação
        if mesoBool == False:
            trun = time.time()-t0
            timefile.write(str(Npar) + "\t" + str(vars[rn]) + "\t" + str(trun) + "\n")
            t.append(trun)
            avgt = np.sum(t)/len(t)
            exct = avgt*(Nfull+n_f)
            print("\n",i,"/",Nfull+n_f,round(trun,3),"T_sim: ",round(avgt/60,2),"m T_batch: ",round(exct/60,2),"m T_all: ",round(exct*len(vars)/(60*60),3),"h")
    
    if mesoBool == False:
        timefile.close()

    if mesoBool == False:
        print("copiando arquivo inicial p pasta de dados")
        os.system("cp " + startfile + " " + out_folder)
        

        print("fazendo trajetórias individuais")
        Nplots = 20
        os.system("python3 plot_each.py " + out_folder + " " + str(Nplots))

        #print("Fazendo um arquivo unico p plotar o mapa")
        #os.system("cat " + out_folder + "/traj/*.dat > " + out_folder +  "/all_traj.dat")
        #print("plotando o mapa")
        #os.system("python3 plot_mapa.py " + out_folder + " " + startfile + " "  + varstring)

        print("Calculo da difusao")
        os.system("python3 difus.py " + out_folder)
        os.system("python3 plot_dif.py " + out_folder)

        #print("Fazendo anlálise dos saltos")
        #os.system("python3 jumps.py " + out_folder)
        #os.system("python3 plot_jumps.py " + out_folder)
        
        time.sleep(1)

        #os.system("rm -r " + out_folder + "/traj")
        
        if batch_bool == 1:
            print("Copiando os role pra uma pasta unificada")
            os.makedirs(rootname,exist_ok=True)
            os.system("cp " + out_folder + "/" + "D_" + out_folder + ".dat" + " " + rootname) # copia o arquivo de difusão
            os.system("cp " + out_folder + "/" + out_folder + "_t_D.pdf" + " " + rootname)
            os.system("cp " + out_folder + "/" + out_folder + "_t_sigma.pdf" + " " + rootname)
            os.system("cp " + out_folder + "/" + "map_" +varstring + ".png" + " " + rootname)
            os.system("mv " + out_folder + " " + rootname)
            os.system("rm -r " + out_folder)
    mesorun.close()
    

if mesoBool == False:
    os.system("python3 plot_var.py ./") 


    #os.system("python3 tweet_wanda.py " + str((time.time()-t_all)/60) + " min")
    #playsound('final.mp3')
    #os.system("shutdown")

if mesoBool: ## Caso para script do mesocentre
    mesoall.close()
import numpy as np
import os
import time

# compilação
t_all = time.time()
program =  "program.out" # nome do programa
os.system("g++ arrumado2.cpp -lm -lgsl -o " + program)
time.sleep(3) # tempo p cancelar caso de probelma na compilacao
#os.system("g++ arrumado.cpp -lm -lgsl -o " + program)

 # carrega as cond. inicias num array
iterations = 200 # Número de pontos no arquivo final
vars = np.linspace(1,5,100) # array do parametro a ser variavel
startfiles = ["rng1k.dat"]
rootname = "A2_Ufreq"
batch_bool = 1
############################

if batch_bool == 1:
    os.makedirs(rootname,exist_ok=True)
############################

for rn in range(0,len(vars)): # loop pelos parametros var
    var = vars[rn]
    varstring = "{:04.4f}".format(var)
    startfile = startfiles[0] # arquivo com as cond. inicias
    start = np.loadtxt(startfile)

    Nrun = 16 # numero máximo de programas simultanios
    Nsim = len(start[:,0])  # numero de simulaçoes
    Nfull = int(Nsim/Nrun) # Numero de rodadas cheias
    Nfinal = Nsim-Nfull*Nrun # Quantidade de programas paralelos caso Nsim n seja multiplo de Nrun

    # printa umas groselhas
    print("Nrun,Nsim,Nfull,Nfinal")
    print(Nrun,Nsim,Nfull,Nfinal)

    # organiza umas coias de pastas
    #out_folder = "exp_phase_r_" + str(round(var,3)).replace("-","neg") # pasta onde vai sair os roles
    out_folder = rootname + "_" + varstring.replace("-","neg") # pasta onde vai sair os roles

    os.makedirs(out_folder,exist_ok=True)
    os.makedirs(out_folder + "/traj",exist_ok=True)
    timefile = open(out_folder + "/timelog.dat","w")
    timefile.write("# #sim_paralela \t parametro \t tempo(s) \n")

    # n_f é p garantir que caso seja um inteiro, o loop n rode a parte final 2x
    n_f = 1
    if Nfinal == 0:
        n_f = 0
    Npar = Nrun
    t = []
    for i in range(0,Nfull+n_f): ## Numero de vezes q vai ter q rodar o role completo, N rodadas cheias + 1 finall
        if i == Nfull:
            Npar = Nfinal
        #print("running " + str(Npar))
        t0 = time.time()
        run_string = ""
        for j in range(0,Npar): # executa em rodadas de 5
            index = Nrun*i+j
            #print(index,start[index,0],start[index,1],rn)
            run_string += "./"+ program \
            + " " + str(index) \
            + " " + str(start[index,0]) \
            + " " + str(start[index,1]) \
            + " " + str(iterations) \
            + " " + str(out_folder) \
            + " " + str(var) \
            + " & "
        run_string += "wait "
        os.system(run_string)
        trun = time.time()-t0
        timefile.write(str(Npar) + "\t" + str(vars[rn]) + "\t" + str(trun) + "\n")
        t.append(trun)
        avgt = np.sum(t)/len(t)
        exct = avgt*(Nfull+n_f)
        print("\n",i,"/",Nfull+n_f,round(trun,3),"runtime ",round(avgt/60,2),"min expected_time:",round(exct/60,2),"min")
    timefile.close()

    os.system("cp " + startfile + " " + out_folder)
    os.system("cat " + out_folder + "/traj/*.dat > " + out_folder +  "/all_traj.dat")

    #print("fazendo trajetórias individuais")
    #os.system("python3 plot_each.py " + out_folder)
    os.system("python3 plot_mapa.py " + out_folder + " " + startfile + " " + out_folder + "/" + varstring)

    print("cp " + out_folder + "/" + varstring + ".png " + "mapas")
    os.system("cp " + out_folder + "/" + varstring + ".png " + "mapas")
    #os.system("rm -r " + out_folder)
    #print("Analise...")
    os.system("python3 difus.py " + out_folder)
    os.system("python3 plot_dif.py " + out_folder)
    #os.system("python3 jumps.py " + out_folder)
    time.sleep(1)
    print("Copiando os role")
    if batch_bool == 1:
        os.system("cp " + out_folder + "/" + "D_" + out_folder + ".dat" + " " + rootname) # copia o arquivo de difusão
        os.system("cp " + out_folder + "/" + out_folder + "_t_D.pdf" + " " + rootname)
        os.system("cp " + out_folder + "/" + out_folder + "_t_sigma.pdf" + " " + rootname)
        os.system("cp " + out_folder + "/" + varstring + ".png" + " " + rootname)
        #os.system("mv " + out_folder + " " + rootname)
        #os.system("rm -r " + out_folder)
        os.system("rm -r " + out_folder + "/traj")


#print("DONE WITH EVERTHING rn=" + str(rn))
os.system("python3 plot_var.py " + rootname)
os.system("python3 tweet_wanda.py " + str((time.time()-t_all)/60) + " min")
#playsound('final.mp3')
os.system("shutdown")

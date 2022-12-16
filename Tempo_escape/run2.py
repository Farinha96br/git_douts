import numpy as np
import os
import time

# compilação
t_all = time.time()
program =  "program.out" # nome do programa
os.system("g++ escape2.cpp -lm -lgsl -o " + program)
time.sleep(3) # tempo p cancelar caso de probelma na compilacao
#os.system("g++ arrumado.cpp -lm -lgsl -o " + program)

startfile = "grid1000.dat" # arquivo com as cond. inicias
start = np.loadtxt(startfile) # carrega as cond. inicias num array


Nrun = 16 # numero máximo de programas simultanios
Nsim = len(start[:,0])  # numero de simulaçoes
Nfull = int(Nsim/Nrun) # Numero de rodadas cheias
Nfinal = Nsim-Nfull*Nrun # Quantidade de programas paralelos caso Nsim n seja multiplo de Nrun

# printa umas groselhas
#print("Nrun,Nsim,Nfull,Nfial")
#print(Nrun,Nsim,Nfull,Nfinal)

vars = [0.1,0.3,0.5,1] # array do parametro a ser variavel
foldername = ["2wave_0.1","2wave_0.3","2wave_0.5","2wave_1.0"]
for rn in range(0,len(vars)): # loop pelos parametros var
    var = vars[rn]
    # organiza umas coias de pastas
    #out_folder = "escape_" + str(round(var,3)).replace("-","neg") # pasta onde vai sair os roles
    out_folder = foldername[rn]
    os.makedirs(out_folder,exist_ok=True)
    os.makedirs(out_folder + "/traj",exist_ok=True)

    # n_f é p garantir que caso seja um inteiro, o loop n rode a parte final 2x
    n_f = 1
    if Nfinal == 0:
        n_f = 0

    Npar = Nrun
    for i in range(0,Nfull+n_f): ## Numero de vezes q vai ter q rodar o role completo, N rodadas cheias + 1 finall
        #if i < Nfull:
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
        + " " + str(out_folder) \
        + " " + str(var) \
        + " " + ">> " + foldername[rn] + "/" + out_folder + "_escape.dat" \
        + " & "
        run_string += "wait "
        os.system(run_string)
        print(str(i) + "/" + str(Nfull))
        #print("batch time = " + str(time.time()-t0))
    time.sleep(2)
    #print("cat as coisas...")
    os.system("python3 organizer.py " + out_folder)
    os.system("python3 plot_escape.py " + out_folder)
    os.system("python3 tweet_wanda.py"  + str(time.time() - t_all))

os.system("shutdown")

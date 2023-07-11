import numpy as np
import os
import time

k = 3

# Grade de pontos iniciais
def gridstart1(N):
    X = np.linspace(0,2*np.pi/(k),N)
    Y = np.linspace(0,2*np.pi/(k),N)
    A = []
    for x in X:
        for y in Y:
            A.append([x,y])
    A = np.array(A)
    return A 

def gridstart2(N):
    X = np.linspace(0,2*np.pi,N)
    Y = np.linspace(0,2*np.pi,N)
    A = []
    for x in X:
        for y in Y:
            A.append([x,y])
    A = np.array(A)
    return A 

A = gridstart1(2500)


# compilação
t_all = time.time()
program =  "basin.out" # nome do programa
os.system("g++ basin_integrator.cpp -lm -lgsl -o " + program)
#time.sleep(5) # tempo p cancelar caso de probelma na compilaca
#os.system("g++ arrumado.cpp -lm -lgsl -o " + program)

 # carrega as cond. inicias num array
Nrun = 100 # numero máximo de programas simultanios
#vars = np.hstack((np.linspace(-1,-0.25,25),np.linspace(-0.25,0.25,301),np.linspace(0.25,1,25))) # array do parametro a ser variavel
vars = [3,2,1,0.5,0.1]
lenvar = len(vars)
rootname = "data-basin_v" # Nome principal da rodada de experimentos
############################

# this flag indicates if we are doing a large batch of simulations and the results should be
# transfered to another folder. 1 = True, 0 = False
batch_bool = 0  # Basicamente separar os resultados
############################

for rn in range(0,len(vars)): # loop pelos parametros var
    var = vars[rn]
    varstring = "{:05.3f}".format(var)

    ##  Coisas pra gerar o script pro mesocentre

    ## Algumas maracutais pro processamento paralelo funcionar direito
    Nsim = len(A[:,0])  # numero de simulaçoes
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
    os.makedirs(out_folder,exist_ok=True)

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
            run_string += "./"+ program \
            + " " + str(A[index,0]) \
            + " " + str(A[index,1]) \
            + " " + str(var) \
            + " >>" + out_folder + "/" + out_folder + ".dat" \
            + " & "
        run_string += "wait "
        # de fato roda o os prgramas
        os.system(run_string)
        # Informações a respeito do tempo de computação
        trun = time.time()-t0
        timefile.write(str(Npar) + "\t" + str(vars[rn]) + "\t" + str(trun) + "\n")
        t.append(trun)
        avgt = np.sum(t)/len(t)
        exct = avgt*(Nfull+n_f)
        print(i,"/",Nfull+n_f,round(trun,3),"T_sim: ",round(avgt/60,2),"m T_batch: ",round(exct/60,2),"m T_all: ",round(exct*len(vars)/(60*60),3),"h")
    timefile.close()

    time.sleep(1)
    os.system("python3 cat.py " + out_folder)
    os.system("python3 plot_disp.py " + out_folder)


os.system("shutdown")
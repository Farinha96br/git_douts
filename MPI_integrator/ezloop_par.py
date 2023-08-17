import os
import sys


Nrun = 8 # numero máximo de programas simultanios


lisdir = sorted(os.listdir())
rootname = sys.argv[1]

rootcommand = "python3 " + sys.argv[2]
folders = []

print(lisdir)


for f in lisdir:
    if f.startswith(rootname):
        print(f)
        folders.append(f)

            # os.system("python3 difus.py " + f)
print(folders)


Nsim = len(folders)  # numero de simulaçoes
Nfull = int(Nsim/Nrun) # Numero de rodadas cheias
Nfinal = Nsim-Nfull*Nrun # Quantidade de programas paralelos caso Nsim n seja multiplo de Nrun

# printa umas groselhas sobre o numero de simulações
print("Nrun,Nsim,Nfull,Nfinal")
print(Nrun,Nsim,Nfull,Nfinal)

n_f = 1
if Nfinal == 0:
    n_f = 0
Npar = Nrun

## Numero de vezes q vai ter q rodar o role completo, N rodadas cheias + 1 final
for i in range(0,Nfull+n_f): 
    if i == Nfull:
        Npar = Nfinal
    run_string = ""
    
    for j in range(0,Npar): # executa em rodadas de 5
        index = Nrun*i+j
        run_string += rootcommand \
        + " " + folders[index] \
        + " &"
    run_string += "wait"
    os.system(run_string)
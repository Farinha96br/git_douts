import numpy as np
import sys
import os


#savetype = ".dat"
savetype = ".npy"


folder = sys.argv[1] # pasta com os dados
# carrega organiza e salva os arquivos em x
data = np.loadtxt(folder + "/datax.dat")
print("---x---")
print("shapex raw txt:",data.shape)

index = np.argsort(data[:,0])
data = data[index,1:]
print("shapex cut npy:",data.shape)

if savetype == ".dat":
    np.savetxt(folder + "/sdatax.dat",data)
else:
    np.save(folder + "/datax.npy",data)
    print("shapex cut npy:",np.load(folder + "/datax.npy").shape)

    
print("---y---")
data = None

# carrega organiza e salva os arquivos em y
data = np.loadtxt(folder + "/datay.dat")
print("shapey raw txt:",data.shape)

index = np.argsort(data[:,0])
data = data[index,1:]
print("shapex cut txt:",data.shape)
if savetype == ".dat":
    np.savetxt(folder + "/sdatay.dat",data)
else:
    np.save(folder + "/datay.npy",data)
    print("shapey cut npy:",np.load(folder + "/datay.npy").shape)

data = None

# tempos
print("---t---")
data = np.loadtxt(folder + "/datat.dat")
print("shapet raw txt:",data.shape)

if savetype != ".dat":
    np.save(folder + "/datat.npy",data)


#os.system("rm " + folder + "/*.dat")




import numpy as np
import matplotlib.pyplot as plt
from numpy import pi

np.random.seed(seed=10)

def H1(grid_x,grid_y):
    return np.sin(3*grid_x)*np.sin(3*grid_y)

pi = np.pi
# parametros da simulaçao
nu = 3e-4
dt = 1e-3
steps = 60000
tf = dt*steps

# griando a malha no espaço real
nx, ny = 256, 256 # numero de pontos na rede
Lx, Ly = 2.0*pi, 2.0*pi      # Tamanho da região simulada

# Construct grid.
dx, dy = Lx/nx, Ly/ny

x = np.arange(0.0, Lx, dx)
y = np.arange(0.0, Ly, dy)
X, Y = np.meshgrid(x, y)

nk, nl = nx//2+1, ny
k = 2.0*pi/Lx * np.arange(0.0, nk)
l = 2.0*pi/Ly * np.append(np.arange(0.0, ny/2.0), np.arange(-ny/2.0, 0.0))



K, L = np.meshgrid(k, l)
Ksq = K**2.0 + L**2.0

print("shape Ksq; Ksq",Ksq.shape)

divsafeKsq = Ksq.copy()
print(divsafeKsq)
divsafeKsq[0,0] = float('Inf')
invKsq = 1.0/divsafeKsq
print("shape invKsq; Ksq",Ksq.shape)

#print(Ksq)
#print(invKsq)

# Define as coisa de fourier 2d assim p ficar mais facil
fft2 = np.fft.rfft2
ifft2 = np.fft.irfft2


# cond. iniciais da função zeta
t = 0.0
zeta = H1(X,Y) + np.random.rand(nx, ny)*1

zetah = fft2(zeta) # coloca no espaço d fourier
print("zeta shape:",zeta.shape)
print("zetah shape:",zetah.shape)
print("invzetah shape:",ifft2(zetah).shape)
print("psih shape:",(-zetah*invKsq).shape)

c = 0



while t < tf:
    # calculando os pedaços da eq.
    #print(t)
    if c%500 == 0:
        print(c)
        fig, ax = plt.subplots()
        fig.set_size_inches(7*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm
        ax.set_ylabel("y")
        ax.set_xlabel("x")
        ax.set_title("mine " + str(t))
        zeta = ifft2(zetah)
        a = ax.pcolormesh(X,Y,zeta)
        fig.colorbar(a,label = "vorticity")
        print(zeta.shape)
        plt.savefig("imgs/" + str(c) + ".png",dpi = 300)
        plt.close()

    psih = - zetah * invKsq # isso aqui vc acha quando faz o laplaciano de zeta no espaço de fourier
    zetax = ifft2(1j*K*zetah) # parcial de zeta na direção x no espaço real (ifft)
    zetay = ifft2(1j*L*zetah) # parcial de zeta na direçao y no espaço real (ifft)
    u = ifft2(1j*L*psih) # derivadas da streamfunction psi em x no espaço real (ifft)
    v = -ifft2(1j*K*psih) # derivadas da streamfunction psi em x no espaço real (ifft)
    # termo que vai ser usado como "fator temporal" ou diferencial no tempo
    rhs = fft2(u*zetax + v*zetay) - nu*Ksq*zetah # faz o passo temporal


    zetah += dt*rhs
    t += dt
    c += 1
plt.close()





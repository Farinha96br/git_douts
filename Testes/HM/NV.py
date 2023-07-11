import numpy as np
import matplotlib.pyplot as plt
import time

from numpy import pi

def H1(grid_x,grid_y):
    return np.sin(grid_x)*np.sin(grid_y)

# Parameters

np.random.seed(seed=10)

nu = 3e-4
Lx = 2.0*pi
nx = 64
dt = 1e-2
nsteps = 60000

# Construct grid.
dx = Lx/nx
nk, nl = nx//2+1, nx
x = np.arange(0.0, Lx, dx)

k = 2.0*pi/Lx * np.arange(0.0, nk)
l = 2.0*pi/Lx * np.append(np.arange(0.0, nx/2.0), np.arange(-nx/2.0, 0.0))


X, Y = np.meshgrid(x, x)
K, L = np.meshgrid(k, l)
Ksq = K**2.0 + L**2.0

divsafeKsq = Ksq.copy()
divsafeKsq[0,0] = float('Inf')
invKsq = 1.0/divsafeKsq


# Define fft
fft2 = np.fft.rfft2
ifft2 = np.fft.irfft2


# Initial condition
t = 0.0
zeta = H1(X,Y) + np.random.rand(nx, nx)*0.1


zetah = fft2(zeta)
print("zeta shape:",zeta.shape)
print("zetah shape:",zetah.shape)
print("invzetah shape:",ifft2(zetah).shape)
print("psih shape:",(-zetah*invKsq).shape)


# Step forward
(7*0.393, 7*0.393) # o valor multiplicando é o tamanho em cm

t1 = time.time()
c = 0
for step in range(nsteps):

    if step % 500 is 0:
        zeta = ifft2(zetah)
        fig = plt.figure(1)
        fig.set_size_inches
        plt.title("reference " + str(t))
        plt.pcolormesh(X,Y,zeta)
        print(zeta.shape)
        #plt.pause(0.01)

        print("step = {:4d}, t = {:06.1f} s, wall time = {:.3f}".format(
            step, t, time.time()-t1))
        plt.savefig("imgs2/" + str(c) + ".png",dpi = 300)

        t1=time.time()



    # Calculate right hand side
    psih = -zetah * invKsq
    zetax = ifft2(1j*K*zetah)
    zetay = ifft2(1j*L*zetah)
    u = ifft2(1j*L*psih)
    v = -ifft2(1j*K*psih)

    rhs = fft2(u*zetax + v*zetay) - nu*Ksq*zetah

    zetah += dt*rhs
    t += dt
    c += 1
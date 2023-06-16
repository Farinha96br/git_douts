import numpy as np
import os
import time
import random as rng
import matplotlib.pyplot as plt

# Sla pra q é isso p falar a vdd

def hip(k,n):
    # retorna a linha eliptica de indice n, para um numero de onda k no sistema
    return n*pi/k

def elip(k,n):
    # retorna a linha eliptica de indice n, para um numero de onda k no sistema
    return (2*n+1)*pi/(2*k)



def drawgrid(ax,M,N):
    # M é o modo em x
    # N é o modo em y
    for m in range(0,2*M):
        ax.axhline(m*pi/N, color = '#888888', linestyle = "--", linewidth = 0.7, zorder = 0)
    for n in range(0,2*N+1):
        ax.axvline(n*pi/N, color = '#888888', linestyle = "--", linewidth = 0.7, zorder = 0)

sy = []
sx = []


pi = 3.14159265359


### SETUP OF THE SCRIPT
# number of random points for the cases wich the condition apply
rng_N = 200
# relevant normalizing parameters
a = 2
# wavenumbers

M = 3
N = 3
kx =   M
ky =   N
cellx = 3.14159265359/(kx)
celly = 3.14159265359/(kx)


# if the wavenumbers should be normalized, 1 = True, 0 = False


# Case for staring conditions generation
#   0:  Random points over the space  0 < x < 1, and  -pi < y < pi
#   1:  Grid very useful to visualize stroboscopi maps
#   2:  Random poins spread over te separatix
#   3:  Line of equaly spaced points between (x0,y0) to (xf,yf)
gen_case = 3


# isso aq é p dar uma olhada nos pontos p ver se ta tudo certo
fig, ax = plt.subplots()
#fig.set_size_inches(7*0.393, 7*0.393)

ax.axvline(2*3.1415, zorder = 0, alpha = 0.5, color = "black")
ax.axvline(0, zorder = 0, alpha = 0.5, color = "black")
ax.axhline(2*3.1415, zorder = 0, alpha = 0.5, color = "black")
ax.axhline(0, zorder = 0, alpha = 0.5, color = "black")


ax.set_xticks([-3.14,0,3.14],["$-\pi$","0",r"$+\pi$"])


#   0:  Random points over the space  0 < x < 1, and  -pi < y < pi
if gen_case == 0:
    for i in range(0,rng_N):
        x = rng.random()*2*pi
        y = rng.random()*2*pi
        sy.append(x)
        sx.append(y)
        print(x,y)


#   1:  Grid very useful to visualize stroboscopic maps
if  gen_case == 1:
    for m in range(0,2*M):
        for n in range(0,2*N):
            for f in np.linspace(0.001,0.4,4):
                x = elip(kx,m)
                y = hip(ky,n)+celly*f
                print(x,y)
                sx.append(x)
                sy.append(y)

if  gen_case == 2:
    for m in range(0,2):
        for n in range(0,2):
            for f in np.linspace(0.001,0.5,10):
                x = elip(kx,m)
                y = hip(ky,n)+celly*f
                print(x,y)
                sx.append(x)
                sy.append(y)
                
                

#   2:  Random poins spread over te separatix
if gen_case == 3:
    for i in range(0,rng_N):
        n = rng.randint(0,6) # numeros p x
        m = rng.randint(0,5) # numeros p y
        coin = rng.randint(0,1) # decide se vai ser distribuido em x ou y

        if coin == 0: # ao longo de x
            x = hip(kx,m)
            y = (rng.random()*2*pi)
            if n == 0:
                x+=0.001
        if coin == 1: # ao longo de y
            y = hip(ky,n)
            x = (rng.random()*2*pi)
        sy.append(x)
        sx.append(y)
        print(x,y)



if gen_case == 4:
    pts = 500
    x0 = np.pi/(2*kx)
    xf = np.pi/(2*kx)
    y0 = 0
    yf = 2*np.pi/(kx)
    #########
    y = np.linspace(y0,yf,pts)
    x = np.linspace(x0,xf,pts)
    for i in range(pts):
        sy.append(x[i])
        sx.append(y[i])
        print(x[i],y[i])


        





drawgrid(ax,3,3)
ax.set_ylim(-1,7)
ax.set_xlim(-1,7)
ax.set_ylabel("$y$")
ax.set_xlabel("$x$")
ax.scatter(sx,sy,s = 2,marker='o', c = "firebrick",zorder = 5)
plt.show()
plt.close()






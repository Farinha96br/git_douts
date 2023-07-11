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
    # M é o modo em y
    # N é o modo em x
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
gen_case = 0


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


#   2:  Grid in 2x2 cell useful to visualize stroboscopic maps in periodic systems
if  gen_case == 2:
    
    N = 15
    #print(f1)
    #print(f2)
    sx = np.linspace(0,hip(kx,2),40)
    sy = [elip(ky,0),elip(ky,1)]

    for x in sx:
        for y in sy:
            print(x,y)

    sx,sy = np.meshgrid(sx,sy)


if  gen_case == 3:
    N = 1000
    x0 = [0,0]
    xf = [2*np.pi/kx,0]
    xp = np.linspace(x0,xf,1000)
    #print(xp.shape)
    for i in range(0,len(xp[:,0])):
        print(xp[i,0],xp[i,1])
    sx = xp[:,0]
    sy = xp[:,1]




drawgrid(ax,3,3)
ax.set_ylim(-1,7)
ax.set_xlim(-1,7)
ax.set_ylabel("$x$")
ax.set_xlabel("$y$")
ax.scatter(sy,sx,s = 2,marker='o', c = "firebrick",zorder = 5)
plt.show()
plt.close()






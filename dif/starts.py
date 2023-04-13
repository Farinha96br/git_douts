import numpy as np
import os
import time
import random as rng
import matplotlib.pyplot as plt

# Sla pra q é isso p falar a vdd
def xhip(kx,n):
    return n*pi/kx

def yhip(ky,n):
    return (2*n+1)*pi/(2*ky)

def drawgrid(ax,M,N):
    for m in range(0,2*M+1):
        ax.axhline(np.pi*m/M, color = '#888888', linestyle = "--", linewidth = 0.7, zorder = 9)
    for n in range(0,2*N):
        ax.axvline((2*n+1)*pi/(2*N), color = '#888888', linestyle = "--", linewidth = 0.7, zorder = 9)

sx = []
sy = []


pi = 3.14159265359


### SETUP OF THE SCRIPT
# number of random points for the cases wich the condition apply
rng_N = 200
# relevant normalizing parameters
a = 2
# wavenumbers
kx =    3
ky =    3
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
        sx.append(x)
        sy.append(y)
        print(x,y)


#   1:  Grid very useful to visualize stroboscopic maps
if  gen_case == 1:
    for x in np.arange(0,2*pi,pi/(kx)):
        for y in np.arange(0,2*pi,pi/(ky)):
            if x+0.025 < 2*np.pi:
                print(x+cellx*0.001,y)
                sx.append(x+cellx*0.01)
                sy.append(y)
                print(x+cellx*0.1,y)
                sx.append(x+cellx*0.1)
                sy.append(y)
                print(x+cellx*0.2,y)
                sx.append(x+cellx*0.2)
                sy.append(y)
                print(x+cellx*0.4,y)
                sx.append(x+cellx*0.3)
                sy.append(y)
                print(x+cellx*0.7,y)
                sx.append(x+cellx*0.7)
                sy.append(y)
                

#   2:  Random poins spread over te separatix
if gen_case == 2:
    for i in range(0,rng_N):
        n = rng.randint(0,6) # numeros p x
        m = rng.randint(0,5) # numeros p y
        coin = rng.randint(0,1) # decide se vai ser distribuido em x ou y

        if coin == 0: # ao longo de x
            x = xhip(kx,n)
            y = (rng.random()*2*pi)
            if n == 0:
                x+=0.001
        if coin == 1: # ao longo de y
            y = yhip(ky,m)
            x = (rng.random()*2*pi)
        sx.append(x)
        sy.append(y)
        print(x,y)



if gen_case == 3:
    pts = 500
    x0 = np.pi/(2*kx)
    xf = np.pi/(2*kx)
    y0 = 0
    yf = 2*np.pi/(kx)
    #########
    y = np.linspace(y0,yf,pts)
    x = np.linspace(x0,xf,pts)
    for i in range(pts):
        sx.append(x[i])
        sy.append(y[i])
        print(x[i],y[i])


        





drawgrid(ax,3,3)
ax.set_ylim(-1,7)
ax.set_xlim(-1,7)
ax.set_ylabel("$x$")
ax.set_xlabel("$y$")
ax.scatter(sy,sx,s = 2,marker='o', c = "firebrick")
plt.show()
plt.close()






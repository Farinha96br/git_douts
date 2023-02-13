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

sx = []
sy = []


pi = 3.14159265359


### SETUP OF THE SCRIPT
# number of random points for the cases wich the condition apply
rng_N = 100
# relevant normalizing parameters
a = 1
# wavenumbers
kx =    12*3.1415
ky =    6
# if the wavenumbers should be normalized, 1 = True, 0 = False


# Case for staring conditions generation
#   0:  Random points over the space  0 < x < 1, and  -pi < y < pi
#   1:  Grid very useful to visualize stroboscopi maps
#   2:  Random poins spread over te separatix
gen_case = 2


# isso aq é p dar uma olhada nos pontos p ver se ta tudo certo
fig, ax = plt.subplots()
#fig.set_size_inches(7*0.393, 7*0.393)
ax.set_xlim([-4,4])
ax.set_ylim([-0.3,1.3])

ax.axvline(3.1415)
ax.axvline(-3.1415)
ax.axhline(0)
ax.axhline(1)

ax.set_xticks([-3.14,0,3.14],["$-\pi$","0",r"$+\pi$"])


#   0:  Random points over the space  0 < x < 1, and  -pi < y < pi
if gen_case == 0:
    for i in range(0,rng_N):
        x = rng.random()
        y = rng.random()*2*pi-pi
        sx.append(x)
        sy.append(y)
        print(x,y)


#   1:  Grid very useful to visualize stroboscopic maps
if  gen_case == 1:
    for x in np.arange(0,1,pi/(kx)):
        for y in np.arange(-pi,pi,pi/(ky)):
            if x+0.025 < 1:
                sx.append(x)
                sy.append(y)
                print(x+0.025,y)
                print(x+0.003,y)

#   2:  Random poins spread over te separatix
if gen_case == 2:
    for i in range(0,rng_N):
        n = rng.randint(0,12) # numeros p x
        m = rng.randint(-6,5) # numeros p y
        coin = rng.randint(0,1) # decide se vai ser distribuido em x ou y

        if coin == 0: # ao longo de x
            x = xhip(kx,n)
            y = (rng.random()*2*pi)-pi
            if n == 0:
                x+=0.001
        if coin == 1: # ao longo de y
            y = yhip(ky,m)
            x = rng.random()*1
        sx.append(x)
        sy.append(y)
        print(x,y)






ax.set_ylabel("$x$")
ax.set_xlabel("$y$")
ax.scatter(sy,sx,s = 0.25,marker='o', c = "firebrick")
plt.show()
plt.close()






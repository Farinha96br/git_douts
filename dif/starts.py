import numpy as np
import os
import time
import random as rng

# Sla pra q é isso p falar a vdd
def xhip(kx,n):
    return n*pi/kx

def yhip(ky,n):
    return (2*n+1)*pi/kx




pi = 3.14159265359


### SETUP OF THE SCRIPT
# number of random points for the cases wich the condition apply
rng_N = 1000
# relevant normalizing parameters
a = 1
# wavenumbers
kx =    12
ky =    12
# if the wavenumbers should be normalized, 1 = True, 0 = False
bool_normalized = 0
# Case for staring conditions generation
#   0:  Random points over the space  0 < x < 1, and  -pi < y < pi
#   1:  Grid very useful to visualize stroboscopi maps
#   2:  Random poins spread over te separatix
gen_case = 1

### ACTUAL SCRIPT

if bool_normalized == 1:
    kx = kx*a
    ky = ky*a

#   0:  Random points over the space  0 < x < 1, and  -pi < y < pi
if gen_case == 0:
    for i in range(0,rng_N):
        x = rng.random()
        y = rng.random()*2*pi-pi
        print(x,y)


#   1:  Grid very useful to visualize stroboscopic maps
if  gen_case == 1:
    for x in np.arange(0,1,pi/(kx)):
        for y in np.arange(-pi,pi,pi/(ky)):
            if x+0.025 < 1:
                print(x+0.025,y)
                print(x+0.003,y)

#   2:  Random poins spread over te separatix
if gen_case == 2:
    for i in range(0,rng_N):
        n = rng.randint(0,6)
        m = rng.randint(-10,10)

    coin = rng.randint(0,1)
    if coin == 0:
        x = xhip(kx,n)
        y = (rng.random()*2*pi)-pi
    if coin == 1:
        y = yhip(ky,m)
        x = rng.random()*1
    print(x,y)






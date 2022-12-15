import numpy as np
import os
import time
import random as rng

# compilação
pi = 3.14159265359
a = 0.18
ky = 61.111111
kx = ky*np.sqrt(2)

ky = ky*a
kx = kx*a
#print(kx)
#print(pi/(kx))
#print(ky)
#print(pi/(ky))


for x in np.arange(0,1,pi/(kx)):
    for y in np.arange(-pi,pi,pi/(ky)):
        if x+0.025 < 1:
            print(x+0.025,y)
            print(x+0.003,y)

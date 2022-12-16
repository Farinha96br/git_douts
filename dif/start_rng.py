import numpy as np
import os
import time
import random as rng

# compilação
pi = 3.14159265359
#x = np.linspace(0,pi,7) + 10
#y = np.linspace(-1*pi,pi,25)
a = 0.18
ky = 144.4444444*a
kx = 104.7166666*a




for i in range(0,5000):
    x = rng.random()
    y = rng.random()*2*pi-pi
    print(x,y)

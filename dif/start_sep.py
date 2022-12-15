import numpy as np
import os
import time
import random as rng

pi = 3.14159265359

def xhip(kx,n):
    return n*pi/kx

def yhip(ky,n):
    return (2*n+1)*pi/kx

# compilação
a = 0.18
ky = 61.111111
kx = 104.719

ky = ky*a
kx = kx*a

cellx = pi/kx
celly = pi/ky

for i in range(0,2000):
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

import numpy as np
import os
import time
import random as rng




# compilação
pi = 3.14159265359
a = 0.18
# experimental
#ky = 61.111111
#kx = ky*np.sqrt(2)
# pras duas ondas
ky = 55.5555
kx = 104.719
#  Normaliza
ky = ky*a
kx = kx*a
#   Pontos hiperbolicos e elipticos
m = 1
n = 1
PH = [m*pi/kx,(2*n+1)*pi/(2*ky)]
PE = [(2*n+1)*pi/(2*kx),m*pi/ky]

# Largura e altura da grade de pontos iniciais, x e y são as coordenadas usuais
Lx = 0.001
Ly = 0.001
#   Numero de pontos em cada direção, 32*32=1024 pontos
Nx = 32
Ny = 32
#   Centro da grade de condições
Cx = PH[0]+0.006
Cy = PH[1]+0.006
# Arrays dos pontos
Px = np.linspace(0,Lx,Nx) - Lx/2 + Cx
Py = np.linspace(0,Ly,Ny) - Ly/2 + Cy
for x in Px:
    for y in Py:
        print(x,y)

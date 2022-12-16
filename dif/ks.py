import numpy as np
import matplotlib.pyplot as plt
import sys

pi = 3.141592653589793

a = 0.18
Ly = 2*3.141592653589793*a

print("kx","ky")
for i in range(1,30):
    print(i,pi*i/a,2*pi*i/Ly)
print("normalizado")
for i in range(1,30):
    print(i,a*pi*i/a,a*2*pi*i/Ly)

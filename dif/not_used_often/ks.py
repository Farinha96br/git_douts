import numpy as np
import matplotlib.pyplot as plt
import sys

pi = 3.141592653589793

a = 1
Ly = 2*3.141592653589793*a

print("kx","ky","|","kx norm","ky norm")
for i in range(1,30):
    print(i,pi*i/a,2*pi*i/Ly,'|',a*pi*i/a,a*2*pi*i/Ly)

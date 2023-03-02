import numpy as np
import matplotlib.pyplot as plt
import sys


def gridstart(N):
    X = np.linspace(0,1,N)
    Y = np.linspace(-3.1415,3.1415,N)
    A = []
    for x in X:
        for y in Y:
            A.append([x,y])
    A = np.array(A)
    return A

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import axes3d, Axes3D

import numpy as np
from math import cos

"""
pi = 3.1415026
alpha = 0.7
phi_ext = 2 * pi * 0.5

def flux_qubit_potential(phi_m, phi_p):
    #print phi_m.shape
    return phi_m
    return 2 * cos(phi_p)*cos(phi_m) - alpha * cos(phi_ext - 2*phi_p)
phi_m = np.linspace(0, 2*pi, 100)
phi_p = np.linspace(0, 2*pi, 100)
X,Y = np.meshgrid(phi_p, phi_m)
Z = flux_qubit_potential(X, Y).T

print X
"""
def GenTable(DataFs):
    X = DataFs.KList
    Y = DataFs.NumMachList
    NumForEach = DataFs.NumForEach;
    for Wei in DataFs.WeightChoice:
        print Wei
        print ','.join(map(str,Y))
        print ','.join(map(str,X))
        for row in xrange(len(X)):
            tmp = [];
            for col in xrange(len(Y)):
                mykey = (Wei,X[row],NumForEach,Y[col])
                if mykey in DataFs.results:
                    tmp.append( DataFs.results[mykey]['CostRatio'] );
                else:
                    tmp.append(-1)
            print ', '.join(map(lambda x: str(round(x,4)),tmp))


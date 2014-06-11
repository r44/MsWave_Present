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
def Draw3D(DataFs):
    RawX = np.array(sorted(DataFs.KList, reverse = True))
    RawX = np.array(DataFs.KList)
    print RawX
    RawY = np.array(DataFs.NumMachList)
    #X,Y = np.meshgrid(RawX, RawY)
    Y,X = np.meshgrid(RawY, RawX)
    print Y
    print X
    NumForEach = DataFs.NumForEach;
    for Wei in DataFs.WeightChoice:
        Z = np.zeros((len(RawX),len(RawY)))
        for row in xrange(len(RawX)):
            for col in xrange(len(RawY)):
                mykey = (Wei,RawX[row],NumForEach,RawY[col])
                Z[row][col] = DataFs.results[mykey]['CostRatio'];
        pi = 1
        print Wei
        print Z
        #fig = plt.figure(figsize=(8,6))
        fig = plt.figure()
        ax = Axes3D(fig)

        ax.set_title('Our/Naive Cost')
        ax.set_xlabel('K')
        ax.set_ylabel('Num of Machines')
        ax.plot_surface(X, Y, Z, rstride=4, cstride=4, alpha=0.25)
        cset = ax.contour(X, Y, Z, zdir='x', offset=-pi, cmap=cm.coolwarm)
        cset = ax.contour(X, Y, Z, zdir='y', offset=3*pi, cmap=cm.coolwarm)
        cset = ax.contour(X, Y, Z, zdir='z', offset=-pi, cmap=cm.coolwarm)


# set range for axis.
        """
        ax.set_xlim3d(-pi, 2*pi);
        ax.set_ylim3d(0, 3*pi);
        ax.set_zlim3d(-pi, 2*pi);
        ax.view_init(70, 30)
        """
#        ax.view_init(0, 135)
        Wei = Wei.replace("/","")
#        fig.savefig(Wei+".png")


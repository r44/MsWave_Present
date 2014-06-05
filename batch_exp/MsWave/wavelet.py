import sys
import numpy as np
from math import log

def wavelet2(T):
    W = np.zeros((T-1,T))
    
    for i in xrange(T/2):
        W[0,i] = 1
        W[0,T-i-1] = -1
    if T >= 4:
        ind1 = [1]+range(3,T/2+1)
        ind2 = [2]+range(T/2+1,T-1)
        W[ind1, :T/2] = wavelet2(T/2)
        W[ind2, T/2:] = wavelet2(T/2)
    return W

def wavelet1(T):
    W = np.zeros((T,T))

    W[0,:] = np.ones((1,T))
    if T > 1:
        W[1:,:] = wavelet2(T)

    for i in xrange(T):
        W[i,:] = W[i,:] / np.count_nonzero(W[i,:])

    return W

def wavelet(T):
    W = np.zeros((T,T))
    tmp = 0
    while tmp < T:
        t = 2**int(log(T-tmp,2))
        W[tmp:tmp+t,tmp:tmp+t] = wavelet1(t)
        tmp += t
    
    s = sorted( range(T), key=lambda x: -np.count_nonzero(W[x,:]) )

    return np.matrix(W[s,:])

if __name__ == '__main__':
    W = wavelet(int(sys.argv[1]))
    print W

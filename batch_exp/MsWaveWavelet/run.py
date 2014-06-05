import sys
import scipy.io as spio
from random import randrange
from random import seed
from MsWave import MsWave
from Site import Site
from numpy import *
from math import log

from wavelet import wavelet

def gen_pivot(data):
    T = data.shape[1]
    pivot = [int(T/4+T/16*i) for i in range(20) if T/4+T/16*i <= T]
    pivot[-1] = T
    return pivot

    pivot = [0]*int(log(T,2))
    t = 0
    while t < T:
        tmp = int(log(T-t,2))
        t += 2**tmp
        for i in range(tmp):
           pivot[-i-1] += max(2**(tmp-i-1),2)
    for i in range(1,len(pivot)):
        pivot[i] += pivot[i-1]

    return pivot

#main
k = 1
lenSeg = 500
nSeg = 400
N = lenSeg*nSeg

#data = (spio.loadmat('../LabelMe'))['data']
HomePath = '/nfs/master/01/r01922165/zzzzz/'
data = (spio.loadmat(HomePath+'ANNsift_base'))['data'].T

seed(304)
Q = 1

for svm5566 in range(1):
    q = [randrange(N) for i in range(Q)]
    #q = [4]

    print 'query id = ' + str(q)
    _query = matrix(data[q])

    sites = dict()
    query = dict()
    pivot = dict()
    for i in range(nSeg):
        W = wavelet(_query.shape[1]).T
        query[i] = _query*W

        s = i*lenSeg;
        e = s+lenSeg;
        cand = dict()
        for j in range(s,e):
            if j in q:
                continue
            cand[j] = ((data[j]*W).tolist())[0]

        pivot[i] = gen_pivot(data[s:e]*W)
        sites[i] = Site(i, cand.keys(), cand)

    print pivot[0]

    ans, cost, level_rs, qcost =  MsWave(k, query, sites, pivot)
    naive = size(_query)*nSeg + nSeg*k + k

    print level_rs
    print 'ans = ' + str(ans)
    print 'cost = '+str(cost)+'/'+str(naive)+'('+str(float(cost)/naive)+')'
    print 'qcost = '+str(qcost)
    print ''


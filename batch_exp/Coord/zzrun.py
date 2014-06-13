import sys
import scipy.io as spio
from random import randrange
from random import seed
from MsWave import MsWave
from Site import Site
from numpy import *

#sys.path.append('..')
#from wavelet_orth import wavelet

def gen_pivot(query, wdata):
    T = query.shape[1]
    
    pivot = [T/4+T/16+T/16*i for i in range(20) if T/4+T/16*i <= T]
    pivot[-1] = T
    return pivot

    norms1 = [query[0,k]**2 for k in xrange(T)]
    norms2 = [linalg.norm(wdata[:,k])**2 for k in xrange(T)]
    norm_all = sum(norms1)*sum(norms2)
    tmp1 = 0
    tmp2 = 0
    th = 0.9
    for j in range(T):
        tmp1 += norms1[j]
        tmp2 += norms2[j]
        if tmp1*tmp2/norm_all >= th:
            p90 = j
            break
    
    pivot = [p90+T/16*i for i in range(20) if p90+T/16*i <= T]
    pivot[-1] = T
    

    return pivot
    

#main
k = 1
lenSeg = 200
nSeg = 500
N = lenSeg*nSeg

HomePath = '/nfs/master/01/r01922165/zzzzz/'
FlickDir = 'Dataset/Image/Flickr/flickr/ParsedData/'

#data = (spio.loadmat('../LabelMe'))['data']
#data = (spio.loadmat('../ANNsift_base'))['data'].T
data = (spio.loadmat(HomePath+FlickDir+'2_ColorStruct256'))['data']

T = data.shape[1]

seed(304)
Q = 1

#path = '../trans_ANN/Weights/500_400/'
path = '/nfs/master/01/r01922165/zzzzz/trans_flickr/2/200_5000/'
folder = ['origin/','2_heur/']

for svm5566 in range(1):
    #q = [randrange(N) for i in range(Q)]
    q = [4]
    print 'query id = ' + str(q)
    
    _query = matrix(data[q])
    sites = dict()
    query = dict()
    pivot = dict()
    
    for i in range(nSeg):
        #W = matrix( (spio.loadmat('../trans/X_'+str(lenSeg)+'_'+str(i+1)))['X'] ).T
        W = matrix( (spio.loadmat(path+folder[1]+'X_'+str(lenSeg)+'_'+str(i+1)))['X'] ).T
        #W = matrix( (spio.loadmat('/nfs/master/01/r01922165/zzzzz/trans_flickr/1/200_5000/origin/X_'+str(lenSeg)+'_'+str(i+1)))['X'] ).T
        #W = wavelet(192)
        
        query[i] = _query*W

        s = i*lenSeg;
        e = s+lenSeg;
        cand = dict()
        for j in range(s,e):
            if j in q:
                continue
            cand[j] = ((data[j]*W).tolist())[0]
        
        pivot[i] = gen_pivot(query[i],data[s:e]*W)
        sites[i] = Site(i, cand.keys(), cand)
    
    ans, cost, level_rs, qcost =  MsWave(k, query, sites, pivot)
    naive = size(_query)*nSeg + nSeg*k + k

    print level_rs
    print 'ans = ' + str(ans)
    print 'cost = '+str(cost)+'/'+str(naive)+'('+str(float(cost)/naive)+')'
    print 'qcost = '+str(qcost)
    print ''

'''
d = []
for i in xrange(N):
    tmp = 0;
    for l in xrange(Q):
        tmp += sum( (k-j)**2 for (k,j) in zip(_query[l,:].tolist()[0], data[i]) )**0.5
    d.append(tmp)

a = sorted( xrange(N), key=lambda k: d[k] )
sys.stderr.write('\n')
a = [i for i in a if i not in q]
print a[:k]
'''


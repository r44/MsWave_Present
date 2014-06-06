import sys
import scipy.io as spio
import numpy as np

lenSeg = 500
nSeg = 200
N = lenSeg*nSeg

data = (spio.loadmat('../ANNsift_base'))['data'].T
T = data.shape[1]

path = '../trans_ANN/Weights/500_200/'
folder = ['3_SimpDiv/','4_Half/','5_Quad/','6_Half10/','7_HalfQuad/','origin/']

for ff in range(4,5):

    first = []
    second = []
    quartile = []
    third = []
    onetenth = []
    half = []
    percent90 = []

    for i in range(nSeg): #xrange(nSeg):
        W = np.matrix( (spio.loadmat(path+folder[ff]+'/X_'+str(lenSeg)+'_'+str(i+1)))['X'] ).T
        
        s = i*lenSeg;
        e = s+lenSeg;
        wdata = data[s:e]*W
        
        norms = [np.linalg.norm(wdata[:,k])**2 for k in xrange(T)]
        norm_all = sum(norms)
        tmp = 0
        ratio = []
        
        aa = 0
        for j in range(T):
            tmp += norms[j]
            ratio.append( tmp/norm_all )
            
            if aa == 0 and tmp/norm_all > 0.90:
                percent90.append(j)
                aa = 1
        
        first.append(ratio[0])
        second.append(ratio[1])
        third.append(ratio[2])
        onetenth.append(ratio[int(T/2)])
        quartile.append(ratio[int(T/2+T/10)])
        half.append(ratio[int(T/2+T/5)])
    
    print folder[ff]
    print 'first', np.mean(first), min(first), max(first)
    print 'secon', np.mean(second), min(second), max(second)
    print 'third', np.mean(third), min(third), max(third)
    print 'onete', np.mean(onetenth), min(onetenth), max(onetenth)
    print 'quart', np.mean(quartile), min(quartile), max(quartile)
    print '_half', np.mean(half), min(half), max(half)
    print '90%: ', np.mean(percent90), min(percent90), max(percent90)
    print ''









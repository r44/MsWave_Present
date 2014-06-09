import sys
import scipy.io as spio
#from random import randrange
from random import sample
from random import seed
sys.path.append('..')
from MsWave import MsWave
from Site import Site
from numpy import *
from math import log
import csv

from wavelet import wavelet

def gen_pivot():
    T = data.shape[1]
    pivot = [0]*int(log(T,2))
    t = 0
    while t < T:
        tmp = int(log(T-t,2))
        t += 2**tmp
        for i in range(tmp):
           pivot[-i-1] += max(2**(tmp-i-1),2)
    for i in range(1,len(pivot)):
        pivot[i] += pivot[i-1]
    if pivot[len(pivot)-1] != T:
        pivot.append(T);
    return pivot

#main
#################################################################################

# Paramaters which wouldn't be changed.

#data = (spio.loadmat('../LabelMe'))['data']
HomePath = '/nfs/master/01/r01922165/zzzzz/'
data = (spio.loadmat(HomePath+'ANNsift_base'))['data'].T
"""
#FlickDir = 'Dataset/Image/Flickr/flickr/ParsedData/'
OutPath = HomePath+'Results/Exp0605/Flickr/500_2000/MsWave/'
FeaType=1
if FeaType == 1:
    data = (spio.loadmat(HomePath+FlickDir+'1_ColorLayout192'))['data']
elif FeaType == 2:
    data = (spio.loadmat(HomePath+FlickDir+'2_ColorStruct256'))['data']
elif FeaType == 3:
    data = (spio.loadmat(HomePath+FlickDir+'3_ScalColor256'))['data']
elif FeaType == 4:
    data = (spio.loadmat(HomePath+FlickDir+'4_HomoText43'))['data']
elif FeaType == 5:
    data = (spio.loadmat(HomePath+FlickDir+'5_EdgeHist150'))['data']
OutFile = OutPath+str(FeaType)+'_0605.csv'
"""
OutPath = HomePath+'Results/Exp0605/ANN_SIFT/200_5000/MsWave/'
OutFile = OutPath+'0605_above2k.csv'
fout = open(OutFile,'wb')
headers = 'qid NumMachine NumForEach k LevelRs Pivots RepeatTime NaiveCost Cost QCost'.split()
dw = csv.DictWriter(fout,headers,restval='NULL');
dw.writeheader()
fout.close()

seed(302)
FeaLen = data.shape[1]
Total = data.shape[0]
W = wavelet(FeaLen).T
RepeatTime = 30;
QList = sample(xrange(Total), RepeatTime)

#################################################################################
# Paramaters to be tuned.

"""
kList = [1,5,10,15,20]
NumForEachList = [100,200,300,400,500]
NumMachList = [100,500,1000,1500,2000]
kList = [2]
NumMachList = [2]
NumForEachList = [2]
"""
kList = [1,5,10,15,20]
NumForEachList = [200]
#NumMachList = [100,500,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000]
NumMachList = range(2200,5001,200)
#################################################################################

record = dict()
for NumMach in NumMachList:
    record['NumMachine']=NumMach;
    # Gen pivot.
    pivot = dict()
    tmp_pivot = gen_pivot()
    for mid in range(NumMach):
        pivot[mid] = tmp_pivot
    record['Pivots'] = '_'.join(str(x) for x in tmp_pivot)
    del tmp_pivot

    for NumForEach in NumForEachList:
        record['NumForEach']=NumForEach
        # Distribute data to each site
        sites = dict()
        for mid in range(NumMach):
            s = mid*NumForEach;
            e = s+NumForEach;
            cand = dict()
            for j in range(s,e):
                if j in QList:
                    continue
                cand[j] = ((data[j]*W).tolist())[0]
            sites[mid] = Site(mid, cand.keys(), cand)

        for k in kList:
            record['k']=k
            for time in xrange(len(QList)):
                qid = QList[time]
                record['qid'] = qid
                _query = matrix(data[qid])*W

                query = dict()
                for i in range(NumMach):
                    query[i] = _query
                ans, cost, level_rs, qcost =  MsWave(k, query, sites, pivot)
                naive = size(_query)*NumMach + NumMach*k + k
                record['Cost'] = cost
                record['QCost'] = qcost
                record['NaiveCost']=naive
                record['LevelRs'] = '_'.join(str(x) for x in level_rs)
                record['RepeatTime']=time
                del query
                fout = open(OutFile,'ab')
                dw = csv.DictWriter(fout,headers,restval='NULL');
                dw.writerow(record)
                fout.close()
                for mid in range(NumMach):
                    sites[mid].init_except_data();
            print record
        del sites
fout.close()

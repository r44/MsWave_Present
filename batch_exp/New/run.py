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

def gen_pivot(data,fname):
    T = data.shape[1]
    print T
    print fname
    if fname == '3_SimpDiv/':
        pivot = [int(T*0.1*(i+1)) for i in range(10)]
    elif fname == '4_Half/':
        pivot = [int(T*0.2*(i+1)) for i in range(5)]
    elif fname == '5_Quad/':
        pivot = [int(T*0.25*(i+1)) for i in range(4)]
    elif fname == '6_Half10/':
        pivot = [int(T*0.1*(i+1)) for i in range(4,10)]
    elif fname == '7_HalfQuad/':
        pivot = [int(T*0.25*(i+1)) for i in range(1,4)]
    elif fname == '9_Five/':
        pivot = [int(T*0.05*(i+1)) for i in range(20)]
    elif fname == 'origin/':
        pivot = [int(T/4+T/16*i) for i in range(20) if T/4+T/16*i <= T]

    pivot[-1] = T

    return pivot

#main
#################################################################################

# Paramaters which wouldn't be changed.

#data = (spio.loadmat('../LabelMe'))['data']
HomePath = '/nfs/master/01/r01922165/zzzzz/'
FlickDir = 'Dataset/Image/Flickr/flickr/ParsedData/'
data = (spio.loadmat(HomePath+'ANNsift_base'))['data'].T
WeightPath = HomePath+'trans_ANN/Weights/'

#MaxNumMach = 2000;
MaxNumMach = 400;
MaxNumForEach = 500;
OutPath = HomePath+'Results/Exp0605/Flickr/500_2000/MsWave/'
path = HomePath+'trans_ANN/Weights/500_400/'
folder = ['origin/']
"""
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
fout = open(OutFile,'wb')
headers = 'qid NumMachine NumForEach k LevelRs Pivots RepeatTime NaiveCost Cost QCost'.split()
dw = csv.DictWriter(fout,headers,restval='NULL');
dw.writeheader()
fout.close()
"""

seed(304)
FeaLen = data.shape[1]
Total = data.shape[0]
RepeatTime = 30;
RepeatTime = 5;
#QList = sample(xrange(Total), RepeatTime)
QList = [4 ,4 ,4 ,4 ,7]

WDict = dict();
for mid in range(MaxNumMach):
    WDict[mid] = matrix( (spio.loadmat(path+folder[0]+'X_'+str(MaxNumForEach)+'_'+str(mid+1)))['X'] ).T
#################################################################################
# Paramaters to be tuned.

"""
kList = [1,5,10,15,20]
NumForEachList = [100,200,300,400,500]
NumMachList = [100,500,1000,1500,2000]
"""
kList = [1]
NumMachList = [40]
NumForEachList = [500]
#################################################################################
record = dict()
for NumMach in NumMachList:
    record['NumMachine']=NumMach;
    # Gen pivot.
    pivot = dict()
    tmp_pivot = gen_pivot(data,folder[0])
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
                cand[j] = ((data[j]*WDict[mid]).tolist())[0]
            sites[mid] = Site(mid, cand.keys(), cand)

        for time in xrange(len(QList)):
            qid = QList[time]
            record['qid'] = qid
            query = dict()
            for mid in range(NumMach):
                query[mid] = matrix(data[qid])*WDict[mid]
            for k in kList:
                record['k']=k
                ans, cost, level_rs, qcost =  MsWave(k, query, sites, pivot)
                naive = size(query[0])*NumMach + NumMach*k + k
                record['Cost'] = cost
                record['QCost'] = qcost
                record['NaiveCost']=naive
                record['LevelRs'] = '_'.join(str(x) for x in level_rs)
                record['RepeatTime']=time
                del query
                """
                fout = open(OutFile,'ab')
                dw = csv.DictWriter(fout,headers,restval='NULL');
                dw.writerow(record)
                fout.close()
                """
                for mid in range(NumMach):
                    sites[mid].init_except_data();
            print record
#fout.close()

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
from scipy.interpolate import interp1d
import CoordDescent as cd

def gen_pivot(data):
    T = data.shape[1]
    # Origin
    pivot = [int(T/2+T/32*i) for i in range(40) if T/2+T/32*i <= T]
    pivot[-1] = T
    return pivot

def update_pivot(level_rs, pivot, cnt, level_rs_est):
    level_rs += [1] * (len(pivot) - len(level_rs))
    f = interp1d( pivot, level_rs, kind='linear')
    tmp = f( range(0,len(level_rs_est)) )
    return [ (cnt*old + new)/(cnt+1) for (old,new) in zip(level_rs_est, tmp) ]



#main
#################################################################################

# Paramaters which wouldn't be changed.

#data = (spio.loadmat('../LabelMe'))['data']
HomePath = '/nfs/master/01/r01922165/zzzzz/'
data = (spio.loadmat(HomePath+'ANNsift_base'))['data'].T
FlickDir = 'Dataset/Image/Flickr/flickr/ParsedData/'
WeightPath = HomePath+'trans_ANN/Weights/500_400/'
WeightPath = HomePath+'trans_ANN/Weights/200_5000/'
OutPath = HomePath+'Results/Exp0605/Flickr/500_2000/New/'
OutPath = HomePath+'Results/Exp0614/ANN_SIFT/New/'
FeaType=0
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
#OutFile = OutPath+str(FeaType)+'_0605.csv'
OutFile = OutPath+'0614_11.csv'
fout = open(OutFile,'wb')
headers = 'qid WChoice NumMachine NumForEach k LevelRs Pivots RepeatTime MatCost NaiveCost Cost QCost'.split()
dw = csv.DictWriter(fout,headers,restval='NULL');
dw.writeheader()
fout.close()

seed(302)
MaxNumMach = 5000;
MaxNumForEach = 200;
#WeightPath = HomePath+'trans_flickr/'+str(FeaType)+'/'+str(MaxNumForEach)+'_'+str(MaxNumMach)+'/'
FeaLen = data.shape[1]
Total = data.shape[0]
RepeatTime = 100;
QList = sample(xrange(Total), RepeatTime)

#################################################################################
# Paramaters to be tuned.

# Para for Exp 0605.
kList = [1,10,20]
NumForEachList = [MaxNumForEach]
NumMachList = [2500,3000,3500]; #1
WChoiceList = [2]   #1
"""

# Para for testing.
kList = [1,2]
NumMachList = [400]
NumForEachList = [500]
WChoiceList = [1]
"""
#################################################################################
record = dict()
record['MatCost'] = FeaLen * (FeaLen-1) / 2;
for WChoice in WChoiceList:
    if WChoice == 1:
        record['WChoice']='origin/';
    elif WChoice == 2:
        record['WChoice']='2_heur/';
    else:
        'Wchoice error'
        exit()
    # Initialize weight matrics.
    WDict = dict();
    for mid in range(MaxNumMach):
        WDict[mid] = matrix( (spio.loadmat(WeightPath + record['WChoice'] +'X_'+str(MaxNumForEach)+'_'+str(mid+1)))['X'] ).T

    for NumMach in NumMachList:
        record['NumMachine']=NumMach;
        # Gen pivot.
        pivot = dict()
        tmp_pivot = gen_pivot(data)
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


            for k in kList:
                record['k'] = k

                cnt = 0
                level_rs_est = [0] * (FeaLen+1)
                for time in xrange(len(QList)):
                    qid = QList[time]
                    record['qid'] = qid
                    query = dict()

                    for mid in range(NumMach):
                        query[mid] = matrix(data[qid])*WDict[mid]

                    ans, cost, level_rs, qcost =  MsWave(k, query, sites, pivot)
                    naive = size(query[0])*NumMach + NumMach*k + k
                    record['Cost'] = cost
                    record['QCost'] = qcost
                    record['NaiveCost']=naive
                    record['LevelRs'] = '_'.join(str(x) for x in level_rs)
                    record['RepeatTime']=time
                    record['Pivots'] = '_'.join(str(x) for x in pivot[0])
                    fout = open(OutFile,'ab')
                    dw = csv.DictWriter(fout,headers,restval='NULL');
                    dw.writerow(record)
                    fout.close()
                    """
                    level_rs_est = update_pivot( [NumMach]+level_rs, [0]+pivot[0], cnt, level_rs_est )
                    cnt += 1
                    new_pivot = cd.CoordDescent(level_rs_est, pivot[0])
                    for g in range(NumMach):
                        pivot[g] = new_pivot
                    """
                    for mid in range(NumMach):
                        sites[mid].init_except_data();
                    print record
                    del query
            del sites
    del WDict
#fout.close()

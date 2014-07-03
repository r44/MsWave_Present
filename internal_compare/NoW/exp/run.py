import sys
import os
import scipy.io as spio
#from random import randrange
from random import sample
from random import seed
sys.path.append('../../../code/')
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
    #pivot = [int(T/2+T/4*i) for i in range(40) if T/2+T/4*i <= T]
    pivot = [int(T/10+T/10*i) for i in range(40) if T/10+T/10*i <= T]
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
HomePath = '/tmp3/r445566/zzzzz/'
DataPath = 'Dataset/'
WeightPath = 'Trans/'
boolTrans = int(sys.argv[1])
boolCD = int(sys.argv[2])
#################################################################################
FeaName = os.getcwd().split('/')[-2]
if FeaName == 'time':
    MaxNumForEach = 200;    MaxNumMach = 5000; StepRange = 500;
elif FeaName == 'ANN':
    MaxNumForEach = 200;    MaxNumMach = 5000; StepRange = 500;
elif FeaName == 'f2':
    MaxNumForEach = 500;    MaxNumMach = 2000; StepRange = 200;
elif FeaName == 'f3':
    MaxNumForEach = 500;    MaxNumMach = 2000; StepRange = 200;
elif FeaName == 'mvd':
    MaxNumForEach = 500;    MaxNumMach = 1900; StepRange = 200;
elif FeaName == 'trh':
    MaxNumForEach = 500;    MaxNumMach = 1900; StepRange = 200;
else:
    print "FeaType Error.";    exit();
#################################################################################
OutFile = sys.argv[0].split('/')[-1]+str('.out')
fout = open(OutFile,'wb')
headers = 'qid WChoice NumMachine NumForEach k LevelRs Pivots RepeatTime MatCost NaiveCost Cost QCost EstResSite'.split()
dw = csv.DictWriter(fout,headers,restval='NULL');
dw.writeheader()
fout.close()
print "Init output file done."
#################################################################################
data = (spio.loadmat(HomePath+DataPath+FeaName))['data']
seed(302)
FeaLen = data.shape[1]; Total = data.shape[0]; RepeatTime = 100;
QList = sample(xrange(Total), RepeatTime)
#################################################################################
# Paramaters to be tuned.
kList = [1,10,20]
NumForEachList = [MaxNumForEach]
NumMachList = [x for x in range(StepRange,MaxNumMach+1,StepRange)]
NumMachList[-1] = MaxNumMach
#################################################################################
record = dict()
record['MatCost'] = FeaLen * (FeaLen-1) / 2;

# Initialize weight matrics.
WDict = dict();
for mid in range(MaxNumMach):
    if boolTrans == 1:
        WDict[mid] = matrix( (spio.loadmat(HomePath+WeightPath+FeaName+'/' +'X_'+str(MaxNumForEach)+'_'+str(mid+1)))['X'] ).T
    else:
        WDict[mid] = matrix(eye(FeaLen))
print 'Read W done.'
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

                if boolCD == 1:
                    level_rs_est = update_pivot( [NumMach]+level_rs, [0]+pivot[0], cnt, level_rs_est )
                    if time % 100 == 0:
                        record['EstResSite'] = '_'.join(map(lambda x:str(round(x,4)),level_rs_est))
                    else:
                        record['EstResSite'] = -1;
                    cnt += 1
                    new_pivot = cd.CoordDescent(level_rs_est, pivot[0])
                    for g in range(NumMach):
                        pivot[g] = new_pivot
                else:
                    pass

                for mid in range(NumMach):
                    sites[mid].init_except_data();
                print record
                del query
        del sites
del WDict
fout.close()

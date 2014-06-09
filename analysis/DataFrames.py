import csv
import collections

from itertools import groupby
import pprint   # pretty print for list
import operator

import numpy as np
import scipy as sp

class DataFrames:
    def __init__(self,filename):
## Parse the raw csv file to get the range of each parameter and the data as list of tuples.
        KDict = collections.defaultdict(bool)
        QidDict = collections.defaultdict(bool)
        NumMachDict = collections.defaultdict(bool)
        NumForEachDict = collections.defaultdict(bool)
        WeiDict = collections.defaultdict(bool)
        TimeDict = collections.defaultdict(bool)

        data = list()
        with open(filename,'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for rowdict in reader:
                k = int(rowdict['k']); qid = int(rowdict['qid']); NumForEach = int(rowdict['NumForEach']);
                NumMach = int(rowdict['NumMachine']); Wei = rowdict['WChoice']; Timeidx = int(rowdict['RepeatTime']);
                Pivots = [int(x) for x in rowdict['Pivots'].split('_')]; LevelRs = [int(x) for x in rowdict['LevelRs'].split('_')]
                KDict[ k ] = QidDict[ qid ] = NumForEachDict[ NumForEach ] = NumMachDict[ NumMach ] = WeiDict[ Wei ] = TimeDict[ Timeidx ] = True
                #data.append( (k,NumForEach,NumMach,Wei,Timeidx,qid,Pivots,LevelRs) )
                rowdict['k'] = k;
                rowdict['qid'] = qid;
                rowdict['NumForEach'] = NumForEach;
                rowdict['NumMachine'] = NumMach;
                rowdict['WChoice'] = Wei;
                rowdict['RepeatTime'] = Timeidx;
                rowdict['Pivots'] = Pivots;
                self.NumLevel = len(Pivots)
                rowdict['LevelRs'] = LevelRs;
                rowdict['Cost'] = int(rowdict['Cost'])
                rowdict['QCost'] = int(rowdict['QCost'])
                rowdict['MatCost'] = int(rowdict['MatCost'])
                self.MatCost = rowdict['MatCost']
                rowdict['NaiveCost'] = int(rowdict['NaiveCost'])
                data.append(rowdict)

        self.KList = sorted(KDict.keys())
        self.QidList = sorted(QidDict.keys())
        self.NumForEachList = sorted(NumForEachDict.keys())
        self.NumMachList = sorted(NumMachDict.keys())
        self.RepeatTime = max(TimeDict.keys())
        self.WeightChoice = WeiDict.keys()
        self.data = data;

    def SimpStat(self):
        #pprint.pprint( self.data)


        sortkeyfn = operator.itemgetter('k','NumForEach','NumMachine','WChoice');
        self.data.sort(key=sortkeyfn);  # Need sort before groupby.

        results = collections.defaultdict(dict);
        for key, group in groupby(self.data, key = sortkeyfn):
            Cost = []; NaiveCost = []; RsList = list();
            for row in group:
                Cost.append(row['Cost'])
                NaiveCost.append(row['NaiveCost'])
                tmp_arr = np.zeros(self.NumLevel)
                for i in xrange(len(row['LevelRs'])):
                    tmp_arr[i] = row['LevelRs'][i]
                RsList.append(tmp_arr)
            results[key] = {'Cost':np.array(Cost), 'NaiveCost':np.array(NaiveCost), 'LevelRs':np.array(RsList)}

        for key,value in results.iteritems():
            print value['LevelRs'].shape
        print self.NumLevel

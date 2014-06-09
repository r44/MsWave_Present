import csv
import collections

from itertools import groupby
import pprint   # pretty print for list
import operator

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
                rowdict['LevelRs'] = LevelRs;
                rowdict['Cost'] = int(rowdict['Cost'])
                rowdict['QCost'] = int(rowdict['QCost'])
                rowdict['MatCost'] = int(rowdict['MatCost'])
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
        print self.data
        print 'g'
        print self.data.sort(key=operator.itemgetter(('k','qid')));
        print self.data
        results = [];
        sortkeyfn = key=lambda s:s[0:6]
#        for key,

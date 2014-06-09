import csv
import collections

from itertools import groupby
import DataFrames
from Draw3D import Draw3D

def AnalyzeFile(filename):
## Start to analyze the file.
    DataFs = DataFrames.DataFrames(filename)
    DataFs.SimpStat()
#    DataFs.PrintStat()
    Draw3D(DataFs)


def main():
    MaxNumMachine = 5000; MaxNumForEach = 200;
    ExpPath = '/nfs/master/01/r01922165/zzzzz/Results/'
    ExpDir = 'Exp0605/'
    ExpData = 'ANN_SIFT/'
    ExpSize = str(MaxNumForEach)+'_'+str(MaxNumMachine)+'/'
    MethodChoice = 0;
    if MethodChoice == 0:
        Method = 'New/'
    elif MethodChoice ==1:
        Method = 'MsWave/'
    else:
        pass
    File = '0605.csv'
    AnalyzeFile(ExpPath+ExpDir+ExpData+ExpSize+Method+File);

    print 'ker'

if __name__ == '__main__':
    main()

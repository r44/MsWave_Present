import csv
import collections

from itertools import groupby
import DataFrames
from Draw3D import Draw3D
from GenTable import GenTable
def AnalyzeFile(filename):
## Start to analyze the file.
    DataFs = DataFrames.DataFrames(filename)
    DataFs.SimpStat()
    #DataFs.PrintStat()
    #Draw3D(DataFs)
    GenTable(DataFs)


def main():
    ExpPath = '/nfs/master/01/r01922165/zzzzz/Results/'
    ExpDir = 'Exp0605/'
    ExpDir = '0605_copy/'
    DataType = 2
    if DataType == 1:
        ExpData = 'ANN_SIFT/'
        MaxNumMachine = 5000; MaxNumForEach = 200;
    elif DataType == 2:
        ExpData = 'Flickr/'
        MaxNumMachine = 2000; MaxNumForEach = 500;
    else:
        exit()

    ExpSize = str(MaxNumForEach)+'_'+str(MaxNumMachine)+'/'
    MethodChoice = 0;
    if MethodChoice == 0:
        Method = 'New/'
    elif MethodChoice ==1:
        Method = 'MsWave/'
    else:
        exit()
    FeaType = 1;
    File = str(FeaType)+'_0605.csv'
    #File = '0605_above2k.csv'
    AnalyzeFile(ExpPath+ExpDir+ExpData+ExpSize+Method+File);

    print 'ker'

if __name__ == '__main__':
    main()

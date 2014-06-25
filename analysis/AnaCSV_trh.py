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
    ExpPath = '/nfs/master/01/r01922165/zzzzz/src/batch_exp/Coord/Exp0618_trh/'
    gg=1
    if gg == 1:
        File1 = '2test.csv'
        File2 = '0623_01.csv'
    else:
        File1 = '2_11test.csv'
        File2 = '0623_11.csv'
    print File1
    AnalyzeFile(ExpPath+File1);
    print File2
    AnalyzeFile(ExpPath+File2);
    """
    for i in range(3):
        for j in range(2):
            File = '0614_'+str(i)+str(j)+'.csv'
            print File
            AnalyzeFile(ExpPath+ExpDir+ExpData+Method+File);
    """
    print 'ker'

if __name__ == '__main__':
    main()

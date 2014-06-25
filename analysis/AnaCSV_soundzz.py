import sys
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
    #ExpPath = '/nfs/master/01/r01922165/zzzzz/Results/'
    ExpPath = '/nfs/undergrad/98/b98902105/Results/Exp0618/'
    DataType = 2
    if DataType == 1:
        ExpData = 'sound_mvd/'
        MaxNumMachine = 1900; MaxNumForEach = 500;
    elif DataType == 2:
        ExpData = 'sound_trh/'
        MaxNumMachine = 1900; MaxNumForEach = 500;
    else:
        exit()

    #ExpSize = str(MaxNumForEach)+'_'+str(MaxNumMachine)+'/'
    """
    MethodChoice = 2;
    if MethodChoice == 0:
        Method = 'New/'
    elif MethodChoice ==1:
        Method = 'MsWave/'
    elif MethodChoice ==2:
        Method = 'Coord/'
    else:
        exit()
    FeaType = 1;

    #File = str(FeaType)+'_0605.csv'
    #File = '0605_above2k.csv'
    #AnalyzeFile(ExpPath+ExpDir+ExpData+ExpSize+Method+File);
    File = '0614_20_1k.csv'
    """
    WChoice = 1;
    if WChoice == 0:    # origin
        File1 = '0618_00.csv'
        File2 = '0618_10.csv'
    elif WChoice == 1:  # heuristic
        File1 = '0618_01.csv'
        File2 = '0618_11.csv'
    else:
        print 'GG'
        exit()

    print File1
    AnalyzeFile(ExpPath+ExpData+File1);
    print File2
    AnalyzeFile(ExpPath+ExpData+File2);
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

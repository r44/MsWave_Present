import arff
import numpy as np
def Arff2Mat(filename):
    ddd=0
    alldata = []
    for row in arff.load(filename):
        tmpdata = [x for x in row if type(x) != str];
        alldata.append(tmpdata)
        """
        print row
        print len(tmpdata)
        print len(row)
        ddd+=1
        if ddd > 30:
        #    print alldata
            print len(alldata[0])
        """
    return np.array(alldata)

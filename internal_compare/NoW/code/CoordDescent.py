import math
def GenPivots(_StartD,_EachLenD,TotalD):
    MaxItr = int(math.ceil(float(TotalD - _StartD) / _EachLenD));
    pivots = [_StartD+_EachLenD*x for x in xrange(MaxItr) if (_StartD+_EachLenD*x)<=TotalD-1]
    pivots[-1] = TotalD-1;
    return pivots

def Loss(EstResSite, _StartD, _EachLenD):
## Calculating Loss value for the current setting.
    TotalD = len(EstResSite);
    pivots = GenPivots(_StartD, _EachLenD, TotalD)
    TotalLoss = EstResSite[0]*(pivots[0] + 4);
    for idx in xrange(1,len(pivots)):
        Ti = pivots[0] if idx == 0 else (pivots[idx]-pivots[idx-1])
        ResNumSite = EstResSite[pivots[idx-1]]; # M
        TotalLoss += ResNumSite*(Ti+4)
    return TotalLoss

def CoordDescent(EstResSite, Pivots):
## Coordinate descent for our loss function.
# EstResSite: D dimension list where d-th value is the estimate number of residual candidate site.
# StartD: The starting dimension to send the query. value = 0~TotalD-1
# EachLenD: The len of each segment dimension.

    StartD = Pivots[0];
    EachLenD = 0 if len(Pivots) == 1 else Pivots[1] - Pivots[0];
    # Total len of vector.
    TotalD = len(EstResSite);
    best_obj = Loss(EstResSite, StartD, EachLenD)

    while True:
#        print StartD, EachLenD
        flag1 = False;
        flag2 = False;
        # 0. Fix EachLenD, Descent for StartD
        beg = int(StartD/2.0);
        fin = min(StartD+beg, TotalD);
        for d in xrange(beg,fin):
            tmp_obj = Loss(EstResSite, d, EachLenD)
            if best_obj > tmp_obj:
                best_obj = tmp_obj;
                StartD = d;
                flag1 = True

        # 1. Fix Start, Descent for EachLenD
        beg = int(EachLenD/2.0)
        fin = min(TotalD-StartD, EachLenD+beg)
        for d in xrange(beg,fin):
            tmp_obj = Loss(EstResSite, StartD, d)
            if best_obj > tmp_obj:
                best_obj = tmp_obj;
                EachLenD = d;
                flag2 = True
        if flag1 == False and flag2 == False:
            break
    return GenPivots(StartD, EachLenD, TotalD)

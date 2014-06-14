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
        flag = False; offset = 0;
        # 0. Fix EachLenD, Descent for StartD
        dir_p_obj = Loss(EstResSite, StartD+1, EachLenD); dir_n_obj = Loss(EstResSite, StartD-1, EachLenD);
        if best_obj <= dir_p_obj and best_obj <= dir_n_obj:
            flag = True
            pass
        elif dir_p_obj < dir_n_obj:
            best_obj = dir_p_obj;
            fin = TotalD; offset = 1;
        else:    # dir_p_obj > dir_n_obj
            best_obj = dir_n_obj;
            fin = 0; offset = -1;
        if not offset == 0:
            StartD = StartD + offset; beg = StartD + offset;
            for d in xrange(beg,fin,offset):
                tmp_obj = Loss(EstResSite, d, EachLenD)
                if best_obj > tmp_obj:
                    best_obj = tmp_obj;
                    StartD = d;
        offset = 0;
        # 1. Fix Start, Descent for EachLenD
        dir_p_obj = Loss(EstResSite, StartD, EachLenD+1); dir_n_obj = Loss(EstResSite, StartD, EachLenD-1);
        if best_obj <= dir_p_obj and best_obj <= dir_n_obj:
            if flag == True:
                break
            pass
        elif dir_p_obj < dir_n_obj:
            best_obj = dir_p_obj;
            fin = TotalD-StartD; offset = 1;
        else:    # dir_p_obj > dir_n_obj
            best_obj = dir_n_obj;
            fin = 1; offset = -1;
        if not offset == 0:
            EachLenD = EachLenD + offset; beg = EachLenD + offset;
            for d in xrange(beg,fin,offset):
                tmp_obj = Loss(EstResSite, StartD, d)
                if best_obj > tmp_obj:
                    best_obj = tmp_obj;
                    EachLenD = d;
    return GenPivots(StartD, EachLenD, TotalD)

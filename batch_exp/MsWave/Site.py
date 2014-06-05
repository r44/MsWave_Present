import numpy
from math import log

class Site:

    def __init__(self, siteid, candlist, cand):
        self.siteid = siteid
        self.candlist = candlist
        self.cand = cand
        self.accdist = dict()
        self.qssum = 0
        self.qwssum = 0
        self.k = 0
        self.ub = 0
        self.lb = 0
        self.T = len(cand[candlist[0]])

    def cp_first(self, query, s, e, qssum, qwssum, k):
        self.k = k
        self.qssum = qssum
        self.qwssum = qwssum
        for sid in self.candlist:
            self.accdist[sid] = dict()
            for q in range(query.shape[0]):
                self.accdist[sid][q] = sum( (i-j)**2 for (i,j) in zip(query[q,:].tolist()[0], self.cand[sid][s:e]))*2**(log(self.T,2)-int(log(max(1,s),2)))
        self.ub, self.lb = self.cal_bound( query, e)
        return sorted(self.ub.values())[:self.k]

    def cp_later(self, query, s, e):
        for q in range(query.shape[0]):
            self.qssum[q] -= sum( i**2 for i in query[q,:].tolist()[0])
            self.qwssum[q] -= sum( query[q,j]**2 * 2**(log(self.T,2)-int(log(j+s,2))) \
                    for j in range(e-s) )
            if e == self.T:
                self.qssum[q] = 0
                self.qwssum[q] = 0

        for sid in self.candlist:
            for q in range(query.shape[0]):
                self.accdist[sid][q] += sum( (i-j)**2 for (i,j) in zip(query[q,:].tolist()[0], self.cand[sid][s:e]))*2**(log(self.T,2)-int(log(s,2)))
        self.ub, self.lb = self.cal_bound( query, e)
        return sorted(self.ub.values())[:self.k]

    def cal_bound(self,query,e):
        ub = dict()
        lb = dict()
        for sid in self.candlist:
            ub_tmp = dict()
            lb_tmp = dict()
            wcssum = sum( v**2 * 2**(log(self.T,2)-int(log(j,2))) for (v,j) in zip(self.cand[sid][e:],range(e,self.T)) )
            cwssum = sum( (v*2**(log(self.T,2)-int(log(j,2))))**2 for (v,j) in zip(self.cand[sid][e:],range(e,self.T)) )
            for q in range(query.shape[0]):
                lb_tmp[q] = self.accdist[sid][q]
                ub_tmp[q] = self.accdist[sid][q] + self.qwssum[q] + wcssum
                ub_tmp[q] += 2*(self.qssum[q] * cwssum )**0.5
            ub[sid] = sum( v**0.5 for v in ub_tmp.values() )
            lb[sid] = sum( v**0.5 for v in lb_tmp.values() )
            
        return ub, lb

    def prune(self, th):
        self.candlist = [sid for sid in self.candlist if self.lb[sid] <= th]
        return len(self.candlist)
    
    def get_ans(self):
        return self.candlist


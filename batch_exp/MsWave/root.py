from math import log
import heapq
import numpy

class root:

    def __init__(self, k, query, pivot):
        self.done = False

        self.ub = []
        self.rc = 0
        self.rs = dict()

        self.k = k
        self.query = query
        self.nquery = query[0].shape[0]
        self.T = query[0].shape[1]

        self.pivot = pivot
        #self.pivot = [T/4+T/16*i for i in range(20) if T/4+T/16*i <= T]
        #self.pivot = [T/16+T/32*i for i in range(20) if T/16+T/32*i <= T]
        #self.pivot = [2**i for i in range(20) if 2**i <= T]
        #self.pivot[-1] = T

        self.level = 0
        self.maxlevel = max(len(p) for p in self.pivot.values())-1

    def send_first(self, siteid):
        self.rs[siteid] = 0
        s = 0
        e = self.pivot[siteid][0]
        query = self.query[siteid]

        qssum = [ sum( query[i,j]**2 for j in range(e,self.T)) for i in range(self.nquery)]
        qwssum = [ sum( query[i,j]**2 * 2**(log(self.T,2)-int(log(j,2))) for j in range(e,self.T)) for i in range(self.nquery)]
        return self.query[siteid][:,s:e], s, e, qssum, qwssum, self.k

    def send_later(self, siteid):
        lev = self.level
        if lev < len(self.pivot[siteid]):
            s = self.pivot[siteid][lev-1]
            e = self.pivot[siteid][lev]
        else:
            s = 0
            e = 0

        return self.query[siteid][:,s:e], s, e

    def cp1(self, ub):
        self.ub += ub

    def cp2(self):
        th = sorted(self.ub)[self.k-1]
        return th

    def aaa(self):
        print self.level

    def check1(self,siteid,rc):
        if rc == 0:
            del self.rs[siteid]
        self.rc += rc

    def check2(self):
        if self.rc <= self.k or self.level == self.maxlevel:
            self.done = True
        self.rc = 0
        self.level += 1
        self.ub = []

    def remainsite(self):
        return self.rs

    def isdone(self):
        return self.done

    def get_answer(self):
        return []


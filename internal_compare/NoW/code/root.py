from math import *
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

        T = query[0].shape[1]

        self.pivot = pivot

        self.level = 0
        self.maxlevel = max(len(p) for p in self.pivot.values())-1

    def send_first(self, siteid):
        self.rs[siteid] = 0
        s = 0
        e = self.pivot[siteid][0]

        qssum = [numpy.linalg.norm(self.query[siteid][i,e:], ord='fro')**2 for i in range(self.query[siteid].shape[0])]
        return self.query[siteid][:,0:e], 0, e, qssum, self.k

    def send_later(self, siteid):
        lev = self.level
        if lev < len(self.pivot[siteid]):
            s = self.pivot[siteid][lev-1]
            e = self.pivot[siteid][lev]
        else:
            s = self.pivot[siteid][-1]
            e = self.pivot[siteid][-1]

        return self.query[siteid][:,s:e], s, e

    def prp1(self, ub):
        self.ub += ub

    def prp2(self):
        if len(self.ub) > self.k:
            th = sorted(self.ub)[self.k-1]
        else:
            th = sorted(self.ub)[-1]
        return th

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


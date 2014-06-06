import sys
from root import root
def MsWave( k, query, sites, pivot):
    
    cost = 0
    qcost = 0
    rt = root(k, query, pivot)
    for site in sites.values():
        levelq, s, e, qssum, k = rt.send_first(site.siteid)
        ub = site.cp_first(levelq, s, e, qssum, k)
        rt.cp1(ub)
        cost += levelq.size + 1 + len(qssum)+ len(ub)
        qcost += levelq.size
    
    for site in sites.values():
        th = rt.cp2()
        rc = site.prune(th)
        rt.check1(site.siteid,rc)
        cost += 2
    rt.check2()
    
    level_rs = []
    while( not rt.isdone() ):
        rs = rt.remainsite()
        level_rs += [len(rs)]
        #print len(rs)
        for site in sites.values():
            if site.siteid not in rs:
                continue
            levelq, s, e  = rt.send_later(site.siteid)
            ub = site.cp_later(levelq, s, e)
            rt.cp1(ub)
            cost += levelq.size + len(ub)
            qcost += levelq.size
        
        for site in sites.values():
            if site.siteid not in rs:
                continue
            th = rt.cp2()
            rc = site.prune(th)
            rt.check1(site.siteid,rc)
            cost += 2
        rt.check2()
    
    rs = rt.remainsite()
    level_rs += [len(rs)]
    
    ans = []
    for site in sites.values():
        if site.siteid not in rs:
            continue
        ans += site.get_ans()
    
    cost += len(ans)

    return ans, cost, level_rs, qcost

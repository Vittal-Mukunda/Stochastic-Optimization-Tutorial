"""Run the certified B&B for classes [lo,hi) : free mode first, then in/out.  Writes trees/<cl>_<mode>.json.gz"""
import sys, time, json, gzip, os
from multiprocessing import Pool
from lmodel import *
from bnb import *
lines = open('reg11_S2.txt').read().split()

def run(args):
    cl, mode, limit, tlim = args
    out = parse_class(lines[cl]); check_class(out)
    t0 = time.time()
    M = Model(out, mode)
    S = Searcher(M, node_limit=limit, time_limit=tlim)
    st, res = S.run()
    info = dict(cl=cl, mode=mode, status=st, nodes=S.nodes, leaves=S.leaves, sec=round(time.time() - t0, 1))
    if st == 'INF':
        with gzip.open(f'trees/{cl}_{mode}.json.gz', 'wt') as f:
            json.dump(dict(info, vars=[list(v) for v in M.vars], rows=[list(l) for (_, _, _, l) in M.rows], tree=res), f)
    if st == 'FEAS':
        info['sol'] = [(M.vars[i], round(float(res[i]), 4)) for i in range(len(res)) if res[i] > 1e-7]
    return info

if __name__ == '__main__':
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    L1, L2, T2 = int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
    nproc = int(sys.argv[6]) if len(sys.argv) > 6 else 14
    log = open(f'drv_{lo}_{hi}.log', 'a')
    with Pool(nproc) as P:
        todo = []
        for r in P.imap_unordered(run, [(cl, 'free', L1, None) for cl in range(lo, hi)]):
            print(json.dumps({k: v for k, v in r.items() if k != 'sol'}), file=log, flush=True)
            if r['status'] != 'INF':
                todo += [(r['cl'], 'in', L2, T2), (r['cl'], 'out', L2, T2)]
        for r in P.imap_unordered(run, todo):
            print(json.dumps(r), file=log, flush=True)

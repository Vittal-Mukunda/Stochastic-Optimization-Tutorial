"""Parallelise hard skeletons by pre-splitting on the auxiliary variable n_1 (aux model only).
For each skeleton index, the subtree is the chain  B(n1,12) -> [n1<=12 | B(n1,13) -> [n1=13 | B(n1,14) -> [n1=14 |
B(n1,15) -> [n1=15 | n1>=16]]]]  whose five leaf boxes are refuted by independent searches (run in parallel).
The assembled subtree is written to the skeleton cache used by run_skel_par.py (aux name).
Usage: python run_presplit.py cl mode nproc idx1,idx2,..."""
import sys, os, time, json, gzip
from multiprocessing import Pool
from lmodel import *
from skel import automorphisms, skeleton_list
from bnb import Searcher, _Abort
lines = open('reg11_S2.txt').read().split()
G = {}
CUTS = [12, 13, 14, 15]

def init(cl, mode):
    out = parse_class(lines[cl]); M = Model(out, mode, aux=True)
    G['M'] = M; G['S'] = Searcher(M, node_limit=10**7); G['cl'] = cl; G['mode'] = mode
    G['reps'] = skeleton_list(M, automorphisms(out))

def piece_path(cl, mode, b, j, lo, hi):
    return f"skelcache/piece_{cl}_{mode}_{b}_{''.join(map(str, j))}_{lo}_{hi}.json.gz"

def work(item):
    idx, lo, hi = item
    M, S = G['M'], G['S']
    b, j = G['reps'][idx]
    pp = piece_path(G['cl'], G['mode'], b, j, lo, hi)
    if os.path.exists(pp):
        with gzip.open(pp, 'rt') as f: d = json.load(f)
        return idx, lo, hi, 'INF', d['sub'], d['nodes'], 0.0
    S.nodes = 0
    jidx = [M.idx[('j', r)] for r in range(N_R)]
    n1 = M.idx[('n', 1)]
    ch = [(b, 1, S.ub[b])] + [(jidx[r], j[r], j[r]) for r in range(N_R)] + [(n1, lo, hi)]
    t0 = time.time()
    u1 = S._apply(ch); pr = S.propagate()
    if pr is None:
        S._undo(u1); sub = ['X']; st = 'INF'
    else:
        u2 = S._apply(pr)
        try:
            sub = S._node(); st = 'INF'
        except _Abort as e:
            sub = None; st = e.args[0]
        S._undo(u2); S._undo(u1)
    if st == 'INF':
        with gzip.open(pp + '.tmp', 'wt') as f: json.dump(dict(sub=sub, nodes=S.nodes), f)
        os.replace(pp + '.tmp', pp)
    return idx, lo, hi, st, sub, S.nodes, round(time.time() - t0, 1)

if __name__ == '__main__':
    cl, mode, nproc = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
    idxs = [int(t) for t in sys.argv[4].split(',')]
    bounds = [(0, 12), (13, 13), (14, 14), (15, 15), (16, 38)]
    items = [(i, lo, hi) for i in idxs for lo, hi in bounds]
    out = parse_class(lines[cl]); M = Model(out, mode, aux=True); reps = skeleton_list(M, automorphisms(out))
    n1 = M.idx[('n', 1)]
    res = {}
    with Pool(nproc, initializer=init, initargs=(cl, mode)) as P:
        for idx, lo, hi, st, sub, nodes, sec in P.imap_unordered(work, items):
            print('piece', idx, lo, hi, st, nodes, sec, flush=True)
            res[(idx, lo, hi)] = (st, sub, nodes)
    for i in idxs:
        if all(res[(i, lo, hi)][0] == 'INF' for lo, hi in bounds):
            t = res[(i, 16, 38)][1]
            for k, (lo, hi) in zip(reversed(CUTS), reversed(bounds[:-1])):
                t = ['B', n1, k, res[(i, lo, hi)][1], t]
            b, j = reps[i]
            cp = f"skelcache/{cl}_{mode}_aux_{b}_{''.join(map(str, j))}.json.gz"
            with gzip.open(cp + '.tmp', 'wt') as f:
                json.dump(dict(sub=t, nodes=sum(res[(i, lo, hi)][2] for lo, hi in bounds)), f)
            os.replace(cp + '.tmp', cp)
            print('skeleton', i, 'assembled', flush=True)
        else:
            print('skeleton', i, 'OPEN', [(lo, hi, res[(i, lo, hi)][0]) for lo, hi in bounds], flush=True)

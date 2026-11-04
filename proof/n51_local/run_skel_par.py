"""Parallel skeleton split: python run_skel_par.py cl mode nproc [strongK] [per-skeleton node limit] [tag]
Each worker builds the model once and refutes skeleton representatives; results are merged into one K node."""
import sys, os, time, json, gzip
from multiprocessing import Pool
from lmodel import *
from skel import automorphisms, skeleton_list
from bnb import Searcher, StrongSearcher, _Abort, tree_stats
lines = open('reg11_S2.txt').read().split()
G = {}

def init(cl, mode, K, lim, aux):
    G['cl'], G['mode'], G['aux'] = cl, mode, aux
    out = parse_class(lines[cl])
    M = Model(out, mode, aux=aux)
    G['M'] = M
    G['S'] = StrongSearcher(M, K=K, node_limit=lim) if K else Searcher(M, node_limit=lim)

def cache_path(cl, mode, b, j, aux=False):
    return f"skelcache/{cl}_{mode}{'_aux' if aux else ''}_{b}_{''.join(map(str, j))}.json.gz"

def work(item):
    b, j = item
    M, S = G['M'], G['S']
    cp = cache_path(G['cl'], G['mode'], b, j, G['aux'])
    # an aux-model run may reuse base-model subtrees: the aux variables and rows are appended at the end, so base
    # indices stay valid (the reverse is not true)
    for p in ([cp, cache_path(G['cl'], G['mode'], b, j)] if G['aux'] else [cp]):
        if os.path.exists(p):
            with gzip.open(p, 'rt') as f:
                d = json.load(f)
            return b, list(j), 'INF', d['sub'], d['nodes'], 0.0
    S.nodes = 0
    jidx = [M.idx[('j', r)] for r in range(N_R)]
    ch = [(b, 1, S.ub[b])] + [(jidx[r], j[r], j[r]) for r in range(N_R)]
    t0 = time.time()
    u1 = S._apply(ch)
    pr = S.propagate()
    if pr is None:
        S._undo(u1); return b, list(j), 'INF', ['X'], 0, 0.0
    u2 = S._apply(pr)
    try:
        sub = S._node(); st = 'INF'
    except _Abort as e:
        sub = None; st = e.args[0]
    S._undo(u2); S._undo(u1)
    if st == 'INF':
        with gzip.open(cp + '.tmp', 'wt') as f:
            json.dump(dict(sub=sub, nodes=S.nodes), f)
        os.replace(cp + '.tmp', cp)
    return b, list(j), st, sub, S.nodes, round(time.time() - t0, 1)

if __name__ == '__main__':
    cl, mode, nproc = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
    K = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    lim = int(sys.argv[5]) if len(sys.argv) > 5 else 10**6
    tag = sys.argv[6] if len(sys.argv) > 6 else 'skelp'
    aux = 'aux' in tag
    out = parse_class(lines[cl]); check_class(out)
    M = Model(out, mode, aux=aux)
    if aux:
        B = Model(out, mode)
        assert M.vars[:len(B.vars)] == B.vars and [r[3] for r in M.rows[:len(B.rows)]] == [r[3] for r in B.rows]
    perms = automorphisms(out)
    reps = skeleton_list(M, perms)
    order = reps[::-1] if (len(sys.argv) > 7 and sys.argv[7] == 'rev') else reps
    print('reps', len(reps), 'group', len(perms), flush=True)
    t0 = time.time(); kids = {}; bad = []; tot = 0
    with Pool(nproc, initializer=init, initargs=(cl, mode, K, lim, aux)) as P:
        for b, j, st, sub, nodes, sec in P.imap_unordered(work, order):
            tot += nodes
            if st == 'INF':
                kids[(b, tuple(j))] = [b, j, sub]
            else:
                bad.append((b, j, st))
            print('skel', M.vars[b], j, st, nodes, sec, flush=True)
    info = dict(cl=cl, mode=mode, status='INF' if not bad else 'PARTIAL', nodes=tot, sec=round(time.time() - t0, 1),
                method='skel-par', sym=len(perms), strong=K, aux=aux, open=[(M.vars[b], j, st) for b, j, st in bad])
    print(json.dumps(info), flush=True)
    if not bad:
        tree = ['K', [list(p) for p in perms], [kids[(b, tuple(j))] for b, j in reps]]
        with gzip.open(f'trees/{cl}_{mode}_{tag}.json.gz', 'wt') as f:
            json.dump(dict(info, vars=[list(v) for v in M.vars], rows=[list(l) for (_, _, _, l) in M.rows], tree=tree), f)

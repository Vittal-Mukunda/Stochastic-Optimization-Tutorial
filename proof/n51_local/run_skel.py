"""python run_skel.py cl mode [sym 0/1] [strongK] [node_limit] [time_limit]"""
import sys, time, json, gzip
from lmodel import *
from skel import *
from bnb import tree_stats
lines = open('reg11_S2.txt').read().split()
cl, mode = int(sys.argv[1]), sys.argv[2]
sym = int(sys.argv[3]) if len(sys.argv) > 3 else 1
K = int(sys.argv[4]) if len(sys.argv) > 4 else 0
lim = int(sys.argv[5]) if len(sys.argv) > 5 else 10**6
tl = float(sys.argv[6]) if len(sys.argv) > 6 else None
out = parse_class(lines[cl]); check_class(out)
M = Model(out, mode)
perms = automorphisms(out) if sym else []
t0 = time.time()
st, res, S = run_skeleton(M, perms, strong=K, node_limit=lim, time_limit=tl, verbose=True)
info = dict(cl=cl, mode=mode, status=st, nodes=S.nodes, leaves=S.leaves, sec=round(time.time() - t0, 1), method='skel', sym=len(perms), strong=K)
print(json.dumps(info), flush=True)
if st == 'INF':
    with gzip.open(f'trees/{cl}_{mode}_skel.json.gz', 'wt') as f:
        json.dump(dict(info, vars=[list(v) for v in M.vars], rows=[list(l) for (_, _, _, l) in M.rows], tree=res), f)
else:
    print('stopped at skeleton', res[0], res[1], flush=True)

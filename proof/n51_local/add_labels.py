"""Add variable/row label tables to tree files produced before the driver saved them (deterministic rebuild)."""
import sys, gzip, json
from lmodel import *
lines = open('reg11_S2.txt').read().split()
for p in sys.argv[1:]:
    with gzip.open(p, 'rt') as f: D = json.load(f)
    if 'vars' in D: continue
    M = Model(parse_class(lines[D['cl']]), D['mode'])
    D['vars'] = [list(v) for v in M.vars]; D['rows'] = [list(l) for (_, _, _, l) in M.rows]
    with gzip.open(p, 'wt') as f: json.dump(D, f)
    print('labelled', p)

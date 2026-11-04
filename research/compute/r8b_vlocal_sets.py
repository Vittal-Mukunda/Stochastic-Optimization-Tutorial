"""R8-B: exact v-local model for a FIXED W in the case where every |Q'_b| = 12 (h_b = 0 for all b in N^+(v)).

When every in-degree is 25 or 26, some v in L has sum_{b in N^+(v)} (|D(v,b)| - 12) = 0 (the total over L is 13 < 26),
and then every Q'_b = D({v,b}) is a 'good' 12-set: |Q n N^-_W(w)| >= 5 for every w in W (row V3), and
sum_W e = 13, i.e. exactly 13 vertices of W have in-degree 26 (binary case).

Variables: multiplicity n_Q >= 0 of each good 12-set Q (sum 26), presence p_Q, e_w in {0,1}.
Rows: V2 point degrees 13 - e_w; V4 |Q n Q'| >= 5 for used pairs (and |Q| = 12 >= 5 for repeats);
V5 Q n Q' n Q'' != {}, Q n Q' n N^-(w) != {}, Q n N^-(w) n N^-(w') != {} for used sets;
V6 pairs/triples/4-sets of W: k_W(X) + #{b : X n Q'_b = {}} >= 12 / 5 / 1;
V7 pair w -> w' with e_w' = 0 has exactly 12 dominators; for e_w' = 1 the excess over in-neighbours inside W is <= 13.

Usage: python r8b_vlocal_sets.py Wfile.json goodsets.json [--time T] [--workers K] [--enum]
"""
import argparse
import itertools
import json
import time
from pathlib import Path

import numpy as np
from ortools.sat.python import cp_model


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('wfile')
    ap.add_argument('gfile')
    ap.add_argument('--time', type=float, default=600)
    ap.add_argument('--workers', type=int, default=3)
    a = ap.parse_args()
    A = np.array(json.loads(Path(a.wfile).read_text())['A'], dtype=int)
    n = 25
    W = range(n)
    sets = [frozenset(s) for s in json.loads(Path(a.gfile).read_text())['12']['sets']]
    inn = [frozenset(z for z in W if A[z, w]) for w in W]
    # per-set V5 filter: Q n N^-(w) n N^-(w') != {} for all w, w'
    cin2 = {(w, x): inn[w] & inn[x] for w, x in itertools.combinations(W, 2)}
    sets = [Q for Q in sets if all(Q & cin2[k] for k in cin2)]
    S = len(sets)
    t0 = time.time()
    bad_pairs = []
    for i, j in itertools.combinations(range(S), 2):
        I = sets[i] & sets[j]
        if len(I) < 5 or any(not (I & inn[w]) for w in W):
            bad_pairs.append((i, j))
    bad_set = set(bad_pairs)
    bad_triples = []
    for i, j, k in itertools.combinations(range(S), 3):
        if (i, j) in bad_set or (i, k) in bad_set or (j, k) in bad_set:
            continue
        if not (sets[i] & sets[j] & sets[k]):
            bad_triples.append((i, j, k))
    prep = round(time.time() - t0, 1)
    m = cp_model.CpModel()
    nQ = [m.NewIntVar(0, 26, f'n{i}') for i in range(S)]
    p = [m.NewBoolVar(f'p{i}') for i in range(S)]
    for i in range(S):
        m.Add(nQ[i] >= 1).OnlyEnforceIf(p[i])
        m.Add(nQ[i] == 0).OnlyEnforceIf(p[i].Not())
    m.Add(sum(nQ) == 26)
    e = [m.NewBoolVar(f'e{w}') for w in W]
    m.Add(sum(e) == 13)
    for w in W:
        m.Add(sum(nQ[i] for i in range(S) if w in sets[i]) == 13 - e[w])               # V2
    for i, j in bad_pairs:
        m.AddBoolOr([p[i].Not(), p[j].Not()])                                           # V4, V5
    for i, j, k in bad_triples:
        m.AddBoolOr([p[i].Not(), p[j].Not(), p[k].Not()])                               # V5
    Dp = {}
    for X in itertools.combinations(W, 2):
        kw = int(np.all(A[:, list(X)] == 1, axis=1).sum())
        Dp[X] = kw + sum(nQ[i] for i in range(S) if not (sets[i] & set(X)))
        m.Add(Dp[X] >= 12)                                                              # V6
        u, w = X
        head = w if A[u, w] else u
        m.Add(Dp[X] == 12).OnlyEnforceIf(e[head].Not())                                 # V7
    for w2 in W:
        tails = [u for u in W if A[u, w2]]
        m.Add(sum(Dp[tuple(sorted((u, w2)))] - 12 for u in tails) <= 13)               # V7 budget
    for k, need in ((3, 5), (4, 1)):
        for X in itertools.combinations(W, k):
            kw = int(np.all(A[:, list(X)] == 1, axis=1).sum())
            if kw >= need:
                continue
            m.Add(kw + sum(nQ[i] for i in range(S) if not (sets[i] & set(X))) >= need)  # V6
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = a.time
    s.parameters.num_workers = a.workers
    st = s.Solve(m)
    rec = {'wfile': a.wfile, 'good12_after_V5_filter': S, 'bad_pairs': len(bad_pairs), 'bad_triples': len(bad_triples),
           'prep_s': prep, 'status': s.StatusName(st), 'solve_s': round(s.WallTime(), 1)}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        rec['chosen'] = [[sorted(sets[i]), s.Value(nQ[i])] for i in range(S) if s.Value(nQ[i])]
        rec['e'] = [s.Value(x) for x in e]
    print(json.dumps({k: v for k, v in rec.items() if k not in ('chosen', 'e')}))
    Path(__file__).parent.joinpath(f'r8b_vlocal_sets_{Path(a.wfile).stem}.json').write_text(json.dumps(rec))


if __name__ == '__main__':
    main()

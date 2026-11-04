"""R8-B: v-local model with W = T[N^-(v)] FIXED (d^-(v) = 25, no-tight branch, order 52).

Unknowns: q[b][w] = [w -> b] for the 26 vertices b in B = N^+(v) and w in W; e_w = d^-(w) - 25 for w in W.
Rows (each a consequence of S_4 + no-tight, see the R8-B report):
 V1 |Q'_b| >= 12, Q'_b = W n N^-(b) = D({v,b})                                  (pair {v,b})
 V2 sum_b q[b][w] = 13 - e_w ; sum_W e <= 13                                      (out-degree of w is 26 - e_w)
 V3 |Q'_b n N^-_W(w)| >= 5                                                        (triple {v,b,w})
 V4 |Q'_b n Q'_b'| >= 5                                                           (triple {v,b,b'})
 V5 Q'_b n Q'_b' n Q'_b'' != {}, Q'_b n Q'_b' n N^-(w) != {}, Q'_b n N^-(w) n N^-(w') != {}   (4-sets through v)
 V6 for X subset W, |X| = 2, 3, 4: |D(X)| = k_W(X) + #{b : X n Q'_b = {}} >= 12, 5, 1  (dominators of X lie in W u B)
 V7 for w -> w' in W: |D(w,w')| = 12 if e_w' = 0 ; sum_{w -> w'} (|D(w,w')| - 12) <= (25 + e_w') e_w' / 2 restricted to W
 (S_3 of W and its pair condition are properties of the fixed W and are checked on input.)
V5 and the triple/4-set part of V6 are added lazily (solve, check, add violated rows, repeat).

Usage: python r8b_vlocal.py Wfile.json [--binary] [--hv0] [--time T] [--workers K] [--rounds R]
  --binary: e_w in {0,1};  --hv0: sum_W e = 13 (choose v in L with no out-excess; then every |Q'_b| = 12).
"""
import argparse
import itertools
import json
import time
from pathlib import Path

import numpy as np
from ortools.sat.python import cp_model


def load_W(path):
    d = json.loads(Path(path).read_text())
    A = np.array(d['A'] if isinstance(d, dict) else d, dtype=int)
    n = len(A)
    assert n == 25 and (A + A.T == 1 - np.eye(n, dtype=int)).all()
    assert (A.sum(axis=0) == 12).all()
    C = A.T @ A
    assert C[np.triu_indices(n, 1)].min() >= 5
    assert all((A[:, u] & A[:, w] & A[:, y]).any() for u, w, y in itertools.combinations(range(n), 3))
    return A


def kW(A, X):
    return int(np.all(A[:, list(X)] == 1, axis=1).sum())


DROP = set()


def solve(A, binary, hv0, tl, workers, lazy):
    n = 25
    W = range(n)
    NB = 26
    Bs = range(NB)
    m = cp_model.CpModel()
    q = {(b, w): m.NewBoolVar(f'q{b}_{w}') for b in Bs for w in W}
    e = {w: m.NewIntVar(0, 1 if binary else 13, f'e{w}') for w in W}
    m.Add(sum(e.values()) == 13) if hv0 else m.Add(sum(e.values()) <= 13)
    for b in Bs:
        m.Add(sum(q[b, w] for w in W) >= 12)                                          # V1
    for w in W:
        m.Add(sum(q[b, w] for b in Bs) == 13 - e[w])                                  # V2
    inn = {w: [z for z in W if A[z, w]] for w in W}
    if 'V3' not in DROP:
        for b in Bs:
            for w in W:
                m.Add(sum(q[b, z] for z in inn[w]) >= 5)                              # V3
    pq = {}
    for b, b2 in itertools.combinations(Bs, 2):
        lits = []
        for w in W:
            z = m.NewBoolVar('')
            m.AddBoolAnd([q[b, w], q[b2, w]]).OnlyEnforceIf(z)
            m.AddBoolOr([q[b, w].Not(), q[b2, w].Not()]).OnlyEnforceIf(z.Not())
            lits.append(z)
            pq[b, b2, w] = z
        if 'V4' not in DROP:
            m.Add(sum(lits) >= 5)                                                     # V4
    avoid = {}

    def av(b, X):
        key = (b, X)
        if key not in avoid:
            z = m.NewBoolVar('')
            lits = [q[b, w].Not() for w in X]
            m.AddBoolAnd(lits).OnlyEnforceIf(z)
            m.AddBoolOr([l.Not() for l in lits]).OnlyEnforceIf(z.Not())
            avoid[key] = z
        return avoid[key]

    ezero = {}
    for w in W:
        ezero[w] = m.NewBoolVar('')
        m.Add(e[w] == 0).OnlyEnforceIf(ezero[w])
        m.Add(e[w] >= 1).OnlyEnforceIf(ezero[w].Not())
    Dp = {}
    for u, w in itertools.combinations(W, 2):
        X = (u, w)
        if 'V6' in DROP:
            continue
        Dp[X] = sum(av(b, X) for b in Bs) + kW(A, X)
        m.Add(Dp[X] >= 12)                                                            # V6 pairs
        head = w if A[u, w] else u
        if 'V7' not in DROP:
            m.Add(Dp[X] == 12).OnlyEnforceIf(ezero[head])                             # V7
    for w2 in (W if not DROP & {'V6', 'V7'} else []):
        tails = [u for u in W if A[u, w2]]
        cap2 = m.NewIntVar(0, 38 * 13, '')
        m.AddMultiplicationEquality(cap2, [e[w2] + 25, e[w2]])
        m.Add(2 * sum(Dp[tuple(sorted((u, w2)))] - 12 for u in tails) <= cap2)        # V7 budget
    s = cp_model.CpSolver()
    s.parameters.num_workers = workers
    log = []
    t_start = time.time()
    for rnd in range(lazy):
        s.parameters.max_time_in_seconds = max(10.0, tl - (time.time() - t_start))
        st = s.Solve(m)
        log.append({'round': rnd, 'status': s.StatusName(st), 'secs': round(s.WallTime(), 1)})
        print(json.dumps(log[-1]), flush=True)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return log, None
        Q = np.array([[s.Value(q[b, w]) for w in W] for b in Bs])
        added = 0
        # V5 checks
        for b, b2, b3 in itertools.combinations(Bs, 3):
            if not (Q[b] & Q[b2] & Q[b3]).any():
                m.AddBoolOr([_and3(m, pq[b, b2, w], q[b3, w]) for w in W])
                added += 1
        for b, b2 in itertools.combinations(Bs, 2):
            for w in W:
                if not (Q[b] & Q[b2] & A[:, w]).any():
                    m.AddBoolOr([pq[b, b2, z] for z in inn[w]])
                    added += 1
        for b in Bs:
            for w, w2 in itertools.combinations(W, 2):
                cin = [z for z in W if A[z, w] and A[z, w2]]
                if not Q[b][cin].any():
                    m.AddBoolOr([q[b, z] for z in cin])
                    added += 1
        # V6 triples and 4-sets
        for k, need in ((3, 5), (4, 1)):
            for X in itertools.combinations(W, k):
                base = kW(A, X)
                cnt = base + int(sum(1 for b in Bs if not Q[b][list(X)].any()))
                if cnt < need:
                    m.Add(sum(av(b, X) for b in Bs) + base >= need)
                    added += 1
        log[-1]['added'] = added
        print(json.dumps({'round': rnd, 'added': added}), flush=True)
        if added == 0:
            return log, {'Q': Q.tolist(), 'e': [s.Value(e[w]) for w in W]}
        if time.time() - t_start > tl:
            break
    return log, 'TIMEOUT_LAZY'


def _and3(m, x, y):
    z = m.NewBoolVar('')
    m.AddBoolAnd([x, y]).OnlyEnforceIf(z)
    m.AddBoolOr([x.Not(), y.Not()]).OnlyEnforceIf(z.Not())
    return z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('wfile')
    ap.add_argument('--binary', action='store_true')
    ap.add_argument('--hv0', action='store_true')
    ap.add_argument('--time', type=float, default=1100)
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--rounds', type=int, default=40)
    ap.add_argument('--drop', default='', help='comma list of row groups to omit (V3,V4,V6,V7); diagnostics only')
    a = ap.parse_args()
    DROP.update(x for x in a.drop.split(',') if x)
    A = load_W(a.wfile)
    log, sol = solve(A, a.binary, a.hv0, a.time, a.workers, a.rounds)
    out = {'wfile': a.wfile, 'binary': a.binary, 'hv0': a.hv0, 'log': log}
    if isinstance(sol, dict):
        out['solution'] = sol
        out['status'] = 'FEASIBLE_ALL_ROWS'
    else:
        out['status'] = sol if sol else log[-1]['status']
    tag = Path(a.wfile).stem + ('_bin' if a.binary else '') + ('_hv0' if a.hv0 else '') + \
        (('_drop' + a.drop.replace(',', '')) if a.drop else '')
    out['drop'] = sorted(DROP)
    Path(__file__).parent.joinpath(f'r8b_vlocal_{tag}.json').write_text(json.dumps(out))
    print(json.dumps({k: out[k] for k in ('binary', 'hv0', 'status')}))


if __name__ == '__main__':
    main()

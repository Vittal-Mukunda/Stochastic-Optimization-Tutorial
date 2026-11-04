"""R8-B: test the all-|Q'_b| = 12 v-local set model (r8b_vlocal_sets.py rows) on many different W.

W ranges over 12-regular S_3 tournaments on 25 vertices with every pair having >= 5 common in-neighbours.
Sources: (1) a random walk from a seed W by reversing directed 3-cycles (scores preserved), accepting only steps that keep
c >= 5 and S_3 (gives non-symmetric W); (2) seed files given on the command line.
For each sampled W: enumerate the good 12-sets (|Q n N^-(w)| >= 5 for all w) and solve the exact model with rows
V2 (point degrees, sum e = 13, e binary), V4/V5 (pair/triple intersections), V6 (pairs/triples/4-sets of W), V7.

Usage: python r8b_multiW.py seed.json [samples] [walk_steps_between] [time_per_model]
"""
import itertools
import json
import random
import sys
import time
from pathlib import Path

import numpy as np
from ortools.sat.python import cp_model

N = 25
TRIPLES = list(itertools.combinations(range(N), 3))


def valid(A):
    C = A.T @ A
    if C[np.triu_indices(N, 1)].min() < 5:
        return False
    for u, w, y in TRIPLES:
        if not (A[:, u] & A[:, w] & A[:, y]).any():
            return False
    return True


def good12(A):
    inmask = np.array([sum(1 << z for z in range(N) if A[z, w]) for w in range(N)], dtype=np.int64)
    good = []
    it = itertools.combinations(range(N), 12)
    while True:
        chunk = list(itertools.islice(it, 600000))
        if not chunk:
            break
        M = np.array([sum(1 << x for x in c) for c in chunk], dtype=np.int64)
        ok = np.ones(len(M), dtype=bool)
        for w in range(N):
            ok &= np.bitwise_count(M & inmask[w]) >= 5
            if not ok.any():
                break
        good.extend(frozenset(chunk[i]) for i in np.nonzero(ok)[0])
    return good


def model(A, sets, tl):
    W = range(N)
    inn = [frozenset(z for z in W if A[z, w]) for w in W]
    cin2 = [inn[w] & inn[x] for w, x in itertools.combinations(W, 2)]
    sets = [Q for Q in sets if all(Q & c for c in cin2)]
    S = len(sets)
    m = cp_model.CpModel()
    nQ = [m.NewIntVar(0, 26, '') for _ in range(S)]
    p = [m.NewBoolVar('') for _ in range(S)]
    for i in range(S):
        m.Add(nQ[i] >= 1).OnlyEnforceIf(p[i])
        m.Add(nQ[i] == 0).OnlyEnforceIf(p[i].Not())
    m.Add(sum(nQ) == 26)
    e = [m.NewBoolVar('') for _ in W]
    m.Add(sum(e) == 13)
    for w in W:
        m.Add(sum(nQ[i] for i in range(S) if w in sets[i]) == 13 - e[w])
    bad = set()
    for i, j in itertools.combinations(range(S), 2):
        I = sets[i] & sets[j]
        if len(I) < 5 or any(not (I & inn[w]) for w in W):
            m.AddBoolOr([p[i].Not(), p[j].Not()])
            bad.add((i, j))
    for i, j, k in itertools.combinations(range(S), 3):
        if (i, j) in bad or (i, k) in bad or (j, k) in bad:
            continue
        if not (sets[i] & sets[j] & sets[k]):
            m.AddBoolOr([p[i].Not(), p[j].Not(), p[k].Not()])
    Dp = {}
    for X in itertools.combinations(W, 2):
        kw = int(np.all(A[:, list(X)] == 1, axis=1).sum())
        Dp[X] = kw + sum(nQ[i] for i in range(S) if not (sets[i] & set(X)))
        m.Add(Dp[X] >= 12)
        u, w = X
        head = w if A[u, w] else u
        m.Add(Dp[X] == 12).OnlyEnforceIf(e[head].Not())
    for w2 in W:
        m.Add(sum(Dp[tuple(sorted((u, w2)))] - 12 for u in W if A[u, w2]) <= 13)
    for k, need in ((3, 5), (4, 1)):
        for X in itertools.combinations(W, k):
            kw = int(np.all(A[:, list(X)] == 1, axis=1).sum())
            if kw < need:
                m.Add(kw + sum(nQ[i] for i in range(S) if not (sets[i] & set(X))) >= need)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = 3
    st = s.Solve(m)
    return S, s.StatusName(st), round(s.WallTime(), 1)


def main():
    seed = sys.argv[1]
    samples = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    between = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 300
    A = np.array(json.loads(Path(seed).read_text())['A'], dtype=np.int64)
    assert valid(A)
    rng = random.Random(9021)
    out = []
    for smp in range(samples):
        acc = 0
        tries = 0
        t0 = time.time()
        while acc < (0 if smp == 0 else between) and tries < 200000:
            tries += 1
            x, y, z = rng.sample(range(N), 3)
            if not (A[x, y] and A[y, z] and A[z, x]):
                continue
            A[x, y] = A[y, z] = A[z, x] = 0
            A[y, x] = A[z, y] = A[x, z] = 1
            if valid(A):
                acc += 1
            else:
                A[y, x] = A[z, y] = A[x, z] = 0
                A[x, y] = A[y, z] = A[z, x] = 1
        C = A.T @ A
        hist = {int(k): int(v) for k, v in zip(*np.unique(C[np.triu_indices(N, 1)], return_counts=True))}
        g = good12(A)
        S, st, secs = model(A, g, tl)
        rec = {'sample': smp, 'accepted_steps': acc, 'walk_s': round(time.time() - t0, 1), 'c_hist': hist,
               'good12': len(g), 'good12_after_V5': S, 'status': st, 'solve_s': secs, 'A': A.tolist()}
        out.append(rec)
        print(json.dumps({k: v for k, v in rec.items() if k != 'A'}), flush=True)
        Path(__file__).parent.joinpath('r8b_multiW.json').write_text(json.dumps(out))


if __name__ == '__main__':
    main()

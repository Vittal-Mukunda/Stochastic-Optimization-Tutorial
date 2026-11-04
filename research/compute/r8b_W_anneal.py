"""R8-B: simulated annealing for regular tournaments on n = 4t+1 vertices in which every pair has >= t-1 common
in-neighbours (n = 25, t = 6 is the structure forced on T[N^-(v)], d^-(v) = 25, in the no-tight order-52 branch).
Moves reverse a directed 3-cycle (preserves all scores).  Cost = sum over pairs of max(0, (t-1) - c(pair)).
Optionally adds the S_3 deficit (number of triples without a common in-neighbour).

Usage: python r8b_W_anneal.py n [steps] [restarts] [--s3]
"""
import itertools
import json
import math
import random
import sys
from pathlib import Path

import numpy as np


def cost(A, thr, s3):
    C = A.T @ A
    n = len(A)
    iu = np.triu_indices(n, 1)
    c = 4 * np.maximum(0, thr - C[iu]).sum() + (np.maximum(0, C[iu] - thr - 1).sum() if HIGHPEN else 0)
    if s3:
        # triples with no common in-neighbour
        miss = 0
        for u, w, y in itertools.combinations(range(n), 3):
            if not (A[:, u] & A[:, w] & A[:, y]).any():
                miss += 1
        c += miss
    return int(c)


def anneal(n, steps, rng, s3=False):
    t = (n - 1) // 4
    thr = t - 1
    k = (n - 1) // 2
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for d in range(1, k + 1):
            A[i, (i + d) % n] = 1
    # randomise
    for _ in range(20 * n * n):
        x, y, z = rng.sample(range(n), 3)
        if A[x, y] and A[y, z] and A[z, x]:
            A[x, y] = A[y, z] = A[z, x] = 0
            A[y, x] = A[z, y] = A[x, z] = 1
    cur = cost(A, thr, s3)
    best = cur
    bestA = A.copy()
    T0 = 2.0
    for it in range(steps):
        if cur == 0:
            break
        T = T0 * (1 - it / steps) + 0.02
        x, y, z = rng.sample(range(n), 3)
        if not (A[x, y] and A[y, z] and A[z, x]):
            continue
        A[x, y] = A[y, z] = A[z, x] = 0
        A[y, x] = A[z, y] = A[x, z] = 1
        new = cost(A, thr, s3)
        if new <= cur or rng.random() < math.exp((cur - new) / T):
            cur = new
            if cur < best:
                best = cur
                bestA = A.copy()
            if HIGHPEN and not s3:
                C = A.T @ A
                if C[np.triu_indices(n, 1)].min() >= thr:
                    return 0, A.copy()
        else:
            A[y, x] = A[z, y] = A[x, z] = 0
            A[x, y] = A[y, z] = A[z, x] = 1
    return best, bestA


HIGHPEN = '--highpen' in sys.argv


def main():
    n = int(sys.argv[1])
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    s3 = '--s3' in sys.argv
    rng = random.Random(1000 + n)
    results = []
    for r in range(restarts):
        best, A = anneal(n, steps, rng, s3)
        C = A.T @ A
        iu = np.triu_indices(n, 1)
        hist = {int(k): int(v) for k, v in zip(*np.unique(C[iu], return_counts=True))}
        results.append({'restart': r, 'best_cost': best, 'c_hist': hist})
        print(json.dumps(results[-1]), flush=True)
        if best == 0:
            Path(__file__).parent.joinpath(f'r8b_W_anneal_n{n}{"_s3" if s3 else ""}_witness.json').write_text(
                json.dumps(A.tolist()))
            break
    Path(__file__).parent.joinpath(f'r8b_W_anneal_n{n}{"_s3" if s3 else ""}.json').write_text(json.dumps(results))


if __name__ == '__main__':
    main()

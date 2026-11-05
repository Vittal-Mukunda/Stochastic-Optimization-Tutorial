#!/usr/bin/env python3
"""Family 3 of the pattern search: block-constant codegree patterns (generalising the K_{12,13} branch of Theorem 7.2).

V = V_1 ∪ ... ∪ V_t with |V_i| = n_i, and Y_ab = y_ij for a in V_i, b in V_j, a != b (y symmetric, 0..6).
Row sums: (n_i - 1) y_ii + sum_{j != i} n_j y_ij = 12.  Optionally ('matching' variants) a perfect matching inside one
even block V_i carries y_ii + delta instead of y_ii (Theorem 7.2's pattern is t = 2, sizes 12/13, y = [[1, 0], [0, 1]]
with delta = 1 on a matching of the 12-block).  Every pattern goes through spectral_engine.analyse; survivors are saved.
Usage: python3 block_patterns.py tmax outdir
"""
import collections
import itertools
import os
import sys

import numpy as np

sys.path.insert(0, 'research/compute/p25')
import spectral_engine as se  # noqa: E402

N = 25


def size_vectors(t):
    """Non-increasing size vectors of length t summing to 25, all parts >= 1."""
    def rec(rem, parts, maxp):
        if parts == 0:
            if rem == 0:
                yield ()
            return
        for s in range(min(rem - (parts - 1), maxp), 0, -1):
            for rest in rec(rem - s, parts - 1, s):
                yield (s,) + rest
    return list(rec(N, t, N))


def y_matrices(sizes, delta_block=None, delta=0):
    """All symmetric y (t x t, entries 0..6) with the row-sum condition (row i of block delta_block gets +delta)."""
    t = len(sizes)
    cells = [(i, j) for i in range(t) for j in range(i, t)]
    y = [[0] * t for _ in range(t)]

    def rowsum(i):
        return (sizes[i] - 1) * y[i][i] + sum(sizes[j] * y[i][j] for j in range(t) if j != i) + \
            (delta if i == delta_block else 0)

    def rec(k):
        if k == len(cells):
            if all(rowsum(i) == 12 for i in range(t)):
                yield [row[:] for row in y]
            return
        i, j = cells[k]
        for v in range(7):
            y[i][j] = y[j][i] = v
            # prune: partial row sums cannot exceed 12
            if rowsum(i) <= 12 and rowsum(j) <= 12:
                yield from rec(k + 1)
        y[i][j] = y[j][i] = 0

    yield from rec(0)


def build(sizes, y, delta_block=None, delta=0):
    blocks = []
    start = 0
    for s in sizes:
        blocks.append(list(range(start, start + s)))
        start += s
    lab = [None] * N
    for i, B in enumerate(blocks):
        for v in B:
            lab[v] = i
    Y = np.zeros((N, N), dtype=np.int64)
    for a in range(N):
        for b in range(N):
            if a != b:
                Y[a, b] = y[lab[a]][lab[b]]
    if delta_block is not None:
        B = blocks[delta_block]
        for k in range(0, len(B), 2):
            Y[B[k], B[k + 1]] += delta
            Y[B[k + 1], B[k]] += delta
    return Y


def main():
    tmax, outdir = int(sys.argv[1]), sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    stats = collections.Counter()
    survivors = []
    for t in range(1, tmax + 1):
        for sizes in size_vectors(t):
            variants = [(None, 0)] + [(i, d) for i in range(t) if sizes[i] % 2 == 0 for d in (1, 2, 3)]
            for db, d in variants:
                for y in y_matrices(sizes, db, d):
                    Y = build(sizes, y, db, d)
                    if Y.max() > 6:
                        continue
                    res = se.analyse(Y, want_ghc=True)
                    key = (t, 'alive' if res['alive'] else res['killed_by'])
                    stats[key] += 1
                    if res['alive']:
                        fn = os.path.join(outdir, 'blk_%s_%s_%s.npy' % ('-'.join(map(str, sizes)),
                                                                       ''.join(str(v) for row in y for v in row),
                                                                       'm%s%d' % (db, d) if db is not None else 'plain'))
                        np.save(fn, Y)
                        survivors.append((sizes, y, db, d, [(f[2], f[1]) for f in res['g_factors']], fn))
        print('t =', t, {k: v for k, v in stats.items() if k[0] == t}, flush=True)
    print('survivors:', len(survivors))
    for s in survivors:
        print('  ', s)


if __name__ == '__main__':
    main()

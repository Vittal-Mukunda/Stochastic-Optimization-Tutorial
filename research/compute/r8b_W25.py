"""R8-B: search Cayley tournaments on groups of order 25 for the structure forced on W = N^-(v), d^-(v) = 25:
12-regular (automatic for Cayley), S_3 (every triple has a common in-neighbour in W), and every pair has at least 5
common in-neighbours in W.  Groups: Z_25 and Z_5 x Z_5; all 2^12 connection sets are tried (no symmetry reduction).
Prints the number of connection sets passing each filter and saves the survivors.
"""
import itertools
import json
from pathlib import Path

import numpy as np


def tour_from(S, elems, add, neg):
    n = len(elems)
    idx = {g: i for i, g in enumerate(elems)}
    A = np.zeros((n, n), dtype=np.int64)
    for g in elems:
        for s in S:
            A[idx[g], idx[add(g, s)]] = 1
    return A


def props(A):
    n = len(A)
    C = A.T @ A           # C[u,w] = # common in-neighbours
    off = C[~np.eye(n, dtype=bool)]
    cmin = int(off.min())
    s3 = True
    if cmin >= 1:
        for u, w, z in itertools.combinations(range(n), 3):
            if not (A[:, u] & A[:, w] & A[:, z]).any():
                s3 = False
                break
    return cmin, s3


def run(name, elems, add, neg):
    zero = elems[0]
    reps = []
    seen = set()
    for g in elems[1:]:
        if g in seen:
            continue
        seen.add(g)
        seen.add(neg(g))
        reps.append(g)
    assert len(reps) == 12
    stats = {'total': 0, 'cmin>=5': 0, 'cmin>=5 and S3': 0}
    surv = []
    hist = {}
    for bits in range(1 << 12):
        S = [reps[i] if (bits >> i) & 1 else neg(reps[i]) for i in range(12)]
        A = tour_from(S, elems, add, neg)
        stats['total'] += 1
        C = A.T @ A
        n = len(A)
        cmin = int(C[~np.eye(n, dtype=bool)].min())
        hist[cmin] = hist.get(cmin, 0) + 1
        if cmin >= 5:
            stats['cmin>=5'] += 1
            _, s3 = props(A)
            if s3:
                stats['cmin>=5 and S3'] += 1
                surv.append([str(s) for s in S])
    print(name, stats, 'cmin histogram', dict(sorted(hist.items())))
    return stats, surv, hist


def main():
    out = {}
    z25 = list(range(25))
    out['Z25'] = run('Z25', z25, lambda g, s: (g + s) % 25, lambda g: (-g) % 25)
    z55 = [(i, j) for i in range(5) for j in range(5)]
    out['Z5xZ5'] = run('Z5xZ5', z55, lambda g, s: ((g[0] + s[0]) % 5, (g[1] + s[1]) % 5),
                       lambda g: ((-g[0]) % 5, (-g[1]) % 5))
    Path(__file__).with_suffix('.json').write_text(json.dumps(
        {k: {'stats': v[0], 'cmin_hist': v[2], 'survivors': v[1][:50], 'n_surv': len(v[1])} for k, v in out.items()},
        indent=1))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Family 1 of the pattern search: every Cayley codegree pattern on Z_25 and on Z_5 x Z_5.

Y(a, b) = y(b - a) with y(g) = y(-g) >= 0, sum_g y(g) = 12 (so the 12 inverse pairs carry a composition of 6).
Patterns are reduced modulo Aut(G) (Z_25^* resp. GL(2, 5)).  Spectra of abelian Cayley patterns are always paired
(chi and conj(chi) give the same eigenvalue), so the filters that bite are (D), (Pf), (EDC), (HM), (GHC).
For a surviving nondegenerate pattern every realisation is a Cayley tournament on the same group (spectral_engine
docstring), and no Cayley tournament on either group has all codegrees >= 5 (proof/N52_SESSION_2026-11-04.md §4);
reconstruct() is run anyway as a check.  Degenerate survivors are saved for p25_exactpattern.py.
Usage: python3 cayley_patterns.py outdir
"""
import collections
import itertools
import json
import os
import sys

import numpy as np

sys.path.insert(0, 'research/compute/p25')
import spectral_engine as se  # noqa: E402

N = 25


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def group_data(name):
    if name == 'Z25':
        els = list(range(25))
        sub = lambda a, b: (a - b) % 25           # noqa: E731
        neg = lambda a: (-a) % 25                 # noqa: E731
        auts = [lambda g, u=u: (u * g) % 25 for u in range(1, 25) if u % 5]
    else:
        els = [(i, j) for i in range(5) for j in range(5)]
        sub = lambda a, b: ((a[0] - b[0]) % 5, (a[1] - b[1]) % 5)   # noqa: E731
        neg = lambda a: ((-a[0]) % 5, (-a[1]) % 5)                  # noqa: E731
        auts = []
        for a, b, c, d in itertools.product(range(5), repeat=4):
            if (a * d - b * c) % 5:
                auts.append(lambda g, a=a, b=b, c=c, d=d: ((a * g[0] + b * g[1]) % 5, (c * g[0] + d * g[1]) % 5))
    zero = els[0]
    pairs, idx, seen = [], {}, set()
    for g in els:
        if g == zero or g in seen:
            continue
        seen |= {g, neg(g)}
        idx[g] = idx[neg(g)] = len(pairs)
        pairs.append(g)
    perms = []
    for f in auts:
        perms.append(tuple(idx[f(pairs[i])] for i in range(12)))
    return els, sub, pairs, idx, sorted(set(perms))


def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    summary = {}
    for gname in ('Z25', 'Z5sq'):
        els, sub, pairs, idx, perms = group_data(gname)
        reps = set()
        for y in compositions(6, 12):
            best = min(tuple(y[p[i]] for i in range(12)) for p in [tuple(np.argsort(q)) for q in perms])
            reps.add(best)
        stats = collections.Counter()
        kept = []
        for y in sorted(reps):
            Y = np.zeros((N, N), dtype=np.int64)
            for i, a in enumerate(els):
                for j, b in enumerate(els):
                    if i != j:
                        Y[i, j] = y[idx[sub(b, a)]]
            res = se.analyse(Y)
            if not res['alive']:
                stats['killed_' + res['killed_by']] += 1
                continue
            status, sols = se.reconstruct(Y)
            stats['alive_' + status + ('_sols%d' % len(sols) if status == 'ok' else '')] += 1
            if status != 'ok' or sols:
                fn = os.path.join(outdir, '%s_%s.npy' % (gname, ''.join(map(str, y))))
                np.save(fn, Y)
                kept.append({'y': y, 'status': status, 'nsols': len(sols), 'file': fn,
                             'g_factors': [(f[2], f[1]) for f in res['g_factors']]})
        summary[gname] = {'orbits': len(reps), 'stats': dict(stats), 'kept': kept}
        print(gname, len(reps), dict(stats), flush=True)
        for k in kept:
            print('   ', k, flush=True)
    with open(os.path.join(outdir, 'summary.json'), 'w') as fh:
        json.dump(summary, fh, indent=1, default=str)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""[check] Stand-alone verifier (pure Python, no shared code): for each file given (format "a: out-neighbours"), check that
it is a tournament on 25 vertices, every out-degree is 12, every pair has >= 5 common in-neighbours, and every triple has
a common in-neighbour (S_3).  Prints the codegree histogram and the minimum number of dominators of a triple."""
import itertools
import sys

for path in sys.argv[1:]:
    out = {}
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        a, rest = line.split(':')
        out[int(a)] = set(int(b) for b in rest.split())
    n = len(out)
    V = range(n)
    tour = all((b in out[a]) != (a in out[b]) for a in V for b in V if a != b) and all(a not in out[a] for a in V)
    inn = {v: set(a for a in V if v in out[a]) for v in V}
    reg = all(len(out[a]) == 12 for a in V)
    cod = [len(inn[a] & inn[b]) for a, b in itertools.combinations(V, 2)]
    hist = {c: cod.count(c) for c in sorted(set(cod))}
    tri = min(len(inn[a] & inn[b] & inn[c]) for a, b, c in itertools.combinations(V, 3))
    ok = n == 25 and tour and reg and min(cod) >= 5 and tri >= 1
    print('%s: n=%d tournament=%s 12-regular=%s codegree histogram=%s min triple dominators=%d  ->  (P25) %s'
          % (path, n, tour, reg, hist, tri, 'YES' if ok else 'NO'))

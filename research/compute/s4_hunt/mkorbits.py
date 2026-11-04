"""Write the orbit-variable instance file for orbit_tabu.c.  Usage: mkorbits.py GROUPSPEC OUTFILE"""
import sys
from itertools import combinations
import numpy as np
from satgroup import build_group


def canon_codes(G, Xs, N):
    best = None
    for g in G:
        im = np.sort(g[Xs], axis=1)
        code = np.zeros(len(Xs), dtype=np.int64)
        for i in range(Xs.shape[1]):
            code = code * N + im[:, i]
        best = code if best is None else np.minimum(best, code)
    return best


def decode(code, N, k):
    out = []
    for _ in range(k):
        out.append(int(code % N)); code //= N
    return out[::-1]


def main(spec, outfile):
    N, G = build_group(spec)
    seen = np.zeros((N, N), dtype=bool)
    vars_ = []
    for u in range(N):
        for v in range(u + 1, N):
            if seen[u, v]:
                continue
            arcs = set()
            for g in G:
                a, b = int(g[u]), int(g[v])
                arcs.add((a, b)); seen[a, b] = seen[b, a] = True
            vars_.append(sorted(arcs))
    lines = []
    for k in (4, 3):
        Xs = np.array(list(combinations(range(N), k)), dtype=np.int64)
        codes = canon_codes(G, Xs, N)
        u, cnt = np.unique(codes, return_counts=True)
        lines.append([(decode(int(c), N, k), int(w)) for c, w in zip(u, cnt)])
    with open(outfile, "w") as f:
        f.write(f"{N} {len(vars_)} {len(lines[0])} {len(lines[1])}\n")
        for arcs in vars_:
            f.write(str(len(arcs)) + " " + " ".join(f"{a} {b}" for a, b in arcs) + "\n")
        for k in range(2):
            for X, w in lines[k]:
                f.write(" ".join(map(str, X)) + f" {w}\n")
    print(N, len(G), len(vars_), len(lines[0]), len(lines[1]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

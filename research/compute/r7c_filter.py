"""R7-C: which labelled 5-regular S_2 tournaments on 11 vertices carry the J = 5, s = 4 pattern of R4-C?

Pattern (R4-C, conditional on J >= 5 and s >= 4): positive dominators A (j=2), B, C, D (j=1), V_0 = the other 7.
Common-in-neighbour conditions:
  c(A,B) = 4, c(C,D) = 0, c(A,C) in 0..4, c(A,D) in 2..4, c(B,C) in 1..4, c(B,D) in 0..3,
  c(u,v) <= 3 whenever u or v lies in V_0  (Lemma A, valid for every J).
Prints, per class, the labelled tuples (A, B, C, D) that pass.
"""
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n52_tight_local import N_R, check_class, parse_class, ROOT  # noqa: E402

WIN = {('A', 'B'): {4}, ('C', 'D'): {0}, ('A', 'C'): set(range(5)), ('A', 'D'): {2, 3, 4},
       ('B', 'C'): {1, 2, 3, 4}, ('B', 'D'): {0, 1, 2, 3}}


def cmat(out):
    inn = [sum(1 << i for i in range(N_R) if (out[i] >> j) & 1) for j in range(N_R)]
    return [[bin(inn[u] & inn[v]).count('1') if u != v else 0 for v in range(N_R)] for u in range(N_R)]


def labellings(out):
    c = cmat(out)
    four = [(u, v) for u in range(N_R) for v in range(u + 1, N_R) if c[u][v] == 4]
    res = []
    for A, B, C, D in itertools.permutations(range(N_R), 4):
        lab = {'A': A, 'B': B, 'C': C, 'D': D}
        if any(c[lab[x]][lab[y]] not in W for (x, y), W in WIN.items()):
            continue
        pos = {A, B, C, D}
        if any(u not in pos or v not in pos for u, v in four):
            continue
        res.append((A, B, C, D))
    return res, len(four)


if __name__ == '__main__':
    lines = (ROOT / 'proof' / 'n51_local' / 'reg11_S2.txt').read_text().split()
    total = 0
    survivors = {}
    hist = {}
    for ci, line in enumerate(lines):
        out = parse_class(line)
        check_class(out)
        labs, nfour = labellings(out)
        hist[nfour] = hist.get(nfour, 0) + 1
        if labs:
            survivors[ci] = labs
            total += len(labs)
    print('classes by number of c=4 pairs:', dict(sorted(hist.items())))
    print('classes with a surviving labelling:', len(survivors), 'labelled tuples:', total)
    (Path(__file__).parent / 'r7c_survivors.json').write_text(json.dumps(survivors))

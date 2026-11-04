"""R8-F-asymptotic: brute-force check of Proposition S on real S_n tournaments.

Run from the project root:  python research/compute/r8f_hereditary_check.py

Proposition S: if T has S_n and |A| = s <= n - 1, then T[D(A)] has S_{n-s}, and for U inside D(A)
the dominators of U in T[D(A)] are exactly D(A + U).  Checked on QR_7 (S_2), QR_19 (S_3) and QR_67 (S_4)
for every A with |A| <= n - 1 containing 0 (Paley is vertex-transitive), and every (n-s)-subset U of D(A).
"""
from __future__ import annotations

import itertools


def paley_out(p):
    qr = {(x * x) % p for x in range(1, p)}
    return [sum(1 << y for y in range(p) if (y - x) % p in qr) for x in range(p)]


def D(out, X, universe):
    m = universe
    for x in X:
        m &= ~(1 << x)
    res = 0
    for w in range(len(out)):
        if (m >> w) & 1 and all((out[w] >> x) & 1 for x in X):
            res |= 1 << w
    return res


def members(mask):
    return [i for i in range(mask.bit_length()) if (mask >> i) & 1]


def main():
    total = 0
    for p, n in ((7, 2), (19, 3), (67, 4)):
        out = paley_out(p)
        full = (1 << p) - 1
        for s in range(1, n):
            for rest in itertools.combinations(range(1, p), s - 1):
                A = (0,) + rest
                R = D(out, A, full)
                Rl = members(R)
                for U in itertools.combinations(Rl, n - s):
                    inner = D(out, U, R)          # dominators of U inside T[R]
                    outer = D(out, A + U, full)   # D(A + U) in T
                    assert inner == outer and inner != 0, (p, A, U)
                    total += 1
        print(f"QR_{p}: Proposition S holds for every A through 0 with |A| <= {n - 1}")
    print("subsets checked:", total)


if __name__ == "__main__":
    main()

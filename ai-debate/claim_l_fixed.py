"""Realize the Y-side of the pair-link for one fixed 12-vertex tournament.

The tournament is QR_11 with a vertex of out-degree 6 adjoined. It is S_2 and
has minimum in-degree 5, so it is a legal candidate for T_X.
"""

from __future__ import annotations

import time

import numpy as np
import z3


def paley(p: int) -> np.ndarray:
    squares = {pow(a, 2, p) for a in range(1, p)}
    A = np.zeros((p, p), dtype=int)
    for i in range(p):
        for s in squares:
            A[i, (i + s) % p] = 1
    return A


def candidate() -> np.ndarray:
    A = np.zeros((12, 12), dtype=int)
    A[:11, :11] = paley(11)
    for j in range(6):
        A[11, j] = 1
    for j in range(6, 11):
        A[j, 11] = 1
    return A


def main() -> None:
    A = candidate()
    indeg = A.sum(axis=0)
    assert indeg.min() >= 5
    r = 12 + indeg
    lam = np.zeros((12, 12), dtype=int)
    for i in range(12):
        for j in range(i + 1, 12):
            alpha = int(np.logical_and(A[i], A[j]).sum())
            assert alpha <= 10
            lam[i, j] = 10 - alpha
    I = [np.flatnonzero(A[:, y]).tolist() for y in range(12)]

    s = z3.Solver()
    s.set("timeout", 300_000)
    Y = 37
    m = [[z3.Bool(f"m_{u}_{x}") for x in range(12)] for u in range(Y)]

    for u in range(Y):
        s.add(z3.PbGe([(m[u][x], 1) for x in range(12)], 5))
        for y in range(12):
            s.add(z3.Or([m[u][x] for x in I[y]]))
    for u in range(Y - 1):
        # lex order on rows, as integers 0..4095
        def key(row: int) -> z3.ArithRef:
            acc = z3.IntVal(0)
            for x in range(12):
                acc = acc * 2 + z3.If(m[row][x], 1, 0)
            return acc

        s.add(key(u) >= key(u + 1))
    for u in range(Y):
        for v in range(u + 1, Y):
            s.add(z3.Or([z3.And(m[u][x], m[v][x]) for x in range(12)]))
    for x in range(12):
        s.add(z3.PbEq([(m[u][x], 1) for u in range(Y)], int(r[x])))
    for i in range(12):
        for j in range(i + 1, 12):
            s.add(
                z3.PbEq(
                    [(z3.And(m[u][i], m[u][j]), 1) for u in range(Y)],
                    int(lam[i, j]),
                )
            )

    print("r", r.tolist(), "lam min/max", int(lam[np.triu_indices(12, 1)].min()), int(lam.max()), flush=True)
    t0 = time.time()
    result = s.check()
    print(result, round(time.time() - t0, 1), flush=True)
    if result != z3.sat:
        return
    model = s.model()
    rows = []
    for u in range(Y):
        rows.append([1 if z3.is_true(model.eval(m[u][x])) else 0 for x in range(12)])
    M = np.array(rows)
    print("weights", sorted(M.sum(1).tolist()), flush=True)
    G = M.T @ M
    ok = True
    for x in range(12):
        ok &= G[x, x] == r[x]
        for y in range(x + 1, 12):
            ok &= G[x, y] == lam[x, y]
    print("gram", bool(ok), "pairwise", all(np.logical_and(M[u], M[v]).any() for u in range(Y) for v in range(u + 1, Y)), flush=True)


if __name__ == "__main__":
    main()

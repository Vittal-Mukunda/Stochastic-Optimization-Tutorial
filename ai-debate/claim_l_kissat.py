"""SAT encoding of the Y-side pair-link for one legal 12-vertex tournament."""

from __future__ import annotations

import time

import numpy as np
from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Cadical195


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


def add_card(cnf: CNF, lits: list[int], bound: int, top: int, kind: str) -> int:
    enc = CardEnc.atleast if kind == "ge" else CardEnc.equals
    part = enc(lits=lits, bound=bound, top_id=top, encoding=EncType.seqcounter)
    cnf.extend(part.clauses)
    return max(top, part.nv)


def main() -> None:
    A = candidate()
    indeg = A.sum(axis=0)
    r = (12 + indeg).astype(int)
    lam = np.zeros((12, 12), dtype=int)
    for i in range(12):
        for j in range(i + 1, 12):
            lam[i, j] = 10 - int(np.logical_and(A[i], A[j]).sum())
    neigh = [[x for x in range(12) if A[x, y]] for y in range(12)]

    Y = 37
    # m[u][x] in 1..444
    m = [[u * 12 + x + 1 for x in range(12)] for u in range(Y)]
    top = Y * 12
    both: list[list[list[int]]] = [[[0] * 12 for _ in range(12)] for _ in range(Y)]
    cnf = CNF()
    for u in range(Y):
        for i in range(12):
            for j in range(i + 1, 12):
                top += 1
                both[u][i][j] = top
                b = top
                cnf.append([-b, m[u][i]])
                cnf.append([-b, m[u][j]])
                cnf.append([b, -m[u][i], -m[u][j]])

    for u in range(Y):
        top = add_card(cnf, [m[u][x] for x in range(12)], 5, top, "ge")
        for y in range(12):
            cnf.append([m[u][x] for x in neigh[y]])
    for u in range(Y):
        for v in range(u + 1, Y):
            # auxiliary OR of pairwise agreements
            ors = []
            for x in range(12):
                top += 1
                b = top
                ors.append(b)
                cnf.append([-b, m[u][x]])
                cnf.append([-b, m[v][x]])
                cnf.append([b, -m[u][x], -m[v][x]])
            cnf.append(ors)
    for x in range(12):
        top = add_card(cnf, [m[u][x] for u in range(Y)], int(r[x]), top, "eq")
    for i in range(12):
        for j in range(i + 1, 12):
            top = add_card(
                cnf,
                [both[u][i][j] for u in range(Y)],
                int(lam[i, j]),
                top,
                "eq",
            )

    print(
        f"vars<={top} clauses={len(cnf.clauses)} r={r.tolist()} "
        f"lam={int(lam[np.triu_indices(12,1)].min())}..{int(lam.max())}",
        flush=True,
    )
    t0 = time.time()
    with Cadical195(bootstrap_with=cnf.clauses) as solver:
        sat = solver.solve()
        print("sat" if sat else "unsat", round(time.time() - t0, 1), flush=True)
        if not sat:
            return
        model = set(lit for lit in solver.get_model() if lit > 0)
        M = np.array([[1 if m[u][x] in model else 0 for x in range(12)] for u in range(Y)])
    G = M.T @ M
    ok = all(G[x, x] == r[x] for x in range(12)) and all(
        G[i, j] == lam[i, j] for i in range(12) for j in range(i + 1, 12)
    )
    hit = all(M[u, neigh[y]].sum() >= 1 for u in range(Y) for y in range(12))
    inter = all(np.logical_and(M[u], M[v]).any() for u in range(Y) for v in range(u + 1, Y))
    print("verified", ok, "hit", hit, "intersect", inter, "weights", M.sum(1).tolist(), flush=True)
    np.save("ai-debate/claim_l_rows.npy", M)
    np.save("ai-debate/claim_l_tournament.npy", A)


if __name__ == "__main__":
    main()

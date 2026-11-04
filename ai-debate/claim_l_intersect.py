"""Exact search for an intersecting realization of the pair-link equations."""

from __future__ import annotations

import time

import numpy as np
from scipy import sparse
from scipy.optimize import Bounds, LinearConstraint, milp


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
    inn = []
    for y in range(12):
        mask = 0
        for i in range(12):
            if A[i, y]:
                mask |= 1 << i
        inn.append(mask)
    valid = np.array(
        [s for s in range(1 << 12) if s.bit_count() >= 5 and all(s & m for m in inn)],
        dtype=np.int32,
    )
    k = len(valid)
    indeg = A.sum(0)
    r = (12 + indeg).astype(int)
    lam = np.zeros((12, 12), dtype=int)
    for i in range(12):
        for j in range(i + 1, 12):
            lam[i, j] = 10 - int(np.logical_and(A[i], A[j]).sum())

    bits = ((valid[:, None] >> np.arange(12)) & 1).astype(np.int8)
    eq_rows = [np.ones(k, dtype=np.float64)]
    eq_rhs = [37.0]
    for x in range(12):
        eq_rows.append(bits[:, x].astype(np.float64))
        eq_rhs.append(float(r[x]))
    for i in range(12):
        for j in range(i + 1, 12):
            eq_rows.append((bits[:, i] * bits[:, j]).astype(np.float64))
            eq_rhs.append(float(lam[i, j]))
    Aeq = np.vstack(eq_rows)
    beq = np.array(eq_rhs)

    pairs = []
    for i, s in enumerate(valid):
        for j in range(i + 1, k):
            if int(s) & int(valid[j]) == 0:
                pairs.append((i, j))
    pcount = len(pairs)
    print("sets", k, "disjoint type-pairs", pcount, "equations", Aeq.shape[0], flush=True)

    nvars = k + pcount
    # equalities on m, zeros on z
    A_eq = sparse.hstack([sparse.csr_matrix(Aeq), sparse.csr_matrix((Aeq.shape[0], pcount))])
    # inequalities
    ri, ci, vi = [], [], []
    row = 0
    for p, (a, b) in enumerate(pairs):
        # m_a - 37 z <= 0
        ri += [row, row]
        ci += [a, k + p]
        vi += [1.0, -37.0]
        row += 1
        # m_b + 37 z <= 37
        ri += [row, row]
        ci += [b, k + p]
        vi += [1.0, 37.0]
        row += 1
    A_ub = sparse.csr_matrix((vi, (ri, ci)), shape=(row, nvars))
    b_ub = np.empty(row)
    b_ub[0::2] = 0
    b_ub[1::2] = 37
    A_all = sparse.vstack([A_eq.tocsr(), A_ub])
    lo = np.concatenate([beq, np.full(row, -np.inf)])
    hi = np.concatenate([beq, b_ub])
    integrality = np.ones(nvars)
    bounds = Bounds(np.zeros(nvars), np.concatenate([np.full(k, 37.0), np.ones(pcount)]))
    print("constraint matrix", A_all.shape, "nnz", A_all.nnz, flush=True)
    t0 = time.time()
    res = milp(
        c=np.zeros(nvars),
        integrality=integrality,
        bounds=bounds,
        constraints=LinearConstraint(A_all, lo, hi),
        options={"time_limit": 600, "presolve": "on"},
    )
    print(res.message, "seconds", round(time.time() - t0, 1), "success", res.success, flush=True)
    if not res.success:
        return
    mult = np.rint(res.x[:k]).astype(int)
    if not np.array_equal(Aeq.astype(np.int64) @ mult, beq.astype(np.int64)):
        raise SystemExit("equation check failed")
    idx = np.flatnonzero(mult > 0)
    for a in idx:
        for b in idx:
            if a < b and int(valid[a]) & int(valid[b]) == 0:
                raise SystemExit("disjoint pair survived")
    print("INTERSECTING", "support", len(idx), "sum", int(mult.sum()), flush=True)
    for t in idx:
        print(int(mult[t]), format(int(valid[t]), "012b"), int(valid[t]).bit_count(), flush=True)
    np.save("ai-debate/claim_l_mult.npy", mult)
    np.save("ai-debate/claim_l_valid.npy", valid)


if __name__ == "__main__":
    main()

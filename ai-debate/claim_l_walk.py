"""Walk the integer fibre of the pair-link equations, looking for an intersecting family."""

from __future__ import annotations

import random

import numpy as np
from scipy.optimize import LinearConstraint, Bounds, milp


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


def conflicts(valid: np.ndarray, mult: np.ndarray) -> int:
    idx = np.flatnonzero(mult > 0)
    bad = 0
    sets = valid[idx]
    ms = mult[idx]
    for i, s in enumerate(sets):
        for j in range(i, len(sets)):
            if int(s) & int(sets[j]) == 0:
                if i == j:
                    # a set repeated is fine; it intersects itself
                    continue
                bad += int(ms[i] * ms[j])
    return bad


def main() -> None:
    rng = random.Random(1)
    A = candidate()
    masks = [0] * 12
    for y in range(12):
        for i in range(12):
            if A[i, y]:
                masks[y] |= 1 << i
    valid = np.array(
        [s for s in range(1 << 12) if s.bit_count() >= 5 and all(s & m for m in masks)],
        dtype=np.int32,
    )
    indeg = A.sum(0)
    r = (12 + indeg).astype(int)
    lam = np.zeros((12, 12), dtype=int)
    for i in range(12):
        for j in range(i + 1, 12):
            lam[i, j] = 10 - int(np.logical_and(A[i], A[j]).sum())
    k = len(valid)
    bits = np.zeros((k, 12), dtype=np.int8)
    for t, s in enumerate(valid):
        for x in range(12):
            bits[t, x] = (int(s) >> x) & 1
    rows = [np.ones(k, dtype=np.int16)]
    rhs = [37]
    for x in range(12):
        rows.append(bits[:, x].astype(np.int16))
        rhs.append(int(r[x]))
    for i in range(12):
        for j in range(i + 1, 12):
            rows.append((bits[:, i] * bits[:, j]).astype(np.int16))
            rhs.append(int(lam[i, j]))
    Aeq = np.vstack(rows).astype(np.float64)
    beq = np.array(rhs, dtype=np.float64)
    print("system", Aeq.shape, flush=True)
    res = milp(
        np.zeros(k),
        integrality=np.ones(k),
        constraints=LinearConstraint(Aeq, beq, beq),
        bounds=Bounds(0, 37),
    )
    if not res.success:
        raise SystemExit(res.message)
    mult = np.rint(res.x).astype(int)
    if not np.array_equal(Aeq.astype(np.int64) @ mult, beq.astype(np.int64)):
        raise SystemExit("starter is not exact")
    print("start conflicts", conflicts(valid, mult), "support", int((mult > 0).sum()), flush=True)

    best = conflicts(valid, mult)
    best_mult = mult.copy()
    for step in range(400):
        support = np.flatnonzero(mult > 0)
        extra = np.array(rng.sample(range(k), 60), dtype=int)
        cols = np.unique(np.concatenate([support, extra]))
        sub = Aeq[:, cols]
        # integer-ish kernel
        _u, svals, vt = np.linalg.svd(sub, full_matrices=True)
        rank = int((svals > 1e-8).sum())
        null = vt[rank:]
        improved = False
        for vec in null:
            scale = np.max(np.abs(vec))
            if scale < 1e-12:
                continue
            cand = np.rint(vec / scale * 12).astype(int)
            # reduce by gcd
            g = int(np.gcd.reduce(cand))
            if g > 1:
                cand //= g
            if np.max(np.abs(cand)) > 6 or np.all(cand == 0):
                continue
            if np.max(np.abs(sub @ cand)) > 1e-6:
                continue
            # exact check
            exact = Aeq[:, cols].astype(object)  # slow path avoided
            if not np.all(np.rint(sub @ cand) == 0) or np.max(np.abs(sub @ cand)) > 1e-4:
                continue
            direction = np.zeros(k, dtype=int)
            direction[cols] = cand
            for sign in (1, -1):
                trial = mult + sign * direction
                if trial.min() < 0 or trial.sum() != 37:
                    continue
                if not np.array_equal(Aeq.astype(np.int64) @ trial, beq.astype(np.int64)):
                    continue
                score = conflicts(valid, trial)
                if score < best:
                    best = score
                    best_mult = trial.copy()
                    mult = trial
                    improved = True
                    print("step", step, "conflicts", best, "support", int((mult > 0).sum()), flush=True)
                    if best == 0:
                        idx = np.flatnonzero(mult > 0)
                        for t in idx:
                            print(int(mult[t]), bin(int(valid[t])), flush=True)
                        np.save("ai-debate/claim_l_mult.npy", mult)
                        return
                    break
            if improved:
                break
        if not improved and step % 40 == 0:
            print("step", step, "no move, best", best, flush=True)
    print("finished best", best, flush=True)


if __name__ == "__main__":
    main()

"""Local model for a tight pair in an S_4 tournament on N = 52 vertices.

P = {a, b} with a -> b and |D(P)| = 11, R = D(P), T[R] a 5-regular S_2 tournament (one of the 551 classes in
proof/n51_local/reg11_S2.txt).  O = V \\ (P u R), |O| = 39.  For y in O, Q_y = R n N^-(y) = D(P + y) and
type 0: y->a, b->y;  type 1: a->y, y->b;  type 2: a->y, b->y   (y->a, y->b would put y in D(P) = R).
For r in R, d^-(r) = 25 + j_r with j_r >= 0 (Lemma T), so r has 51 - 25 - j_r - 7 = 19 - j_r out-neighbours in O.

Every row is a consequence of S_4 (via nu_2 >= 11, nu_3 >= 5, nu_4 >= 1 and Lemma 1.2) and of N = 52:
  C1   sum_y 1 = 39
  C3   |D(U)| >= nu_|U| for U subset of R, |U| = 2, 3, 4
  C4   |D(U + a)|, |D(U + b)| >= nu_{|U|+1} for U subset of R, |U| = 1, 2, 3
  C5   #{y : r in Q_y} = 19 - j_r
  DEG  d^-(a) = 11 + n_0 >= 23,  d^-(b) = 12 + n_1 >= 23
  ADM  Q_y meets every N^-_R(z)  (otherwise y dominates D({a, b, z}), contradicting Lemma 1.2)
  INT  (optional) Q_y n Q_y' nonempty  (otherwise y' dominates D({a, b, y}))
No case analysis on J, s or heavy patterns is assumed.
"""
import itertools
import sys
import time
from pathlib import Path

import highspy
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'proof' / 'n51_local'))
from lmodel import N_R, NU, admissible, cR, check_class, parse_class, popc  # noqa: E402

N_O = 39
OUT_TO_O = 19


def build(out, intersecting=False, fix_J=None, min_dA=23, min_dB=23, fix_j=None):
    adm = admissible(out, tuple(range(5, 12)))
    types = (0, 1, 2)
    xvars = [(S, t) for S in adm for t in types]
    nx = len(xvars)
    nvar = nx + N_R + (len(adm) if intersecting else 0)
    col_lo = np.zeros(nvar)
    col_hi = np.full(nvar, float(N_O))
    col_hi[nx:nx + N_R] = 14
    if fix_j is not None:
        col_lo[nx:nx + N_R] = fix_j
        col_hi[nx:nx + N_R] = fix_j
    if intersecting:
        col_hi[nx + N_R:] = 1
    rows = []

    def xrow(pred):
        return {i: 1.0 for i, (S, t) in enumerate(xvars) if pred(S, t)}

    rows.append((xrow(lambda S, t: True), N_O, N_O, 'C1'))
    for k in (2, 3, 4):
        for U in itertools.combinations(range(N_R), k):
            Um = sum(1 << u for u in U)
            need = NU[k] - cR(out, Um)
            if need > 0:
                rows.append((xrow(lambda S, t: not (S & Um)), need, np.inf, ('C3', Um)))
    for tt in (0, 1):
        for k in (1, 2, 3):
            for U in itertools.combinations(range(N_R), k):
                Um = sum(1 << u for u in U)
                need = NU[k + 1] - cR(out, Um)
                if need > 0:
                    rows.append((xrow(lambda S, t: t == tt and not (S & Um)), need, np.inf, ('C4', tt, Um)))
    for r in range(N_R):
        co = xrow(lambda S, t: (S >> r) & 1)
        co[nx + r] = 1.0
        rows.append((co, OUT_TO_O, OUT_TO_O, ('C5', r)))
    rows.append((xrow(lambda S, t: t == 0), min_dA - 11, np.inf, 'DEG_a'))
    rows.append((xrow(lambda S, t: t == 1), min_dB - 12, np.inf, 'DEG_b'))
    if fix_J is not None:
        rows.append(({nx + r: 1.0 for r in range(N_R)}, fix_J, fix_J, 'J'))
    if intersecting:
        base = nx + N_R
        for i, S in enumerate(adm):
            co = {xi: 1.0 for xi, (S2, t) in enumerate(xvars) if S2 == S}
            co[base + i] = -float(N_O)
            rows.append((co, -np.inf, 0, ('IND', S)))
        for i, j in itertools.combinations(range(len(adm)), 2):
            if not (adm[i] & adm[j]):
                rows.append(({base + i: 1.0, base + j: 1.0}, -np.inf, 1, ('DISJ', adm[i], adm[j])))
    return adm, xvars, col_lo, col_hi, rows


def solve(out, time_limit=120.0, **kw):
    adm, xvars, lo, hi, rows = build(out, **kw)
    h = highspy.Highs()
    h.setOptionValue('output_flag', False)
    h.setOptionValue('time_limit', time_limit)
    h.setOptionValue('threads', 1)
    inf = highspy.kHighsInf
    nvar = len(lo)
    h.addVars(nvar, lo, hi)
    h.changeColsIntegrality(nvar, np.arange(nvar, dtype=np.int32),
                            np.full(nvar, highspy.HighsVarType.kInteger))
    for co, rlo, rhi, _ in rows:
        idx = np.array(list(co.keys()), dtype=np.int32)
        val = np.array(list(co.values()))
        h.addRow(-inf if rlo == -np.inf else rlo, inf if rhi == np.inf else rhi, len(idx), idx, val)
    h.run()
    st = h.modelStatusToString(h.getModelStatus())
    sol = None
    if st == 'Optimal':
        x = h.getSolution().col_value
        nx = len(xvars)
        sol = {
            'Q': [(xvars[i][0], xvars[i][1], int(round(x[i]))) for i in range(nx) if x[i] > 0.5],
            'j': [int(round(x[nx + r])) for r in range(N_R)],
        }
    return st, sol


def main():
    lines = (ROOT / 'proof' / 'n51_local' / 'reg11_S2.txt').read_text().split()
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    inter = len(sys.argv) > 3 and sys.argv[3] == 'int'
    for ci in range(lo, min(hi, len(lines))):
        out = parse_class(lines[ci])
        check_class(out)
        t0 = time.time()
        st, sol = solve(out, intersecting=inter)
        msg = f'class {ci}: {st} ({time.time() - t0:.1f}s)'
        if sol:
            qs = sorted(((popc(S), t, m) for S, t, m in sol['Q']), reverse=True)
            msg += f" J={sum(sol['j'])} j={sol['j']} q-profile={[(q, t, m) for q, t, m in qs if q > 5]}"
        print(msg, flush=True)


if __name__ == '__main__':
    main()

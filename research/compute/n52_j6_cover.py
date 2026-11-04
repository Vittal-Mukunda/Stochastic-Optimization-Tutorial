"""Covering model for one J=6, 6+2 labelling on a FIXED S_2 class.

T[R] is an input (one of the 551 classes). Heavies: one cover (M=empty) and one
Y with M = a 4-subset of V_+. Lights are multiplicities of 6-subsets, typed
relative to {a,b}. Rows are only S_4 covering of subsets of R and of those
sets plus a or b, plus (I1) residual miss-counts.

Question this answers: can the pair-level 6+2 pattern extend to an assignment
of the 37 light vertices that meets every triple/4-set bound on R and on R+a, R+b?
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

from ortools.sat.python import cp_model

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "proof" / "n51_local"))
from lmodel import N_R, admissible, cR, check_class, parse_class, popc  # noqa: E402

NU = {2: 11, 3: 5, 4: 1}


def solve_one(out, jvec, M_y, tl=30.0, workers=8):
    pos = [r for r in range(11) if jvec[r] > 0]
    M = frozenset(M_y)
    lights = admissible(out, (6,))
    # residual misses after heavies: each r needs 20+j_r misses; cover misses nobody;
    # Y misses exactly the vertices in M.
    need_miss = [20 + jvec[r] - (1 if r in M else 0) for r in range(11)]
    m = cp_model.CpModel()
    x = {(S, t): m.NewIntVar(0, 39, "") for S in lights for t in (0, 1, 2)}
    # M_y for a light with Q=S is the complement of S (S is Q_y, a 6-subset)
    # wait: admissible returns Q_y bitmasks of size 6, so M = FULL ^ S has size 5.
    # LIGHT has e=0 so |M|=6, |Q|=5. I had this backwards!
    #
    # e_y = q_y - 5, light => q=5, |Q_y|=5, |M_y|=6.
    # Fix: lights are 5-subsets Q.
    raise RuntimeError("see fix below")


def miss_of_Q(Q_mask):
    return ((1 << 11) - 1) ^ Q_mask


def solve(out, jvec, M_y, tl=60.0, workers=8):
    """Q_y size 5 for lights; heavy cover Q=all 11; heavy Y has Q = R \\ M_y, |Q|=7."""
    Mbit = 0
    for r in M_y:
        Mbit |= 1 << r
    lights = admissible(out, (5,))  # Q of size 5
    need_miss = [20 + jvec[r] - (1 if r in M_y else 0) for r in range(11)]
    # cover contributes 0 misses; Y contributes 1 miss to each r in M_y
    m = cp_model.CpModel()
    x = {(S, t): m.NewIntVar(0, 39, "") for S in lights for t in (0, 1, 2)}
    tot = {S: sum(x[S, t] for t in (0, 1, 2)) for S in lights}
    m.Add(sum(tot.values()) == 37)
    for r in range(11):
        m.Add(sum(tot[S] for S in lights if ((miss_of_Q(S) >> r) & 1)) == need_miss[r])
    m.Add(sum(x[S, 0] for S in lights) >= 13)  # d^-(a) >= 24
    m.Add(sum(x[S, 1] for S in lights) >= 11)  # d^-(b) >= 23; +1 if we want 24

    def n_missing(Ubit, types=(0, 1, 2)):
        # heavies: cover misses nobody. Y misses U iff U subset M_y
        y_hit = 1 if (Ubit & Mbit) == Ubit else 0
        return y_hit + sum(x[S, t] for S in lights for t in types if (miss_of_Q(S) & Ubit) == Ubit)

    for k in (2, 3, 4):
        for U in itertools.combinations(range(11), k):
            Ubit = sum(1 << u for u in U)
            m.Add(cR(out, Ubit) + n_missing(Ubit) >= NU[k])
    for t in (0, 1):
        for k in (1, 2, 3):
            for U in itertools.combinations(range(11), k):
                Ubit = sum(1 << u for u in U)
                # D(U union {a}) for type 0: y of type 0 with U subset M_y, plus R-dominators of U
                # For |U|=1, R-dominators of {u} are the 5 in-neighbours.
                if k == 1:
                    rdom = 5
                    need = NU[2]  # 11
                else:
                    rdom = cR(out, Ubit)
                    need = NU[k + 1]
                m.Add(rdom + n_missing(Ubit, (t,)) >= need)

    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = tl
    sol.parameters.num_workers = workers
    st = sol.Solve(m)
    return sol.StatusName(st), len(lights)


def main():
    lines = (ROOT / "proof" / "n51_local" / "reg11_S2.txt").read_text().split()
    # class 0 labelling from n52_j6_hand: V_+ = [1,2,0,4], M = all four, j(1)=j(2)=2, j(0)=j(4)=1
    out = parse_class(lines[0])
    check_class(out)
    jvec = [0] * 11
    jvec[1] = 2
    jvec[2] = 2
    jvec[0] = 1
    jvec[4] = 1
    t0 = time.time()
    st, nL = solve(out, jvec, [1, 2, 0, 4], tl=90, workers=8)
    rec = {"class": 0, "j": jvec, "M": [0, 1, 2, 4], "lights": nL, "status": st,
           "secs": round(time.time() - t0, 1)}
    print(json.dumps(rec), flush=True)
    # a few more classes
    more = []
    for ci in (1, 2, 5, 10, 20, 50, 100, 200, 400):
        out = parse_class(lines[ci])
        check_class(out)
        # use first 4 vertices as V_+ with j=2,2,1,1 if c-Lemma A holds, else skip
        jvec = [2, 2, 1, 1] + [0] * 7
        t0 = time.time()
        st, nL = solve(out, jvec, [0, 1, 2, 3], tl=45, workers=4)
        row = {"class": ci, "status": st, "secs": round(time.time() - t0, 1), "lights": nL}
        print(json.dumps(row), flush=True)
        more.append(row)
    Path(__file__).parent.joinpath("n52_j6_cover.json").write_text(
        json.dumps({"first": rec, "sample": more}, indent=1))


if __name__ == "__main__":
    main()

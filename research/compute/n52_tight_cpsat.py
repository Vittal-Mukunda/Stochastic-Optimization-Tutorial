"""CP-SAT version of the N = 52 tight-pair local model in n52_tight_local.py (same rows, same variables).

Usage: python n52_tight_cpsat.py LO HI [int] [time_limit] [workers]
"""
import sys
import time
from pathlib import Path

import numpy as np
from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n52_tight_local import N_O, N_R, build, check_class, parse_class, popc, ROOT  # noqa: E402


def solve(out, time_limit=300.0, workers=8, **kw):
    adm, xvars, lo, hi, rows = build(out, **kw)
    m = cp_model.CpModel()
    v = [m.NewIntVar(int(lo[i]), int(hi[i]), f'v{i}') for i in range(len(lo))]
    for co, rlo, rhi, _ in rows:
        expr = sum(int(c) * v[i] for i, c in co.items())
        if rlo != -np.inf:
            m.Add(expr >= int(rlo))
        if rhi != np.inf:
            m.Add(expr <= int(rhi))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_workers = workers
    st = s.Solve(m)
    sol = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        nx = len(xvars)
        sol = {
            'Q': [(xvars[i][0], xvars[i][1], s.Value(v[i])) for i in range(nx) if s.Value(v[i]) > 0],
            'j': [s.Value(v[nx + r]) for r in range(N_R)],
        }
    return s.StatusName(st), sol


def main():
    lines = (ROOT / 'proof' / 'n51_local' / 'reg11_S2.txt').read_text().split()
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    inter = len(sys.argv) > 3 and sys.argv[3] == 'int'
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 300.0
    w = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    for ci in range(lo, min(hi, len(lines))):
        out = parse_class(lines[ci])
        check_class(out)
        t0 = time.time()
        st, sol = solve(out, time_limit=tl, workers=w, intersecting=inter)
        msg = f'class {ci}: {st} ({time.time() - t0:.1f}s)'
        if sol:
            qs = sorted(((popc(S), t, mm) for S, t, mm in sol['Q']), reverse=True)
            msg += f" J={sum(sol['j'])} j={sol['j']} heavy={[(q, t, mm) for q, t, mm in qs if q > 5]}"
        print(msg, flush=True)


if __name__ == '__main__':
    main()

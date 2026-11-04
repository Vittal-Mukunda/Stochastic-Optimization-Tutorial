"""LP relaxation probe for the N = 52 tight-pair local model: range of J, and LP feasibility per fixed J."""
import sys
import time
from pathlib import Path

import highspy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n52_tight_local import N_R, build, check_class, parse_class, ROOT  # noqa: E402


def lp(out, objective=None, integer=False, time_limit=60, **kw):
    adm, xvars, lo, hi, rows = build(out, **kw)
    h = highspy.Highs()
    h.setOptionValue('output_flag', False)
    h.setOptionValue('time_limit', float(time_limit))
    inf = highspy.kHighsInf
    n = len(lo)
    h.addVars(n, lo, hi)
    if integer:
        h.changeColsIntegrality(n, np.arange(n, dtype=np.int32), np.full(n, highspy.HighsVarType.kInteger))
    for co, rlo, rhi, _ in rows:
        idx = np.array(list(co.keys()), dtype=np.int32)
        h.addRow(-inf if rlo == -np.inf else rlo, inf if rhi == np.inf else rhi, len(idx), idx,
                 np.array(list(co.values())))
    nx = len(xvars)
    if objective == 'minJ' or objective == 'maxJ':
        sgn = 1.0 if objective == 'minJ' else -1.0
        for r in range(N_R):
            h.changeColCost(nx + r, sgn)
    h.run()
    st = h.modelStatusToString(h.getModelStatus())
    val = h.getInfo().objective_function_value if st == 'Optimal' else None
    return st, val


if __name__ == '__main__':
    lines = (ROOT / 'proof' / 'n51_local' / 'reg11_S2.txt').read_text().split()
    for ci in map(int, sys.argv[1:]):
        out = parse_class(lines[ci])
        check_class(out)
        t0 = time.time()
        print(ci, 'minJ', lp(out, 'minJ'), 'maxJ', lp(out, 'maxJ'), flush=True)
        for J in range(0, 15):
            print('   J', J, lp(out, fix_J=J), flush=True)
        print(f'   ({time.time() - t0:.1f}s)')

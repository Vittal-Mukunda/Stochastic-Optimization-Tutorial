"""R8-D: does a tight pair at N = 52 with J in {6,7,8} need a 'cover' y (Q_y = R, e_y = 6)?

Loads the pair-level model of n52_pairlevel.py verbatim and adds, after the Lemma I row
sum_M n[M] (6 - |M|) = 14 - J, one extra row:
  forbid_cover:  n[empty miss-set] == 0      (no outside y with Q_y = R)
For each J <= 8 partition that survives the unmodified model, it reports the status with no cover.
Solver output (CP-SAT, 3 workers), no certificate.

Usage: python r8d_cover.py [time_limit] [workers]
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
SRC = (HERE / 'n52_pairlevel.py').read_text(encoding='utf-8')
ANCHOR = '    m.Add(sum(n[M] * (6 - len(M)) for M in heavy_sets) == 14 - J)\n'
assert SRC.count(ANCHOR) == 1
PATCHED = SRC.replace(ANCHOR, ANCHOR + '    if FORBID_COVER:\n        m.Add(n[frozenset()] == 0)\n')
PATCHED = PATCHED.replace("if __name__ == '__main__':", "if False:")
NS = {'__name__': 'n52_pairlevel_patched', 'FORBID_COVER': False}
exec(compile(PATCHED, 'n52_pairlevel_patched', 'exec'), NS)


def main():
    tl = float(sys.argv[1]) if len(sys.argv) > 1 else 120.0
    w = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    base = json.loads((HERE / 'n52_pairlevel_6_14.json').read_text())
    feas = [r for r in base if r['status'] != 'INFEASIBLE' and r['J'] <= 8]
    out = []
    for r in feas:
        jvec = r['j'] + [0] * (11 - len(r['j']))
        rec = {'J': r['J'], 'j': r['j']}
        for flag in (False, True):
            NS['FORBID_COVER'] = flag
            t0 = time.time()
            st, info = NS['model'](jvec, tl, w)
            key = 'no_cover' if flag else 'unmodified'
            rec[key] = st
            rec[key + '_secs'] = round(time.time() - t0, 1)
            if info:
                rec[key + '_heavy'] = info['heavy']
        print(json.dumps(rec), flush=True)
        out.append(rec)
    (HERE / 'r8d_cover.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()

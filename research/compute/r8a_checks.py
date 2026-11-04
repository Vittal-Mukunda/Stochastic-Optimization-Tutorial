"""R8-A audit side checks.

1. Section 2 partition filter of N52_TIGHT_J_GE_6.md: partitions of 9 into parts 1..6 with sum e(6-e) <= 25,
   and which of those admit a labelled placement on 5 vertices with every tau <= 5.
2. c >= 0 survivors at J = 5 by excess partition (from r8a_vplus_enum).
3. Rerun of n52_pairlevel.model for J = 0..5 with 3 workers, with c >= 1 and with c >= 0.
"""
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r8a_vplus_enum as E  # noqa: E402

out = {}

rows = []
for part in E.partitions(9, 6):
    w = sum(e * (6 - e) for e in part)
    placeable = False
    if w <= 25:
        for combo in itertools.product(*[list(itertools.combinations(range(5), 6 - e)) for e in part]):
            tau = [sum(e for e, M in zip(part, combo) if u in M) for u in range(5)]
            if max(tau) <= 5:
                placeable = True
                break
    rows.append({'partition': part, 'sum_e(6-e)': w, 'tau<=5 placement exists': placeable})
out['s5_filter'] = rows
print('partitions of 9 with a tau<=5 placement:', [r['partition'] for r in rows if r['tau<=5 placement exists']])

for jp in ([2, 1, 1, 1], [1, 1, 1, 1, 1]):
    cnt = Counter()
    s = len(jp)
    for heavy in E.heavy_multisets(s, 9):
        st, _ = E.solve_pairs(s, jp, heavy, 0)
        if st == 'ok':
            cnt['+'.join(str(6 - len(M)) for M in sorted(heavy, key=len))] += 1
    out[f'c0_survivors_{jp}'] = dict(cnt)
    print('c>=0 survivors', jp, dict(cnt))

if '--cpsat' in sys.argv:
    from n52_pairlevel import model, partitions as P2
    res = []
    for use_s2 in (True, False):
        for J in range(0, 6):
            for part in P2(J, J, 11):
                jvec = list(part) + [0] * (11 - len(part))
                st, info = model(jvec, tl=120.0, workers=3, use_s2=use_s2)
                rec = {'c_min': 1 if use_s2 else 0, 'J': J, 'j': list(part), 'status': st}
                if info:
                    rec['heavy'] = info['heavy']
                print(json.dumps(rec), flush=True)
                res.append(rec)
    out['cpsat_rerun'] = res

(Path(__file__).parent / 'r8a_checks.json').write_text(json.dumps(out, indent=1, default=str))

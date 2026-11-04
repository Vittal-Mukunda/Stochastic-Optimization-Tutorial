"""CP-SAT on the N = 52 tight-pair local model, one class, one fixed J.  Usage: n52_byJ.py CLASS J TL WORKERS [int]"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n52_tight_cpsat import solve  # noqa: E402
from n52_tight_local import check_class, parse_class, popc, ROOT  # noqa: E402

ci, J, tl, w = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
inter = len(sys.argv) > 5 and sys.argv[5] == 'int'
out = parse_class((ROOT / 'proof' / 'n51_local' / 'reg11_S2.txt').read_text().split()[ci])
check_class(out)
t0 = time.time()
st, sol = solve(out, time_limit=tl, workers=w, fix_J=J, intersecting=inter)
rec = {'class': ci, 'J': J, 'status': st, 'secs': round(time.time() - t0, 1), 'intersecting': inter}
if sol:
    rec['j'] = sol['j']
    rec['Q'] = [[S, t, m] for S, t, m in sol['Q']]
    rec['heavy'] = sorted([(popc(S), t, m) for S, t, m in sol['Q'] if popc(S) > 5], reverse=True)
print(json.dumps(rec), flush=True)

"""Speed probe: CP-SAT on the N = 52 local model with the j-vector fixed.  Usage: CLASS TL WORKERS j0,j1,...,j10"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n52_tight_cpsat import solve  # noqa: E402
from n52_tight_local import check_class, parse_class, popc, ROOT  # noqa: E402

ci, tl, w = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
j = [int(x) for x in sys.argv[4].split(',')]
out = parse_class((ROOT / 'proof' / 'n51_local' / 'reg11_S2.txt').read_text().split()[ci])
check_class(out)
t0 = time.time()
st, sol = solve(out, time_limit=tl, workers=w, fix_j=j)
print(ci, j, st, f'{time.time() - t0:.1f}s',
      sorted([(popc(S), t, m) for S, t, m in sol['Q'] if popc(S) > 5], reverse=True) if sol else '')

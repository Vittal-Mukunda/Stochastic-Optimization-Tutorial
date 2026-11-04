"""R8-E exploration: heavy-pattern counts per partition, and class-free survivors (c free per pair)."""
import itertools
import sys
import time

from r8e_lib import heavy_patterns, pattern_data, d_bounds, solve_sets, partitions

cmin = int(sys.argv[1]) if len(sys.argv) > 1 else 1
Jmax = int(sys.argv[2]) if len(sys.argv) > 2 else 5
for J in range(0, Jmax + 1):
    for part in partitions(J):
        t0 = time.time()
        p = len(part)
        Hs = heavy_patterns(list(part), 14 - J)
        surv = []
        for H in Hs:
            pd = pattern_data(list(part), H)
            # (P2) with the most favourable c(u, v) = 3 for u in V_0
            if any(pd['Ex'][v] < 0 for v in range(p)):
                continue
            pairs = list(itertools.combinations(range(p), 2))
            # c(u, v) on a pair of V_+ only affects that pair's interval: allowed D = union over c of [lo_c, hi_c]
            allowed = {pr: set() for pr in pairs}
            for cc in range(cmin, 5):
                bnd = d_bounds({pr: cc for pr in pairs}, pd, p)
                for pr in pairs:
                    allowed[pr] |= set(range(bnd[pr][0], bnd[pr][1] + 1))
            sol = solve_sets({pr: sorted(allowed[pr]) for pr in pairs}, pd['rho'], p)
            found = (None, sol) if sol is not None else None
            if found:
                surv.append((H, found))
        print(J, part, 'patterns', len(Hs), 'class-free survivors', len(surv), f'{time.time() - t0:.1f}s', flush=True)
        for H, f in surv[:5]:
            print('   ', H, f[0])

"""R8-E: cross-check the reduction (r8e_lib.decide_placement) against HiGHS MILP on the UNREDUCED pair-level rows.

The MILP has every variable of the brief's system: n_M for all M subset of V_+ with |M| <= 5, nlight, L_u, Ex_u and
D, k, s on all 55 pairs, with c fixed by the class.  HiGHS is floating point; this is a consistency check of the
reduction, not a certificate.  Usage: python r8e_highs_crosscheck.py NSAMPLE SEED
"""
import itertools
import json
import random
import sys
import time
from pathlib import Path

import highspy

from r8e_lib import NR, NO, LAM, parse, cmatrix, partitions, placements, decide_placement

ROOT = Path(__file__).resolve().parents[2]


def milp(c, jv, tl=60.0):
    J = sum(jv)
    pos = [r for r in range(NR) if jv[r] > 0]
    h = highspy.Highs()
    h.setOptionValue('output_flag', False)
    h.setOptionValue('threads', 1)
    h.setOptionValue('time_limit', tl)
    I = highspy.HighsVarType.kInteger
    sets = [frozenset(M) for k in range(0, min(len(pos), 5) + 1) for M in itertools.combinations(pos, k)]
    n = {M: h.addVariable(0, 14 - J, type=I) for M in sets}
    nlight = h.addVariable(0, NO, type=I)
    h.addConstr(sum((6 - len(M)) * n[M] for M in sets) == 14 - J)
    h.addConstr(nlight + sum(n[M] for M in sets) == NO)
    L, Ex = {}, {}
    for u in range(NR):
        hs = [M for M in sets if u in M]
        L[u] = h.addVariable(0, 20 + jv[u], type=I)
        Ex[u] = h.addVariable(0, 5 + 10 * jv[u], type=I)
        h.addConstr(L[u] + sum(n[M] for M in hs) == 20 + jv[u])
        h.addConstr(Ex[u] + sum(LAM[11 - len(M)] * n[M] for M in hs) == 5 + 10 * jv[u])
    h.addConstr(sum(L[u] for u in range(NR)) - 6 * nlight == 0)
    D, k, s = {}, {}, {}
    for u, v in itertools.combinations(range(NR), 2):
        hs = [M for M in sets if u in M and v in M]
        lo = 12 if (jv[u] and jv[v]) else 12
        hi = 43 if (jv[u] and jv[v]) else 12        # Lemma A: |D(u, v)| = 12 when j_u = 0 or j_v = 0
        D[u, v] = D[v, u] = h.addVariable(lo, hi, type=I)
        k[u, v] = k[v, u] = h.addVariable(0, NO, type=I)
        s[u, v] = s[v, u] = h.addVariable(0, 5 + 10 * max(jv[u], jv[v]), type=I)
        h.addConstr(D[u, v] - k[u, v] - sum(n[M] for M in hs) == c[u][v])
        h.addConstr(s[u, v] - 4 * D[u, v] + sum((6 - len(M)) * n[M] for M in hs) == -c[u][v] - 45)
        h.addConstr(s[u, v] - Ex[u] <= 0)
        h.addConstr(s[u, v] - Ex[v] <= 0)
    for u in range(NR):
        o = [v for v in range(NR) if v != u]
        hs = [M for M in sets if u in M]
        h.addConstr(sum(s[u, v] for v in o) - 2 * Ex[u] == 0)
        h.addConstr(sum(k[u, v] for v in o) - 5 * L[u] == 0)
        h.addConstr(sum(D[u, v] for v in o) + sum((6 - len(M)) * n[M] for M in hs) == 120 + 5 * jv[u])
    h.run()
    st = h.modelStatusToString(h.getModelStatus())
    return st


def main():
    ns = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    s2 = [l.strip() for l in (ROOT / 'proof/n51_local/reg11_S2.txt').read_text().split()]
    allc = [l.strip() for l in (ROOT / 'proof/n51_local/reg11.txt').read_text().split()]
    nons2 = [l for l in allc if l not in set(s2)]
    suites = [('S2', s2, [p for J in range(2, 6) for p in partitions(J)]),
              ('S2-J6', s2, [(2, 2, 1, 1), (2, 1, 1, 1, 1), (1,) * 6, (2, 2, 2), (3, 1, 1, 1)]),
              ('nonS2-c0', nons2, [(2, 1, 1, 1), (1,) * 5, (2, 2, 1), (1, 1, 1, 1)])]
    out = []
    for name, lines, parts in suites:
        agree = disagree = 0
        tally = {}
        t0 = time.time()
        tries = 0
        while sum(tally.values()) < ns and tries < 50 * ns:
            tries += 1
            line = rng.choice(lines)
            c = cmatrix(parse(line))
            part = rng.choice(parts)
            jv = rng.choice(list(placements(part)))
            mine, _ = decide_placement(c, jv)
            if not mine and _ == 'lemmaA' and rng.random() < 0.9:
                continue                      # keep only a few Lemma-A-excluded samples
            st = milp(c, jv) if _ != 'lemmaA' else 'Infeasible (Lemma A filter, not solved)'
            hfeas = st.startswith('Optimal') or st == 'Feasible'
            hinf = st.startswith('Infeasible')
            key = f"{','.join(map(str, part))}:{'F' if mine else 'I'}:{st}"
            tally[key] = tally.get(key, 0) + 1
            if (mine and hfeas) or (not mine and hinf):
                agree += 1
            else:
                disagree += 1
                out.append({'suite': name, 'class': line, 'j': jv, 'mine': mine, 'highs': st})
        rec = {'suite': name, 'samples': sum(tally.values()), 'agree': agree, 'disagree': disagree,
               'secs': round(time.time() - t0, 1), 'tally': tally}
        print(json.dumps(rec), flush=True)
        out.append(rec)
    (ROOT / 'research/CERTIFICATES/r8e_highs_crosscheck.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()

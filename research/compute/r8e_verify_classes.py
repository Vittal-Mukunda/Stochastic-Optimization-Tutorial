"""R8-E: verify proof/n51_local/reg11_S2.txt (and reg11.txt) independently.

Checks: each line is a 5-regular tournament on 11 vertices; S_2 (every pair has a common dominator inside);
pairwise non-isomorphic (own backtracking isomorphism test, bucketed by vertex invariants); exact |Aut|;
completeness by orbit counting: sum over listed classes of 11!/|Aut T| must equal the number of labelled
5-regular (resp. 5-regular S_2) tournaments on {0..10}, which is computed here from scratch by rooting at vertex 0:
N^+(0) = {1..5}, A = T[{1..5}], B = T[{6..10}], cross matrix X (X[a][b] = 1 iff a -> b) with row sums 5 - out_A(a)
and column sums 1 + out_B(b); the labelled count is C(10,5) * sum over labelled (A, B) of #valid X, and #valid X is
constant on isomorphism classes of A and of B.
"""
import itertools
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

from r8e_lib import parse, cmatrix, vertex_invariant, isomorphisms, automorphisms, to_string

ROOT = Path(__file__).resolve().parents[2]


def tour5_classes():
    """Isomorphism classes of tournaments on 5 labelled vertices: list of (rep adjacency, |Aut|, #labelled)."""
    pairs = list(itertools.combinations(range(5), 2))
    seen = {}
    for bits in range(1 << 10):
        adj = [[0] * 5 for _ in range(5)]
        for k, (i, j) in enumerate(pairs):
            if bits >> k & 1:
                adj[i][j] = 1
            else:
                adj[j][i] = 1
        canon = min(tuple(adj[p[i]][p[j]] for i in range(5) for j in range(5)) for p in itertools.permutations(range(5)))
        seen.setdefault(canon, []).append(adj)
    out = []
    for canon, members in seen.items():
        rep = members[0]
        aut = sum(1 for p in itertools.permutations(range(5))
                  if all(rep[p[i]][p[j]] == rep[i][j] for i in range(5) for j in range(5)))
        assert len(members) * aut == 120
        out.append((rep, aut, len(members)))
    return out


def matrices(rows, cols):
    """All 5x5 0/1 matrices with given row and column sums."""
    res = []
    cur = []

    def rec(i, colrem):
        if i == 5:
            if all(x == 0 for x in colrem):
                res.append([r[:] for r in cur])
            return
        for S in itertools.combinations(range(5), rows[i]):
            if any(colrem[b] == 0 for b in S):
                continue
            row = [1 if b in S else 0 for b in range(5)]
            cr = [colrem[b] - row[b] for b in range(5)]
            # remaining rows must be able to fill columns
            if any(x > 4 - i for x in cr):
                continue
            cur.append(row)
            rec(i + 1, cr)
            cur.pop()

    if sum(rows) != sum(cols):
        return res
    rec(0, list(cols))
    return res


def labelled_counts():
    cls = tour5_classes()
    assert len(cls) == 12 and sum(m for _, _, m in cls) == 1024
    total_reg = 0
    total_s2 = 0
    nX = 0
    for A, autA, mA in cls:
        for B, autB, mB in cls:
            rows = [5 - sum(A[a]) for a in range(5)]
            cols = [1 + sum(B[b]) for b in range(5)]
            Xs = matrices(rows, cols)
            nX += len(Xs)
            s2 = 0
            for X in Xs:
                adj = np.zeros((11, 11), dtype=np.int64)
                for a in range(5):
                    adj[0, 1 + a] = 1
                    adj[6 + a, 0] = 1
                    for a2 in range(5):
                        adj[1 + a, 1 + a2] = A[a][a2]
                        adj[6 + a, 6 + a2] = B[a][a2]
                    for b in range(5):
                        if X[a][b]:
                            adj[1 + a, 6 + b] = 1
                        else:
                            adj[6 + b, 1 + a] = 1
                assert (adj.sum(axis=1) == 5).all() and ((adj + adj.T + np.eye(11, dtype=np.int64)) == 1).all()
                c = adj.T @ adj
                np.fill_diagonal(c, 99)
                if c.min() >= 1:
                    s2 += 1
            total_reg += mA * mB * len(Xs)
            total_s2 += mA * mB * s2
    k = math.comb(10, 5)
    return k * total_reg, k * total_s2, nX


def check_file(path, want_s2):
    lines = [l.strip() for l in Path(path).read_text().splitlines() if l.strip()]
    advs = [parse(l) for l in lines]
    info = {'file': str(path), 'lines': len(lines)}
    reg = all(all(sum(row) == 5 for row in adj) for adj in advs)
    roundtrip = all(to_string(adj) == l for adj, l in zip(advs, lines))
    cms = [cmatrix(adj) for adj in advs]
    s2flags = [min(c[u][v] for u in range(11) for v in range(11) if u != v) >= 1 for c in cms]
    cmax = max(max(c[u][v] for u in range(11) for v in range(11) if u != v) for c in cms)
    invs = [vertex_invariant(adj, c) for adj, c in zip(advs, cms)]
    buckets = {}
    for i, inv in enumerate(invs):
        buckets.setdefault(tuple(sorted(inv)), []).append(i)
    iso_pairs = []
    for b in buckets.values():
        for i, j in itertools.combinations(b, 2):
            if isomorphisms(advs[i], advs[j], invs[i], invs[j], first_only=True):
                iso_pairs.append((i, j))
    auts = [automorphisms(adj) for adj in advs]
    orbit_sum = sum(math.factorial(11) // len(a) for a in auts)
    info.update(five_regular=reg, roundtrip=roundtrip, n_S2=sum(s2flags), all_S2=all(s2flags),
                max_c=cmax, invariant_buckets=len(buckets), isomorphic_pairs=iso_pairs,
                aut_orders=sorted(set(len(a) for a in auts)),
                aut_order_counts={str(k): sum(1 for a in auts if len(a) == k) for k in sorted(set(len(a) for a in auts))},
                sum_11fact_over_aut=orbit_sum)
    return info, auts


def main():
    t0 = time.time()
    lab_reg, lab_s2, nX = labelled_counts()
    t1 = time.time()
    res = {'labelled_regular': lab_reg, 'labelled_regular_S2': lab_s2, 'rooted_cross_matrices': nX,
           'secs_counts': round(t1 - t0, 1)}
    print(json.dumps(res), flush=True)
    s2info, s2auts = check_file(ROOT / 'proof' / 'n51_local' / 'reg11_S2.txt', True)
    s2info['complete'] = s2info['sum_11fact_over_aut'] == lab_s2 and not s2info['isomorphic_pairs'] and s2info['all_S2']
    print(json.dumps(s2info), flush=True)
    allinfo, allauts = check_file(ROOT / 'proof' / 'n51_local' / 'reg11.txt', False)
    allinfo['complete'] = allinfo['sum_11fact_over_aut'] == lab_reg and not allinfo['isomorphic_pairs']
    print(json.dumps(allinfo), flush=True)
    # S_2 members of reg11.txt must be exactly the reg11_S2.txt classes (up to isomorphism)
    s2lines = [l.strip() for l in (ROOT / 'proof/n51_local/reg11_S2.txt').read_text().splitlines() if l.strip()]
    alllines = [l.strip() for l in (ROOT / 'proof/n51_local/reg11.txt').read_text().splitlines() if l.strip()]
    s2set = set(s2lines)
    allS2 = [l for l in alllines if min(cmatrix(parse(l))[u][v] for u in range(11) for v in range(11) if u != v) >= 1]
    same_strings = set(allS2) == s2set
    res.update(reg11_S2=s2info, reg11=allinfo, S2_subset_of_reg11_identical_strings=same_strings,
               secs_total=round(time.time() - t0, 1))
    res['reg11_S2_aut'] = [len(a) for a in s2auts]
    res['reg11_S2_aut_generators_note'] = 'full automorphism groups recomputed by r8e_lib.automorphisms'
    out = ROOT / 'research' / 'CERTIFICATES' / 'r8e_classes_verification.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(res, indent=1))
    print('same strings:', same_strings, 'total secs', res['secs_total'])


if __name__ == '__main__':
    main()

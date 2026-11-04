"""R8-E certificate checker (self-contained; imports nothing from r8e_lib / n52_pairlevel).

Reduced pair-level system for a tight pair at N = 52 with j-partition `part` placed on positions 0..p-1 of V_+
(see r8e_lib.py docstring for the derivation from the brief's rows).  A heavy pattern is a multiset {M: n} of
subsets of V_+ with sum n (6 - |M|) = 14 - J.  Infeasibility of a pattern is shown by
  P1: Ex_u < 0 or L_u < 0 for some u                      (checked here directly)
  P2: c(u, v) + Ex_v < 3 for some u in V_0, v in V_+        (per class; checked here directly)
  P3: a tree certificate for: integer D on pairs of V_+ in the domains below with row sums rho_u.
      ['E', a, b] empty domain | ['F', y] box/gcd-infeasible row combination | ['S', a, b, t, L, R] split.
Usage: python r8e_check_certificates.py [--perclass]
"""
import gzip, itertools, json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CD = ROOT / 'research' / 'CERTIFICATES'
LAM = {6: 4, 7: 7, 8: 9, 9: 10, 10: 10, 11: 10}


def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0:
        yield ()
    for q in range(min(n, mx), 0, -1):
        for r in parts(n - q, q):
            yield (q,) + r


def all_patterns(p, total):  # every multiset, no pruning
    subs = [S for k in range(min(p, 5) + 1) for S in itertools.combinations(range(p), k)]
    def rec(i, rem):
        if rem == 0:
            yield ()
        elif i < len(subs):
            for n in range(rem // (6 - len(subs[i])), -1, -1):
                for r in rec(i + 1, rem - n * (6 - len(subs[i]))):
                    yield (((subs[i], n),) if n else ()) + r
    yield from rec(0, total)


def key(H):
    return ';'.join(f"{''.join(map(str, M)) or '-'}x{n}" for M, n in sorted(H, key=lambda t: (len(t[0]), t[0])))


def data(part, H):
    p = len(part)
    Ex = [5 + 10 * j for j in part]; L = [20 + j for j in part]; tau = [0] * p
    h = {pr: 0 for pr in itertools.combinations(range(p), 2)}; E = dict(h)
    for M, n in H:
        for u in M:
            Ex[u] -= n * LAM[11 - len(M)]; L[u] -= n; tau[u] += n * (6 - len(M))
        for pr in itertools.combinations(M, 2):
            h[pr] += n; E[pr] += n * (6 - len(M))
    rho = [120 + 5 * part[u] - tau[u] - 12 * (11 - p) for u in range(p)]
    return Ex, L, h, E, rho


def dom(c, a, b, Ex, h, E):
    lo = max(12, c + h[a, b], -(-(c + 45 + E[a, b]) // 4))
    hi = min(43, 39 + c + h[a, b], (c + 45 + E[a, b] + min(Ex[a], Ex[b])) // 4)
    return set(range(lo, hi + 1))


def verify(t, D, rho):
    if t[0] == 'E':
        return not D[t[1], t[2]]
    if t[0] == 'F':
        y = t[1]; tt = sum(y[u] * rho[u] for u in range(len(rho))); lo = hi = g = 0
        for (a, b), S in D.items():
            k = y[a] + y[b]
            if k:
                if not S:
                    return True
                lo += min(k * min(S), k * max(S)); hi += max(k * min(S), k * max(S)); g = math.gcd(g, abs(k))
        return tt < lo or tt > hi or (g > 0 and tt % g != 0)
    a, b, s = t[1], t[2], t[3]
    L = dict(D); L[a, b] = {d for d in D[a, b] if d <= s}
    R = dict(D); R[a, b] = {d for d in D[a, b] if d > s}
    return verify(t[4], L, rho) and verify(t[5], R, rho)


def p1(part, H):
    Ex, L, *_ = data(part, H)
    return min(Ex + L) < 0


def check_classfree(fn, cmin):
    cert = json.loads(fn.read_text()); assert cert['cmin'] == cmin
    by = {tuple(d['part']): {r['H']: r for r in d['patterns']} for d in cert['partitions']}
    n_checked = n_p1 = 0
    for J in range(cert['Jmin'], cert['Jmax'] + 1):
        for part in parts(J):
            p = len(part)
            for H in all_patterns(p, 14 - J):
                if p1(part, H):
                    n_p1 += 1; continue
                Ex, L, h, E, rho = data(part, H)
                D = {pr: set().union(*(dom(c, *pr, Ex, h, E) for c in range(cmin, 5))) for pr in h}
                r = by[part][key(H)]
                assert 'tree' in r and verify(r['tree'], D, rho), (part, key(H))
                n_checked += 1
    return n_p1, n_checked


def parse(s):
    A = [[0] * 11 for _ in range(11)]
    for k, (i, j) in enumerate(itertools.combinations(range(11), 2)):
        A[i][j], A[j][i] = (1, 0) if s[k] == '1' else (0, 1)
    return A


def check_classes(fn):
    out = []
    for s in fn.read_text().split():
        A = parse(s); assert all(sum(r) == 5 for r in A)
        c = [[sum(A[w][u] * A[w][v] for w in range(11)) for v in range(11)] for u in range(11)]
        assert all(1 <= c[u][v] <= 4 for u in range(11) for v in range(11) if u != v)
        out.append((A, c))
    return out


def check_perclass(fn, classes):
    cert = json.load(gzip.open(fn, 'rt')); m = cert['meta']
    p3 = {(tuple(a), b, tuple(ct)): t for a, b, ct, t in cert['p3']}
    done = {}; nplac = norb = nA = 0
    for J in range(m['Jmin'], m['Jmax'] + 1):
        for part in parts(J):
            p = len(part); pairs = list(itertools.combinations(range(p), 2))
            mine = {key(H) for H in all_patterns(p, 14 - J) if not p1(part, H)}
            plist = cert['patterns'][','.join(map(str, part))]; assert set(plist) == mine
            Hs = [[(tuple(int(x) for x in t.split('x')[0].replace('-', '')), int(t.split('x')[1])) for t in k.split(';')]
                  if k else [] for k in plist]
            datas = [data(part, H) for H in Hs]
            vals = [(v, part.count(v)) for v in sorted(set(part), reverse=True)]
            for ci, (A, c) in enumerate(classes):
                auts = cert['auts'].get(str(ci), [list(range(11))])
                assert all(A[f[i]][f[k]] == A[i][k] for f in auts for i in range(11) for k in range(11))
                seen = set()
                for jv in jvecs(vals):
                    nplac += 1
                    rep = max(tuple(jv[f.index(x)] for x in range(11)) for f in auts)
                    if rep in seen:
                        continue
                    seen.add(rep); norb += 1; jv = rep
                    Vp = sorted([r for r in range(11) if jv[r]], key=lambda r: (-jv[r], r))
                    V0 = [r for r in range(11) if not jv[r]]
                    if any(c[u][v] == 4 for u in V0 for v in range(11) if v != u):
                        nA += 1; continue
                    ct = tuple(c[Vp[a]][Vp[b]] for a, b in pairs)
                    for hi, (Ex, L, h, E, rho) in enumerate(datas):
                        if any(c[u][Vp[b]] + Ex[b] < 3 for u in V0 for b in range(p)):
                            continue
                        k3 = (part, hi, ct)
                        if k3 not in done:
                            D = {pr: dom(c[Vp[pr[0]]][Vp[pr[1]]], *pr, Ex, h, E) for pr in pairs}
                            done[k3] = p3.get(k3) is not None and verify(p3[k3], D, rho)
                        assert done[k3], (ci, jv, hi)
    return nplac, norb, nA, len(done)


def jvecs(vals):
    def rec(i, free, jv):
        if i == len(vals):
            yield tuple(jv); return
        v, m = vals[i]
        for S in itertools.combinations(free, m):
            for x in S: jv[x] = v
            yield from rec(i + 1, [x for x in free if x not in S], jv)
            for x in S: jv[x] = 0
    yield from rec(0, list(range(11)), [0] * 11)


if __name__ == '__main__':
    classes = check_classes(ROOT / 'proof' / 'n51_local' / 'reg11_S2.txt')
    print('reg11_S2.txt:', len(classes), 'classes, all 5-regular with 1 <= c <= 4')
    n_p1, n_tree = check_classfree(CD / 'r8e_classfree_c1_J0-5.json', 1)
    print(f'class-free J<=5, c in [1,4]: {n_p1} patterns killed by P1, {n_tree} by verified P3 trees -> ALL INFEASIBLE')
    if '--perclass' in sys.argv:
        print('per-class replay (placements, orbits, Lemma-A excluded, P3 keys verified):',
              check_perclass(CD / 'r8e_perclass_S2_J0-5.json.gz', classes))
    print('CHECK PASSED')

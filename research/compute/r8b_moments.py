"""R8-B: solver-free checks for the no-tight branch at order 52.

1. Identity checks G1-G6, D1-D3 on random tournaments (every tournament / 25-26 degrees).
2. Third-moment integer search inside a 12-regular tournament W on 25 vertices
   with every pair-common-in-neighbour count in {5,6} (the equality case of c >= 5).
3. Exact moments on the recorded z5-symmetric W (r8b_W25_cpsat_s3_z5.json).
4. Pair-level necessary-condition filter at a 12-dominator pair (no T[R] arcs).
"""
from __future__ import annotations

import itertools
import json
import random
import sys
from collections import Counter
from math import comb
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent


def rand_tour(n, rng):
    A = np.zeros((n, n), dtype=np.int64)
    for i, j in itertools.combinations(range(n), 2):
        if rng.random() < 0.5:
            A[i, j] = 1
        else:
            A[j, i] = 1
    return A


def tour_2526(rng, flips=8000):
    n = 52
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for d in range(1, 26):
            A[i, (i + d) % n] = 1
    for i in range(26):
        A[i, i + 26] = 1
    for _ in range(flips):
        x, y, z = rng.sample(range(n), 3)
        if A[x, y] and A[y, z] and A[z, x]:
            A[x, y] = A[y, z] = A[z, x] = 0
            A[y, x] = A[z, y] = A[x, z] = 1
    return A


def Dset(A, X):
    X = list(X)
    n = len(A)
    return [w for w in range(n) if w not in X and all(A[w, x] for x in X)]


def check_identities(A, rng, deg2526=False):
    n = len(A)
    din = A.sum(axis=0)
    dout = A.sum(axis=1)
    ok = True
    notes = []
    Dpair = {}
    for u, w in itertools.combinations(range(n), 2):
        Dpair[u, w] = Dpair[w, u] = len(Dset(A, (u, w)))
    for w in range(n):
        lhs = sum(Dpair[w, b] for b in range(n) if A[w, b])
        rhs = sum(int(dout[x]) - 1 for x in range(n) if A[x, w]) - comb(int(din[w]), 2)
        if lhs != rhs:
            ok = False
            notes.append(('G1', w, lhs, rhs))
        if sum(Dpair[a, w] for a in range(n) if A[a, w]) != comb(int(din[w]), 2):
            ok = False
            notes.append(('G2', w))
    if sum(Dpair[u, w] for u, w in itertools.combinations(range(n), 2)) != sum(comb(int(d), 2) for d in dout):
        ok = False
        notes.append('G3a')
    if sum(comb(int(d), 2) for d in dout) != sum(comb(int(d), 2) for d in din):
        ok = False
        notes.append('G3b')
    for v in rng.sample(range(n), min(3, n)):
        Wv = [x for x in range(n) if A[x, v]]
        Bv = [x for x in range(n) if A[v, x]]
        lhs = sum(Dpair[p, q] for p, q in itertools.combinations(Wv, 2))
        rhs = sum(comb(int(sum(A[w, x] for x in Wv)), 2) for w in Wv) + \
            sum(comb(len([x for x in Wv if not A[x, b]]), 2) for b in Bv)
        if lhs != rhs:
            ok = False
            notes.append(('G4', v, lhs, rhs))
    g6n = 0
    for _ in range(200):
        p, q = rng.sample(range(n), 2)
        R = Dset(A, (p, q))
        if len(R) != 12:
            continue
        g6n += 1
        if g6n > 2:
            break
        O = [y for y in range(n) if y not in R and y not in (p, q)]
        t = {r: int(sum(A[x, r] for x in R)) - 5 for r in R}
        for u in R:
            lhs = sum(Dpair[u, w] for w in R if w != u)
            rhs = sum(int(sum(A[wp, x] for x in R)) - 1 for wp in R if A[wp, u]) + \
                sum(len([r for r in R if A[y, r]]) - 1 for y in O if A[y, u])
            if lhs != rhs:
                ok = False
                notes.append(('G5', u, lhs, rhs))
        for u, w in itertools.combinations(R, 2):
            s = sum(len(Dset(A, (u, w, x))) - 5 for x in R if x not in (u, w))
            C = [wp for wp in R if A[wp, u] and A[wp, w]]
            K = [y for y in O if A[y, u] and A[y, w]]
            TC = sum(t[x] for x in C)
            Eb = sum(len([r for r in R if A[r, y]]) - 5 for y in K)
            pred = 5 * Dpair[u, w] - len(C) - 50 - TC - Eb
            if s != pred:
                ok = False
                notes.append(('G6', u, w, s, pred))
    if deg2526:
        L = [x for x in range(n) if din[x] == 25]
        H = [x for x in range(n) if din[x] == 26]
        if len(L) != 26 or len(H) != 26:
            ok = False
            notes.append(('deg', len(L), len(H)))
        Ls = set(L)
        for w in range(n):
            ex = sum(Dpair[w, b] - 12 for b in range(n) if A[w, b])
            if w in Ls:
                if ex != 13 - int(sum(A[w, x] for x in L)):
                    ok = False
                    notes.append(('D1', w, ex))
            else:
                if ex != int(sum(A[w, x] for x in H)):
                    ok = False
                    notes.append(('D2', w, ex))
            exin = sum(Dpair[a, w] - 12 for a in range(n) if A[a, w])
            want = 0 if w in Ls else 13
            if exin != want:
                ok = False
                notes.append(('D3', w, exin, want))
    return ok, notes, g6n


def analyze_W(A):
    n = len(A)
    din = A.sum(axis=0)
    dout = A.sum(axis=1)
    C = A.T @ A
    c_off = C[~np.eye(n, dtype=bool)]
    hist = {int(k): int(v) for k, v in zip(*np.unique(C[np.triu_indices(n, 1)], return_counts=True))}
    # k, nu on triples
    k_list = []
    nu_list = []
    sigma = []
    csum = []
    for x, y, z in itertools.combinations(range(n), 3):
        k = int((A[:, x] & A[:, y] & A[:, z]).sum())
        nu = int((A[x, :] & A[y, :] & A[z, :]).sum())
        # transitivity: one vertex beats the other two
        beats = (A[x, y] and A[x, z]) or (A[y, x] and A[y, z]) or (A[z, x] and A[z, y])
        cyc = (A[x, y] and A[y, z] and A[z, x]) or (A[x, z] and A[z, y] and A[y, x])
        sig = 0 if cyc else 1
        cs = int(C[x, y] + C[x, z] + C[y, z])
        k_list.append(k)
        nu_list.append(nu)
        sigma.append(sig)
        csum.append(cs)
        # identity: k + nu == cs - 11 - sig
        if k + nu != cs - 11 - sig:
            return {'error': 'M1_fail', 'triple': (x, y, z), 'k': k, 'nu': nu, 'cs': cs, 'sig': sig}
    k_arr = np.array(k_list)
    nu_arr = np.array(nu_list)
    sig_arr = np.array(sigma)
    trans = sig_arr == 1
    cyc = ~trans
    return {
        'n': n,
        'regular_12': bool((din == 12).all() and (dout == 12).all()),
        'c_hist': hist,
        'cmin': int(c_off.min()),
        'S3': bool((k_arr >= 1).all()),
        'transitive': int(trans.sum()),
        'cyclic': int(cyc.sum()),
        'sum_k': int(k_arr.sum()),
        'sum_k_trans': int(k_arr[trans].sum()),
        'sum_k_cyc': int(k_arr[cyc].sum()),
        'sum_nu': int(nu_arr.sum()),
        'sum_C_k_2': int(sum(comb(int(k), 2) for k in k_arr)),
        'sum_C_nu_2': int(sum(comb(int(nu), 2) for nu in nu_arr)),
        'sum_C_k_3': int(sum(comb(int(k), 3) for k in k_arr)),
        'sum_C_nu_3': int(sum(comb(int(nu), 3) for nu in nu_arr)),
        'k_hist': {int(a): int(b) for a, b in zip(*np.unique(k_arr, return_counts=True))},
        'k_hist_trans': {int(a): int(b) for a, b in zip(*np.unique(k_arr[trans], return_counts=True))},
        'k_hist_cyc': {int(a): int(b) for a, b in zip(*np.unique(k_arr[cyc], return_counts=True))},
        'nu_hist': {int(a): int(b) for a, b in zip(*np.unique(nu_arr, return_counts=True))},
        'min_k': int(k_arr.min()),
        'mean_k_trans': float(k_arr[trans].mean()) if trans.any() else None,
        'mean_k_cyc': float(k_arr[cyc].mean()) if cyc.any() else None,
        'C_c_3': int(sum(comb(int(C[i, j]), 3) for i, j in itertools.combinations(range(n), 2))),
    }


def search_W_margin():
    """Integer points of the W-internal moments with c in {5,6}, k>=1.

    Forced (c in {5,6} on a 12-regular W of order 25):
      150 pairs c=5, 150 pairs c=6
      1650 trans, 650 cyc
      sum k = 5500, sum k_trans = 3750, sum k_cyc = 1750
      sum C(k,2) = 4500
      sum C(k,3) = sum C(nu,3)
      k + nu = 4 + delta - sigma, delta = #c=6 pairs in the triple in {0,1,2,3}
    We do not know the (delta, sigma) joint, so we search over level L = k+nu
    in {3,4,5,6,7} with k>=1, nu=L-k>=0.
    """
    # First: ignore the delta split, only use first/second/third moments and min k=1
    # Variables n_{k,nu} for feasible (k,nu)
    from ortools.sat.python import cp_model

    # levels possible: L = 4+delta-sigma in {3,4,5,6,7}
    pairs = []
    for L in range(3, 8):
        for k in range(1, L + 1):
            pairs.append((k, L - k, L))
    m = cp_model.CpModel()
    n = {p: m.NewIntVar(0, 2300, f'n{p}') for p in pairs}
    m.Add(sum(n.values()) == 2300)
    m.Add(sum(n[p] for p in pairs if p[2] % 2 == 1 or True) == 2300)
    # trans vs cyc unknown split of levels; only global moments
    m.Add(sum(p[0] * n[p] for p in pairs) == 5500)
    m.Add(sum(p[1] * n[p] for p in pairs) == 5500)  # mu=c so sum nu = sum k in regular
    m.Add(sum(comb(p[0], 2) * n[p] for p in pairs) == 4500)
    m.Add(sum(comb(p[1], 2) * n[p] for p in pairs) == 4500)
    m.Add(sum(comb(p[0], 3) * n[p] for p in pairs) == sum(comb(p[1], 3) * n[p] for p in pairs))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = 30
    s.parameters.num_workers = 2
    st = s.Solve(m)
    rec = {'status': s.StatusName(st)}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        rec['rows'] = [[p[0], p[1], p[2], s.Value(n[p])] for p in pairs if s.Value(n[p])]
        rec['sum_k'] = sum(p[0] * s.Value(n[p]) for p in pairs)
        rec['sum_Ck2'] = sum(comb(p[0], 2) * s.Value(n[p]) for p in pairs)
        rec['Ck3_minus_Cnu3'] = sum((comb(p[0], 3) - comb(p[1], 3)) * s.Value(n[p]) for p in pairs)
        rec['min_k'] = min(p[0] for p in pairs if s.Value(n[p]))
    # With the forced trans/cyc first moments
    m2 = cp_model.CpModel()
    # L_trans = 4+delta-1 = 3+delta in {3,4,5,6}; L_cyc = 4+delta in {4,5,6,7}
    nT = {}
    nC = {}
    for delta in range(4):
        Lt = 3 + delta
        Lc = 4 + delta
        for k in range(1, Lt + 1):
            nT[delta, k] = m2.NewIntVar(0, 1650, '')
        for k in range(1, Lc + 1):
            nC[delta, k] = m2.NewIntVar(0, 650, '')
    m2.Add(sum(nT.values()) == 1650)
    m2.Add(sum(nC.values()) == 650)
    m2.Add(sum(k * nT[d, k] for d, k in nT) == 3750)
    m2.Add(sum(k * nC[d, k] for d, k in nC) == 1750)
    m2.Add(sum(comb(k, 2) * nT[d, k] + comb(k, 2) * nC[d, k] for (d, k) in nT for _ in [0] if False) == 0)
    m2.Add(sum(comb(k, 2) * nT[d, k] for d, k in nT) + sum(comb(k, 2) * nC[d, k] for d, k in nC) == 4500)
    # nu = L-k; sum nu = 5500 already if sum k = 5500 and we don't constrain sum nu separately
    # third moment
    def nuT(d, k):
        return (3 + d) - k
    def nuC(d, k):
        return (4 + d) - k
    m2.Add(sum(comb(k, 3) * nT[d, k] for d, k in nT) + sum(comb(k, 3) * nC[d, k] for d, k in nC)
           == sum(comb(nuT(d, k), 3) * nT[d, k] for d, k in nT) + sum(comb(nuC(d, k), 3) * nC[d, k] for d, k in nC))
    # also sum nu
    m2.Add(sum(nuT(d, k) * nT[d, k] for d, k in nT) + sum(nuC(d, k) * nC[d, k] for d, k in nC) == 5500)
    m2.Add(sum(comb(nuT(d, k), 2) * nT[d, k] for d, k in nT) + sum(comb(nuC(d, k), 2) * nC[d, k] for d, k in nC) == 4500)
    st2 = s.Solve(m2)
    rec['with_trans_cyc'] = {'status': s.StatusName(st2)}
    if st2 in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        rec['with_trans_cyc']['trans'] = [[d, k, 3 + d - k, s.Value(nT[d, k])] for d, k in nT if s.Value(nT[d, k])]
        rec['with_trans_cyc']['cyc'] = [[d, k, 4 + d - k, s.Value(nC[d, k])] for d, k in nC if s.Value(nC[d, k])]
        rec['with_trans_cyc']['min_k'] = min(
            [k for d, k in nT if s.Value(nT[d, k])] + [k for d, k in nC if s.Value(nC[d, k])])
    return rec


def pairlevel_filter():
    """Solver-free necessary conditions at a 12-dominator pair, integer only.

    t_r >= 0, sum t = 6.
    E_R = sum e_r, e_r in {0,1} in the binary case, E_R + e_a <= 13.
    For r with e_r = 0: every in-pair of r has |D| = 12, so in particular
    the 5+t_r in-neighbours in R have |D|=12.
    s(u,w) = 5 D - c - 50 - T_C - E_both >= 0.
    When D=12: c + T_C + E_both <= 10.
    c >= 1, T_C >= 0, E_both >= 0.

    Pair-sum at u in R:
      sum_{w in R, w != u} |D(u,w)| = (R-part) + (O-part)
    From G5: sum_{w in R-u} |D(u,w)|
      = sum_{z in N^-_R(u)} (d^+_R(z) - 1) + sum_{y in O, y -> u} (|M_y| - 1)

    d^+_R(z) = 6 - t_z, so first sum = sum_{z ->R u} (5 - t_z) = 5(5+t_u) - T_in
    where T_in = sum_{z in N^-_R(u)} t_z.
    #{y in O: y -> u} = 20 + e_u - t_u.
    |M_y| = 12 - q_y = 7 - (q_y - 5).
    sum_{y: y->u} (|M_y|-1) = sum (6 - e_y) = 6(20+e_u-t_u) - tau_u
    where tau_u = sum_{y: u in M_y} e_y.

    So sum_{w in R-u} |D| = 25 + 5 t_u - T_in + 120 + 6 e_u - 6 t_u - tau_u
      = 145 - t_u + 5 t_u wait: 25 + 5 t_u - T_in + 120 + 6 e_u - 6 t_u - tau
      = 145 - t_u - T_in + 6 e_u - tau_u.

    11 pairs, each |D| >= 12, so sum >= 132.
    145 - t_u - T_in + 6 e_u - tau_u >= 132
    13 + 6 e_u >= t_u + T_in + tau_u.

    T_in <= sum_{all r != u} t_r = 6 - t_u, so T_in + t_u <= 6.
    Thus the inequality is weak if tau is small.

    If e_u = 0: 13 >= t_u + T_in + tau_u, and all 11 |D|? No - only in-pairs
    of u in the WHOLE tournament have |D|=12. The pairs {u,w} for w in R
    with w -> u (i.e. w in N^-_R(u)) are in-pairs of u, hence |D|=12.
    Pairs with u -> w are in-pairs of w, so |D|=12 if e_w=0.

    Count of |D|=12 forced among the 11 R-pairs at u (e_u=0):
    the 5+t_u in-neighbours, plus the out-neighbours w with e_w=0.

    This filter just records the numerical bounds. Feasible as integers:
    t partition of 6, binary e, tau >= 0, T_in >= 0, T_in + t_u <= 6,
    13 + 6 e_u >= t_u + T_in + tau_u, and when e_u=0 the 5+t_u in-pairs
    have D=12 so their s-condition c+T_C+E_both <= 10 is open.
    """
    # Count integer (t-vector, e-vector) meeting Landau and the pair-sum inequality
    # with some nonnegative tau, T_in. This is a necessary-condition survival count,
    # not a tournament.
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    t = [m.NewIntVar(0, 6, f't{i}') for i in range(12)]
    e = [m.NewIntVar(0, 1, f'e{i}') for i in range(12)]
    ea = m.NewIntVar(0, 1, 'ea')
    m.Add(sum(t) == 6)
    m.Add(sum(e) + ea <= 13)
    # Landau: prefix of sorted scores. Encode weakly: for each k, there exist
    # k vertices whose (5+t) sum is >= C(k,2). Use the k smallest via a
    # sorted copy.
    rec = {'landau_api': False}
    for i in range(11):
        m.Add(t[i] >= t[i + 1])
    ts = list(reversed(t))
    for k in range(1, 13):
        m.Add(sum(5 + ts[i] for i in range(k)) >= k * (k - 1) // 2)
    # pair-sum inequality: exists T_in, tau >= 0
    for u in range(12):
        Tin = m.NewIntVar(0, 6, f'Tin{u}')
        tau = m.NewIntVar(0, 40, f'tau{u}')
        m.Add(Tin + t[u] <= 6)
        m.Add(t[u] + Tin + tau <= 13 + 6 * e[u])
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = 20
    s.parameters.num_workers = 2
    st = s.Solve(m)
    rec['status'] = s.StatusName(st)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        rec['t'] = [s.Value(x) for x in t]
        rec['e'] = [s.Value(x) for x in e]
        rec['ea'] = s.Value(ea)
    # Even the all-zero-t (impossible since sum t=6) analogue: the inequality
    # never forbids a partition of 6. Hand check: worst case t_u=6, T_in=0,
    # needs tau <= 7 + 6 e_u, true for tau=0.
    rec['hand_worst_case'] = {
        't_u_max': 6,
        'need': '13 + 6 e_u >= 6 + T_in + tau',
        'survives_at_tau_0_Tin_0': True,
        'closes_branch': False,
    }
    return rec


def main():
    rng = random.Random(902)
    ident = []
    for n in (20, 31, 52):
        for trial in range(2):
            ok, notes, g6 = check_identities(rand_tour(n, rng), rng)
            ident.append({'kind': 'generic', 'n': n, 'ok': ok, 'notes': notes[:5], 'g6': g6})
    for trial in range(3):
        A = tour_2526(rng)
        din = A.sum(axis=0)
        assert sorted(din.tolist()) == [25] * 26 + [26] * 26
        ok, notes, g6 = check_identities(A, rng, deg2526=True)
        ident.append({'kind': 'deg25/26', 'n': 52, 'ok': ok, 'notes': notes[:8], 'g6': g6})

    z5p = HERE / 'r8b_W25_cpsat_s3_z5.json'
    Wrec = {}
    if z5p.exists():
        A = np.array(json.loads(z5p.read_text())['A'], dtype=np.int64)
        Wrec = analyze_W(A)
        # predicted identities
        Wrec['predicted'] = {
            'sum_k': 25 * comb(12, 3),
            'sum_Ck2_from_c': 150 * comb(5, 3) + 150 * comb(6, 3),
            'transitive_from_scores': 25 * (6 * comb(5, 2) + 6 * comb(6, 2)),
        }

    margin = search_W_margin()
    filt = pairlevel_filter()

    out = {
        'identities': ident,
        'identities_all_ok': all(r['ok'] for r in ident),
        'z5_W': {k: v for k, v in Wrec.items()},
        'W_integer_margin': margin,
        'pairlevel_filter': filt,
    }
    dest = HERE / 'r8b_moments.json'
    dest.write_text(json.dumps(out, indent=1))
    print(json.dumps({
        'identities_all_ok': out['identities_all_ok'],
        'g6_counts': [r['g6'] for r in ident],
        'z5_S3': Wrec.get('S3'),
        'z5_cmin': Wrec.get('cmin'),
        'z5_sum_k': Wrec.get('sum_k'),
        'z5_sum_Ck2': Wrec.get('sum_C_k_2'),
        'z5_Ck3_eq': Wrec.get('sum_C_k_3') == Wrec.get('sum_C_nu_3'),
        'z5_min_k': Wrec.get('min_k'),
        'z5_k_hist': Wrec.get('k_hist'),
        'margin_status': margin.get('status'),
        'margin_min_k': margin.get('min_k'),
        'margin_tc_status': margin.get('with_trans_cyc', {}).get('status'),
        'margin_tc_min_k': margin.get('with_trans_cyc', {}).get('min_k'),
        'filter_status': filt.get('status'),
        'filter_closes': filt['hand_worst_case']['closes_branch'],
    }, indent=2))


if __name__ == '__main__':
    main()

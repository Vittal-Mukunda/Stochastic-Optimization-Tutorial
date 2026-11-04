"""R8-E driver: exact pair-level decision for tight pairs at N = 52 (see r8e_lib.py for the reduction).

  python r8e_pairlevel.py classfree CMIN JMIN JMAX
      every partition of J, every heavy pattern, c(u, v) free in [CMIN, 4] independently on each pair of V_+;
      writes research/CERTIFICATES/r8e_classfree_c{CMIN}_J{JMIN}-{JMAX}.json (P3 trees for every pattern passing P1).
  python r8e_pairlevel.py perclass CLASSFILE TAG JMIN JMAX WORKERS
      every class of CLASSFILE, every Aut-orbit of placements of every partition, Lemma A filter, exact decision with
      the class's own c; writes research/CERTIFICATES/r8e_perclass_{TAG}_J{JMIN}-{JMAX}.json.gz and a summary json.
"""
import gzip
import itertools
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

from r8e_lib import (NR, LAM, parse, cmatrix, automorphisms, partitions, placements, orbit_reps, positions,
                     heavy_patterns, pattern_data, d_bounds, solve_sets, cert_tree, tree_size)

ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / 'research' / 'CERTIFICATES'


def hkey(H):
    return ';'.join(f"{''.join(map(str, M)) or '-'}x{n}" for M, n in H)


# ---------------------------------------------------------------- direct check of a feasible point (no reduction)
def full_check(c, jv, H_vertices, Dplus):
    """Rebuild every variable of the brief's pair-level system from (c, j, heavy multiset on vertices, D on V_+ pairs)
    with D = 12 on pairs meeting V_0, and check every row literally.  Returns list of violated rows."""
    bad = []
    J = sum(jv)
    Vp = [r for r in range(NR) if jv[r] > 0]
    nheavy = sum(n for _, n in H_vertices)
    if sum(n * (6 - len(M)) for M, n in H_vertices) != 14 - J:
        bad.append('LI')
    if any(not set(M) <= set(Vp) or len(M) > 5 for M, _ in H_vertices):
        bad.append('A-support')
    nlight = 39 - nheavy
    if nlight < 0:
        bad.append('nlight')
    L, Ex = {}, {}
    for u in range(NR):
        L[u] = 20 + jv[u] - sum(n for M, n in H_vertices if u in M)
        Ex[u] = 5 + 10 * jv[u] - sum(n * LAM[11 - len(M)] for M, n in H_vertices if u in M)
        if L[u] < 0 or Ex[u] < 0:
            bad.append(f'L/Ex {u}')
    if sum(L.values()) != 6 * nlight:
        bad.append('sumL')
    D, k, s = {}, {}, {}
    for u, v in itertools.combinations(range(NR), 2):
        h = sum(n for M, n in H_vertices if u in M and v in M)
        E = sum(n * (6 - len(M)) for M, n in H_vertices if u in M and v in M)
        D[u, v] = Dplus[u, v] if (u in Vp and v in Vp) else 12
        k[u, v] = D[u, v] - c[u][v] - h
        s[u, v] = 4 * D[u, v] - c[u][v] - 45 - E
        if not (12 <= D[u, v] <= 43 and 0 <= k[u, v] <= 39 and 0 <= s[u, v] <= min(Ex[u], Ex[v])):
            bad.append(f'pair {u},{v}')
        if (jv[u] == 0 or jv[v] == 0) and (c[u][v] > 3 or D[u, v] != 12):
            bad.append(f'A {u},{v}')
        if c[u][v] < 0 or c[u][v] > 4:
            bad.append('c range')
        D[v, u], k[v, u], s[v, u] = D[u, v], k[u, v], s[u, v]
    for u in range(NR):
        o = [v for v in range(NR) if v != u]
        if sum(s[u, v] for v in o) != 2 * Ex[u]:
            bad.append(f'sum s {u}')
        if sum(k[u, v] for v in o) != 5 * L[u]:
            bad.append(f'sum k {u}')
        tau = sum(n * (6 - len(M)) for M, n in H_vertices if u in M)
        if sum(D[u, v] for v in o) != 120 + 5 * jv[u] - tau:
            bad.append(f'sum D {u}')
    return bad


# ---------------------------------------------------------------- class-free
def classfree(cmin, Jmin, Jmax):
    out = {'cmin': cmin, 'cmax': 4, 'Jmin': Jmin, 'Jmax': Jmax, 'partitions': []}
    for J in range(Jmin, Jmax + 1):
        for part in partitions(J):
            t0 = time.time()
            p = len(part)
            pairs = list(itertools.combinations(range(p), 2))
            Hs = heavy_patterns(list(part), 14 - J)
            recs = []
            nfeas = 0
            for H in Hs:
                pd = pattern_data(list(part), H)
                dom = {pr: set() for pr in pairs}
                for cc in range(cmin, 5):
                    bnd = d_bounds({pr: cc for pr in pairs}, pd, p)
                    for pr in pairs:
                        dom[pr] |= set(range(bnd[pr][0], bnd[pr][1] + 1))
                dom = {pr: sorted(v) for pr, v in dom.items()}
                tree = cert_tree(dom, pd['rho'], p)
                rec = {'H': hkey(H)}
                if tree is None:
                    sol = solve_sets(dom, pd['rho'], p)
                    rec['feasible'] = {f'{a},{b}': d for (a, b), d in sol.items()}
                    nfeas += 1
                else:
                    rec['tree'] = tree
                recs.append(rec)
            out['partitions'].append({'J': J, 'part': list(part), 'n_patterns_P1': len(Hs), 'n_feasible': nfeas,
                                      'secs': round(time.time() - t0, 3), 'patterns': recs})
            print(J, part, len(Hs), 'P1-patterns;', nfeas, 'class-free feasible', flush=True)
    CERT.mkdir(exist_ok=True)
    fn = CERT / f'r8e_classfree_c{cmin}_J{Jmin}-{Jmax}.json'
    fn.write_text(json.dumps(out))
    return out


# ---------------------------------------------------------------- per class
_G = {}


def _init(lines, Jmin, Jmax):
    _G['lines'] = lines
    pats = {}
    for J in range(Jmin, Jmax + 1):
        for part in partitions(J):
            Hs = heavy_patterns(list(part), 14 - J)
            pats[part] = [(H, pattern_data(list(part), H)) for H in Hs]
    _G['pats'] = pats
    _G['memo'] = {}


def decide_class(ci):
    t0 = time.time()
    adj = parse(_G['lines'][ci])
    c = cmatrix(adj)
    auts = automorphisms(adj)
    c4 = [(u, v) for u, v in itertools.combinations(range(NR), 2) if c[u][v] == 4]
    c4v = set(x for pr in c4 for x in pr)
    res = {'class': ci, 'aut': len(auts), 'n_c4_pairs': len(c4), 'parts': {}}
    if len(auts) > 1:
        res['aut_list'] = [list(f) for f in auts]
    p3used = {}
    witnesses = []
    for part, plist in _G['pats'].items():
        p = len(part)
        pairs = list(itertools.combinations(range(p), 2))
        allp = list(placements(part))
        reps = orbit_reps(allp, auts)
        nA = nfeas = ninf = 0
        for jv in reps:
            Vp = positions(jv)
            if not c4v <= set(Vp):
                nA += 1
                continue
            V0 = [r for r in range(NR) if jv[r] == 0]
            minc = [min(c[u][Vp[b]] for u in V0) if V0 else 99 for b in range(p)]
            cpp = {(a, b): c[Vp[a]][Vp[b]] for a, b in pairs}
            ctup = tuple(cpp[pr] for pr in pairs)
            feas = None
            for hi, (H, pd) in enumerate(plist):
                if any(pd['Ex'][b] + minc[b] < 3 for b in range(p)):
                    continue  # (P2)
                key = (part, hi, ctup)
                if key not in _G['memo']:
                    bnd = d_bounds(cpp, pd, p)
                    dom = {pr: list(range(bnd[pr][0], bnd[pr][1] + 1)) for pr in pairs}
                    tree = cert_tree(dom, pd['rho'], p)
                    sol = solve_sets(dom, pd['rho'], p) if tree is None else None
                    _G['memo'][key] = (tree, sol)
                tree, sol = _G['memo'][key]
                p3used[key] = tree
                if tree is None:
                    feas = (hi, H, sol)
                    break
            if feas is None:
                ninf += 1
            else:
                nfeas += 1
                if len(witnesses) < 3:
                    hi, H, sol = feas
                    Hv = [(tuple(Vp[x] for x in M), n) for M, n in H]
                    Dplus = {}
                    for (a, b), d in sol.items():
                        Dplus[Vp[a], Vp[b]] = Dplus[Vp[b], Vp[a]] = d
                    bad = full_check(c, jv, Hv, {(min(u, v), max(u, v)): d for (u, v), d in Dplus.items()})
                    witnesses.append({'class': ci, 'part': list(part), 'j': list(jv), 'heavy': [[list(M), n] for M, n in Hv],
                                      'D_plus': {f'{u},{v}': d for (u, v), d in Dplus.items() if u < v},
                                      'full_check_violations': bad})
        res['parts'][','.join(map(str, part))] = {'placements': len(allp), 'orbits': len(reps), 'lemmaA_excluded': nA,
                                                 'infeasible': ninf, 'feasible': nfeas}
    res['witnesses'] = witnesses
    res['p3'] = [[list(k[0]), k[1], list(k[2]), t] for k, t in p3used.items()]
    res['secs'] = round(time.time() - t0, 2)
    return res


def perclass(classfile, tag, Jmin, Jmax, workers):
    lines = [l.strip() for l in Path(classfile).read_text().splitlines() if l.strip()]
    t0 = time.time()
    with Pool(workers, initializer=_init, initargs=(lines, Jmin, Jmax)) as pool:
        results = []
        for i, r in enumerate(pool.imap(decide_class, range(len(lines)), chunksize=4)):
            results.append(r)
            if i % 50 == 0:
                print(f'class {i} done, {time.time() - t0:.0f}s', flush=True)
    # merge
    summary = {}
    p3 = {}
    witnesses = []
    for r in results:
        for part, d in r['parts'].items():
            s = summary.setdefault(part, {k: 0 for k in d} | {'classes_with_feasible': 0})
            for k, v in d.items():
                s[k] += v
            s['classes_with_feasible'] += d['feasible'] > 0
        for part, hi, ct, t in r['p3']:
            p3[(tuple(part), hi, tuple(ct))] = t
        witnesses += r['witnesses']
    secs = round(time.time() - t0, 1)
    meta = {'classfile': str(classfile), 'tag': tag, 'Jmin': Jmin, 'Jmax': Jmax, 'n_classes': len(lines),
            'workers': workers, 'secs': secs, 'summary': summary,
            'total_orbits': sum(s['orbits'] for s in summary.values()),
            'total_feasible': sum(s['feasible'] for s in summary.values()),
            'n_p3_entries': len(p3), 'n_p3_feasible_entries': sum(1 for t in p3.values() if t is None),
            'max_tree_size': max((tree_size(t) for t in p3.values() if t), default=0),
            'witnesses': witnesses[:40], 'n_witnesses_recorded': len(witnesses),
            'witness_full_check_all_clean': all(not w['full_check_violations'] for w in witnesses)}
    CERT.mkdir(exist_ok=True)
    cert = {'meta': {k: meta[k] for k in ('classfile', 'tag', 'Jmin', 'Jmax', 'n_classes')},
            'patterns': {','.join(map(str, part)): [hkey(H) for H, _ in pl] for part, pl in _pat_lists(Jmin, Jmax).items()},
            'auts': {str(r['class']): r['aut_list'] for r in results if 'aut_list' in r},
            'p3': [[list(k[0]), k[1], list(k[2]), t] for k, t in p3.items()]}
    with gzip.open(CERT / f'r8e_perclass_{tag}_J{Jmin}-{Jmax}.json.gz', 'wt') as f:
        json.dump(cert, f)
    (CERT / f'r8e_perclass_{tag}_J{Jmin}-{Jmax}_summary.json').write_text(json.dumps(meta, indent=1))
    print(json.dumps({k: meta[k] for k in ('secs', 'total_orbits', 'total_feasible', 'n_p3_entries', 'max_tree_size',
                                           'witness_full_check_all_clean')}))
    for part, s in summary.items():
        print(part, s)
    return meta


def _pat_lists(Jmin, Jmax):
    out = {}
    for J in range(Jmin, Jmax + 1):
        for part in partitions(J):
            out[part] = [(H, None) for H in heavy_patterns(list(part), 14 - J)]
    return out


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'classfree':
        classfree(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    elif mode == 'perclass':
        perclass(ROOT / sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))

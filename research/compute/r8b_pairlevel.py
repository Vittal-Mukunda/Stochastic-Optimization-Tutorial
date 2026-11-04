"""R8-B: pair-level model at a 12-dominator pair {a, v}, v of in-degree 25, in the no-tight branch at order 52.

Setting (all proved in the R8-B report): T has S_4 on 52 vertices, every pair has >= 12 dominators.  v has
d^-(v) = 25, so W = N^-(v) is 12-regular.  a in W, R = D({a,v}) = N^-_W(a) (12 vertices).
O = Y1 u B with Y1 = N^+_W(a) (12 vertices: a -> y -> v) and B = N^+(v) (26 vertices).
Bm = {y in B : y -> a} has 13 + e_a vertices.  e_x = d^-(x) - 25 >= 0.

Variables: T[R] (66 arcs), x[y][r] = [y -> r] for the 38 outside vertices, m_y = [y -> a] for y in B, e_r, e_a.

Rows (each a consequence of S_4 + no-tight; numbering as in the report):
 R1  d^-_R(r) = 5 + t_r >= 5                                   (F2 at P = {a,v})
 R2  c(u,w) >= 1                                              (4-set {a,v,u,w}: dominator beats a, v so lies in R)
 R3  q_y = |R n N^-(y)| >= 5                                   (F2)
 R4  Q_y n Q_y' != {}                                          (4-set {a,v,y,y'})
 R5  N^-_R(r) n Q_y != {}                                      (4-set {a,v,r,y})
 R6  #{y in Y1 : y -> r} = 7 - t_r ; #{y in B : y -> r} = 13 + e_r   (W 12-regular; d^-(r) = 25 + e_r)
 R7  e_a + sum_R e_r <= 13                                     (sum_{W} e <= 13: arc count at v)
 R8  |D(U)| >= 5 for every triple U of R                        (F1; D(U) = R-dominators u O-dominators)
 R9  |D(u,w)| = c(u,w) + #{y : y -> u, w} >= 12 ; = 12 if u -> w and e_w = 0 ;
     sum_{u in R, u -> w} (|D(u,w)| - 12) <= (25 + e_w) e_w / 2  (T[N^-(w)] has in-degrees 12 + eps, sum eps = that)
 R10 D(U) != {} for every 4-set U of R                          (S_4)
 R11 {v,r,r'}: c + #{y in Y1 : y -> r, r'} >= 5 ; {v,r,r',r''}: nonempty   (F1, S_4; D lies in W)
 R12 |Bm| = 13 + e_a ; {a,r}: d^-_R(r) + #{y in Bm : y -> r} >= 12, = 12 if e_a = 0 ;
     {a,r,r'}: c + #{y in Bm : y -> r,r'} >= 5 ; {a,r,r',r''}: nonempty      (D lies in N^-(a) = R u Bm)
 R13 y in Y1: q_y <= 11                                         (y has in-degree 12 in W and a -> y)
Variants: --binary (e in {0,1}: in-degrees 25/26 assumed), --ea0 (choose a with e_a = 0; always possible because
at most 13 vertices of W have e >= 1).

Usage: python r8b_pairlevel.py [--binary] [--ea0] [--time T] [--workers K] [--nosym]
"""
import argparse
import itertools
import json
import time
from pathlib import Path

from ortools.sat.python import cp_model

NR = 12
R = list(range(NR))
NY1, NB = 12, 26


def build(binary, ea0, sym=True, fixW=None, avert=0):
    m = cp_model.CpModel()
    arc = {}
    for u, w in itertools.combinations(R, 2):
        arc[u, w] = m.NewBoolVar(f'a{u}_{w}')
        arc[w, u] = arc[u, w].Not()
    indeg = {r: sum(arc[w, r] for w in R if w != r) for r in R}
    t = {r: m.NewIntVar(0, 6, f't{r}') for r in R}
    for r in R:
        m.Add(indeg[r] == 5 + t[r])                                    # R1
    emax = 1 if binary else 13
    e = {r: m.NewIntVar(0, emax, f'e{r}') for r in R}
    ea = m.NewIntVar(0, 0 if ea0 else emax, 'ea')
    m.Add(sum(e.values()) + ea <= 13)                                 # R7
    ezero = {}
    for r in R:
        ezero[r] = m.NewBoolVar(f'ez{r}')
        m.Add(e[r] == 0).OnlyEnforceIf(ezero[r])
        m.Add(e[r] >= 1).OnlyEnforceIf(ezero[r].Not())
    eazero = m.NewBoolVar('eaz')
    m.Add(ea == 0).OnlyEnforceIf(eazero)
    m.Add(ea >= 1).OnlyEnforceIf(eazero.Not())

    Y1 = [f'y{i}' for i in range(NY1)]
    Bv = [f'b{i}' for i in range(NB)]
    O = Y1 + Bv
    x = {(y, r): m.NewBoolVar(f'x{y}_{r}') for y in O for r in R}
    mm = {y: m.NewBoolVar(f'm{y}') for y in Bv}
    m.Add(sum(mm.values()) == 13 + ea)                                # R12 |Bm|
    for y in O:
        m.Add(sum(x[y, r] for r in R) <= 7)                            # R3
    for y in Y1:
        m.Add(sum(x[y, r] for r in R) >= 1)                            # R13
    for r in R:
        m.Add(sum(x[y, r] for y in Y1) == 7 - t[r])                    # R6
        m.Add(sum(x[y, r] for y in Bv) == 13 + e[r])
    if fixW is not None:
        # W = N^-(v) given; a = avert; R = N^-_W(a) relabelled 0..11, Y1 = N^+_W(a) relabelled y0..y11
        Rl = [z for z in range(25) if fixW[z][avert]]
        Yl = [z for z in range(25) if z != avert and fixW[avert][z]]
        for i, j in itertools.combinations(range(NR), 2):
            m.Add(arc[i, j] == int(fixW[Rl[i]][Rl[j]]))
        for k, y in enumerate(Y1):
            for i in range(NR):
                m.Add(x[y, i] == int(fixW[Yl[k]][Rl[i]]))
        sym = False

    def AND(lits, name=''):
        b = m.NewBoolVar(name)
        m.AddBoolAnd(lits).OnlyEnforceIf(b)
        m.AddBoolOr([l.Not() for l in lits]).OnlyEnforceIf(b.Not())
        return b

    # R4
    for y, z in itertools.combinations(O, 2):
        m.AddBoolOr([AND([x[y, r].Not(), x[z, r].Not()]) for r in R])
    # R5
    for r in R:
        for y in O:
            m.AddBoolOr([AND([arc[w, r], x[y, w].Not()]) for w in R if w != r])

    # dominator indicators
    domR = {}   # (w, U) -> w beats all of U
    domO = {}   # (y, U)
    for k in (2, 3, 4):
        for U in itertools.combinations(R, k):
            for w in R:
                if w not in U:
                    domR[w, U] = AND([arc[w, u] for u in U])
            for y in O:
                domO[y, U] = AND([x[y, u] for u in U])
    bm = {}
    for U in itertools.combinations(R, 1):
        for y in Bv:
            bm[y, U] = AND([mm[y], x[y, U[0]]])
    for k in (2, 3):
        for U in itertools.combinations(R, k):
            for y in Bv:
                bm[y, U] = AND([mm[y], domO[y, U]])

    c = {}
    Dp = {}
    for U in itertools.combinations(R, 2):
        u, w = U
        c[U] = sum(domR[z, U] for z in R if z not in U)
        m.Add(c[U] >= 1)                                               # R2
        Dp[U] = m.NewIntVar(12, 50, f'D{u}_{w}')
        m.Add(Dp[U] == c[U] + sum(domO[y, U] for y in O))              # R9
        m.Add(Dp[U] == 12).OnlyEnforceIf([arc[u, w], ezero[w]])
        m.Add(Dp[U] == 12).OnlyEnforceIf([arc[w, u], ezero[u]])
        m.Add(c[U] + sum(domO[y, U] for y in Y1) >= 5)                 # R11
        m.Add(c[U] + sum(bm[y, U] for y in Bv) >= 5)                   # R12
    # R9 in-excess budget
    for w in R:
        exc = []
        for u in R:
            if u == w:
                continue
            U = tuple(sorted((u, w)))
            z = m.NewIntVar(0, 38, '')
            m.Add(z == Dp[U] - 12).OnlyEnforceIf(arc[u, w])
            m.Add(z == 0).OnlyEnforceIf(arc[w, u])
            exc.append(z)
        cap2 = m.NewIntVar(0, 38 * 13, '')
        m.AddMultiplicationEquality(cap2, [e[w] + 25, e[w]])
        m.Add(2 * sum(exc) <= cap2)
    # R12 pair {a, r}
    for r in R:
        Dar = indeg[r] + sum(bm[y, (r,)] for y in Bv)
        m.Add(Dar >= 12)
        m.Add(Dar == 12).OnlyEnforceIf(eazero)
    for U in itertools.combinations(R, 3):
        m.Add(sum(domR[w, U] for w in R if w not in U) + sum(domO[y, U] for y in O) >= 5)   # R8
        m.AddBoolOr([domR[w, U] for w in R if w not in U] + [domO[y, U] for y in Y1])     # R11
        m.AddBoolOr([domR[w, U] for w in R if w not in U] + [bm[y, U] for y in Bv])       # R12
    for U in itertools.combinations(R, 4):
        m.AddBoolOr([domR[w, U] for w in R if w not in U] + [domO[y, U] for y in O])      # R10

    if not sym and fixW is not None:
        code = {y: sum((1 << r) * x[y, r] for r in R) for y in Bv}
        for i in range(NB - 1):
            m.AddImplication(mm[Bv[i + 1]], mm[Bv[i]])
            m.Add(code[Bv[i]] >= code[Bv[i + 1]]).OnlyEnforceIf([mm[Bv[i]], mm[Bv[i + 1]]])
            m.Add(code[Bv[i]] >= code[Bv[i + 1]]).OnlyEnforceIf([mm[Bv[i]].Not(), mm[Bv[i + 1]].Not()])
    if sym:
        for i in range(NR - 1):
            m.Add(t[i] >= t[i + 1])
        code = {y: sum((1 << r) * x[y, r] for r in R) for y in O}
        for i in range(NY1 - 1):
            m.Add(code[Y1[i]] >= code[Y1[i + 1]])
        for i in range(NB - 1):
            m.AddImplication(mm[Bv[i + 1]], mm[Bv[i]])
            m.Add(code[Bv[i]] >= code[Bv[i + 1]]).OnlyEnforceIf([mm[Bv[i]], mm[Bv[i + 1]]])
            m.Add(code[Bv[i]] >= code[Bv[i + 1]]).OnlyEnforceIf([mm[Bv[i]].Not(), mm[Bv[i + 1]].Not()])
    return m, dict(arc=arc, t=t, e=e, ea=ea, x=x, mm=mm, Dp=Dp, Y1=Y1, Bv=Bv)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--binary', action='store_true')
    ap.add_argument('--ea0', action='store_true')
    ap.add_argument('--time', type=float, default=600)
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--nosym', action='store_true')
    ap.add_argument('--fixW', default='', help='JSON file with W adjacency "A"; fixes T[R] and Y1 arcs')
    ap.add_argument('--avert', type=int, default=0)
    a = ap.parse_args()
    t0 = time.time()
    fixW = json.loads(Path(a.fixW).read_text())['A'] if a.fixW else None
    m, V = build(a.binary, a.ea0, not a.nosym, fixW, a.avert)
    tb = time.time() - t0
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = a.time
    s.parameters.num_workers = a.workers
    st = s.Solve(m)
    rec = {'binary': a.binary, 'ea0': a.ea0, 'sym': not a.nosym, 'status': s.StatusName(st),
           'build_s': round(tb, 1), 'solve_s': round(s.WallTime(), 1)}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        arc = V['arc']
        rec['out_R'] = [[w for w in R if w != u and s.BooleanValue(arc[u, w])] for u in R]
        rec['t'] = [s.Value(V['t'][r]) for r in R]
        rec['e'] = [s.Value(V['e'][r]) for r in R]
        rec['e_a'] = s.Value(V['ea'])
        rec['Y1_miss'] = [[r for r in R if s.BooleanValue(V['x'][y, r])] for y in V['Y1']]
        rec['B_miss'] = [[r for r in R if s.BooleanValue(V['x'][y, r])] for y in V['Bv']]
        rec['B_to_a'] = [int(s.BooleanValue(V['mm'][y])) for y in V['Bv']]
        rec['D_pairs'] = {f'{u},{w}': s.Value(V['Dp'][u, w]) for u, w in itertools.combinations(R, 2)}
    print(json.dumps({k: rec[k] for k in ('binary', 'ea0', 'status', 'build_s', 'solve_s')}))
    tag = ('bin' if a.binary else 'gen') + ('_ea0' if a.ea0 else '') + (f'_fixW_a{a.avert}' if a.fixW else '')
    rec['fixW'] = a.fixW
    rec['avert'] = a.avert
    (Path(__file__).parent / f'r8b_pairlevel_{tag}.json').write_text(json.dumps(rec, indent=1))


if __name__ == '__main__':
    main()

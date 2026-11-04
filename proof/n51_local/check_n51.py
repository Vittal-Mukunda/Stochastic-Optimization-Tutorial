"""Independent checker for the N = 51 'J >= 3' certificates.

It does NOT import the producer (lmodel / bnb / lpcert).  From the class string alone it rebuilds
  * the variable universe: x[S,t] for every admissible S (|S| in {5,6,9,10,11}, S meets the in-neighbourhood of every
    vertex of R) and type t (types 0,1,2 in modes 'in'/'out'; one generic type in mode 'free'), and j[r], r in R;
  * every constraint row from its label, with its own set arithmetic (frozensets);
  * every node box from the root box, the branching bounds and the intersecting rule
    (lb x[S,t] >= 1  =>  ub x[S',t'] = 0 for all S' disjoint from S);
and checks every leaf: either an exact integer Farkas certificate, or ('X') two disjoint sets both forced >= 1.
Usage: python check_n51.py reg11_S2.txt tree1.json.gz [tree2 ...]
"""
import sys, gzip, json, itertools

R = tuple(range(11))


def parse(line):
    line = line.strip()
    assert len(line) == 55 and set(line) <= {'0', '1'}
    beats = {(i, j): False for i in R for j in R}
    pos = 0
    for i in R:
        for j in R:
            if j > i:
                if line[pos] == '1':
                    beats[(i, j)] = True
                else:
                    beats[(j, i)] = True
                pos += 1
    return beats


def class_ok(beats):
    for i in R:
        if sum(beats[(i, j)] for j in R) != 5 or sum(beats[(j, i)] for j in R) != 5:
            return False
    for u in R:
        for v in R:
            if u < v and not any(beats[(w, u)] and beats[(w, v)] for w in R):
                return False
    return True


def bits_to_set(m):
    return frozenset(i for i in R if (m >> i) & 1)


class System:
    def __init__(self, beats, mode, aux=False):
        self.beats = beats
        self.mode = mode
        self.aux = aux
        innb = {z: frozenset(w for w in R if beats[(w, z)]) for z in R}
        self.adm = []
        for k in (5, 6, 9, 10, 11):
            for S in itertools.combinations(R, k):
                S = frozenset(S)
                if all(S & innb[z] for z in R):
                    self.adm.append(S)
        self.types = (0, 1, 2) if mode in ('in', 'out', 'reg') else ('g',)
        self.xvars = [(S, t) for S in self.adm for t in self.types]
        self.key = {}
        for (S, t) in self.xvars:
            self.key[('x', S, t)] = len(self.key)
        for r in R:
            self.key[('j', r)] = len(self.key)
        if aux:
            # auxiliary integer variables, each tied to the x variables by an equality row (labels Z, N, Cc)
            for S in self.adm:
                if len(S) in (5, 6):
                    self.key[('z', S)] = len(self.key)
            for t in self.types:
                self.key[('n', t)] = len(self.key)
            for r in R:
                self.key[('c', r)] = len(self.key)
        self.n = len(self.key)
        self.xvars_by_key = {self.key[('x', S, t)]: (S, t) for (S, t) in self.xvars}

    def cR(self, U):
        return sum(1 for w in R if w not in U and all(self.beats[(w, u)] for u in U))

    def row(self, lab):
        """returns (coef dict over variable keys, sense, rhs) for a label, or raises."""
        x = lambda pred: {self.key[('x', S, t)]: 1 for (S, t) in self.xvars if pred(S, t)}
        nu = {1: 23, 2: 11, 3: 5, 4: 1}
        kind = lab[0]
        if kind == 'C1':
            return x(lambda S, t: True), '==', 38
        if kind == 'C3':
            U = bits_to_set(lab[1])
            assert 2 <= len(U) <= 4
            return x(lambda S, t: not (S & U)), '>=', nu[len(U)] - self.cR(U)
        if kind == 'C4':
            assert self.mode in ('in', 'out', 'reg')
            p, U = lab[1], bits_to_set(lab[2])
            assert 1 <= len(U) <= 3
            tp = {'a': 0, 'b': 1}[p]                 # type 0 = beats a (not b); type 1 = beats b (not a)
            return x(lambda S, t: t == tp and not (S & U)), '>=', nu[len(U) + 1] - self.cR(U)
        if kind == 'C5':
            r = lab[1]
            co = x(lambda S, t: r in S)
            co[self.key[('j', r)]] = 1
            return co, '==', 18
        if kind == 'C6':
            return {self.key[('j', r)]: 1 for r in R}, '<=', (0 if self.mode == 'reg' else 2)
        if kind == 'M':
            what = lab[1]
            n0 = lambda: x(lambda S, t: t == 0)
            n1 = lambda: x(lambda S, t: t == 1)
            Jc = {self.key[('j', r)]: 1 for r in R}
            if self.mode == 'in':
                if what == 'n1=12':
                    return n1(), '==', 12
                if what == 'n0>=13':
                    return n0(), '>=', 13
                if what == 'n0+J<=19':
                    co = n0(); co.update(Jc); return co, '<=', 19
            if self.mode == 'reg':
                if what == 'n0=14':
                    return n0(), '==', 14
                if what == 'n1=13':
                    return n1(), '==', 13
            if self.mode == 'out':
                if what == 'n0=13':
                    return n0(), '==', 13
                if what == 'n1>=12':
                    return n1(), '>=', 12
                if what == 'n1+J<=18':
                    co = n1(); co.update(Jc); return co, '<=', 18
            raise ValueError(lab)
        if kind == 'P2':
            return x(lambda S, t: len(S) >= 9), '==', 1
        if kind == 'P5':
            return x(lambda S, t: len(S) == 6), '<=', 2
        if kind == 'P3':
            r = lab[1]
            co = x(lambda S, t: len(S) in (9, 10) and r not in S)
            co[self.key[('j', r)]] = -1
            return co, '<=', 0
        if kind == 'P4':
            r = lab[1]
            co = x(lambda S, t: len(S) in (6, 9, 10) and r not in S)
            co[self.key[('j', r)]] = -1
            return co, '<=', 1
        if kind == 'Z':
            assert self.aux
            S = bits_to_set(lab[1]); assert len(S) in (5, 6)
            co = x(lambda S2, t: S2 == S); co[self.key[('z', S)]] = -1
            return co, '==', 0
        if kind == 'N':
            assert self.aux
            tp = lab[1]
            co = x(lambda S, t: t == tp); co[self.key[('n', tp)]] = -1
            return co, '==', 0
        if kind == 'Cc':
            assert self.aux
            r = lab[1]
            co = x(lambda S, t: len(S) == 6 and r not in S); co[self.key[('c', r)]] = -1
            return co, '==', 0
        raise ValueError(lab)


def check_file(path, lines):
    with gzip.open(path, 'rt') as f:
        D = json.load(f)
    cl, mode = D['cl'], D['mode']
    beats = parse(lines[cl])
    assert class_ok(beats), 'class is not 5-regular S_2'
    aux = any(v[0] in ('z', 'n', 'c') for v in D['vars'])
    Sy = System(beats, mode, aux)
    # map the producer's variable labels to our keys
    vmap = []
    for v in D['vars']:
        if v[0] == 'x':
            S = bits_to_set(v[1])
            t = v[2] if mode in ('in', 'out', 'reg') else 'g'
            vmap.append(Sy.key[('x', S, t)])        # KeyError = producer variable not in our universe
        elif v[0] == 'z':
            vmap.append(Sy.key[('z', bits_to_set(v[1]))])
        elif v[0] == 'n':
            vmap.append(Sy.key[('n', v[1])])
        elif v[0] == 'c':
            vmap.append(Sy.key[('c', v[1])])
        else:
            assert v[0] == 'j'
            vmap.append(Sy.key[('j', v[1])])
    labels = [tuple(l) for l in D['rows']]
    rowcache = {}

    def getrow(i):
        if i not in rowcache:
            rowcache[i] = Sy.row(labels[i])
        return rowcache[i]

    lb = [0] * Sy.n
    ub = [0] * Sy.n
    for k in Sy.key.values():
        ub[k] = 38
    for r in R:
        ub[Sy.key[('j', r)]] = 0 if mode == 'reg' else 2
    # variables that count outside vertices with a given Q_y = S: x[S,t] and (aux) z[S]
    xsets = {Sy.key[('x', S, t)]: S for (S, t) in Sy.xvars}
    xsets.update({k: key[1] for key, k in Sy.key.items() if key[0] == 'z'})
    stats = {'leaves': 0, 'X': 0, 'branch': 0}

    def node_box(lb, ub):
        """apply the intersecting rule; return (lb, ub, conflict)."""
        lb2, ub2 = list(lb), list(ub)
        forced = [S for k, S in xsets.items() if lb[k] >= 1]
        conflict = any(not (A & B) for A in forced for B in forced)
        if forced:
            for k, S in xsets.items():
                if any(not (S & F) for F in forced):
                    ub2[k] = 0
        return lb2, ub2, conflict

    def walk(t, lb, ub):
        if t[0] == 'K':
            # skeleton split (Lemma P): the unique y* with q >= 9 (set S*, type t*) and the vector j, modulo
            # automorphisms of T[R] (relabelling R by an automorphism maps configurations to configurations)
            perms = [tuple(p) for p in t[1]] or [tuple(R)]
            for p in perms:
                assert sorted(p) == list(R)
                assert all(beats[(i, k)] == beats[(p[i], p[k])] for i in R for k in R if i != k), 'not an automorphism'
            reps = {}
            for item in t[2]:
                (S, tt) = Sy.xvars_by_key[vmap[item[0]]]
                reps[(S, tt, tuple(item[1]))] = item
            jkeys = [Sy.key[('j', r)] for r in R]
            jvecs = [jv for jv in itertools.product((0, 1, 2), repeat=11) if sum(jv) <= 2
                     and all(lb[jkeys[r]] <= jv[r] <= ub[jkeys[r]] for r in R)]
            covered = 0
            for (S, tt) in Sy.xvars:
                if len(S) < 9:
                    continue
                for jv in jvecs:
                    if any(jv[r] == 0 for r in R if r not in S):
                        continue                      # excluded by row P3 together with x[S*,t*] = 1
                    ok = False
                    for p in perms:
                        S2 = frozenset(p[r] for r in S)
                        j2 = [0] * 11
                        for r in R:
                            j2[p[r]] = jv[r]
                        if (S2, tt, tuple(j2)) in reps:
                            ok = True; break
                    assert ok, ('skeleton not covered', sorted(S), tt, jv)
                    covered += 1
            stats['skeletons'] = stats.get('skeletons', 0) + covered
            for item in t[2]:
                k = vmap[item[0]]
                assert len(Sy.xvars_by_key[k][0]) >= 9
                lb2, ub2 = list(lb), list(ub)
                lb2[k] = max(lb2[k], 1)
                assert lb2[k] <= ub2[k]
                for r in R:
                    assert lb[jkeys[r]] <= item[1][r] <= ub[jkeys[r]]
                    lb2[jkeys[r]] = ub2[jkeys[r]] = item[1][r]
                lb3, ub3, conflict = node_box(lb2, ub2)
                if item[2][0] == 'X':
                    assert conflict
                    stats['X'] += 1
                    continue
                walk(item[2], lb3, ub3)
            return
        if t[0] == 'B':
            stats['branch'] += 1
            v, kk = vmap[t[1]], t[2]
            assert lb[v] <= kk < ub[v], 'branch value outside the box'
            for child, (lo, hi) in ((t[3], (lb[v], kk)), (t[4], (kk + 1, ub[v]))):
                lb2, ub2 = list(lb), list(ub)
                lb2[v], ub2[v] = lo, hi
                lb3, ub3, conflict = node_box(lb2, ub2)
                if child[0] == 'X':
                    assert conflict, 'X-leaf without a disjoint forced pair'
                    stats['X'] += 1
                    continue
                walk(child, lb3, ub3)
            return
        assert t[0] == 'L'
        stats['leaves'] += 1
        if isinstance(t[1], list):
            assert len(t) == 3 and len(t[1]) == len(t[2]) == len(set(t[1]))
            y = {int(i): int(v) for i, v in zip(t[1], t[2])}
        else:
            y = {int(i): int(v) for i, v in t[1].items()}
        c = {}
        yb = 0
        for i, yi in y.items():
            co, sense, rhs = getrow(i)
            if sense == '>=':
                assert yi >= 0
            elif sense == '<=':
                assert yi <= 0
            yb += yi * rhs
            for k, a in co.items():
                c[k] = c.get(k, 0) + yi * a
        mx = sum(ck * (ub[k] if ck > 0 else lb[k]) for k, ck in c.items())
        assert yb > mx, 'certificate margin not positive'

    lb0, ub0, conflict = node_box(lb, ub)
    assert not conflict
    walk(D['tree'], lb0, ub0)
    return cl, mode, stats


if __name__ == '__main__':
    lines = open(sys.argv[1]).read().split()
    assert len(lines) == 551
    for p in sys.argv[2:]:
        try:
            cl, mode, st = check_file(p, lines)
            print('OK', cl, mode, st, flush=True)
        except Exception as e:
            print('FAIL', p, repr(e), flush=True)

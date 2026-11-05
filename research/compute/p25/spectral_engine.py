#!/usr/bin/env python3
"""Exact spectral / arithmetic tests for a hypothesised codegree pattern Y of a (P25)/(R25) tournament.

Setting (proof/N52_SESSION_2026-11-04.md, Lemma 7.1): T is a 12-regular tournament on 25 vertices, M = T - T^t its
skew +-1 matrix, codeg(a, b) = |N-(a) ∩ N-(b)| = 5 + Y_ab (a != b), Y_aa = 0.  Then

    M M^t = 27 I + 4 Y - 3 J,   Y 1 = 12 * 1,   M Y = Y M.

Necessary conditions on Y tested here (all exact, integer/rational arithmetic via python-flint):
  (V)   Y symmetric, zero diagonal, entries 0..6, row sums 12.
  (P)   pairing: charpoly(Y) = (x - 12) g(x)^2 with g in Z[x].
  (D)   positivity: every root theta of g has 27 + 4 theta > 0.
  (Pf)  Pfaffian: prod over roots of g of (27 + 4 theta) = 25 pi^2 with pi an odd integer.
  (EDC) eigenspace discriminants: for each Q-irreducible factor f of g with g = prod f^k, let E_f = ker f(Y) ∩ 1^⊥
        (rational, dim 2k deg f).  M preserves E_f, b(x, y) = x^t M y is a nondegenerate skew form on it, and
        Gram(b) = Gram(q) * [M|E_f], so  det q(E_f) * N_f^k  is a rational square, N_f = prod_{f(theta)=0} (27 + 4 theta).
  (HM)  for a rational theta with k >= 2: q(E_theta) = <1, D> (x) q' with D = 27 + 4 theta, i.e. q(E_theta) becomes
        hyperbolic over Q(sqrt(-D)); checked through Hasse invariants at the primes that split there.
  (GHC) the 24-dim form 27 I + 4 Y - 3 J on Q^25 / <1> is the Gram form of the rows of M, which span 1^⊥ ≅ I_24:
        all its Hasse invariants are trivial.
If every eigenvalue of Y on 1^⊥ has multiplicity exactly 2 ("nondegenerate"), M = sum_j sigma_j s_j (v_j u_j^t - u_j v_j^t)
over orthonormal bases (u_j, v_j) of the 12 eigenplanes, s_j = sqrt(27 + 4 theta_j), sigma in {+-1}^12: `reconstruct`
lists every tournament with codegree pattern exactly Y (up to reversal) by checking the 2^11 sign vectors.
"""
import itertools
import sys
from fractions import Fraction

import flint
import numpy as np

N = 25


# ---------------------------------------------------------------- basic objects
def load_tournament(path):
    T = np.zeros((N, N), dtype=np.int64)
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            a, rest = line.split(':')
            for b in rest.split():
                T[int(a), int(b)] = 1
    assert (T + T.T + np.eye(N, dtype=np.int64) == 1).all(), 'not a tournament'
    return T


def pattern_of(T):
    C = T.T @ T                      # common in-neighbours
    Y = C - 5
    np.fill_diagonal(Y, 0)
    return Y


def valid_pattern(Y, strict=True):
    """strict: a (R25)/(P25) pattern (entries 0..6); non-strict: any regular tournament (codegrees may be < 5)."""
    Y = np.asarray(Y)
    ok = Y.shape == (N, N) and (Y == Y.T).all() and (np.diag(Y) == 0).all() and (Y.sum(axis=1) == 12).all()
    return ok and (not strict or (Y.min() >= 0 and Y.max() <= 6))


def to_fmpz(Y):
    return flint.fmpz_mat([[int(v) for v in row] for row in np.asarray(Y)])


def poly_at_matrix(f, Yz):
    """f(Y) for f in Z[x], Y an fmpz_mat (Horner)."""
    coeffs = [int(c) for c in f.coeffs()]          # low -> high
    n = Yz.nrows()
    I = flint.fmpz_mat([[1 if i == j else 0 for j in range(n)] for i in range(n)])
    R = I * coeffs[-1]
    for c in reversed(coeffs[:-1]):
        R = R * Yz + I * c
    return R


# ---------------------------------------------------------------- number theory helpers
def is_square_int(n):
    n = int(n)
    if n < 0:
        return False
    r = flint.fmpz(n).isqrt()
    return int(r) * int(r) == n


def is_square_rat(q):
    q = Fraction(q)
    return q > 0 and is_square_int(q.numerator) and is_square_int(q.denominator)


def squarefree_part(n):
    """Signed squarefree part of a nonzero integer (uses flint factorisation)."""
    n = int(n)
    s = -1 if n < 0 else 1
    out = 1
    for p, e in flint.fmpz(abs(n)).factor():
        if e % 2:
            out *= int(p)
    return s * out


def sqclass(q):
    """Squarefree integer representing the square class of a nonzero rational."""
    q = Fraction(q)
    return squarefree_part(q.numerator * q.denominator)


def primes_of(n):
    return [int(p) for p, _ in flint.fmpz(abs(int(n))).factor()] if abs(int(n)) > 1 else []


def legendre(a, p):
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def _split(a, p):
    """a (nonzero integer) = p^k u with u a p-unit; returns (k, u)."""
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k, a


def hilbert(a, b, p):
    """Hilbert symbol (a, b)_p for nonzero squarefree-class integers a, b and a prime p."""
    a, b = int(a), int(b)
    al, u = _split(a, p)
    be, v = _split(b, p)
    if p != 2:
        eps = (p - 1) // 2
        s = (-1) ** (al * be * eps)
        if be % 2:
            s *= legendre(u, p)
        if al % 2:
            s *= legendre(v, p)
        return s
    e = lambda x: ((x % 8) - 1) // 2 % 2          # noqa: E731  x odd
    w = lambda x: (((x % 8) ** 2 - 1) // 8) % 2     # noqa: E731
    t = e(u) * e(v) + al * w(v) + be * w(u)
    return -1 if t % 2 else 1


def hasse(diag, p):
    """Hasse invariant prod_{i<j} (a_i, a_j)_p of the diagonal form <a_1, ..., a_n> (square classes as ints)."""
    s = 1
    for i in range(len(diag)):
        for j in range(i + 1, len(diag)):
            s *= hilbert(diag[i], diag[j], p)
    return s


def is_padic_square(a, p):
    """Is the nonzero squarefree integer a a square in Q_p?"""
    k, u = _split(int(a), p)
    if k % 2:
        return False
    if p == 2:
        return u % 8 == 1
    return legendre(u, p) == 1


def diagonal_classes(G):
    """Square classes of a diagonalisation of the positive definite integer Gram matrix G (fmpz_mat), via leading
    principal minors: d_i = Delta_i / Delta_{i-1}."""
    n = G.nrows()
    rows = G.tolist()
    deltas = [1]
    for i in range(1, n + 1):
        sub = flint.fmpz_mat([[rows[r][c] for c in range(i)] for r in range(i)])
        d = int(sub.det())
        if d <= 0:
            return None, None          # not positive definite (should not happen for genuine Gram matrices)
        deltas.append(d)
    diag = [squarefree_part(deltas[i] * deltas[i - 1]) for i in range(1, n + 1)]
    return diag, deltas


def hm_bad_primes(Gq, D, k):
    """Primes at which the positive definite form q (integer Gram matrix Gq, dim 2k, det q = D^k mod squares) fails to
    be hyperbolic over Q_p although p splits in Q(sqrt(-D)).  Empty iff q = <1, D> (x) q' over Q (given the
    determinant condition): at non-split p the extension kills every Hilbert symbol of Q_p-elements, the archimedean
    place of Q(sqrt(-D)) is complex, and at split p, q must be k*H, whose Hasse invariant (product over i < j) is 1 for
    odd p and (-1)^C(k,2) at p = 2."""
    diag, deltas = diagonal_classes(Gq)
    primes = {2}
    for dlt in deltas[1:]:
        primes |= set(primes_of(dlt))
    primes |= set(primes_of(D))
    bad = []
    for p in sorted(primes):
        if is_padic_square(squarefree_part(-D), p):
            target = 1 if p != 2 else (-1) ** (k * (k - 1) // 2)
            if hasse(diag, p) != target:
                bad.append(p)
    return bad


# ---------------------------------------------------------------- the analysis
def analyse(Y, want_hasse=True, want_ghc=True, strict=True):
    """Exact tests (V), (P), (D), (Pf), (EDC), (HM), (GHC).  Returns a dict; res['alive'] is False as soon as one
    necessary condition fails (res['killed_by'] names it)."""
    res = {'alive': True}
    if not valid_pattern(Y, strict):
        res.update(alive=False, killed_by='V')
        return res
    Yz = to_fmpz(Y)
    cp = Yz.charpoly()
    x12 = flint.fmpz_poly([-12, 1])
    h, r = divmod(cp, x12)
    assert r == 0
    content, facs = h.factor()
    assert int(content) == 1
    res['factors_h'] = [(str(f), int(e)) for f, e in facs]
    if any(e % 2 for _, e in facs):
        res.update(alive=False, killed_by='P')
        return res
    gfacs = [(f, e // 2) for f, e in facs]          # g = prod f^k
    res['g_factors'] = [(str(f), k, f.degree()) for f, k in gfacs]
    # roots (numeric, for positivity and for the record)
    roots = []
    for f, k in gfacs:
        rts = np.roots([float(c) for c in reversed([int(c) for c in f.coeffs()])])
        roots += [complex(z).real for z in rts] * k
    roots.sort()
    res['theta'] = roots
    res['mult2'] = all(k == 1 for _, k in gfacs) and len(set(round(t, 9) for t in roots)) == 12
    # (D)
    neg = [f for f, k in gfacs if any((27 + 4 * complex(z).real) <= 1e-9
                                       for z in np.roots([float(c) for c in reversed([int(c) for c in f.coeffs()])]))]
    if neg:
        res.update(alive=False, killed_by='D')
        return res
    # (Pf): prod (27 + 4 theta) over the 12 roots with multiplicity = prod_f ((-4)^d f(-27/4))^k
    Nf = {}
    prod = Fraction(1)
    for f, k in gfacs:
        d = f.degree()
        val = sum(Fraction(int(c)) * Fraction(-27, 4) ** i for i, c in enumerate(f.coeffs()))
        nf = Fraction((-4) ** d) * val
        assert nf.denominator == 1
        Nf[str(f)] = int(nf)
        prod *= nf ** k
    res['prod_s2'] = int(prod)
    q = Fraction(prod, 25)
    ok_pf = q.denominator == 1 and is_square_int(q.numerator) and int(flint.fmpz(q.numerator).isqrt()) % 2 == 1
    res['pi'] = int(flint.fmpz(q.numerator).isqrt()) if (q.denominator == 1 and is_square_int(q.numerator)) else None
    if not ok_pf:
        res.update(alive=False, killed_by='Pf')
        return res
    # (EDC) and (HM)
    one = flint.fmpz_mat([[1] * N])
    res['edc'] = []
    for f, k in gfacs:
        F = poly_at_matrix(f, Yz)
        if f(12) == 0:                                  # keep only the part inside 1^⊥
            F = flint.fmpz_mat(F.tolist() + one.tolist())
        B, nullity = F.nullspace()
        Bl = B.tolist()
        basis = flint.fmpz_mat([[Bl[r][c] for c in range(nullity)] for r in range(N)])
        assert nullity == 2 * k * f.degree(), (nullity, k, f.degree())
        Gq = basis.transpose() * basis
        detq = int(Gq.det())
        val = Fraction(detq) * Fraction(Nf[str(f)]) ** k
        ok = is_square_rat(val)
        rec = {'f': str(f), 'k': k, 'deg': f.degree(), 'dim': nullity, 'det_q_class': squarefree_part(detq),
               'N_f_class': squarefree_part(Nf[str(f)]), 'ok': ok}
        if ok and want_hasse and f.degree() == 1 and k >= 2:
            theta = -int(f.coeffs()[0])
            bad = hm_bad_primes(Gq, 27 + 4 * theta, k)
            rec['hasse_bad_primes'] = bad
            if bad:
                ok = False
                rec['ok'] = False
                rec['killed_by'] = 'HM'
        res['edc'].append(rec)
        if not ok:
            res.update(alive=False, killed_by=rec.get('killed_by', 'EDC'))
            return res
    # (GHC)
    if want_ghc:
        G = [[(27 if i == j else 0) + 4 * int(Y[i][j]) - 3 for j in range(N)] for i in range(N)]
        G24 = flint.fmpz_mat([row[:24] for row in G[:24]])
        diag, deltas = diagonal_classes(G24)
        if diag is None:
            res.update(alive=False, killed_by='GHC-psd')
            return res
        primes = {2}
        for dlt in deltas[1:]:
            primes |= set(primes_of(dlt))
        bad = [p for p in sorted(primes) if hasse(diag, p) != 1]
        res['ghc_bad_primes'] = bad
        if bad or not is_square_int(deltas[-1]):
            res.update(alive=False, killed_by='GHC')
            return res
    return res


# ---------------------------------------------------------------- reconstruction (nondegenerate case)
def reconstruct(Y, tol=1e-7):
    """All tournaments with codegree pattern exactly Y, if every eigenvalue of Y on 1^⊥ has multiplicity 2.
    Returns (status, list of 0/1 adjacency matrices, one per reversal pair)."""
    Y = np.asarray(Y, dtype=float)
    # orthonormal basis of 1^⊥
    Qm, _ = np.linalg.qr(np.column_stack([np.ones(N)] + [np.eye(N)[:, i] for i in range(N - 1)]))
    P = Qm[:, 1:]
    w, V = np.linalg.eigh(P.T @ Y @ P)
    V = P @ V
    pairs = []
    i = 0
    while i < len(w):
        j = i
        while j + 1 < len(w) and abs(w[j + 1] - w[i]) < 1e-6:
            j += 1
        m = j - i + 1
        if m != 2:
            return 'degenerate' if m > 2 else 'odd', []
        pairs.append((w[i:j + 1].mean(), V[:, i], V[:, j]))
        i = j + 1
    Bs = []
    for theta, u, v in pairs:
        s = np.sqrt(27 + 4 * theta)
        Bs.append(s * (np.outer(v, u) - np.outer(u, v)))
    Bs = np.array(Bs).reshape(12, N * N)
    signs = np.array([(1,) + t for t in itertools.product((1, -1), repeat=11)], dtype=float)
    Ms = signs @ Bs                                       # (2048, 625)
    off = ~np.eye(N, dtype=bool).ravel()
    err = np.abs(np.abs(Ms[:, off]) - 1).max(axis=1)
    found = []
    for idx in np.nonzero(err < 1e-6)[0]:
        Mi = np.rint(Ms[idx].reshape(N, N)).astype(np.int64)
        if not ((Mi == -Mi.T).all() and (np.abs(Mi[~np.eye(N, dtype=bool)]) == 1).all()):
            continue
        T = (Mi > 0).astype(np.int64)
        if not (T.sum(axis=1) == 12).all():
            continue
        if not (pattern_of(T) == np.asarray(Y, dtype=np.int64)).all():
            continue
        found.append(T)
    return 'ok', found


def has_S3(T):
    """Every 3-set has a common in-neighbour."""
    In = [set(np.nonzero(T[:, v])[0]) for v in range(N)]
    for a, b, c in itertools.combinations(range(N), 3):
        if not (In[a] & In[b] & In[c]):
            return False
    return True


def canon_key(T):
    return ''.join(str(int(x)) for x in T.ravel())


# ---------------------------------------------------------------- self-test on the two known (R25) examples
def validate(paths):
    ok_all = True
    for path in paths:
        T = load_tournament(path)
        Y = pattern_of(T)
        res = analyse(Y)
        status, sols = reconstruct(Y)
        Trev = T.T.copy()
        hit = any((S == T).all() or (S == Trev).all() for S in sols)
        print(path)
        print('  alive:', res['alive'], ' killed_by:', res.get('killed_by'), ' g factors:',
              [(f[2], f[1]) for f in res.get('g_factors', [])], ' pi =', res.get('pi'))
        print('  EDC:', [(e['deg'], e['k'], e['det_q_class'], e['N_f_class'], e['ok']) for e in res.get('edc', [])])
        print('  GHC bad primes:', res.get('ghc_bad_primes'))
        print('  reconstruction:', status, len(sols), 'tournament(s) up to reversal; contains the input:', hit)
        ok_all &= res['alive'] and hit
    return ok_all


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'validate':
        paths = sys.argv[2:] or ['research/compute/r25/codeg5_reg25_example_seed12.txt',
                                 'research/compute/r25/codeg5_reg25_example_seed13.txt']
        print('VALIDATION', 'PASSED' if validate(paths) else 'FAILED')

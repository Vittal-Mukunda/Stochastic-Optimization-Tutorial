#!/usr/bin/env python3
"""[check] Unit tests for the number theory in spectral_engine: Hilbert symbols (product formula, known values) and the
(HM) hyperbolicity test on forms whose answer is known by theory."""
import random
import sys

import flint

sys.path.insert(0, 'research/compute/p25')
import spectral_engine as se  # noqa: E402

rng = random.Random(7)
# known values
assert se.hilbert(-1, -1, 2) == -1 and se.hilbert(-1, -1, 3) == 1 and se.hilbert(2, 3, 3) == -1
assert se.hilbert(2, 5, 2) == -1 and se.hilbert(3, 5, 5) == -1 and se.hilbert(5, 5, 5) == 1 and se.hilbert(3, 3, 3) == -1
# product formula over random squarefree pairs
cnt = 0
for _ in range(3000):
    a = se.squarefree_part(rng.choice([-1, 1]) * rng.randint(1, 3000))
    b = se.squarefree_part(rng.choice([-1, 1]) * rng.randint(1, 3000))
    ps = set([2] + se.primes_of(a) + se.primes_of(b))
    prod = -1 if (a < 0 and b < 0) else 1
    for p in ps:
        prod *= se.hilbert(a, b, p)
    assert prod == 1, (a, b)
    cnt += 1
print('Hilbert symbol product formula: %d random pairs OK' % cnt)


def conj(diag, rng):
    """Integer Gram matrix of the diagonal form `diag` in a random unimodular basis."""
    n = len(diag)
    U = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for _ in range(3 * n):
        i, j = rng.sample(range(n), 2)
        c = rng.randint(-2, 2)
        for r in range(n):
            U[r][i] += c * U[r][j]
    Um = flint.fmpz_mat(U)
    Dm = flint.fmpz_mat([[diag[i] if i == j else 0 for j in range(n)] for i in range(n)])
    return Um.transpose() * Dm * Um


# theory: I_4 = norm form of (-1,-1)_Q; hyperbolic over Q(sqrt(-D)) iff that field splits (-1,-1), i.e. iff 2 does not
# split in it (the algebra ramifies at 2 and infinity; infinity is complex).  D = 7: -7 = 1 mod 8, 2 splits -> fail.
assert se.hm_bad_primes(conj([1, 1, 1, 1], rng), 7, 2) == [2]
assert se.hm_bad_primes(conj([1, 1, 1, 1], rng), 3, 2) == []
assert se.hm_bad_primes(conj([1, 1, 1, 1], rng), 15, 2) == [2]      # -15 = 1 mod 8
assert se.hm_bad_primes(conj([1, 1, 1, 1], rng), 11, 2) == []       # -11 = 5 mod 8
# forms <1, D> (x) q' must always pass
for _ in range(300):
    D = rng.choice([3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51])
    k = rng.choice([2, 3, 4, 6])
    q = [rng.randint(1, 40) for _ in range(k)]
    diag = []
    for a in q:
        diag += [a, a * D]
    assert se.hm_bad_primes(conj(diag, rng), D, k) == [], (D, k, q)
print('HM test: theory cases and 300 random <1,D> (x) q\' forms OK')

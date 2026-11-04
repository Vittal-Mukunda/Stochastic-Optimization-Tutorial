"""R8-D: exact-arithmetic checks of the spectral thresholds at N = 52 (no solver).

Checks, with fractions only:
 (1) sigma(J) = max sum x_i^2 over reals 0 <= x_i <= 6 with sum x_i <= 14 - J (the largest possible sum of squares
     of the off-diagonal entries of a tight row of M); brute force over integer vectors and the vertex formula.
 (2) Gershgorin threshold: tight-row off-diagonal sum 14 - J < 6 = diagonal  <=>  J >= 9.
 (3) Trace/Frobenius bound: a t x t symmetric matrix with diagonal 6, at most r positive eigenvalues and
     off-diagonal row square sums <= sigma satisfies 36 t^2 <= r (36 t + t sigma), i.e. t <= r (36 + sigma)/36.
     Corollary 2' (d^-(v) = 23, r = 23, t >= 50) needs t_max < 50; Corollary 3' (d^-(v) = 24, r = 24) needs
     t_max < 12 + E_A.
 (4) Corollary 2' bookkeeping: 11 E_A >= 23 * Jmin, slack 14 - E_A on the B-rows, t >= 51 - slack.
 (5) Distinct-set version (entries <= 5 once duplicates are merged).
"""
import itertools
from fractions import Fraction as F


def sigma_formula(s, cap=6):
    q, r = divmod(s, cap)
    return q * cap * cap + r * r


def sigma_brute(s, cap=6):
    best = 0
    for k in range(1, s + 1):
        for parts in itertools.combinations_with_replacement(range(1, cap + 1), k):
            if sum(parts) <= s:
                best = max(best, sum(p * p for p in parts))
    return best


def main():
    print('(1) sigma(J): max sum of squares of a tight row, entries in [0,6], sum <= 14-J')
    sig = {}
    for J in range(3, 15):
        s = 14 - J
        a, b = sigma_formula(s), sigma_brute(s) if s > 0 else 0
        assert a == b, (J, a, b)
        sig[J] = a
        print(f'  J={J:2d}  rowsum<= {s:2d}  sigma={a:3d}  gershgorin_strict={s < 6}')
    print('(2) Gershgorin strict iff J >= 9:', all((14 - J < 6) == (J >= 9) for J in range(3, 15)))

    print('(3)+(4) Corollary 2 at N=52 (d^-(v)=23, r=23, 51 rows)')
    for Jmin in range(3, 10):
        EA = -(-23 * Jmin // 11)              # ceil(23 Jmin / 11)
        EA = min(EA, 14)
        slack = 14 - EA
        tlow = 51 - slack
        tmax = F(23) * (36 + sig[Jmin]) / 36
        print(f'  Jmin={Jmin}: E_A>={EA}, B-slack<={slack}, t>={tlow}, Frobenius t<={float(tmax):.3f}'
              f' -> {"CONTRADICTION" if tmax < tlow else "no contradiction"}')
        if 11 * 14 < 23 * Jmin:
            print('     (also 11*E_A >= 23*Jmin is impossible with E_A <= 14)')

    print('(3) Corollary 3 at N=52 (d^-(v)=24, r=24): t >= 12 + E_A')
    for Jmin in range(6, 10):
        tmax = F(24) * (36 + sig[Jmin]) / 36
        print(f'  Jmin={Jmin}: Frobenius t<={float(tmax):.3f} -> needs E_A >= {int(tmax) - 11} for a contradiction')
    print('  Gershgorin (all tight J>=9): t <= 24 -> E_A <= 12, W_A <= 14')

    print('(5) distinct-set block (entries <= 5): sigma5(J)')
    for J in range(6, 15):
        s5 = sigma_formula(14 - J, 5)
        assert s5 == sigma_brute(14 - J, 5)
        print(f'  J={J}: sigma5={s5}, u <= {float(F(24) * (36 + s5) / 36):.3f}')


if __name__ == '__main__':
    main()

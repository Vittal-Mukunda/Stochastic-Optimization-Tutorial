"""R8-F-asymptotic: heuristic test of the ignored joint structure of the families {D(A + y)}.

Run from the project root:  python research/compute/r8f_intersect.py

At level i (|A| = n - i) of a c*-extremal profile, R = D(A) has about a_i n vertices and the sets
Q_y = D(A + y) = R cap N^-(y) have about a_{i-1} n vertices.  S_n forces, for j <= i:
   |Q_{y_1} cap ... cap Q_{y_j}| = |D(A + y_1 + ... + y_j)| >= nu_{n-i+j} ~ a_{i-j} n   (a_0 := 0, i.e. >= 1),
while the counting of Lemma 3.1 (k = n) forces about e^{n ln 2} distinct y.  This script asks whether
a RANDOM family (each Q_y a uniform a_{i-1}n-subset of R) could carry the j-wise intersection
condition, by comparing exponential rates (per n, natural log):
   bad_j = (j - 1) ln 2 - I_j,
where I_j is the large-deviation rate of the event 'j random sets meet in at most a_{i-j} n points'
(exact hypergeometric rate for j = 2, binomial approximation for j >= 3).  bad_j > 0 means a typical
set lies in exponentially many violating j-tuples, so a random family is far from feasible.
This is a HEURISTIC diagnostic, not a proof about tournaments.
Writes research/compute/r8f_intersect.json.
"""
from __future__ import annotations

import json
import os

import mpmath as mp

mp.mp.dps = 40
LN2 = mp.log(2)
HERE = os.path.dirname(os.path.abspath(__file__))


def F(x):
    x = mp.mpf(x)
    return mp.mpf(0) if x == 1 else mp.log(x) + (x - 1) * mp.log1p(1 / (x - 1))


def Phi(a, b):
    return F(a) - F(a - b)


def root_A(b):
    lo, hi = 2 * b, 2 * b + 1
    for _ in range(150):
        mid = (lo + hi) / 2
        if Phi(mid, b) > LN2:
            lo = mid
        else:
            hi = mid
    return hi


def H(p):
    p = mp.mpf(p)
    if p <= 0 or p >= 1:
        return mp.mpf(0)
    return -p * mp.log(p) - (1 - p) * mp.log(1 - p)


def KL(x, p):
    x, p = mp.mpf(x), mp.mpf(p)
    if x <= 0:
        return -mp.log(1 - p)
    return x * mp.log(x / p) + (1 - x) * mp.log((1 - x) / (1 - p))


def hyper_rate(a, b, x):
    """-(1/n) ln P(|Q cap Q'| = x n) for uniform b n-subsets of an a n-set."""
    return -(b * H(x / b) + (a - b) * H((b - x) / (a - b)) - a * H(b / a))


def main():
    a = [mp.mpf(0), mp.mpf(1)]
    for j in range(2, 16):
        a.append(root_A(a[-1]))
    rows = []
    for i in range(2, 13):
        R, q = a[i], a[i - 1]
        row = {"i": i, "a_i": float(R), "a_{i-1}": float(q), "Phi_check": float(Phi(R, q))}
        for j in range(2, min(i, 5) + 1):
            need = a[i - j]
            mean = R * (q / R) ** j
            if j == 2:
                I = hyper_rate(R, q, need) if need < mean else mp.mpf(0)
            else:
                I = R * KL(need / R, (q / R) ** j) if need < mean else mp.mpf(0)
            row[f"j{j}"] = {"required_over_n": float(need), "random_mean_over_n": float(mean),
                            "LD_rate": float(I), "bad_exponent": float((j - 1) * LN2 - I)}
        rows.append(row)
        print(f"i={i:2d}  |R|/n={float(R):9.4f} |Q|/n={float(q):9.4f}  " +
              "  ".join(f"j={j}: need {row[f'j{j}']['required_over_n']:.3f} mean {row[f'j{j}']['random_mean_over_n']:.3f} "
                        f"bad {row[f'j{j}']['bad_exponent']:+.4f}" for j in range(2, min(i, 5) + 1)))
    with open(os.path.join(HERE, "r8f_intersect.json"), "w", encoding="utf-8") as fh:
        json.dump({"rows": rows, "note": "heuristic; a_0 := 0 encodes 'nonempty'"}, fh, indent=1)


if __name__ == "__main__":
    main()

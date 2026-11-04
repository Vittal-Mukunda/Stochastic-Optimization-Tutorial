"""R8-F-asymptotic: the constraint |D(A)| >= f(n - |A|) cannot close an induction above c*.

Run from the project root:  python research/compute/r8f_transport.py

For gamma > c* the HYPOTHETICAL input f(i) >= gamma i 2^i (i < n), stronger than anything known, is fed
into the nu-profile calculus as nu_s >= ceil(gamma (n - s) 2^(n - s)) for 1 <= s <= n - 1.  The script
builds  m_s = max(b_s, ceil(gamma (n-s) 2^(n-s)))  (b = barrier profile of r8f_barrier.py),
m_n = 1, m_0 = N = 2 m_1 + n + 2, and checks exactly (python integers) every constraint of the calculus
(chain, top, all outer and, for n <= 100, all recursive Lemma 3.1 instances), the hypothetical inputs,
and N < gamma n 2^n.  If all hold, the calculus plus the induction hypothesis at level < n does NOT
yield f(n) >= gamma n 2^n.
Writes research/compute/r8f_transport.json.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r8f_barrier as B  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def ceil_gamma(num, den, i):
    # ceil(gamma * i * 2^i) with gamma = num/den exactly
    return -((-num * i * 2 ** i) // den)


def build(n, I, num, den):
    """Top levels (s >= n - I): barrier values; deep levels: m_s = max(2 m_{s+1} + n + 2, phi_s)."""
    I = min(I, n, B.IMAX)
    b = B.profile(n, I)
    m = [0] * (n + 1)
    m[n] = 1
    for s in range(n - 1, 0, -1):
        phi = ceil_gamma(num, den, n - s)
        if s >= n - I:
            m[s] = max(b[s], phi)
        else:
            m[s] = max(2 * m[s + 1] + n + 2, phi)
    m[0] = 2 * m[1] + n + 2
    return m


def main():
    out = {}
    for num, den in ((4, 5), (79, 100), (78, 100), (775, 1000)):
        g = num / den
        rows = {}
        for n in (32, 48, 64, 80, 100, 128, 200, 256, 400, 512):
            m = build(n, B.IMAX, num, den)
            rec = n <= 100
            ok, viol, cnt = B.check_profile(m, n, recursive=rec)
            hyp_in = all(m[s] >= ceil_gamma(num, den, n - s) for s in range(1, n))
            below = m[0] * den < num * n * 2 ** n
            hyp = B.check_hyp(m, n)[0] if n <= 256 else None
            rows[n] = {"exact_constraints_ok": ok, "violation": viol, "checked": cnt, "recursive_checked": rec,
                       "inputs_nu_s_ge_gamma_ok": hyp_in, "N_below_gamma_n_2n": below,
                       "N_over_n2n": m[0] / (n * 2 ** n), "lemmaB1_hyp": hyp}
            print(f"gamma={g:.3f} n={n:4d}: calculus ok={ok} ({cnt} checks, rec={rec}), inputs ok={hyp_in}, "
                  f"N/(n2^n)={m[0] / (n * 2 ** n):.6f} < gamma: {below}, B1-hyp={hyp}", flush=True)
        out[f"{num}/{den}"] = rows
    with open(os.path.join(HERE, "r8f_transport.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()

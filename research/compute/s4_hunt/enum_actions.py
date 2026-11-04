"""List odd-order group actions (affine Z_p x| C_e, cyclic Z_m) on 52..66 points with few pair orbits."""
import itertools, json, sys
from gactions import *

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def isprime(n): return n > 1 and all(n % r for r in range(2, int(n**.5) + 1))

out = []
VMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 40
# affine
for p in [q for q in range(3, 67) if isprime(q)]:
    for e in [d for d in divisors(p - 1) if d % 2 == 1 and d > 1]:
        types = []  # (label, size)
        for d in divisors(e):
            types.append((("C", d), p * e // d))
            types.append((("ZC", d), e // d))
        types = [t for t in types if t[1] <= 66]
        # multisets of block types with total size in [52, 66]
        def rec(i, rem, cur):
            if i == len(types):
                tot = sum(types[j][1] * k for j, k in cur)
                if 52 <= tot <= 66 and any(types[j][1] > 1 for j, k in cur):
                    yield list(cur)
                return
            lab, sz = types[i]
            for k in range(0, rem // sz + 1):
                if lab == ("ZC", e) and k > 1:  # more than 1 fixed point useless-ish; allow <=1
                    break
                yield from rec(i + 1, rem - k * sz, cur + ([(i, k)] if k else []))
        for combo in rec(0, 66, []):
            # rough V estimate: sum sizes^2/(2|G|)
            N = sum(types[j][1] * k for j, k in combo)
            if N * N / (2 * p * e) > VMAX * 1.3:
                continue
            out.append(("aff", p, e, [(types[j][0], k) for j, k in combo], N))
# cyclic
for m in range(3, 67, 2):
    ds = [d for d in divisors(m) if d > 1]
    def rec2(i, rem, cur):
        if i == len(ds):
            tot = sum(d * k for d, k in cur)
            if 52 <= tot <= 66 and len(cur) and max(d for d, k in cur) == m:
                yield list(cur)
            return
        for k in range(0, rem // ds[i] + 1):
            yield from rec2(i + 1, rem - k * ds[i], cur + ([(ds[i], k)] if k else []))
    for combo in rec2(0, 66, []):
        N = sum(d * k for d, k in combo)
        for f in (0, 1):
            if N + f <= 66 and (N + f) ** 2 / (2 * m) <= VMAX * 1.3:
                out.append(("cyc", m, 1, combo + ([(1, f)] if f else []), N + f))
res = []
for spec in out:
    kind, p, e, combo, N = spec
    if kind == "aff":
        t, mm = affine_group(p, e)
        subs = []
        for (lab, d), k in combo:
            gen = [power(mm, e // d)] if d > 1 else []
            if lab == "ZC":
                gen = gen + [t]
            subs += [gen] * k
        NN, P = action([t, mm], subs)
    else:
        c = cyclic(p)
        subs = []
        for d, k in combo:
            subs += [[power(c, d)] if d < p else []] * k
        NN, P = action([c], subs)
    assert NN == N
    V = n_pair_orbits(N, P)
    if V <= VMAX:
        res.append({"kind": kind, "p": p, "e": e, "combo": [[list(x) if isinstance(x, tuple) else x, k] for x, k in combo], "N": N, "order": len(P), "V": V})
res.sort(key=lambda r: (-r["N"], r["V"]))
json.dump(res, open("actions.json", "w"), indent=0)
for r in res: print(r["N"], r["V"], r["kind"], r["p"], r["e"], r["combo"])

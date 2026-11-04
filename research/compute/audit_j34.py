"""Exact case tree for J = 3 and J = 4 at N = 52.

Inputs, not re-proved here: Lemma J (J >= 3), Lemma A (a heavy vertex beats
only vertices of positive excess, and every pair from such a vertex into the
zero-excess set has 12 dominators), the bound of at most 4 common
in-neighbours inside the 5-regular block, and the identities

    heavy excess = 14 - J,
    sum of pair-dominator counts at u = 120 + 5 j_u - tau_u,
    Ex(u) = 5 + 10 j_u - sum lambda(q_y) over heavy y that beat u,
    triple excess = 4 |D| - c - 45 - E_both, with 0 <= c <= 4.

A heavy vertex of excess e beats exactly 6 - e vertices of the positive set.
lambda is charged to those vertices. A configuration survives only if every
pair-dominator count is an integer of size at least 12 and the resulting
triple-excess interval meets [0, Ex] at both endpoints.
"""

from __future__ import annotations

LAMBDA = {6: 4, 7: 7, 8: 9, 9: 10, 10: 10, 11: 0}


def partitions(total: int, parts: int, lo: int, hi: int):
    if parts == 0:
        if total == 0:
            yield ()
        return
    for first in range(lo, hi + 1):
        if first > total:
            break
        for rest in partitions(total - first, parts - 1, first, hi):
            yield (first,) + rest


def compositions(total: int, parts: int):
    if parts == 1:
        if total >= 1:
            yield (total,)
        return
    for first in range(total - parts + 1, 0, -1):
        for rest in compositions(total - first, parts - 1):
            if rest and first < rest[0]:
                continue
            yield (first,) + rest


def subsets(n: int, k: int):
    if k == 0:
        yield ()
        return
    for i in range(n - k + 1):
        for rest in subsets(n - i - 1, k - 1):
            yield (i,) + tuple(i + 1 + x for x in rest)


def pair_counts(strength):
    s = len(strength)
    out = {}
    total = sum(strength)
    for i in range(s):
        for j in range(i + 1, s):
            others = total - strength[i] - strength[j]
            numer = strength[i] + strength[j] - others
            if numer % 2:
                return None
            out[(i, j)] = numer // 2
    return out


def examine(j_value: int):
    examined = 0
    survivors = []
    reasons = {}
    excess = 14 - j_value
    for s in range(1, j_value + 1):
        lo = 6 - s
        for degrees in compositions(j_value, s):
            for n_heavy in range(0, excess + 1):
                for shape in partitions(excess, n_heavy, lo, 6):
                    choices = []
                    for e in shape:
                        choices.append(list(subsets(s, 6 - e)))
                    stacks = [()]
                    for options in choices:
                        stacks = [prev + (miss,) for prev in stacks for miss in options]
                    for misses in stacks:
                        examined += 1
                        reason = kill(degrees, shape, misses) or "survivor"
                        reasons[reason] = reasons.get(reason, 0) + 1
                        if reason == "survivor":
                            survivors.append((degrees, shape, misses))
    return examined, survivors, reasons


def kill(degrees, shape, misses):
    s = len(degrees)
    tau = [0] * s
    lam = [0] * s
    for e, miss in zip(shape, misses):
        q = 5 + e
        for u in miss:
            tau[u] += e
            lam[u] += LAMBDA[q]
    budget = [5 + 10 * j for j in degrees]
    ex = [budget[u] - lam[u] for u in range(s)]
    if any(value < 0 for value in ex):
        return "lambda"
    if s == 1:
        return None if tau[0] == 5 * degrees[0] else "pair-sum"
    strength = [12 * (s - 1) + 5 * degrees[u] - tau[u] for u in range(s)]
    counts = pair_counts(strength)
    if counts is None:
        return "not-integral"
    for pair, count in counts.items():
        if count < 12:
            return "below-12"
        both = 0
        for e, miss in zip(shape, misses):
            if pair[0] in miss and pair[1] in miss:
                both += e
        upper = 4 * count - 45 - both
        lower = upper - 4
        if upper < 0:
            return "negative-excess"
        room = min(ex[pair[0]], ex[pair[1]])
        if lower > room:
            return "exceeds-Ex"
    return None


def main():
    import json
    from pathlib import Path

    failures = []
    payload = {}
    for j_value in (3, 4):
        examined, survivors, reasons = examine(j_value)
        print(f"J={j_value} examined={examined} survivors={len(survivors)} reasons={reasons}")
        for item in survivors[:20]:
            print(" survivor", item)
        payload[str(j_value)] = {
            "examined": examined,
            "survivors": len(survivors),
            "reasons": reasons,
        }
        if survivors:
            failures.append(j_value)
    out = Path(__file__).with_name("audit_j34_result.json")
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit(f"surviving J values: {failures}")
    print("no survivor for J=3 or J=4")


if __name__ == "__main__":
    main()

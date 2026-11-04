"""Exact search for the DRT(51) pair-link of an S_4 tournament.

X has 12 vertices. Y contributes 37 subsets N_u of X.
A solution is a tournament on X together with those subsets such that
every constraint forced by S_4 in a doubly regular tournament of order 51 holds.
"""

from __future__ import annotations

import time

import z3

N = 12
Y = 37  # 51 - 12 - 2


def main() -> None:
    s = z3.SolverFor("QF_FD")
    s.set("timeout", 600_000)

    # beat[i][j]: i -> j
    beat = [[z3.Bool(f"b_{i}_{j}") for j in range(N)] for i in range(N)]
    for i in range(N):
        s.add(z3.Not(beat[i][i]))
        for j in range(i + 1, N):
            s.add(beat[i][j] == z3.Not(beat[j][i]))

    # m[u][x]: x lies in N_u, i.e. x beats the external vertex u
    m = [[z3.Bool(f"m_{u}_{x}") for x in range(N)] for u in range(Y)]

    # in-degree at least 5. Sum of in-degrees is C(12,2)=66, so this is the full score constraint.
    for x in range(N):
        s.add(z3.PbGe([(beat[y][x], 1) for y in range(N) if y != x], 5))

    # T_X is S_2: every pair has a common in-neighbour in X.
    for i in range(N):
        for j in range(i + 1, N):
            s.add(
                z3.PbGe(
                    [
                        (z3.And(beat[k][i], beat[k][j]), 1)
                        for k in range(N)
                        if k != i and k != j
                    ],
                    1,
                )
            )

    # Each external set meets every in-neighbourhood, has size at least 5,
    # and the sets pairwise intersect.
    for u in range(Y):
        s.add(z3.PbGe([(m[u][x], 1) for x in range(N)], 5))
        for y in range(N):
            s.add(
                z3.PbGe(
                    [
                        (z3.And(beat[x][y], m[u][x]), 1)
                        for x in range(N)
                        if x != y
                    ],
                    1,
                )
            )
    for u in range(Y):
        for v in range(u + 1, Y):
            s.add(z3.PbGe([(z3.And(m[u][x], m[v][x]), 1) for x in range(N)], 1))

    # Column sums: |{u : x in N_u}| = 12 + in_X(x)
    for x in range(N):
        s.add(
            z3.Sum([z3.If(m[u][x], 1, 0) for u in range(Y)])
            == 12 + z3.Sum([z3.If(beat[y][x], 1, 0) for y in range(N) if y != x])
        )

    # For every pair, common out-neighbours in X plus common out-neighbours in Y equal 10.
    for i in range(N):
        for j in range(i + 1, N):
            internal = [
                z3.And(beat[i][z], beat[j][z]) for z in range(N) if z != i and z != j
            ]
            external = [z3.And(m[u][i], m[u][j]) for u in range(Y)]
            s.add(
                z3.Sum([z3.If(t, 1, 0) for t in internal + external]) == 10
            )

    # Lexicographic row order, to cut identical row permutations.
    def row_key(u: int):
        # integer whose binary digits are the membership bits
        acc = z3.IntVal(0)
        for x in range(N):
            acc = acc * 2 + z3.If(m[u][x], 1, 0)
        return acc

    for u in range(Y - 1):
        s.add(row_key(u) >= row_key(u + 1))

    print("constraints", len(s.assertions()), flush=True)
    t0 = time.time()
    result = s.check()
    print("result", result, "seconds", round(time.time() - t0, 1), flush=True)
    if result == z3.sat:
        model = s.model()
        print("SAT model found")
        for i in range(N):
            outs = [j for j in range(N) if j != i and z3.is_true(model.eval(beat[i][j]))]
            print(i, "out", outs)


if __name__ == "__main__":
    main()

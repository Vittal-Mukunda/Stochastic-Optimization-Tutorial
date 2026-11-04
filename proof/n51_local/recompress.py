"""Shrink the integer Farkas multipliers of tree files (smallest power-of-two rescaling that still verifies exactly),
and store leaves in the compact form ['L', [rows], [values]].  The tree structure is unchanged.
Usage: python recompress.py in.json.gz out.json.gz"""
import sys, gzip, json
from lmodel import Model, parse_class, popc, N_R
from lpcert import exact_value

lines = open('reg11_S2.txt').read().split()


def main(src, dst):
    with gzip.open(src, 'rt') as f:
        D = json.load(f)
    M = Model(parse_class(lines[D['cl']]), D['mode'], aux=any(v[0] in ('z', 'n', 'c') for v in D['vars']))
    assert [list(v) for v in M.vars] == D['vars'] and [list(l) for (_, _, _, l) in M.rows] == D['rows']
    rows = [(co, s, b) for co, s, b, l in M.rows]
    xs = [(i, v[1]) for i, v in enumerate(M.vars) if v[0] in ('x', 'z')]
    jidx = [M.idx[('j', r)] for r in range(N_R)]

    def close(lb, ub):
        forced = {S for i, S in xs if lb[i] >= 1}
        for i, S in xs:
            if any(not (S & F) for F in forced):
                ub[i] = 0
        return lb, ub

    def shrink(y, lb, ub):
        items = [(int(k), int(v)) for k, v in y.items()]
        big = max(abs(v) for _, v in items)
        best = items
        for sh in range(big.bit_length() - 4, 0, -2):
            cand = []
            for k, v in items:
                w = (abs(v) + (1 << (sh - 1))) >> sh
                cand.append((k, w if v > 0 else -w))
            cand = [(k, w) for k, w in cand if w]
            yy = [0] * len(rows)
            for k, w in cand:
                yy[k] = w
            m = exact_value(rows, lb, ub, yy)
            if m is not None and m > 0:
                best = cand
                break
        best.sort()
        return ['L', [k for k, _ in best], [w for _, w in best]]

    def walk(t, lb, ub):
        if t[0] == 'L':
            return shrink(t[1], lb, ub)
        if t[0] == 'X':
            return t
        if t[0] == 'B':
            v, k = t[1], t[2]
            kids = []
            for child, (lo, hi) in ((t[3], (lb[v], k)), (t[4], (k + 1, ub[v]))):
                lb2, ub2 = list(lb), list(ub)
                lb2[v], ub2[v] = lo, hi
                lb2, ub2 = close(lb2, ub2)
                kids.append(walk(child, lb2, ub2))
            return ['B', v, k, kids[0], kids[1]]
        if t[0] == 'K':
            items = []
            for b, jv, sub in t[2]:
                lb2, ub2 = list(lb), list(ub)
                lb2[b] = max(lb2[b], 1)
                for r in range(N_R):
                    lb2[jidx[r]] = ub2[jidx[r]] = jv[r]
                lb2, ub2 = close(lb2, ub2)
                items.append([b, jv, walk(sub, lb2, ub2)])
            return ['K', t[1], items]
        raise ValueError(t[0])

    lb, ub = close(list(M.lb), list(M.ub))
    D['tree'] = walk(D['tree'], lb, ub)
    D['leaf_format'] = 'compact'
    with gzip.open(dst, 'wt') as f:
        json.dump(D, f, separators=(',', ':'))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

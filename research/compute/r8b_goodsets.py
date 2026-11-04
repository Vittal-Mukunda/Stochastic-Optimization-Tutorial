"""R8-B: for a fixed W = T[N^-(v)] (25 vertices, 12-regular), enumerate the 'good' sets Q subset W with |Q| = k and
|Q n N^-_W(w)| >= 5 for every w in W.  Row V3 of the v-local model says every Q'_b = D({v,b}) (b in N^+(v)) is good,
and |Q'_b| >= 12.  Also records which good 12-sets are in-neighbourhoods N^-_W(a).

Usage: python r8b_goodsets.py Wfile.json [kmax]
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np


def main():
    wf = sys.argv[1]
    kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 13
    d = json.loads(Path(wf).read_text())
    A = np.array(d['A'], dtype=np.int64)
    n = 25
    inmask = np.array([sum(1 << z for z in range(n) if A[z, w]) for w in range(n)], dtype=np.int64)
    innb = {w: frozenset(z for z in range(n) if A[z, w]) for w in range(n)}
    res = {}
    for k in range(12, kmax + 1):
        good = []
        it = itertools.combinations(range(n), k)
        while True:
            chunk = list(itertools.islice(it, 500000))
            if not chunk:
                break
            M = np.array([sum(1 << x for x in c) for c in chunk], dtype=np.int64)
            ok = np.ones(len(M), dtype=bool)
            for w in range(n):
                ok &= np.bitwise_count(M & inmask[w]) >= 5
            for i in np.nonzero(ok)[0]:
                good.append(chunk[i])
        nbhd = [frozenset(innb[w]) for w in range(n)]
        n_in = sum(1 for g in good if frozenset(g) in nbhd) if k == 12 else None
        res[k] = {'count': len(good), 'in_neighbourhoods_among_them': n_in, 'sets': [list(g) for g in good[:20000]]}
        print(k, len(good), n_in, flush=True)
    Path(__file__).parent.joinpath(f'r8b_goodsets_{Path(wf).stem}.json').write_text(json.dumps(res))


if __name__ == '__main__':
    main()

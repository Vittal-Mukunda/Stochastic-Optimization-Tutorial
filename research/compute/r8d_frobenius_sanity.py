"""R8-D: numerical sanity checks of the linear-algebra lemmas used in the report (random instances, numpy).

For random 0/1 matrices X (t rows, r columns, every row of weight 11, optionally a few rows of weight 12):
  (L1) M = X X^T - 5 * 11^T has at most r positive eigenvalues (Weyl), and for every principal submatrix M_S,
       tr(M_S)^2 <= r * ||M_S||_F^2 whenever tr(M_S) >= 0.
  (L2) if every row has weight 11 and 5 r < 121, M is positive semidefinite (M = X (I - 5/121 J) X^T).
  (L3) duplicated rows do not change the number of positive eigenvalues (congruence).
These are checks of the statements, not of any tournament.
"""
import numpy as np

rng = np.random.default_rng(902)


def rand_rows(t, r, extra=0):
    X = np.zeros((t, r))
    for i in range(t):
        k = 11 + (1 if i < extra else 0)
        X[i, rng.choice(r, k, replace=False)] = 1
    return X


def npos(A, tol=1e-9):
    return int((np.linalg.eigvalsh(A) > tol).sum())


def main():
    bad = 0
    for trial in range(400):
        r = int(rng.choice([23, 24]))
        t = int(rng.integers(20, 60))
        X = rand_rows(t, r, extra=int(rng.integers(0, 4)))
        M = X @ X.T - 5.0
        if npos(M) > r:
            bad += 1
        S = rng.choice(t, int(rng.integers(5, t + 1)), replace=False)
        MS = M[np.ix_(S, S)]
        if np.trace(MS) >= 0 and np.trace(MS) ** 2 > r * (MS ** 2).sum() + 1e-6:
            bad += 1
        X0 = rand_rows(t, r)
        M0 = X0 @ X0.T - 5.0
        if np.linalg.eigvalsh(M0).min() < -1e-9:
            bad += 1
        Xd = np.vstack([X0, X0[:3]])
        if npos(Xd @ Xd.T - 5.0) != npos(M0):
            bad += 1
    print('violations:', bad)
    X = rand_rows(51, 23)
    M = X @ X.T - 5.0
    off = M - np.diag(np.diag(M))
    print('random 51x23 example: tr^2 =', np.trace(M) ** 2, ' 23*||M||_F^2 =', 23 * (M ** 2).sum(),
          ' mean off-diag row square sum =', round((off ** 2).sum(1).mean(), 2), '(the lemma needs <= 40)')


if __name__ == '__main__':
    main()

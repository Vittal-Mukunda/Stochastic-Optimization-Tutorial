"""LP solving (HiGHS via highspy) and exact Farkas certificates for systems of integer rows.

A system is: rows (co: dict var->int, sense in '>=','<=','==', rhs: int) and a box lb <= x <= ub (ints).
A certificate is an integer vector y (one entry per row) with y_i >= 0 on '>=' rows, y_i <= 0 on '<=' rows, such that
   sum_i y_i * rhs_i  >  max_{lb <= x <= ub} sum_j (sum_i y_i a_ij) x_j .
Since every feasible x satisfies sum_i y_i (a_i . x) >= sum_i y_i rhs_i, such a y proves infeasibility.
"""
import numpy as np
import highspy
from scipy.sparse import csc_matrix

INF = highspy.kHighsInf


def to_highs(nvars, rows, lb, ub):
    I, J, V = [], [], []
    rl, ru = [], []
    for i, (co, sense, rhs) in enumerate(rows):
        for j, a in co.items():
            I.append(i); J.append(j); V.append(float(a))
        rl.append(float(rhs) if sense in ('>=', '==') else -INF)
        ru.append(float(rhs) if sense in ('<=', '==') else INF)
    A = csc_matrix((V, (I, J)), shape=(len(rows), nvars))
    lp = highspy.HighsLp()
    lp.num_col_ = nvars
    lp.num_row_ = len(rows)
    lp.col_cost_ = np.zeros(nvars)
    lp.col_lower_ = np.array(lb, dtype=float)
    lp.col_upper_ = np.array(ub, dtype=float)
    lp.row_lower_ = np.array(rl)
    lp.row_upper_ = np.array(ru)
    lp.a_matrix_.format_ = highspy.MatrixFormat.kColwise
    lp.a_matrix_.start_ = A.indptr
    lp.a_matrix_.index_ = A.indices
    lp.a_matrix_.value_ = A.data
    return lp


def solve_lp(nvars, rows, lb, ub, cost=None, time_limit=None):
    """Returns ('feasible', x) or ('infeasible', ray or None) or (status_string, None)."""
    h = highspy.Highs()
    h.setOptionValue('output_flag', False)
    h.setOptionValue('presolve', 'off')      # keep dual ray available
    if time_limit:
        h.setOptionValue('time_limit', float(time_limit))
    lp = to_highs(nvars, rows, lb, ub)
    if cost is not None:
        lp.col_cost_ = np.array(cost, dtype=float)
    h.passModel(lp)
    h.run()
    st = h.getModelStatus()
    if st == highspy.HighsModelStatus.kOptimal:
        return 'feasible', np.array(h.getSolution().col_value)
    if st == highspy.HighsModelStatus.kInfeasible:
        ray = None
        try:
            _st, has, vals = h.getDualRay()
            if has:
                ray = np.array(vals)
        except Exception:
            ray = None
        return 'infeasible', ray
    return str(st), None


def exact_value(rows, lb, ub, y):
    """margin = y.rhs - max_box (A^T y).x  (exact ints).  Certificate valid iff margin > 0 and signs ok."""
    for (co, sense, rhs), yi in zip(rows, y):
        if sense == '>=' and yi < 0:
            return None
        if sense == '<=' and yi > 0:
            return None
    c = {}
    yb = 0
    for (co, sense, rhs), yi in zip(rows, y):
        if yi == 0:
            continue
        yb += yi * rhs
        for j, a in co.items():
            c[j] = c.get(j, 0) + yi * a
    mx = 0
    for j, cj in c.items():
        mx += cj * (ub[j] if cj > 0 else lb[j])
    return yb - mx


def round_ray(rows, ray, K=1 << 40):
    m = max(abs(ray).max(), 1e-300)
    y = []
    for (co, sense, rhs), v in zip(rows, ray):
        t = int(round(v / m * K))
        if sense == '>=' and t < 0:
            t = 0
        if sense == '<=' and t > 0:
            t = 0
        y.append(t)
    return y


def cert_lp(nvars, rows, lb, ub):
    """Certificate-search LP: max y.rhs - sum_j (ub_j p_j - lb_j q_j), A^T y = p - q, p,q >= 0, |y| <= 1."""
    m = len(rows)
    # variables: y (m), p (n), q (n)
    nv = m + 2 * nvars
    cost = np.zeros(nv)
    ylb, yub = [], []
    for i, (co, sense, rhs) in enumerate(rows):
        cost[i] = -float(rhs)
        ylb.append(0.0 if sense == '>=' else -1.0)
        yub.append(0.0 if sense == '<=' else 1.0)
    for j in range(nvars):
        cost[m + j] = float(ub[j])
        cost[m + nvars + j] = -float(lb[j])
    crow = [dict() for _ in range(nvars)]
    for i, (co, sense, rhs) in enumerate(rows):
        for j, a in co.items():
            crow[j][i] = a
    crows = []
    for j in range(nvars):
        co = dict(crow[j])
        co[m + j] = -1
        co[m + nvars + j] = 1
        crows.append((co, '==', 0))
    lbv = ylb + [0.0] * (2 * nvars)
    ubv = yub + [INF] * (2 * nvars)
    st, sol = solve_lp(nv, crows, lbv, ubv, cost=cost)
    if st != 'feasible':
        return None
    return sol[:m]


def certify(nvars, rows, lb, ub, ray=None):
    """Try to produce an exact integer certificate; returns (y, margin) or None."""
    cands = []
    if ray is not None:
        cands += [ray, -ray]
    for cand in cands:
        y = round_ray(rows, cand)
        v = exact_value(rows, lb, ub, y)
        if v is not None and v > 0:
            return y, v
    yr = cert_lp(nvars, rows, lb, ub)
    if yr is not None:
        y = round_ray(rows, yr)
        v = exact_value(rows, lb, ub, y)
        if v is not None and v > 0:
            return y, v
    return None

"""Sanity check: the local model is satisfiable once J may exceed 2.  For a class and mode, minimise J over the model
without the hypothesis J <= 2 (no Lemma P rows, all set sizes 5..11, j_r <= 8, J <= 8; note sum_y (q_y - 5) = 8 - J
forces J <= 8) as an integer program (HiGHS), and re-check the integer optimum against every row exactly.
Usage: python sanity_minJ.py timelimit cl:mode [cl:mode ...]"""
import sys, time
import highspy
from lmodel import *
from lpcert import to_highs
lines = open('reg11_S2.txt').read().split()
tl = float(sys.argv[1])
for arg in sys.argv[2:]:
    cl, mode = arg.split(':'); cl = int(cl)
    M = Model(parse_class(lines[cl]), mode, Jmax=8, pattern=False)
    rows = [(co, s, b) for co, s, b, l in M.rows]
    lp = to_highs(len(M.vars), rows, M.lb, M.ub)
    lp.integrality_ = [highspy.HighsVarType.kInteger] * len(M.vars)
    cost = [0.0] * len(M.vars)
    for r in range(11): cost[M.idx[('j', r)]] = 1.0
    lp.col_cost_ = cost
    h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('time_limit', tl)
    h.passModel(lp); t0 = time.time(); h.run()
    st = h.getModelStatus(); info = h.getInfo()
    msg = f'{cl} {mode}: {st}'
    if h.getSolution().value_valid:
        x = [int(round(v)) for v in h.getSolution().col_value]
        good = all(M.lb[k] <= x[k] <= M.ub[k] for k in range(len(x)))
        for co, s, b in rows:
            v = sum(c * x[k] for k, c in co.items())
            good &= (v >= b) if s == '>=' else ((v <= b) if s == '<=' else (v == b))
        jv = [x[M.idx[('j', r)]] for r in range(11)]
        qs = [bin(M.vars[k][1]).count('1') for k in range(len(x)) if M.vars[k][0] == 'x' for _ in range(x[k])]
        msg += (f' | best integer J = {sum(jv)} (exact row check: {good}), lower bound {info.mip_dual_bound:.3f};'
                f' j = {jv}; |Q_y| counts = { {q: qs.count(q) for q in sorted(set(qs))} }')
    print(msg, f'[{time.time() - t0:.0f} s]', flush=True)

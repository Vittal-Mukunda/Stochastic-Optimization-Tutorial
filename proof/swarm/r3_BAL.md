# R3-BAL: balanced no-tight-pair Case A (Erdos #902, N = 52)

## Status (final for this lane)
- Verdict: UNDECIDED. The balanced no-tight-pair Case A is not shown impossible.
- Proved by hand (sections 1-2): U + A = 338 (two routes); x <= 1 impossible; eta_T >= Z >= sum (gamma-s)^+ >= N; K := eta_T + eta_M >= 3 for any survivor; K <= 2 impossible (Prop 2.2).
- Open: K = 3 (needs E_tail >= 79; crude bound 132) and K >= 4 (no inequality in this lane excludes it; the master inequality is satisfied by defect-rich configurations).
- Read: BRIEF sec 0-10, ROUND1_SYNTHESIS, r1_MOM-BALANCED (sec 2-5), r2_CASEA (W1-W8), r2_AUDIT (items 1-6). Only the derivations written below are relied upon; no lane claim is used without re-derivation or an explicit "imported" label (1.9).

## 0. Setting (as given in the task)
- T tournament on N = 52 vertices, property F1: every triple has >= 5 dominators.
- D(X) = vertices outside X beating all of X; D+(X) = vertices outside X beaten by all of X.
- d-(v), d+(v) in/out-degree; e(v) = d-(v) - 25; sum e = 26; e >= -1 (Lemma B).
- Pair P tight if |D(P)| = 11.
- Case: balanced, no tight pair. Every in-degree is 25 or 26; V0 = {e = 0} (26 vertices), V1 = {e = 1} (26 vertices). No pair has |D(P)| = 11.
- NT-B01 kills the subcase with all pair counts in {12,13}; so a survivor has some lambda_P >= 14, where lambda_P = |D(P)|, x_P = lambda_P - 12 >= 0, sum of x = 338.

## 1. Re-derived setup (checked from definitions)

Notation: V0 = {e=0} (d- = 25, d+ = 26), V1 = {e=1} (d- = 26, d+ = 25); |V0| = |V1| = 26; no tight pair, so lambda_P >= 12 and x_P = lambda_P - 12 >= 0; sum x_P = 16250 - 15912 = 338.

**(1.1) Identity for any triple Y.** O = V minus Y has 49 vertices. Inclusion-exclusion on A_i = {z in O : z -> y_i}: |D+(Y)| = 49 - sum|A_i| + sum|A_i cap A_j| - |D(Y)|, with sum|A_i| = sum d-(y_i) - 3 and sum|A_i cap A_j| = sum lambda_ij - sigma(Y). So
  k(Y) + l(Y) = L_Y := 52 - sum_i d-(y_i) + sum_{pairs} lambda - sigma(Y),  k = |D(Y)|, l = |D+(Y)|.
Checked: summing over all 22100 triples gives 1149200 - 1690650 + 812500 - 16250 = 254800 (matches sum L).

**(1.2) Lemma 2.1 (in-neighbourhoods).** For v in V0: sum_{a in N-(v)} lambda_av = C(25,2) = 300 over 25 terms, each >= 12, so all = 12 and x_{av} = 0 whenever the head v is in V0. For v in V1: sum over 26 in-nbrs = C(26,2) = 325, so sum of x over in-arcs = 13. Hence x is supported on arcs with head in V1; the pairs inside V0 have x = 0.

**(1.3) Tail identity (T).** For v with O = N+(v): sum_{b in O} x_{vb} = (26-e(v))(e(v)-1)/2 + sum_{b in O} e(b). For v in V0 this reads sum = f(v) - 13, where f(v) := |N+(v) cap V1|. Hence **f(v) >= 13 on V0**. For v in V1 the out-x-mass equals f(v) := |N+(v) cap V1|.

**(1.4) Notation for the reduction.** For v in V0 put u_v := f(v) - 13 >= 0. Then sum_{V0} f = 351 (V0->V1 arcs), so sum_{V0} u = 13, and x-out-mass of v in V0 is u_v. For w in V1 put s_w := f(w) - 12 (T1 out-degree minus 12), sum_{V1} s = 13. Put U := sum_{V0} u^2, A := sum_{V1} s^2. Also gamma_w := x-mass on V0->w arcs (sum_{V1} gamma = 13), and the x-mass of T1-in-arcs of w is 13 - gamma_w.

**(1.5) Key identity: U + A = 338 (proved; two independent derivations).**
 Route 1 (scores). Cyclic triples: cyc(a->b) := |N-(a) cap N+(b)| = d-(a) - lambda_ab = 13 + e(a) - x_ab. Summing over mixed arcs: V0->V1 gives 351*13 - 13 = 4550, V1->V0 gives 325*14 = 4550, total 9100. Each cyclic triple with a = 1 or 2 has exactly two mixed arcs and each cyclic triple with a = 0 or 3 has none, so 2(c_1 + c_2) = 9100, c_1 + c_2 = 4550 and c_0 + c_3 = 5850 - 4550 = 1300. Here c_3 = 2600 - sum_{V1} C(f,2) and c_0 = 2600 - sum_{V0} C(26-f,2) (out-degree inside V0 is 26 - f = 13 - u). With f = 12 + s on V1: sum_{V1} C(f,2) = (sum f^2 - 325)/2 and sum f^2 = 3744 + 24*13 + A = 4056 + A, so sum_{V1} C(f,2) = (3731 + A)/2; likewise sum_{V0} C(13-u,2) = (3731 + U)/2. Then c_0 + c_3 = 5200 - (3731*2 + A + U)/2 = 1300 gives **A + U = 338**. This is the same as STAR (r1_MOM-BALANCED 3.2) with d_v = u_v and o_w = f(w).
 Route 2 (V0-internal triples). For Y inside V0 the dominator and dominated counts are
  sum_{Y in V0} k = sum_{V0} C(13-u,3) + sum_{V1} C(13-s,3),   sum_{Y in V0} l = sum_{V0} C(12+u,3) + sum_{V1} C(13+s,3),
 (uses |N+(w) cap V0| = 13 - u on V0, = 13 - s on V1, and |N-(z) cap V0| = 12 + u on V0, = 13 + s on V1). Pointwise: C(13-u,3)+C(12+u,3) = 506 + 11.5u(u-1) and C(13-s,3)+C(13+s,3) = 572 + 12 s^2. Hence sum_{Y in V0}(k+l) = 27878.5 + 11.5 U + 12 A. On the other hand k+l = L = 13 - sigma for Y inside V0 (a = 0, X = 0), so the sum is 33800 - T0 with T0 = number of transitive V0-triples = sum_{V0} C(13-u,2) = (3731 + U)/2. Equating: 12 U + 12 A = 4056, i.e. **U + A = 338**. (Checks: 26*506 = 13156, 26*572 = 14872, C(26,3) = 2600 triples inside V0.)

**(1.6) Consequences.** A = sum s^2 >= 169 (since U <= 169 because sum u = 13 and u >= 0). And A <= 169 + 25 N where N := sum_{s<0} |s| (proof: s^+ <= 13, s^- <= 12, sum s^+ = 13 + N). So U >= 169 - 25N and U <= 13 max u.

**(1.7) Internal structure of T1 = T[V1] (proved).** Let y := x - 1 >= -1 on T1-arcs. Out-x-mass of w in V1 equals f(w) = out-degree in T1, so sum of y over T1-out-arcs of w is 0. In-x-mass from T1 is 13 - gamma_w, and T1-in-degree is 25 - f(w) = 13 - s_w, so the y-sum over T1-in-arcs of w is s_w - gamma_w. Consequently, with Z := number of T1-arcs with x = 0:
  eta_T := sum over T1 pairs C(x,2) >= Z >= sum_{w in V1} (gamma_w - s_w)^+ >= N.
 (Proof of eta_T >= Z: C(x,2) = y(y+1)/2 >= y for y >= 1, and sum over y>=1 of y equals Z because the y-sum over all T1-arcs is 0. Proof of Z >= (gamma-s)^+: a vertex w with y-sum over in-arcs equal to s-gamma needs at least gamma - s zero in-arcs when gamma > s.)

**(1.8) Tail lemma (proved by case check).** Write L_Y = 13 + t_Y with t_Y = X_Y - a_Y - sigma_Y, X_Y = sum of x over the three pairs, a_Y = |Y cap V1|. Then:
 (a) t_Y <= X_Y - 1 whenever a_Y >= 1 (a=1: cyc t = X-1, trans t = X-2; a=2: cyc t = X-2, trans t = X-3; a=3: cyc X-3, trans X-4). For a=0, t <= 0.
 (b) Every triple with t_Y >= 1 contains a pair with x >= 2. (Each case: a=1 needs X >= 2 cyclic or X >= 3 transitive, and the mixed arcs carry x <= 1 each; a=2 cyclic has X = alpha + x_{ww'} <= 2 if all x <= 1; a=2 transitive needs X >= 4 from at most three x-terms; a=3 needs X >= 4.)
 (c) Hence if all x <= 1 then E_tail := sum over L >= 14 of e(L) = 0, where e(L) := Lambda(L) - Lambda_q(L) (values e(14..18) = 2, 8, 20, 40, 70 from r1_MOM-BALANCED 3.6/5.1).

**(1.9) Master inequality (imported, re-checked in r2_AUDIT item 2h and 4).** 520 + 2 ex <= 147 eta_T + 138 eta_M + E_tail, with eta_M := sum over V0->V1 pairs C(x,2) and ex >= 0 the defect term from the family in r1_MOM-BALANCED 3.4b. (From 23842 + 2ex <= 69 S2 + 9 eta + E_tail and S2 = 338 + 2 eta_T + 2 eta_M.)
 Consequence: with all x <= 1, master gives 520 <= 0, a contradiction (this is a second proof of the x <= 1 case; the first is Prop 4.1(b) of r1_MOM-BALANCED, which I re-derived as: x <= 1 forces gamma = s >= 0, so A <= 169 and U = 169, u = 13 at one v0, s = 13 at one w0, then gamma_{w0} = 13 needs 13 arcs of x = 1 into w0 from V0 but only v0 has u-mass).

## 2. Defect bounds for a survivor (new; proved from 1.3-1.8)

Notation: eta_T, eta_M as in (1.7),(1.9); K := eta_T + eta_M; N, A, U as in (1.4)-(1.6); Z = number of zero T1-arcs; m := max_{V0} u_v attained at v0; s* := max_{V1} s_w attained at w0.

**(2.1) Facts.**
 (a) eta_T >= Z >= sum_w (gamma_w - s_w)^+ >= N, and sum_w (s_w - gamma_w)^+ = sum_w (gamma_w - s_w)^+ <= Z (since sum (s - gamma) = 0).
 (b) 169 <= A <= 169 + 25N and 0 <= U <= 169 (U + A = 338).
 (c) m >= U/13 >= (169 - 25N)/13 (since U <= m * sum u = 13m).
 (d) s* (13 + N) + 12N >= A >= 169, so s* >= (169 - 12N)/(13 + N).
 (e) gamma_{w0} >= s* - eta_T (from (2.1a)).
 (f) For p in V0 with p != v0: sum over p of alpha_{p w0} <= sum_{p != v0} u_p = 13 - m, where alpha_{p w} is the x-value on the arc p->w.

**(2.2) Proposition (proved): K <= 2 is impossible.** Suppose K <= 2; then N <= Z <= eta_T <= 2.
 By (d): s* >= 13 - 25*2/15 > 9.6, so s* >= 10 (integer), hence gamma_{w0} >= 10 - eta_T >= 8 by (e).
 By (c): m >= (169 - 50)/13 = 9.15, so m >= 10 and 13 - m <= 3.
 If v0 does not beat w0, gamma_{w0} = sum over p of alpha_{p w0} <= 13 - m <= 3, contradicting gamma_{w0} >= 8.
 If v0 beats w0: by (f) alpha_{v0 w0} >= gamma_{w0} - 3 >= 5, so eta_M >= C(5,2) = 10 > 2, contradicting K <= 2.
 QED. (Numbers displayed: 25*2/15 = 3.33, 169 - 50 = 119, 119/13 = 9.15, 13 - 10 = 3, C(5,2) = 10.)

**(2.3) What survives the three inequalities.** For K = 3 (so N <= 3): s* >= (169 - 36)/16 = 8.3, so s* >= 9; gamma_{w0} >= 9 - 3 = 6; m >= (169 - 75)/13 = 7.2, so m >= 8 and 13 - m <= 5. If v0 does not beat w0 then gamma_{w0} <= 5 < 6, a contradiction; so v0 beats w0 and alpha_{v0 w0} >= 6 - 5 = 1. Hence for K = 3: v0 -> w0 with x(v0,w0) >= 1 and u_{v0} >= 8, s_{w0} >= 9. So K >= 3 for every survivor (proved), and K = 3 is not yet excluded.

**(2.4) The master inequality and its limits (proved from 1.9).** Write 520 + 2 ex <= 147 eta_T + 138 eta_M + E_tail. Using f_G(2) = 12, f_H(2) = 0, f_H(3) = 12 (computed: f_G(x) = C(12+x,3) - 220 - 66x, f_H(x) = C(11+x,3) - 220 - 66(x-1)):
 - If all x <= 1: E_tail = 0 and the inequality fails (520 <= 0). This is the x <= 1 kill.
 - Four T1-arcs with x = 2 (eta_T = 4, eta_M = 0, ex = 0, E_tail = 0): 588 >= 520, so the master inequality is satisfied. The master cannot exclude this.
 - Four mixed arcs with x = 2 (eta_M = 4): ex = 4*12 = 48, need 552 >= 520 + 96: fails unless E_tail >= 64. So mixed heavy arcs are costlier.
 - Three T1-arcs with x = 2 (eta_T = 3): need E_tail >= 520 - 441 = 79.
 - Tail lemma (1.8) plus the cyclic count cyc(P) = 14 - x_P (for a T1-arc with head x_P: cyc = d-(tail) - lambda = 26 - 14 = 12 when x_P = 2) bounds the tail per heavy arc: triples through P with t >= 1 are (i) cyclic (at most 12 of them, e = 2 each when the other arcs have x = 1), (ii) transitive with third vertex c in V0 beating both ends with x = 1 on both arcs (at most 6, since such c have u_c >= 2 and sum u = 13), (iii) triples containing a second heavy arc (at most 3 such triples, e <= 8). Crude total for three x=2 arcs: 3 * (12*2 + 6*2) = 108 from (i)-(ii), plus at most 3 triples containing two heavy arcs with e <= 8, so E_tail <= 108 + 24 = 132, which is above 79. So K = 3 is NOT excluded by this count (conditional gap: need the zero arcs, Z = 3, to kill cyclic tails).

**(2.5) Consequence for the structure.** Any survivor has K >= 3, and heavy pairs (x >= 2) exist. The master inequality is satisfied by any configuration with 147 eta_T + 138 eta_M >= 520 (K >= 4 with eta_M small), and it gives no upper bound on defects. A kill must therefore come from an upper bound on defects or from a structural argument on heavy pairs, neither of which I have.

## 3. Dead ends (each with its reason)

- **D1. Moment master alone.** The master inequality (1.9) is a LOWER bound on defects (more defects = more room). It kills only the defect-poor regime. Defect-rich survivors (e.g. four T1-arcs with x = 2) are consistent with it. Dead as a closing argument.
- **D2. F1 summed over one class.** sum_{Y in V0} k >= 13156 always (convexity: min at u, s in {0,1}, value 13*286 + 13*220 = 6578 per class), against the requirement 5 * 2600 = 13000. Slack 156 always, so no contradiction. Likewise sum_{Y in V1} k = sum_{V1} C(12+s,3) + sum_{V0} C(13+u,3) >= 6578 + 8450 = 15028 >= 13000 (slack 2028). Dead.
- **D3. Upper bound l <= L - 5 on V0-triples.** Using k >= 5 with k + l = L gives sum_{Y in V0} l <= 20800 - T0; the balanced value of sum_{Y in V0} l is 6578 + 8450 = 15028 <= 18928. Not binding. Dead.
- **D4. Score constraints alone** (U + A = 338, 169 <= A <= 169 + 25N): consistent for every N >= 0 (they only force defects through N and the concentration of u and s). Not contradictory on their own.
- **D5. Mistake caught (not a dead end of the case):** the count of V0-triples is C(26,3) = 2600, not C(25,3) = 2300; with 2300 one gets a false contradiction U + A = 13. Corrected in 1.5.
- **D6. Route via x <= 1 tails.** My first attempt counted tail triples from a = 1 with X = 2 cyclic as L = 14; the correct count is X = alpha_p only (a cyclic a=1 triple has one mixed arc into w). Irrelevant to the conclusion since E_tail = 0 when x <= 1.

## 4. Verdict and what the next step needs

**Verdict: UNDECIDED.** I did not find a kill for balanced no-tight-pair Case A.

Proved (hand-checked, every step written out in this file):
 (P1) U + A = 338, with A = sum_{V1}(f-12)^2 and U = sum_{V0}(f-13)^2 (sections 1.4-1.5, two routes).
 (P2) x <= 1 everywhere is impossible (section 2.4 and r1_MOM-BALANCED Prop 4.1(b), now also via the defect chain).
 (P3) eta_T >= Z >= sum_w (gamma_w - s_w)^+ >= N; A >= 169; m >= (169 - 25N)/13.
 (P4) K := eta_T + eta_M >= 3 for every survivor; K <= 2 is impossible (Prop 2.2).

Open (what a survivor must look like):
 (O1) K = 3: need E_tail >= 79 (eta_T = 3, eta_M = 0) or >= 103 (one T1-arc with x = 3). Crude bound E_tail <= 126. Needs the zero arcs (Z = 3) to cut the cyclic tails.
 (O2) K >= 4: no inequality in this lane excludes it. The master inequality is satisfied.

Surviving structure (minimal, as the lane could describe): some pair with lambda >= 14 (x >= 2), in fact at least three units of defect (eta_T + eta_M >= 3); T1-defects are cheaper than mixed defects (f_H(2) = 0 but f_G(2) = 12); for K = 3 the V0 vertex with largest u has u >= 8, the V1 vertex with largest s has s >= 9, and v0 beats w0 with x >= 1 (section 2.3). (K <= 2 is impossible by Prop 2.2.)

Next identity needed: an upper bound on eta_T + eta_M (defects) — equivalently, an inequality that gets worse as defects grow. Candidate: the third-moment (cubic) identity over triples, which would bound E_tail by a cubic in X and thereby bound defects from above. Not done here.

Dead ends are listed in section 3. Lane-reported round-2 claims were re-derived (the STAR identity, the score window D1 in [162.5, 318.5], the tail identity). The score window is now the cleaner statement U + A = 338 with U in [13, 169].

<!-- END -->


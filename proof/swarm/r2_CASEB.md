# R2-CASEB: Round 2 lane, Case B (tight pair P={a,b}, |D(P)|=11)

Target: f(4) >= 53, i.e. no tournament on N=52 vertices has property S_4 (F1: every triple has >= 5 dominators).

## Status

- Stage: finished (round 2 lane R2-CASEB). Final verdicts below.
- PROVED by hand (verified twice): identity (I) sum_Y (k-5) = sum_y C(t_y,3) - 715; identity (II) sum over pairs D = 110 + sum_y C(t_y,2); the h = 0 counts (65 excess triples, 35 pair excess); pair identities (PS), (S), mod-4 form s(u,v) = 3 + 4 delta - c; Lemma L5b (c_in = c_out for every pair of a regular tournament on 11 vertices); x-second-moment identity sum x^2 = 110 + 2 sum C(c,3).
- PRIMARY (h = 0, J = 14): NOT DECIDED. No contradiction found. All counting constraints hold, including for the doubly regular T[R] (QR_11). Conditional residual reduction given in L6(d).
- SECONDARY ((I) on J = 5 survivors): (I) kills none of the four survivors (heavy deficits 39, 39, 46, 50, all <= 65). Partitions 2^4+1, 2^3+1^3, 1^9 are killed by (I) alone.
- Dead ends recorded in L8 (second moment is circular without a cap; counting in R is consistent; spectral check consistent; V_0 links consistent).
- S_4 used? Only in L11: under full S_4 every pair of R has c >= 1 (dominators of {a,b,r,r'} lie in R). Not used in L1-L10.

## Plan

1. Read BRIEF.md sections 0-10 (rules, notation, proved facts, dead ends, method).
2. Read r1_AUDIT-52-B sections 1, 2, 4, 5, 8.
3. Verify identities (I) and (II) by hand, with every count displayed.
4. Attack branch h = 0: second moment of k over triples in R; the 5-block requirement for triples with no R-dominator; 5-regularity of T[R] and the c-counts; O-internal arcs if needed.
5. Secondary: (I) gives sum over y of (20 - C(t_y,3)) <= 65 for general J; test J = 5 configurations.
6. Verdict per branch, with explicit configurations and constraints on survivors.

## Log

(entries appended below as work proceeds)

### L1. Inputs (from BRIEF section 8 and AUDIT-52-B sections 2, 4, 8)

Setting: P = {a,b} tight, R = D(P), |R| = 11, O = 39 outside vertices. For r in R: d^-(r) = 25 + j_r, with j_r >= 0 (Lemma T: every dominator of a tight pair has in-degree >= 25). Sum of j_r = J. For y in O: q_y = |R cap N^-(y)| >= 5, t_y = 11 - q_y, e_y = q_y - 5 = 6 - t_y >= 0, sum over O of e_y = 14 - J (E).

Verified again: r in R has 5 in-neighbours inside R, none in P, and 20 + j_r in O (since d^-(r) = 25 + j_r). Out-degree of r in R is 5. Hence sum over O of q_y = sum_r (19 - j_r) = 209 - J, and 209 - J - 5*39 = 14 - J. OK.

Since T[R] has min in-degree >= 5 (F2) and sum of in-degrees = C(11,2) = 55 = 11*5, T[R] is 5-regular. OK.

### L2. Identity (I), verified

For Y a triple in R: k(Y) = x_Y + m_Y, where x_Y = #{w in R minus Y : w beats Y} and m_Y = #{y in O : Y inside M_y}. (Y inside M_y iff Y cap Q_y = empty, since M_y = R minus Q_y.)
- Sum over Y of x_Y = sum over w in R of C(out_R(w), 3) = 11 * C(5,3) = 11 * 10 = **110**.
- Sum over Y of m_Y = sum over y of C(t_y, 3) (each M_y has C(t_y,3) triples).
- Sum over the C(11,3) = 165 triples: sum k = 110 + sum_y C(t_y,3). Subtracting 5 * 165 = 825: **sum_Y (k(Y) - 5) = sum_y C(t_y,3) - 715.** OK.
- Equivalently sum_y (20 - C(t_y,3)) = 780 - sum_y C(t_y,3) = 65 - sum_Y e_Y, where e_Y := k(Y) - 5 >= 0 (F1). So **sum_y (20 - C(t_y,3)) <= 65, with slack sum_Y e_Y.** OK.

Note: a light y (q_y = 5, t_y = 6) contributes 20 - C(6,3) = 0 to this sum. Only heavy y (t_y <= 5) contribute, with deficits: t = 0,1,2 give 20; t = 3 gives 19; t = 4 gives 16; t = 5 gives 10.

### L3. Identity (II), verified

For u != v in R: D_uv = |D({u,v})| = c_uv + m_uv, where c_uv = #{w in R : w beats u and v} and m_uv = #{y in O : u, v both in M_y}. (a and b are beaten by all of R, so they do not dominate a pair inside R.)
- Sum over the 55 pairs of c_uv = sum over w of C(5,2) = 11 * 10 = **110**.
- Sum over pairs of m_uv = sum over y of C(t_y,2).
- Sum over pairs of D_uv = **110 + sum_y C(t_y,2)**. OK.

Branch h = 0 (all t_y = 6): sum D = 110 + 39*15 = 110 + 585 = 695 = 55*12 + 35. So sum over pairs of delta_uv = 35 with delta_uv := D_uv - 12 >= 0 (D >= 12 from AUDIT-52-B section 2(b)). OK.

Branch h = 0 (all t_y = 6, all e_y = 0): sum over Y of e_Y = 39*20 - 715 = 780 - 715 = **65**. Check: 110 + 780 = 890 = 5*165 + 65. OK.

### L4. The h = 0 reformulation as a covering problem (verified)

Let O_w := N^+_R(w) (|O_w| = 5, w not in O_w) for w in R, and M_y (|M_y| = 6) for y in O. Let F be the multiset of 11 + 39 = 50 sets. Then for a triple Y in R, k(Y) = #{S in F : Y inside S}. For a pair {u,v} in R, D_uv = #{S in F : u,v in S}. For a point u in R, #{S in F : u in S} = 5 + (20 + j_u) = 25 + j_u = d^-(u).

So the question is: can 39 six-subsets and 11 five-subsets (the out-neighbourhoods of a 5-regular tournament on R) cover every triple of the 11-set at least 5 times, with point-degrees 25 + j_u (j_u >= 0, sum j = 14)?

Identities in h = 0, all verified:
- (PS) sum over v != u of D_uv = 120 + 5 j_u, so **sum over v of delta_uv = 5 j_u** for each u in R. Check: sum over u of 5 j_u = 70 = 2 * 35. OK.
- (S) s(u,v) := sum over w of e_{uvw} = 4 D_uv - c_uv - 45 = 3 + 4 delta_uv - c_uv (E_both = 0 since no heavy vertex). So **0 <= 3 + 4 delta_uv - c_uv**, hence: delta_uv = 0 forces c_uv <= 3; c_uv = 4 forces delta_uv >= 1.
- (B) s(u,v) <= Ex(u) = 5 + 10 j_u and <= 5 + 10 j_v. So delta_uv <= (2 + c_uv + 10 min(j_u,j_v))/4.
- Ex(u) := sum over Y containing u of e_Y = 5 + 10 j_u. Check: sum over u of Ex(u) = 3 * 65 = 195 = 55 + 140. OK.
- Consequence: for u in V_0 (j_u = 0): delta_uv = 0 for all v, so D_uv = 12 for all v, and sum over v of c_uv = 20 with c_uv <= 3. Since sum over v of (3 - c_uv) = 30 - 20 = 10 = 2 Ex(u). OK.
- Consequence: all of the excess sum_pairs delta = 35 sits on pairs inside V_+ (the set of j >= 1 vertices), and for u in V_+, sum over v in V_+ of delta_uv = 5 j_u.

### L5a. Mod-4 pair identity in branch h = 0 (verified)

Write s(u,v) := sum over w in R minus {u,v} of e_{uvw} (triple excesses through the pair). In h = 0, (S) reads s(u,v) = 4 D_uv - c_uv - 45 = 3 + 4 delta_uv - c_uv. Hence

  **s(u,v) = sum_w e_{uvw} = 3 + 4 delta_uv - c_uv, so s(u,v) ≡ 3 - c_uv (mod 4), and s(u,v) >= 0.**

Consequences: s(u,v) = 0 forces c_uv = 3 and delta_uv = 0 (all triples through u,v have e = 0). c_uv = 0, 1, 2, 3, 4 give s ≡ 3, 2, 1, 0, 3 (mod 4). Summing over pairs: sum s = 165 + 140 - 110 = 195 = 3 * 65. OK.

## L6. Conditional structure when T[R] is doubly regular (c_uv = 2 for every pair; e.g. the Paley tournament QR_11, where c = (11-3)/4 = 2 is the standard count)

Assumption flagged: T[R] doubly regular. Nothing else is assumed.

(a) s(u,v) = 1 + 4 delta_uv >= 1 for every pair of R. So **every pair of R lies in a triple of positive excess**.

(b) For j_u = 0 (u in V_0): all delta_uv = 0, so s(u,v) = 1 for all v. Hence the triples through u with positive excess, counted with multiplicity e, form a family in which every pair {v,w} of R minus u lies in exactly one (since sum over w of e_{uvw} = 1 for each v, and e is integer). So the excess triples through u form a **perfect matching** of R minus {u} (5 pairs, each giving a triple with e = 1), and all other triples through u have e = 0.

(c) For u in V_+: the link multigraph G_u on the 10 points R minus u has edge {v,w} with multiplicity e_{uvw}, and vertex degrees s(u,v) = 1 + 4 delta_uv, total edges 5 + 10 j_u (= Ex(u)). Handshake check: sum of degrees = 10 + 20 j_u = 2 (5 + 10 j_u). OK.

(d) Residual reduction, valid when the 11 complements C_w := R minus O_w (6-sets, C_w is the complement of the out-neighbourhood of w) are among the M_y. Verified count: for a triple Y, with x = x_Y, n_i := #{w : |O_w cap Y| = i}. Using sum_w |O_w cap Y| = 15 (each point of R lies in 5 out-sets), sum_w C(|O_w cap Y|,2) = 3 * c = 6 (each pair lies in 2 out-sets), and n_3 = x:
  n_2 = 6 - 3x, n_1 = 3 + 3x, n_0 = 2 - x (check: n_0+n_1+n_2+n_3 = 2-x+3+3x+6-3x+x = 11, OK).
  C_w contains Y iff O_w cap Y = empty, so #{complements containing Y} = 2 - x_Y. Hence the other 28 blocks must cover Y at least 5 - x_Y - (2 - x_Y) = **3 times**, for every triple Y, with excess sum 28*20 - 165*3 = 65. Point degrees of the residual 28 blocks: 14 + j_u (sum 168 = 28*6). Residual pair counts: 7 + delta_uv.
  For u in V_0 the residual link is 14 five-subsets of the 10-set R minus u, each point in 7 of them, every pair covered >= 3, total 140 = 45*3 + 5. Each point has pair-excess 4*7 - 27 = 1, so the pair-excess forms a perfect matching, consistent with (b). OK.
  This is a conditional reduction only: the 28 residual blocks must 3-fold cover the triples of an 11-set, with the matching structure at each V_0 vertex. It was not decided.

(e) Schonheim-type check (not a proof, only a necessary bound): each point u of V_0 needs at least L_3(10,5,2) = ceil(2 * ceil(9*3/4)) = ceil(2*7) = 14 residual blocks through it, and there are exactly 14 + j_u. So for V_0 vertices the bound is tight. OK.

## L5b. Lemma (regular tournament on 11 vertices), proved

Let T[R] be 5-regular on 11 vertices. For any pair u,v with u -> v: |N^-(u) cap N^-(v)| = |N^+(u) cap N^+(v)|.
Proof: classify the other 9 vertices by their relation to u and v. Let c_in = |N^-(u) cap N^-(v)|, c_out = |N^+(u) cap N^+(v)|, p = |N^+(u) cap N^-(v)|. Out-degree of u: 5 = 1 (v) + c_out + p, so p = 4 - c_out. In-degree of v: 5 = 1 (u) + c_in + p (in-nbrs of v are u, plus those in N^-(u) and those in N^+(u)), so c_in = 4 - p = c_out. QED. (Verified: the 9 vertices split as c_in + c_out + p + q = 9 with q = 5 - c_out, giving c_in + c_out + (4-c_out) + (5-c_out) = 9 - c_out + c_in... consistent with c_in = c_out.)

Consequence: for every pair in R, the number of common in-neighbours in R equals the number of common out-neighbours in R, c_uv = g_uv. Then, with x_Y the number of R-dominators of a triple Y,
sum_Y x_Y(x_Y - 1)/2 = sum over pairs {w,w'} of C(g_{ww'},3) = sum over pairs of C(c_{ww'},3). So
**sum_Y x_Y^2 = 110 + 2 * sum over pairs of C(c_uv,3).** OK.

## L7. Secondary: identity (I) applied to the J = 5 survivors of AUDIT-52-B section 8.2 (verified)

Rule: sum over heavy y of (20 - C(t_y,3)) <= 65, with slack sum_Y e_Y = 65 - sum over heavy y of deficit. Deficits by t_y (= 6 - e_y): t = 0,1,2: 20; t = 3: 19; t = 4: 16; t = 5: 10.

| configuration (parts e_y) | s | heavy deficit sum | slack sum_Y e_Y | verdict under (I) |
|---|---|---|---|---|
| 6 + 3 | 4 | 20 + 19 = 39 | 26 | survives |
| 6 + 3 | 5 | 39 | 26 | survives |
| 6 + 2 + 1 | 5 | 20 + 16 + 10 = 46 | 19 | survives |
| 6 + 1 + 1 + 1 | 5 | 20 + 10 + 10 + 10 = 50 | 15 | survives |

So **(I) kills none of the four J = 5 survivors** of 8.2. Each survives with positive slack. Computation check: 65 - 39 = 26, 65 - 46 = 19, 65 - 50 = 15.

Partitions (E = 9) that (I) does kill on its own, for reference: 2+2+2+2+1 (deficit 4*16 + 10 = 74 > 65), 2+2+2+1+1+1 (3*16 + 3*10 = 78), and 1^9 (90). All of these are also killed in 8.2 by K1. The rule is weak for J = 5 because the deficits of heavy vertices are small (at most 20 each).

## L8. Dead ends (recorded with reasons)

* **DE1, second moment via pairs of sets.** Identity: sum_Y C(k_Y,2) = sum over pairs {S,S'} in F of C(|S cap S'|,3). With k >= 5 and sum k = 890 one gets sum_Y C(k,2) >= 1975 (from 100 triples with k = 5 and 65 with k = 6, sum C(k,2) = 1000 + 975). But C(x,3) is convex, so first moments of the intersection sizes (sum over pairs of |S cap S'| = sum_u C(25+j_u,2) = 3643 + sum j^2/2) give only a LOWER bound on sum C(x,3). An upper bound would need a cap on intersections, and blocks can coincide (|S cap S'| = 6). **Dead** without further structure.
* **DE2, pure counting.** Every first-moment identity was checked and holds: sum Ex = 195 = 3*65, sum_v s(u,v) = 2 Ex(u) = 10 + 20 j_u, sum over pairs of s = 195, sum over pairs of delta = 35 = (5 * 14)/2. The doubly regular case (L6) satisfies all of them with excess 65 spread. **No contradiction from counting in R.**
* **DE3, spectral.** Let A be the adjacency matrix of T[R] and B the 39 x 11 block-incidence matrix. Then X := A^T A + B^T B has off-diagonal entries D_uv and diagonal 25 + j_u, so X = 12 J + diag(13 + j) + Delta with Delta >= 0 symmetric, zero diagonal, row sums 5 j. X 1 = (145 + 6 j) checked. No contradiction found in the eigen-check. Not pursued further (the triple-level constraint is stronger than any quadratic form on pairs).
* **DE4, links at V_0 vertices.** For u in V_0 the link has 5 quadruples O_w \ u (w in N^-(u)) and 20 quintuples M_y \ u, each point v of R minus u lies in 12 link sets, and the link's pair-excess at v is 3 - c_uv >= 0. Consistent, with no contradiction at this level. Only the DRT case gives the sharp matching structure of L6(b).
* **DE5, the naive mod-4 argument.** s(u,v) ≡ 3 - c_uv (mod 4) (L5a) is consistent with everything; it gives no parity obstruction because c_uv is free in {0,...,4} for non-DRT tournaments, and in the DRT case s = 1 + 4 delta is only a constraint on pair-degrees of the excess hypergraph.

## L9. Verdict on the primary target (h = 0)

**Not decided.** I could not exclude the branch h = 0 (J = 14, every y in O is a 5-vertex with t_y = 6, all triple excess sums to 65) by hand. Everything proved is consistent with it:
* every counting identity (I), (II), (PS), (S), (B), Ex, mod-4 pair identity holds;
* the doubly regular case T[R] = QR_11 with the 11 complement blocks is consistent with all counting, and reduces to the conditional residual problem of L6(d): 28 six-subsets of an 11-set that 3-cover the triples, with point degrees 14 + j_u, plus the matching structure at V_0.

Status for the report: branch h = 0 OPEN. Nothing is proved_by_hand that excludes it. Anything I would call a survivor is labelled "not excluded by the stated counts".

## L10. Hand checks of the numbers (second pass)

1. C(6,3) = 20, so 39 * 20 = 780 and 780 - 715 = 65. OK.
2. 165 * 5 = 825, 825 - 110 = 715. OK.
3. 11 * C(5,3) = 110, 11 * C(5,2) = 110. OK.
4. C(11,2) = 55, 55 * 12 = 660, 695 - 660 = 35. OK.
5. Sum over u of (25 + j_u) = 275 + 14 = 289 = 11*5 + 39*6 = 55 + 234 = 289. OK.
6. Deficits: C(6-t,3) for t=3: C(3,3)=1, deficit 19; t=4: C(4,3)=4, deficit 16; t=5: C(5,3)=10, deficit 10. OK.
7. Biplane counts for DRT(11): n_0 = 2 - x, n_1 = 3 + 3x, n_2 = 6 - 3x, n_3 = x; sum = 11 and sum C(i,2) n_i = (6-3x) + 3x = 6 ✓; sum i n_i = (3+3x) + 2(6-3x) + 3x = 15 ✓.
8. Residual requirement 5 - x - (2 - x) = 3, constant. OK. Residual excess 28*20 - 3*165 = 560 - 495 = 65 ✓.
9. Residual pair count 7 + delta: m_uv = 10 + delta; complement pair count 3 (from 11 - (5+5-2)); 10 + delta - 3 = 7 + delta ✓.
10. 14 * 10 = 140 = 45*3 + 5. Per point: 4*7 - 9*3 = 28 - 27 = 1 ✓.

## L11. Use of full S_4 (flagged): every pair of R has a common in-neighbour in R (c_rr' >= 1)

Assume S_4 (every 4-set has a dominator). Take r != r' in R and the 4-set Z = {a, b, r, r'}. A dominator w of Z beats a and b, so w lies in D(P) = R by definition of R. It beats r and r', so w is in R minus {r, r'} and beats both. Hence c_rr' >= 1. QED. This uses S_4 only, not F1. Consequence with L5a: a pair with c_rr' = 1 has s(r,r') ≡ 2 (mod 4) and s >= 2.

Status: proved_by_hand under S_4 (flagged). Not used in L1-L10.

<!-- END -->

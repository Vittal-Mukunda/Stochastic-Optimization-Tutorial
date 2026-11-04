# Erdos #902: synthesis of rounds 1 and 2 (lead, 24 Oct 2026)

Written by the lead from the lane files in this folder. It lists what was verified, what is still open, what was corrected, and what round 2 added. Nothing here is a new closed result. Lane claims from round 2 have **not** been independently audited unless section 4 says so.

## 0. Bottom line

- **f(4) >= 52 stands.** The chain in [52] and [EP] was re-verified line by line in `r1_AUDIT-51.md` and `r1_AUDIT-52-B.md`. Only (F1) is used.
- **T1 (f(4) >= 53, no S_4 tournament on 52 vertices) is still OPEN.** Rounds 1 and 2 closed no case. The tight-pair case reduced to explicit survivors. The no-tight-pair case is not closed.
- **Literature (`r1_LIT.md`):** nothing public pre-empts f(4) >= 52. Best public lower bounds: 47 (Szekeres-Szekeres 1965), 48 (Wilder, Lean, unrefereed), 49 (conditional, computer-assisted). Upper bound 67 (QR_67).
- **Open question about the method:** all arguments so far use only (F1) (every triple has at least 5 dominators). Nobody has checked whether an F1-tournament on 52 vertices exists. If one does, T1 needs full S_4. Round 2 lane R2-CASEB flags this: it uses a 4-set fact that needs full S_4.

## 1. Verified by hand in round 1 (auditors: r1_AUDIT-51, r1_AUDIT-52-B)

| item | statement | where |
|---|---|---|
| Chain of [52] | every S_4 tournament on <= 51 vertices has a triple with <= 4 dominators; f(4) >= 52 | AUDIT-51 sec 1-3 |
| SF | any N, tight pair P, dominator r of P with d-(r) = 25: every y outside P u R with y -> r has q_y = 5; c(r,v) <= 3; D({r,v}) = 12 for all v in R | AUDIT-51 sec 4; AUDIT-52-B sec 3 |
| Theorem 1' | any N, every tight pair has J >= 3 | AUDIT-51 sec 5 |
| Lemma B | no in-degree 23 at N = 52 | AUDIT-51 sec 8 (AUDIT-52-B sec 6.2 self-audit) |
| D >= 12 inside R | for a tight pair P, every pair inside R = D(P) has \|D\| >= 12 | AUDIT-52-B sec 2(b) |
| tau inequality | for a tight pair at N = 52, tau_u <= 5 j_u for every u in V_+ | AUDIT-52-B sec 7.1 |
| Lemma C (uniform) | every tight pair has s = \|V_+\| >= 4; invariant nu_u = j_u - m_u with sum over V_+ equal to 14 - 6h | AUDIT-52-B sec 4.3 |
| J >= 5 | every tight pair at N = 52 has J >= 5 (J = 4 killed by a complete case list) | AUDIT-52-B sec 5.2 |

## 2. Survivors: what a tight pair must still look like (AUDIT-52-B sec 8)

- Counting at the level of (E), (PS), (S), (B) and the invariant leaves **four J = 5 configurations**: (s=4) 6+3 with j = 2 on a vertex beaten by the q = 8 vertex; (s=5) 6+3, 6+2+1, 6+1+1+1.
- **Branch h = 0 (J = 14)**: every outside vertex is a 5-vertex. Not excluded by round 2 (see section 6).
- J >= 6 has not been examined case by case.

## 3. Case A: no tight pair (open)

- Claim Q says every vertex with e = -1 lies in >= 12 tight pairs. So with no tight pair, e(v) >= 0 for all v, and sum e = 26.
- F2 gives \|D(P)\| >= 12 for every pair.
- The head identity gives sum over pairs of (D_P - 12) = 325 + S2/2 (S2 = sum e^2 >= 26).
- Round 2 (`r2_CASEA.md`, not audited) proved the tail identity, the 12-regular in-neighbourhood at e = 0 vertices, and a score window in the balanced sub-case. It did not show Case A impossible.

## 4. Round-1 claims after the round-2 audit (`r2_AUDIT.md`)

**Verified (by hand, by the round-2 auditor):**
- NT-B01 (`r1_DUAL.md` sec 6): no tournament on 52 vertices has all in-degrees in {25,26} and all pair counts in {12,13}.
- Lemma Theta (`r1_DUAL.md` sec 3): the values r_L, M(L), Theta(L) for L = 10..16, the closed form Theta(L) = 20 + 5z + C(z,2) + 2C(z,3) (z = L - 10), and the summed inequality A3 <= sum Theta(L_Y) - 10 a2 + 70 a1.
- Lemma Delta and Lemma Sigma (`r1_NO-Z.md` sec 2-3), including the closed forms for sum X^2.
- `r1_MOM-EXACT.md` A.3 (totals 254163 + 24.5 S2, expansions of 6C(26-e,3) and 6C(25+e,3)) and the pair identity V1.
- `r1_MOM-BALANCED.md` Lemmas 2.1-2.2, the STAR identity (3.2), Propositions 4.1(a)-(c), 4.2, 4.3 (conditional on the chain (3.3)-(3.6), which was re-derived).

**Conditional:**
- f(A_b) >= 3 for b in B_0 (`r1_NO-Z` sec 3) needs J >= 5, which comes from AUDIT-52-B sec 4.3 and 5.2.
- The tight-pair partition analysis (AUDIT-52-B 5.2) uses the formulas (E), (PS), (S), (B), Ex, c <= 4, which the round-2 audit did not re-derive.

**FLAWED (corrections to the record):**
- **F1** (`r1_MOM-BALANCED` sec 5, bullet 2): the statement "(5.1) forces E_tail > 0 or S2 >= 346 (take eta = ex = 0)" is wrong. With eta = ex = 0 the pair counts are forced: S2 = 338 exactly, and (5.1) then gives E_tail >= 520. The correct general inequality is 520 + 2 ex <= 147 eta + 69 G + E_tail, where G = sum over G->H arcs of x(x - 1).
- **F2** (`r1_MOM-BALANCED` sec 4, and repeated in sec 5): "sum d^2 = 13 forces N^- >= 9, hence eta >= 9" is not supported. The proved bound gives N^- >= (169 - sum d^2)/25 = 156/25, so N^- >= 7 and eta >= 7.
- **F3** (`r1_NO-Z` sec 6, Lemma 6.4): "at least 78 - 12E pairs of A lie in no common tight set" is valid only when f and m are 0/1-valued. In general the step needs an upper bound on Theta.
- **F4** (typo, `r1_MOM-BALANCED` sec 3.6): the L = 11 and L = 12 factorizations have the wrong sign. The correct forms are g(u) - 1/4 = -(2/3)(u+1/2)(u-1/2)(u-3/2) and g(u) - 1 = -(1/3)(u-1)(u+1)(2u-3). Values of lambda are unaffected.

**Not checked by the round-2 audit (do not rely on without re-deriving):** `r1_DUAL.md` sections 1, 2 (beyond the moment set used by Lemma Theta), 4, 5 (including the IB-min impossibility and the n <= 1625 bound), and 7; `r1_MOM-BALANCED.md` sections 1 and 6; `r1_AUDIT-52-B.md` sections 6.1, 7, 8 (self-audited only).

## 5. Corrections and withdrawn statements (from round 1)

- **Claim L is false** (`[EP]` sec 8.2; realisation in `ai-debate/claim_l_intersect.py`, verified). Stands.
- `[TP]` sec 9 (old proof of Lemma C): superseded by AUDIT-52-B sec 4.3. Its J = 3, 4, 5 sections are right in conclusion but garbled: the stray "5+3+3" bullet in the J = 4 list, the missing 5+5 case (now done in AUDIT-52-B 5.2), and the "11 dominators" in the 5+5 row of the s = 4 table (the true value is 17).
- `[TP]` Lemma A: the m(v) slip is repaired in AUDIT-52-B sec 3. The argument holds at every order.
- `[52]` sec 2 closing paragraph had a gap; filled by Proposition SF (AUDIT-51 sec 4).
- Literature attribution: Graham and Spencer (1971) only say "it is possible that T_67 is also minimal"; they state no conjecture (`r1_LIT.md` sec 2). Bozoki and Jeffries phrase it more strongly.

## 6. Round 2 (workflow `wf_64c5193d-2ef`, three lanes at effort high, lane reports not audited)

**R2-CASEA (Case A, no tight pair): partial.** File `r2_CASEA.md`.
- Proved by the lane: tail identity (for each v, the sum over b in N+(v) of x_{vb} = (26-e(v))(e(v)-1)/2 + sum of e(b) over N+(v)); head identity; in Case A with e(v) = 0, T[N^-(v)] is 12-regular on 25 vertices; in the balanced sub-case (all e in {0,1}), the score window sum over V_1 of f^2 in [4225, 4381].
- Dead ends recorded: the H-count inside N^-(v) and the O-count inside N^+(v) give only lower bounds with room; the cyclic-triple total is consistent for every S2.
- Case A impossibility: **conjectural, not proved.**

**R2-CASEB (tight pair, branch h = 0): partial.** File `r2_CASEB.md`.
- Identity (I), checked here: sum over Y inside R of (k(Y) - 5) = sum over y of C(t_y,3) - 715, so sum over y of (20 - C(t_y,3)) = 65 - sum over Y of (k - 5) <= 65.
- Identity (II): sum over the 55 pairs of R of D_uv = 110 + sum over y of C(t_y,2). In branch h = 0 this gives sum of (D - 12) = 35.
- Identity (I) kills **none** of the four J = 5 survivors. Heavy-vertex deficits: 39 (6+3, s=4), 39 (6+3, s=5), 46 (6+2+1), 50 (6+1+1+1), against the bound 65. It kills the partitions 2+2+2+2+1, 2+2+2+1+1+1 and 1^9 (deficits 74, 78, 90).
- Branch h = 0 is **not excluded.** The sub-case T[R] = QR_11 reduces to a conditional 3-cover question: can 28 six-subsets of an 11-set cover each triple of R exactly three times with point degrees 14 + j_u? This is conditional, not proved.
- Lane claim L11 uses full S_4 (not F1 alone): every pair of R has a common in-neighbour inside R.

**Round 2 status:** no tight pair or Case A configuration is excluded. The synthesis finds no contradiction in any branch.

## 7. Round 2 next-round proposal (superseded by round 3, section 8)

1. Settle the F1-only question first.
2. Branch h = 0 as a finite design problem on an 11-set, with the QR_11 sub-case as the first test.
3. Balanced Case A with the score window and the internal weights y = x - 1.
4. Do not use the H-count or O-count (`r2_CASEA` dead ends) as a closing argument.

## 8. Round 3 (workflow `wf_c186bc80-3af`, three lanes, each audited)

**Outcome: all three lanes undecided. No case of T1 is closed.**

**R3-F1EXIST (`r3_F1EXIST.md`): undecided.** Decides nothing about existence of an F1-tournament on 52 vertices.
- Verified (auditor, by hand): in a balanced-degree F1 tournament some triple has k >= 8. Proof: if all k lie in [5,7], then sum k^2 <= 12 M1 - 35*22100, so 2 M2 <= 11 M1 - 773500 = 627900, but 2 M2 >= 628056.
- Verified: every F1 tournament on 52 has d+(v) >= 3 for every v (if d+(v) <= 2, T - v is F1 on 51, which the N <= 51 chain excludes).
- Refuted: an interval-type Z_17 candidate (a triple with k = 0).
- **Auditor overclaim:** the moment test excludes nothing on its own. It constrains only profiles with support in [5,7].
- **Decisive fact:** whether an F1-tournament on 52 vertices exists. Existence would kill every F1-only proof of T1; nonexistence would already prove T1 (since F1 is weaker than S_4).

**R3-H0 (`r3_H0.md`): undecided.** Branch h = 0 (J = 14, all 39 outside vertices are 5-vertices) is not excluded.
- Verified: the setup; the out-sets of QR_11 form a symmetric 2-(11,5,2) design; an explicit V_0 link is consistent (H0-6).
- **Correction to round 2:** the QR_11 "3-cover" reduction (r2_CASEB L6) assumed the complements R minus O_w are among the blocks. That assumption is not implied by the setup, so the reduction is withdrawn as a general argument.
- **Caveat on H0-6:** the consistent V_0 link needs two vertices of O with identical M_y, which the setup does not forbid. Nothing forces this, and nothing rules it out.
- Auditor flaw (H0-5): the matching in the V_0 link need not consist of disjoint pairs. The statement is weakened accordingly.

**R3-BAL (`r3_BAL.md`): undecided.** Balanced no-tight-pair Case A.
- Verified: U + A = 338 (two routes), with 169 <= A <= 169 + 25N, where N = sum of |s| over s < 0; K = eta_T + eta_M <= 2 is impossible; K >= 3; E_tail = 0 whenever all x <= 1.
- **Auditor flaw (important):** the lane's K = 3 survivor analysis dropped the 2*ex term from the master inequality. Correct form: 520 + 2 ex <= 147 eta_T + 138 eta_M + E_tail, with 2 ex >= 22 Z_HH. Consequences: three x = 2 arcs force E_tail >= 145 (not 79); one x = 3 arc forces E_tail >= 147 (not 103); four x = 2 arcs (lane claimed consistent) force E_tail >= 20.
- **Still open:** the lane's crude bound E_tail <= 132 is unchecked. Until it is verified, K = 3 survivors are not excluded.
- Coefficient check: 138 = 2 * 69, consistent with G = 2 eta_M, so the corrected master inequality matches round 2's form.

**Process note:** the round-3 prompt pointed lanes to "F1-F4 in r2_AUDIT.md". Round-3 auditors could not find those labels in the file; the corrections are the ones in section 4. The round-3 audits found no dependence on withdrawn statements, except the one flaw above, which was a dropped term rather than a withdrawn item.

**Round 3 status:** no case closed. The decisive open fact is F1 existence on 52 vertices. The balanced no-tight case is the most concrete remaining target, and its survivors depend on the unverified tail bound.

## 9. Round 4 (workflow `wf_166863cb-003`, balanced no-tight case; lanes audited)

**Outcome: K = 3 pattern (A) is dead. Everything else in the balanced case is open. The master inequality cannot finish the case.**

**R4-MASTER (`r4_MASTER.md`): master verified.**
- Re-derived: 520 + 2 ex <= 147 eta_T + 138 eta_M + E_tail, with eps(14..18) = 2, 8, 20, 40, 70; Lambda <= Lambda_q for L <= 13; sum of X^2 = 48 S2 + sum of xi_v^2; sum of xi_v^2 = 17238; sum of L^2 = 2930876 + 46 S2.
- Sharper signed form: Lambda - Lambda_q = (L-11)(L-12)(L-13)/3 for all L >= 5. So E_tail can be replaced by the signed sum over all triples. That sum depends on the third moment of L, which is not yet controlled.
- Auditor corrections: (i) "eta_T = ex = 0 forces S2 = 338" is false as stated. The correct statement is that ex = 0 forces eta_M = 0 (f_G(x) > 0 for x >= 2), and then S2 = 338 + 2 eta_T. The round-1 bullet "E_tail > 0 or S2 >= 346" is fine as stated. (ii) The Prop 4.3 constants (36536, 2450) are not checked, and its impossibility claim for eta = 0 is **not established**: it needs an upper bound on the non-special tail, which is not supplied.

**R4-K3 (`r4_K3.md`): pattern (A) dead; pattern (B) open.**
- Pattern (A) (three x = 2 pairs), requirement 178 - 11t with t = number of T-arcs: 178 (all M), 167, 156, 145 (all T). Killed for every T/M mix and every intersection shape by crude counting of tail triples. Auditor verified each kill; the t = 2 star margin is 4 (corrected from 8), and the M-T-T path is included with bound 146 < 156.
- Threshold correction: E_tail is nonzero already when t_Y >= 1 (not >= 2). A single M-arc can give L = 14 in a cyclic triple with a V0 vertex.
- Pattern (B) (one x = 3 pair): requirement 147 (T-arc, two forced zeros) or 180 (M-arc). The lane's crude tail totals (270, 240) are **not valid upper bounds** (they omit eps = 2 classes). Open.

**R4-K4 (`r4_K4.md`): undecided.**
- Requirements for K = 4: TTTT 20, T3+T2 22, TTTM 31, T3+M2 33, TTMM 42, TMMM 53, T2+M3 55, MMMM 64, M3+M2 66. Four T-arcs with x = 2 need E_tail >= 20, and a single T-arc can contribute up to about 25. So this is not killed.
- Auditor: the lane's per-arc tail bounds are not valid as stated (an omitted family of M-arc triples; a multi-heavy-triple bound that is false, e.g. a cyclic triple with e = 20). The conclusion "not killed" stands, but the totals are not established.

**Key structural finding (lead).** The master inequality is a lower bound on defects, not an upper bound. Its requirement is R = 520 + 2 ex - 147 eta_T - 138 eta_M. Examples:
- Five T-arcs with x = 2 give ex >= 55 (five forced zeros), so R <= 520 + 110 - 735 = -105 < 0. The master is satisfied with no tail at all.
- A single T-arc with x = 3 gives R = 147, and two of them already make R negative.

So the master cannot exclude any configuration with enough defects, which is the same weakness round 3 saw from the other side. Closing the balanced case needs a different constraint: an upper bound on the defect profile, or a third-moment identity for the tail. More tail counting alone will not do it.

<!-- END -->

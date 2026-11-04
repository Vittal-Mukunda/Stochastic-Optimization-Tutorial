# r1_NO-Z: vertices of in-degree 24 at N = 52 (lane NO-Z)

*Hand derivations only, 24 Oct 2026. Citations: [EP] ERDOS902_PROOF.md, [52] F4_GE_52_HAND_PROOF.md, [A52] N52_ATTEMPT.md, [TP] N52_TIGHT_PAIRS.md, audits r1_AUDIT-51.md, r1_AUDIT-52-B.md. Only (F1) is used (every triple has >= 5 dominators).*

## Status (keep current)

* Section 1: exact set-system set-up around a vertex v with d^-(v)=24 (the 51 sets A_x = D({v,x}) in the 24-set A). Proved.
* Section 2: Lemma Delta (an exact second-moment identity for a tight pair {x,v}, x in A). Proved. Gives: F_x <= 6, and "twin" structure when F_x <= 2.
* Section 3: tight pairs {v,b} with b in B: f(A_b) >= J_b - 2 >= 3. Proved.
* OPEN: full exclusion of Z. (updated below as work proceeds)

## 0. Notation

N = 52, T an F1-tournament. By [A52] Lemma 1 (audited, r1_AUDIT-51 section 8) every in-degree is >= 24, so e >= -1 everywhere; e(w) = d^-(w) - 25, d^+(w) = 26 - e(w), sum_V e = 26.
Fix v with d^-(v) = 24 (so e(v) = -1). A = N^-(v), |A| = 24; B = N^+(v), |B| = 27.
For x != v put A_x := A ∩ N^-(x) = D({v,x}) (vertices beating both v and x; for x in A this is the set of in-neighbours of x inside T[A]).
a_x := |A_x| >= 11 (F2). For x in A write a_x = 11 + f_x, f_x >= 0. For b in B write a_b = 11 + m_b, m_b >= 0.
E := sum_{w in A} e(w), E_B := sum_{b in B} e(b). Since sum_V e = 26 and e(v) = -1: **E + E_B = 27**.
L := {x in A : f_x = 0}; for x in L the pair {x,v} is tight with dominator set R_x = A_x. B_0 := {b in B : m_b = 0}; for b in B_0 the pair {v,b} is tight with dominator set A_b.
Lemma T: every dominator of a tight pair has in-degree >= 25, i.e. e >= 0. Theorem [TP]/audits: every tight pair has J = sum_{R} e >= 5 and at least 4 dominators with e >= 1.

## 1. Exact set-system identities (all proved here)

**(S1)** For distinct x, y, both != v: |A_x ∩ A_y| = |D({v,x,y})| >= 5 (F1). For w in A and x != v, w: w in A_x iff w -> x.
**(S2)** A vertex w in A lies in exactly d^+(w) - 1 = 25 - e(w) of the 51 sets A_x (the out-neighbours of w other than v).
**(S3)** sum_{x in A} a_x = C(24,2) = 276 = 24*11 + 12, so sum_A f = 12; at most 12 vertices have f > 0, hence |L| >= 12. For w in A: d^-_A(w) = 11 + f_w, d^+_A(w) = 23 - 11 - f_w = 12 - f_w.
**(S4)** Arc count A -> B: w in A beats 26 - e(w) vertices; of these 1 is v and 12 - f_w lie in A, so w beats 13 - e(w) + f_w vertices of B. Hence
 sum_{b in B} a_b = sum_w (13 - e(w) + f_w) = 312 - E + 12 = 324 - E, and sum_b m_b = 324 - E - 27*11 = 27 - E = E_B.
 (So sum_b m_b = E_B = sum_B e. In particular E <= 27.)
**(S5)** The number of b in B with m_b >= 1 is at most sum m_b = 27 - E, so |B_0| >= E. Therefore the number of tight pairs through v is |L| + |B_0| >= 12 + E.
**(S6)** Z-vertices in A: if z in A has e(z) = -1 (d^-(z) = 24), then z is not a dominator of any tight pair (Lemma T). Since R_a ⊂ A for a in L, z not in R_a, i.e. a -> z for all a in L \ {z}. So d^-_A(z) = 11 + f_z >= |L \ {z}|.
 [Consequence: if z in A ∩ Z then |L \ {z}| <= 11 + f_z.]

(Check of S3/S4 once more: arcs of T[A]: C(24,2) = 276, in-degree sum 24*11 + sum f = 264 + 12 = 276 OK so sum f = 12. Out-degree of w in T[A]: 23 - (11 + f_w) = 12 - f_w. Out-degree of w in T total: 51 - (25 + e) = 26 - e. Minus v minus 12 - f_w gives 13 - e + f_w in B. OK. Sum over 24 vertices: 312 - E + 12 = 324 - E. Each b has a_b >= 11: 27*11 = 297; 324 - E >= 297 gives E <= 27. OK.)

## 2. Lemma Delta: second-moment identity for a tight pair {x,v}, x in L

Let x in L, R := R_x = A_x (|R| = 11, T[R] is 5-regular by F2/tightness), N^+ := N^+_A(x) (|N^+| = 23 - 11 = 12). For a in N^+ let q_a := |R ∩ N^-(a)| = |A_x ∩ A_a| >= 5 and X_a := q_a - 5 >= 0 (X_a <= 6). F_x := sum_{r in R} f_r.

**Lemma Delta.** (i) sum_{a in N^+} X_a = 6 - F_x, in particular F_x <= 6. (ii) sum_{a in N^+} X_a^2 = 36 - 11 F_x + 2 Delta_x, where Delta_x := sum_{s<s' in R} (|D({v,s,s'})| - 5) >= 0. Hence sum X_a^2 >= 36 - 11 F_x.
(iii) Consequently: F_x = 0 => exactly one a has X_a = 6 (and the others 0); F_x = 1 => exactly one a has X_a = 5; F_x = 2 => exactly one a has X_a = 4 (Delta_x = 1). For F_x >= 3 nothing is forced.

*Proof.* (i) r in R has d^+_A(r) = 12 - f_r (S3). Its out-neighbours in A: 5 inside R (5-regular), x itself (r -> x because r in R_x), and the remaining 12 - f_r - 6 = 6 - f_r in N^+. So the number of arcs R -> N^+ is sum_r (6 - f_r) = 66 - F_x, and this equals sum_a q_a. Since q_a >= 5 for the 12 vertices a, 66 - F_x >= 60 and sum X_a = 66 - F_x - 60 = 6 - F_x.
(ii) For s != s' in R, |D({v,s,s'})| = |A ∩ N^-(s) ∩ N^-(s')| = number of w in A with w -> s and w -> s'. So sum_{s<s'} |D({v,s,s'})| = sum_{w in A} C(n_w, 2), n_w := |N^+(w) ∩ R|. Now: w in R: n_w = 5 (5-regular), 11 such w, contribution 11*10 = 110. w = x: n_x = 0 (R beats x), contribution 0. w in N^+: n_w = 11 - q_a = 6 - X_a. So the sum is 110 + sum_{a} C(6 - X_a, 2). The left side is 5*C(11,2) + Delta_x = 275 + Delta_x. With C(6 - X, 2) = (30 - 11X + X^2)/2 and 12 terms:
 275 + Delta_x = 110 + 180 - (11/2) sum X + (1/2) sum X^2 = 290 - (11/2)(6 - F_x) + (1/2) sum X^2.
 Multiply by 2: 550 + 2 Delta_x = 580 - 66 + 11 F_x + sum X^2, so sum X^2 = 36 - 11 F_x + 2 Delta_x. (Check: 580 - 66 = 514; 550 - 514 = 36. OK.)
(iii) sum X^2 <= (sum X)^2 = (6 - F)^2 for nonnegative integers, with equality iff at most one nonzero term. F = 0: 36 <= sum X^2 <= 36, so equality: one X = 6. F = 1: sum X^2 >= 25 and <= 25: one X = 5. F = 2: sum X = 4, sum X^2 >= 14; partitions of 4 have sum of squares 16 (4), 10 (3+1), 8 (2+2), 6, 4: only (4) works; then 16 = 14 + 2 Delta, Delta = 1. ∎

*Interpretation.* If F_x <= 2 the tight pair {x,v} has a 'twin' a in N^+_A(x) with q_a = 11 - F_x, i.e. a beats only F_x vertices of R and contributes 6 - F_x to the excess budget sum_{y in O}(q_y - 5) = 14 - J_x of (E)/[TP]. [For F_x = 0: a is beaten by all of R and by x, so R_a ⊇ R ∪ {x}.]

**Budget split for x in L.** [TP] (E): sum over all y outside {x,v} ∪ R of (q_y - 5) = 14 - J_x. y ranges over N^+ (12 vertices) and B (27 vertices). The N^+ part is 6 - F_x. Hence the B part is
 sum_{b in B} (|A_b ∩ R| - 5) = 8 - J_x + F_x >= 0.
(Direct check: sum_b |A_b ∩ R| = sum_{r in R} (13 - e(r) + f_r) = 143 - J_x + F_x (S4); minus 5*27 = 135 gives 8 - J_x + F_x. OK.)
So J_x <= 8 + F_x <= 14 for every x in L.

## 3. Uniform second-moment identity for ANY set A_y (not only tight), and tight pairs {v,b}, b in B

**Lemma Sigma.** Let y != v and S := A_y, s := |S| = 11 + m, g := f(S) = sum_{w in S} f_w, Delta_S := sum_{w<w' in S} (c^-(w,w') - 5) >= 0 where c^-(w,w') = |D({v,w,w'})| = |A ∩ N^-(w) ∩ N^-(w')| (>= 5 by F1). For a in A put X_a := |S ∩ R_a| - 5 where R_a = N^-_A(a) = A_a. (X_a >= 5-5 = 0 by (S1) when a != y; if y in A and a = y then X_y = s - 5 >= 6.) Then
 (a) sum_{a in A} X_a = 12 s - g - 120;
 (b) sum_{a in A} X_a^2 = 6 s^2 - 114 s + 600 + (11 - 2s) g + 2 Delta_S.
*Proof.* (a) sum_a |S ∩ R_a| = sum_{w in S} d^+_A(w) = sum_{w in S}(12 - f_w) = 12 s - g; subtract 5*24 = 120.
(b) sum_a |S ∩ R_a|^2 = sum_{w,w' in S} #{a in A : w -> a, w' -> a} = sum_{w in S}(12 - f_w) + 2 sum_{w<w'} c^+(w,w'), c^+ = common out-neighbours inside A. For w -> w' (w != w'): the 22 other vertices of A split as: in-in c^-, out-out c^+, and the mixed ones; #{u -> w} = 11 + f_w, #{u -> w'} = 11 + f_w' - 1 (w itself is an in-neighbour of w'), so c^+ = 22 - (11 + f_w + 10 + f_w' - c^-) = 1 + c^- - f_w - f_w' (check: 22 - |X ∪ Y| with |X ∪ Y| = (11+f_w) + (10+f_w') - c^-; X = N^-(w) which does not contain w', Y = N^-(w') \ {w}.) So
 sum_a |S∩R_a|^2 = 12 s - g + 2 sum_{w<w'} (c^- + 1 - f_w - f_w') = 12 s - g + 2(5 C(s,2) + Delta_S) + s(s-1) - 2(s-1) g = 12 s + 6 s(s-1) - (2s - 1) g + 2 Delta_S.
 Then sum X^2 = sum |..|^2 - 10 sum |..| + 25*24 = 12 s + 6 s(s-1) - (2s-1) g + 2Delta_S - 10(12 s - g) + 600 = 6 s^2 - 114 s + 600 + (11 - 2s) g + 2 Delta_S. (12 s - 6 s - 120 s = -114 s. OK.) ∎
For s = 11: sum X = 12 - g, sum X^2 = 72 - 11 g + 2 Delta_S. (6*121 = 726; 114*11 = 1254; 726 - 1254 + 600 = 72.)

**Tight sets.** If s = 11 (so y in L or y in B_0), T[S] is 5-regular so X_a = 0 for a in S and the 13 vertices a in A \ S carry all of it:
 sum_{a in A\S} X_a = 12 - g, sum_{a in A\S} X_a^2 = 72 - 11 g + 2 Delta_S >= 72 - 11 g. (For y = x in L this includes a = x with X_x = 6, consistent with Lemma Delta.)
**Near-twin lemma.** Since X_a <= 6, sum X^2 <= (max X)(sum X), so for a tight set S with g = f(S) <= 6 we get max_a X_a >= (72 - 11 g)/(12 - g), i.e. max X >= 6, 5.5, 5, 4.33, 3.5, 2.43, 1 for g = 0..6; as X is an integer: **max X >= 6 (g=0), 6 (g=1), 5 (g=2), 5 (g=3), 4 (g=4), 3 (g=5), 1 (g=6)**; for g >= 7 no constraint (72 - 77 < 0).
 [Details: g=1: need >= 61/11 = 5.545, so 6; g=2: 50/10 = 5; g=3: 39/9 = 4.33, so 5; g=4: 28/8 = 3.5, so 4; g=5: 17/7 = 2.43, so 3; g=6: 6/6 = 1.]
 So (for a in A \ S with X_a >= 5) S is almost contained in the in-neighbourhood R_a: |S ∩ R_a| >= 10, i.e. a beats at most one vertex of S.

**Tight pairs {v,b}, b in B_0.** Let S = A_b, J_b = e(S) >= 5 [TP]. The budget (E) of [TP] for P = {v,b} reads sum_{y not in P ∪ S}(|A_b ∩ A_y| - 5) = 14 - J_b. The y's are the 13 vertices of A \ S (total 12 - g by the above) and the 26 vertices b' in B \ {b}. For the latter: sum_{b'} |S ∩ A_{b'}| = sum_{w in S}(#b' != b, w -> b') = sum_{w in S}(13 - e_w + f_w - 1) = 132 - J_b + g, minus 5*26 = 130 gives 2 - J_b + g. Hence
 **f(A_b) = g >= J_b - 2 >= 3 for every b in B_0.** (Check: (12 - g) + (2 - J_b + g) = 14 - J_b. OK.)

**Pair-excess at a vertex.** For any z in A: eps_z := sum_{a in A, a != z}(c^-(a,z) - 5) = sum_{w in R_z}(d^+_A(w) - 1) - 5*23 = sum_{w in R_z}(11 - f_w) - 115 = 11(11 + f_z) - f(R_z) - 115 = **6 + 11 f_z - f(R_z) >= 0**. For z = x in L this is 6 - F_x (matches Lemma Delta (i)). Summing: sum_z eps_z = 2 Gamma, Gamma := sum over the 276 pairs of A of (c^- - 5) = 66 + (sum f^2)/2 (also from sum_x C(11 + f_x, 2) = 1446 + (sum f^2)/2 minus 5*276 = 1380).

## 4. Bridge lemma (from Proposition SF, audited in r1_AUDIT-51.md section 4)

Z_0 := {r in A : e(r) = 0}. T := L ∪ B_0 = the set of x != v with {v,x} tight (so |A_x| = 11). W := {r in A : e(r) >= 1} (heavy).

**Bridge Lemma.** Let r in Z_0, x in T with r -> x (i.e. r in A_x). Then for EVERY y in N^-(r) (y in A or in B; note v is not in N^-(r)) one has |A_x ∩ A_y| = 5.
*Proof.* P = {x,v} is tight with D(P) = A_x and r in D(P) has d^-(r) = 25. Proposition SF: every y outside P ∪ D(P) with y -> r has q_y = |D(P) ∩ N^-(y)| = 5. Now y in N^-(r) is not x (r -> x), not v (r -> v), so y lies in D(P) or outside P ∪ D(P). If y outside: q_y = |A_x ∩ N^-(y)| = |A_x ∩ A_y| (A_x ⊂ A) = 5. If y in D(P) = A_x: |A_x ∩ A_y| is the in-degree of y inside T[A_x], which is 5 (5-regular). ∎

Consequences (all for r in Z_0 and x in T ∩ N^+(r), "Q*_r := T ∩ N^+(r)"):
* (B1) for a in A with a -> r and x in Q*_r: c^-(a,x) = |D({v,a,x})| = 5.
* (B2) for b in B with b -> r (there are d^-_B(r) = 14 - f_r of them, see below) and x in Q*_r: |A_b ∩ A_x| = 5.
* (B3) A vertex y with |A_x ∩ A_y| >= 6 (y "big" for the tight pair {x,v}) must satisfy r in A_y, i.e. r -> y, for EVERY r in Z_0 ∩ A_x. So the excess of a tight pair {x,v} is carried only by vertices y that are beaten by all of Y_x := Z_0 ∩ A_x. (This is Lemma A of [TP] restated.)
(Counting d^-_B(r): d^-(r) = 25, in A it has 11 + f_r in-neighbours (r -> v so v is not one), hence 14 - f_r in B.)

**Z-vertices inside A.** z in A with e(z) = -1: z is in no A_x with x in T (Lemma T), so x -> z for all x in T \ {z}; as computed in (S6). In B: B_0 ⊂ N^-_B(z), and d^-_B(z) = 14 + e_z - f_z = 13 - f_z. Hence **if Z ∩ A != ∅ then |B_0| <= 13 and |L \ {z}| <= 11 + f_z**; with |B_0| >= E (S5): E <= 13.

## 5. The tight sets form a quasi-design; skew identity; moment identity

Recall T = L ∪ B_0 is the set of x != v with {v,x} tight, tau := |T| >= 12 + E (S5). For S = A_x (x in T) and a in A put X_a(S) := |S ∩ A_a| - 5 (= |S ∩ R_a| - 5 >= 0), where A_a = R_a = N^-_A(a).

**Lemma 5.1 (tight-in-A: exact intersections).** (a) If x in L and a in A \ {x} with a -> x, then |R_x ∩ R_a| = 5 (a lies in R_x, whose induced tournament is 5-regular, and R_x ∩ R_a is the in-neighbourhood of a inside R_x). (b) For distinct x, y in L, |R_x ∩ R_y| = 5 exactly. [Either y -> x or x -> y; apply (a).] (c) More generally for S = A_x tight and a in S: |S ∩ A_a| = 5; and if x, y in T with x in A_y or y in A_x then |A_x ∩ A_y| = 5. So excess |A_x ∩ A_y| - 5 > 0 for tight x,y requires x notin A_y and y notin A_x; for x in L this forces y in B_0 with y -> x, and for two elements of L it never happens.
Consequences: (i) X_a(R_x) = 0 for a in L, so the A-part 6 - F_x of Lemma Delta sits on Phi ∩ N^+_A(x) (Phi := {f > 0}); (ii) the ell := |L| sets R_x, x in L, are 11-subsets of the 24-set A meeting pairwise in exactly 5 points.

**Lemma 5.2 (clusters; from Bridge).** Let S = A_x, S' = A_y be tight (x,y in T) with |S ∩ S'| >= 6. Then Z_0 ∩ S = Z_0 ∩ S', so S Δ S' ⊂ W (heavy vertices). 
*Proof.* |S ∩ S'| >= 6 > 5 so by 5.1(c) x notin S', y notin S, and y is a vertex outside P_x ∪ D(P_x) with q_y >= 6. By Bridge (B3 in Section 4), every r in Z_0 ∩ S beats y (r in S'). So Z_0 ∩ S ⊂ S'; symmetrically Z_0 ∩ S' ⊂ S. Also Z-vertices (e = -1) are in no tight set (Lemma T). So S Δ S' consists of vertices with e >= 1. ∎

**Lemma 5.3 (skew identity).** Let S, S' be two 11-subsets of A each inducing a 5-regular tournament in T[A] (e.g. two tight sets). Then
 11 - |S ∩ S'| = sum_{a in S' \ S} X_a(S) + sum_{a in S \ S'} X_a(S'), where X_a(S) = |S ∩ R_a| - 5.
*Proof.* Put I = S ∩ S', i = |I|, S_1 = S \ I, S'_1 = S' \ I (|S_1| = |S'_1| = 11 - i). sum_{a in S'_1} |S ∩ R_a| = (number of arcs from S to S'_1) = arcs(I -> S'_1) + arcs(S_1 -> S'_1); likewise sum_{a in S_1} |S' ∩ R_a| = arcs(I -> S_1) + arcs(S'_1 -> S_1). Now arcs(S_1 -> S'_1) + arcs(S'_1 -> S_1) = (11 - i)^2 (S_1, S'_1 disjoint). Each w in I has exactly 5 out-neighbours in S and 5 in S' (5-regular); so arcs(I -> S_1) = 5i - C(i,2) = arcs(I -> S'_1) (the C(i,2) arcs inside I are counted once as out-arcs of I). Therefore the right side equals (11-i)^2 + 2(5i - C(i,2)) - 5*2(11 - i) = 121 - 22i + i^2 + 10 i - i^2 + i - 110 + 10 i = 11 - i. ∎
 (Check of the arithmetic: -22i + 10i + i + 10i = -i; 121 - 110 = 11. OK.)
 *Use.* For tight S, S' with |S ∩ S'| = 5, six units of excess must sit on points of the symmetric difference. If x in L and b in B_0 with x -> b, then x in A_b \ R_x carries X_x(R_x) = 6, so the identity gives |R_x ∩ A_b| = 5 and all other terms vanish (consistent with 5.1(c)).

**Lemma 5.4 (moment identity for the tight family).** Let t_a := #{S in T : a in S} = |N^+(a) ∩ T| for a in A. Then
 sum_a t_a = 11 tau and **sum_a t_a^2 = 5 tau^2 + 6 tau + 2 Xi_TT**, where Xi_TT := sum over unordered pairs {S,S'} of tight sets of (|S ∩ S'| - 5) >= 0 (Xi_TT = 0 if no two tight sets are 'clustered').
*Proof.* sum_a C(t_a,2) = sum_{S<S'} |S ∩ S'| = 5 C(tau,2) + Xi_TT. So sum t^2 = 5 tau(tau-1) + 2 Xi_TT + 11 tau = 5 tau^2 + 6 tau + 2 Xi_TT. ∎ (This only uses |S ∩ S'| >= 5; the exactness of 5 for most pairs is what makes it sharp.)
 Variance form: sum_a (t_a - 11 tau/24)^2 = 6 tau - tau^2/24 + 2 Xi_TT. [5 tau^2 - 121 tau^2/24 = -tau^2/24.]
 *Z-vertices in A*: a in Z ∩ A has t_a = 0 (S6). With 23 remaining points, Cauchy-Schwarz gives sum t^2 >= (11 tau)^2/23 = 5.2609 tau^2, hence 0.2609 tau^2 <= 6 tau + 2 Xi_TT, i.e. **if Z ∩ A != ∅ then tau <= 23 + 7.67 Xi_TT/tau.** (121/23 = 5.26087; 5.26087 - 5 = 0.26087; 6/0.26087 = 23.0; 2/0.26087 = 7.667.) With two Z-vertices in A: 22 points, 121/22 = 5.5 so 0.5 tau^2 <= 6 tau + 2Xi_TT, tau <= 12 + 4 Xi_TT/tau.

## 6. Fisher-type lemma for the tight family; popularity window; pair-coverage identity

**Lemma 6.1 (excess row sums).** For S = A_x, x in T: xi_S := sum over S' = A_y, y in T \ {x}, of (|S ∩ S'| - 5) satisfies xi_S <= 14 - J_x <= 9.
*Proof.* By (E) of [TP] (Section 1 there), for the tight pair {v,x}: sum over all y outside {v,x} ∪ A_x of (q_y - 5) = 14 - J_x, with q_y = |A_x ∩ A_y|; the y inside A_x contribute 0 (they have q = 5 by 5-regularity). All terms are >= 0, and the y in T \ {x} form a sub-sum. ∎

**Lemma 6.2 (Fisher-type bound).** Let T' ⊂ T be a set of tight vertices with xi_S < 6 for all S in T'. Then the characteristic vectors 1_S (S in T') are linearly independent in R^A; hence |T'| <= 24. In particular **#{x in T : J_x >= 9} <= 24**, and if tau = |T| >= 25 then at least tau - 24 tight vertices x have xi >= 6 (so J_x <= 8 and x is in a cluster in the sense of Lemma 5.2).
*Proof.* The Gram matrix of {1_S : S in T'} has diagonal 11 and off-diagonal entries |S ∩ S'| = 5 + c_{SS'}, c >= 0 (S1). So Gram = 6I + 5J + C' with C' symmetric, non-negative, zero diagonal, row sums <= max xi < 6. By Gershgorin every eigenvalue of C' is >= -(max row sum) > -6, so for u != 0: u^T Gram u >= 6|u|^2 + 0 + u^T C' u > 0 (J is PSD). So Gram is positive definite, the vectors are independent, and they live in R^24. For the last claim: J_x >= 9 gives xi <= 14 - 9 = 5 < 6 by Lemma 6.1. ∎

**Lemma 6.3 (popularity window).** Let t_a = |T ∩ N^+(a)| (number of tight sets containing a), tau = |T|, so sum_{a in A} t_a = 11 tau. For a in A define Lambda_a := sum_{S in T} (|S ∩ R_a| - 5) >= 0 (the sets S = A_y with y in T, y != a; for a in L the term S = R_a itself, with |R_a ∩ R_a| = 11, is included and contributes 6). Then
 Lambda_a = sum_{w in R_a} t_w - 5 tau = 6 tau - t_a - sum_{w in N^+_A(a)} t_w.
For a in L: 6 <= Lambda_a <= 6 + (14 - J_a) <= 20 - J_a <= 15, hence
 **6 tau - t_a - 15 <= sum_{w in N^+_A(a)} t_w <= 6 tau - t_a - 6   (a in L).**
*Proof.* Sum_{S}|S ∩ R_a| = sum_{w in R_a} #{S : w in S} = sum_{w in R_a} t_w. Since A = R_a ⊔ N^+_A(a) ⊔ {a}, sum_{R_a} t_w = 11 tau - t_a - sum_{N^+(a)} t_w. For a in L: S = R_a gives 6; other S in T with a in S give exactly 5 (5.1), the others give X_a(S) >= 0, and sum over all y != a of the excess is 14 - J_a (Lemma 6.1 argument). ∎

**Lemma 6.4 (pair-coverage identity).** For w != w' in A write D_{ww'} = |D({w,w'})| (>= 11). Then
 sum over the 276 pairs of A of (D_{ww'} - 11) = Theta := 178.5 + 12.5 E + (sum_A f^2 + sum_B m^2)/2  >= 198 + 12 E.
Moreover, by the audit r1_AUDIT-52-B Section 2, D_{ww'} >= 12 for every pair inside a tight set, and D = 12 when one of them lies in Z_0 (Proposition SF). So (cov + excess) <= Theta, where cov = number of pairs of A contained in some tight set. Hence at least 276 - Theta pairs are uncovered, i.e. **at least 78 - 12E pairs {w,w'} of A lie in no common tight set** (for f, m in {0,1}-valued minimal case).
*Proof.* D_{ww'} = #{u beating both}; sum over pairs = sum_u C(|N^+(u) ∩ A|, 2). For u in A, |N^+(u) ∩ A| = 12 - f_u; for u in B, = 24 - a_u = 13 - m_u; v beats no vertex of A. sum_{u in A} C(12 - f_u, 2) = sum (66 - 11.5 f + f^2/2) = 1584 - 138 + (sum f^2)/2 = 1446 + (sum f^2)/2. sum_b C(13 - m_b, 2) = sum (78 - 12.5 m + m^2/2) = 2106 - 12.5(27 - E) + (sum m^2)/2 = 1768.5 + 12.5E + (sum m^2)/2. Total 3214.5 + 12.5E + (sum f^2 + sum m^2)/2; subtract 11*276 = 3036. With sum f = 12, sum_B m = 27 - E (integers: sum f^2 >= 12, sum m^2 >= 27 - E) we get >= 178.5 + 12.5E + 19.5 - E/2 = 198 + 12E. ∎
 (Status: the coverage side is only a heuristic estimate (about 240-265 pairs covered for tau in 17..30 by Cauchy-Schwarz); the statement about uncovered pairs is a consequence only when combined with such a bound, so it is recorded as an inequality, not used further.)

<!-- END -->

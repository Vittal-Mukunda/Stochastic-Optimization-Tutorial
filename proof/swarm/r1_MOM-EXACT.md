# r1_MOM-EXACT: exact moment identities at N = 52

Lane MOM-EXACT. Hand derivations only. F1-tournament on 52 vertices: every triple has >= 5 dominators.

## Status (kept current)

- (started) file created; nothing proved yet.

## Plan

(a) re-derive L_Y and the universal identities; (b) classify what is fixed by degrees; (c) search for contradiction.

---

## A. The exact identities at N = 52 (general degrees and pair counts)

Notation. T tournament on 52 vertices (F1: every triple has k >= 5). For a vertex v, e(v) = d-(v) - 25, d+(v) = 26 - e(v),
sum_v e(v) = 26 (since sum d- = C(52,2) = 1326 = 52*25 + 26). For a pair P = {w,w'}: D_P = |D(P)| (vertices OUTSIDE P that beat both).
S2 = sum_v e(v)^2, S3 = sum_v e(v)^3. For a triple Y: k = |D(Y)|, k+ = |D+(Y)| (vertices outside Y beaten by all of Y),
sigma(Y) = 1 if Y transitive, 0 if cyclic.   a -> b means "a beats b".

### A.1 The sum L_Y = k + k+  (re-derived)

**Lemma A1.** For every triple Y = {y1,y2,y3} in a tournament on N vertices,
k + k+ = L_Y := N - sum_i d-(y_i) + sum_{i<j} D_{y_i y_j} - sigma(Y)   (formula (A1) below; N = 52 form (A1')).

Proof, general N (so that N = 51 and 52 are both checked). There are N-3 vertices outside Y. For outside w let S(w) be the set of y_i that w beats,
and n_j = #{w : |S(w)| = j}, so n_3 = k, n_0 = k+, n_0+n_1+n_2+n_3 = N-3.
(i) sum_i |N-(y_i) \ Y| = n_1 + 2 n_2 + 3 n_3. The left side is sum_i d-(y_i) - 3 (the three arcs inside Y give exactly 3 in-arcs to Y).
(ii) sum_{i<j} |D({y_i,y_j}) \ Y| = n_2 + 3 n_3. And |D({y_i,y_j}) \ Y| = D_ij - [y_l beats y_i and y_j] where l is the third index;
exactly one l has this property when Y is transitive (the source), none when Y is cyclic. So the left side equals sum D_ij - sigma(Y).
Put A = sum d-(y_i) - 3 and B = sum D_ij - sigma. Then n_3 = k, n_2 = B - 3k, n_1 = A - 2 n_2 - 3 n_3 = A - 2B + 3k,
n_0 = (N-3) - n_1 - n_2 - n_3 = (N-3) - A + B - k.   Hence
k + k+ = (N-3) - A + B = N - sum d-(y_i) + sum D_ij - sigma(Y).   (A1)
Check N = 51 with all d- = 25, D = 12: 51 - 75 + 36 - sigma = 12 - sigma. OK, matches [52] (M1).
At **N = 52**, with e_i = e(y_i):  L_Y = 52 - (75 + E_Y) + (36 + X_Y) - sigma = **13 - E_Y + X_Y - sigma(Y)**,
where E_Y = e(y1)+e(y2)+e(y3) and X_Y = sum_{i<j} (D_ij - 12).   (A1')  Equivalent form: L_Y = -23 - E_Y + sum D_ij - sigma.  QED

Note: every D_ij >= 11, so X_Y >= -3; sigma in {0,1}; e >= -1.

### A.2 Universal identities (each is a double count; N = 52 used for the numbers)

Write c_P := |N+(w) ∩ N+(w') \ {w,w'}| (vertices outside P beaten by both). Count the 50 vertices x outside P = {w,w'} by (a,b) = ([x->w],[x->w']):
n_11 = D_P, n_00 = c_P. Sum over x of ([x->w]+[x->w']) = d-(w)+d-(w') - 1 (the arc between w,w' gives one in-arc to P), = 2 n_11 + (n_10+n_01).
So n_10+n_01 = d-(w)+d-(w')-1-2D_P and c_P = 50 - D_P - (d-(w)+d-(w')-1-2D_P) = 51 + D_P - d-(w) - d-(w'), i.e.

**c_P = 1 + D_P - e(w) - e(w')**.   (A2)   [matches BRIEF section 4.]
Also n_01 = #{x : w->x, x->w'} = (d-(w') - [w->w']) - D_P. Define for an ORDERED pair (w,w') with epsilon = [w->w']:

**m(w,w') := |N+(w) ∩ N-(w') \ {w,w'}| = d-(w') - epsilon - D_P = 25 + e(w') - [w->w'] - D_P.**  (A3)

**Identities.**
* (I1) sum_Y k = sum_w C(d+(w),3) = sum_w C(26-e_w, 3).   [k(Y) = #{w : Y ⊆ N+(w)}]
* (I2) sum_Y k+ = sum_w C(d-(w),3) = sum_w C(25+e_w, 3).
* (I3) sum_Y C(k,2) = sum_{P} C(c_P, 3) = sum_P C(1 + D_P - e_w - e_w', 3).   [count (Y,{w,w'}) with Y ⊆ N+(w)∩N+(w')\{w,w'}]
* (I3') sum_Y C(k+,2) = sum_P C(D_P, 3).   [Y ⊆ N-(w)∩N-(w') \ P = D(P)]
* (I4) sum_Y k k+ = sum_{ordered (w,w')} C(m(w,w'), 3).   [w beats Y, Y beats w']
* (I5) sum_Y C(k,3) = sum_W C(k+(W),3).  [pairs (Y,W): every vertex of W beats every vertex of Y; for fixed Y, W ⊆ D(Y); for fixed W, Y ⊆ D+(W)]

Each triple/pair set above automatically excludes the named vertices, since D(Y) and D+(Y) are disjoint from Y and the counted sets are subsets of outside-vertex sets. QED (each is a direct count).

**Class-refined first moments (new; they use the tournament induced on N+(w) and N-(w)).**
* (I6) sum_{Y transitive} k(Y) = sum_{arcs w->x} C(c_{wx}, 2),  c_{wx} = 1 + D_wx - e_w - e_x.
  Proof: k(Y) counts w with Y ⊆ N+(w). T[N+(w)] has, for x in N+(w), out-degree (inside N+(w)) equal to |N+(x) ∩ N+(w)| = c_{wx} (w is not beaten by x, and x not in own out-set).
  A transitive triple has exactly one vertex beating the other two, so #transitive triples in T[N+(w)] = sum_{x in N+(w)} C(c_wx,2). Sum over w. QED
* (I7) sum_{Y transitive} k+(Y) = sum_{arcs x->w} C(D_xw, 2).
  Proof: k+(Y) counts w with Y ⊆ N-(w); in T[N-(w)] the in-degree of x equals |N-(x) ∩ N-(w)| = D_{xw}; a transitive triple has exactly one sink, with in-degree 2 in the triple. QED
  The cyclic-class sums are the complements: sum_{cyc} k = sum_w C(d+,3) - (I6), sum_{cyc} k+ = sum_w C(d-,3) - (I7).
  (Check DRT(51): arcs 1275, c = 12: 1275*C(12,2) = 1275*66 = 84150 = [52] (M2). OK.)

### A.3 Totals in terms of degrees (hand algebra, double-checked)

Expand (26-x)(25-x)(24-x): (26-x)(25-x) = 650 - 51x + x^2; times (24-x): 15600 - 1224x + 24x^2 - 650x + 51x^2 - x^3 = 15600 - 1874x + 75x^2 - x^3.
Expand (25+x)(24+x)(23+x): (25+x)(24+x) = 600 + 49x + x^2; times (23+x): 13800 + 1127x + 23x^2 + 600x + 49x^2 + x^3 = 13800 + 1727x + 72x^2 + x^3.
So 6 C(26-e,3) = 15600 - 1874e + 75e^2 - e^3 and 6 C(25+e,3) = 13800 + 1727e + 72e^2 + e^3. Sum over the 52 vertices (sum e = 26, 52*15600 = 811200, 52*13800 = 717600):
* 6 sum_Y k  = 811200 - 1874*26 + 75 S2 - S3 = 811200 - 48724 + 75 S2 - S3 = 762476 + 75 S2 - S3.
* 6 sum_Y k+ = 717600 + 1727*26 + 72 S2 + S3 = 717600 + 44902 + 72 S2 + S3 = 762502 + 72 S2 + S3.
* sum_Y (k + k+) = (1524978 + 147 S2)/6 = **254163 + 24.5 S2**  [1524978/6 = 254163].
* sum_Y (k - k+) = (762476 - 762502 + 3 S2 - 2 S3)/6 = **(3 S2 - 2 S3 - 26)/6**.
Balanced check (26 vertices e = 1, 26 vertices e = 0: S2 = S3 = 26): sum k = (762476 + 1950 - 26)/6 = 764400/6 = 127400 (= BRIEF); sum (k-k+) = (78 - 52 - 26)/6 = 0. OK.
Independent check of sum L: sum_Y L_Y from (A1'): sum_Y E_Y = C(51,2)*26 = 1275*26 = 33150; sum_Y sum_ij D_ij = 50 Theta, Theta := sum_P D_P = sum_w C(26-e_w,2) = (33800 - 51*26 + S2)/2 = (32474 + S2)/2 = 16237 + S2/2;
sum_Y sigma = (number of transitive triples) = sum_w C(d+(w),2) = Theta. So sum L = -23*22100 - 33150 + 49 Theta = -508300 - 33150 + 49*16237 + 24.5 S2 = -541450 + 795613 + 24.5 S2 = 254163 + 24.5 S2. OK (agrees).

### A.4 The cubic identity (check)

Put delta = k - k+ and L = k + k+, so k = (L+delta)/2, k+ = (L-delta)/2. With b = L/2 - 1 and t = delta/2: 6C(k,3) = (k-1)^3 - (k-1) with k - 1 = b + t, and 6C(k+,3) = (b-t)^3 - (b-t).
6[C(k,3) - C(k+,3)] = [(b+t)^3 - (b-t)^3] - [(b+t) - (b-t)] = 6 b^2 t + 2 t^3 - 2t.   With t = delta/2: = 3 b^2 delta + delta^3/4 - delta.
Multiply by 4: 24[C(k,3) - C(k+,3)] = delta^3 + (12 b^2 - 4) delta, and 12 b^2 = 3(L-2)^2 = 3L^2 - 12L + 12, so
   24[C(k,3) - C(k+,3)] = delta ( delta^2 + 3L^2 - 12L + 8 ).    CONFIRMED (matches BRIEF).
(I5) therefore reads  **sum_Y delta_Y (delta_Y^2 + g(L_Y)) = 0, g(L) = 3L^2 - 12L + 8**; g(10) = 188, g(11) = 239, g(12) = 296, g(13) = 359.
Quick numeric spot check: L = 13, k = 5, k+ = 8: C(5,3) - C(8,3) = 10 - 56 = -46; times 24 = -1104; delta = -3: -3(9 + 359) = -1104. OK.
Another: L = 11, k = 6, k+ = 5: 20 - 10 = 10, *24 = 240; delta = 1: 1*(1 + 239) = 240. OK.

---

## B. The vertex pair-sum identity (NEW, exact, and it makes the pair profile rigid)

Notation: x_P := D_P - 12 (>= -1; a tight pair has x = -1). eps^-(w) := sum over z in N-(w) of e(z).  eps^+(w) := sum over z in N+(w) of e(z).
Then eps^-(w) + eps^+(w) = 26 - e(w).

**Proposition V1.** For every vertex w of any tournament on 52 vertices,
   sum_{u != w} D_{wu} = 25 d-(w) - eps^-(w),   equivalently   **sum_{u != w} x_{wu} = 13 + 25 e(w) - eps^-(w).**
Proof. D_{wu} = #{z not in {w,u} : z->w and z->u}. Swap the order of counting: sum_u D_{wu} = sum_{z in N-(w)} #{u not in {w,z} : z->u}.
For z in N-(w), z beats w, so the out-neighbours of z other than w number d+(z) - 1 = 25 - e(z). Hence sum_u D_wu = sum_{z in N-(w)} (25 - e(z)) = 25 d-(w) - eps^-(w).
With d-(w) = 25 + e(w): 625 + 25 e(w) - eps^-(w); subtract 12*51 = 612. QED
Checks: (i) sum over w of the right side = 13*52 + 25*26 - sum_z e(z) d+(z) = 676 + 650 - (26*26 - S2) = 650 + S2, and the left side is 2 sum_P x_P = 2(Theta - 15912) = 2(325 + S2/2) = 650 + S2. OK.
(ii) The same count for common out-neighbours gives sum_u c_{wu} = sum_{z in N+(w)} (d-(z) - 1) = 24 d+(w) + eps^+(w); with c = 1 + D - e_w - e_u this is consistent with V1 (it reduces to eps^+ + eps^- = 26 - e_w). OK.

**Corollary V2 (vertices of in-degree 24 force tight pairs; consistent with Claim Q).** Let e(w) = -1. Then sum_u x_wu = -12 - eps^-(w).
Since e(z) >= -1 for all z (no in-degree 23, [A52] Lemma 1, audited) and e(z) >= 0 for in-neighbours not in Z, and w has <= 2 in-neighbours in Z (Claim Q),
eps^-(w) >= -2, so sum_u x_wu <= -10; as every x >= -1, w lies in at least 10 tight pairs. (Claim Q says >= 12; this is weaker but needs only the degree count.)
More generally #{tight pairs at w} >= -sum_u x_{wu} = eps^-(w) - 13 - 25 e(w) + ... [exact: sum of x over non-tight pairs at w is >= 0, so t_w >= -(13 + 25e_w - eps^-(w))].

**Proposition V3 (balanced degrees: the excess is concentrated inside U).** Suppose every in-degree is 25 or 26. Put U = {e = 1}, W = {e = 0}, |U| = |W| = 26.
For w in U let a_w = |N-(w) ∩ U|; for w in W let b_w = |N-(w) ∩ U|. Then eps^-(w) = a_w resp. b_w, and
 * sum_{w in U} a_w = C(26,2) = 325 (each pair in U has one arc);
 * sum_{w in W} b_w = (#arcs U->W) = 650 - C(26,2) = 325 (since sum over W of d- is 25*26 = 650 = arcs inside W + arcs U->W).
Let X_UU, X_WW, X_UW be the totals of x_P over pairs inside U, inside W, and between. By V1:
   2 X_UU + X_UW = sum_{w in U}(38 - a_w) = 988 - 325 = 663,
   2 X_WW + X_UW = sum_{w in W}(13 - b_w) = 338 - 325 = 13.
Hence **X_UU - X_WW = 325, 2 X_WW + X_UW = 13, X_UU + X_WW + X_UW = 338** (no sign assumption on x was used).
Consequently, if no pair is tight (all x >= 0): X_WW <= 6, X_UW <= 13, X_UU = 325 + X_WW >= 325: **all but at most 13 units of the excess sit on the 325 pairs inside U, and that block has average D >= 13.**
(If x >= 0 fails, i.e. tight pairs exist, the same three equations still hold.)
Also: for w in W, b_w <= 13 whenever no pair at w is tight (sum_u x_wu = 13 - b_w >= 0); for w in U: a_w + sum_u x_wu = 38.
Sanity: the 'ideal' profile x = [P ⊂ U] would need a_w = 13 for all 26 vertices of U, impossible since the average of a_w is 12.5; so even the ideal block needs a little defect.

<!-- END -->

# R4-MASTER: independent re-derivation of the master inequality (Erdos #902, round 4)

Lane: R4-MASTER. Target: f(4) >= 53, balanced no-tight-pair Case A.
Setting: T is an F1 tournament on 52 vertices; V0 (26, in-degree 25), V1 (26, in-degree 26); x_P = |D(P)| - 12 >= 0; sum x_P = 338 over 1326 pairs.

## Status

- DONE: all four items re-derived by hand (see Log, sections L1-L8). Verdict: VERIFIED.
- (a) eps(L) = Lambda(L) - Lambda_q(L) = (L-11)(L-12)(L-13)/3 for L >= 14; values 2, 8, 20, 40, 70 at L = 14..18. VERIFIED. The same closed form holds for all L >= 5.
- (b) Lambda(L) <= Lambda_q(L) for 5 <= L <= 13, with equality at L = 11, 12, 13. VERIFIED (L <= 4 cannot occur, since k >= 5 and l >= 0).
- (c) sum X_Y = 16900; sum X_Y^2 = 48 S2 + sum_v xi_v^2; sum_v xi_v^2 = 17238 (STAR re-derived: sum d^2 + sum o^2 = 4394); sum L_Y^2 = 2930876 + 46 S2. VERIFIED.
- (d) 520 + 2 ex <= 147 eta_T + 138 eta_M + E_tail, with E_tail = sum over L >= 14 of eps(L). VERIFIED under H1 + H2 (balanced, no tight pair), using F1 only through k >= 5. Sharper signed form in L7.
- Corrections to earlier audit items: r1 sec 5 "(5.1) forces E_tail > 0 or S2 >= 346" is imprecise (L6). Synthesis F1 and F4 CONFIRMED.
- Not consulted: r3_BAL.md (not needed for the target, and its forbidden sections were avoided).

## Plan

1. Read BRIEF.md (sections 0-10) for rules and notation.
2. Read ROUND1_SYNTHESIS.md sections 4 and 8.
3. Read r1_MOM-BALANCED.md sections 2-5.
4. Read r3_BAL.md S1-S6 and S8 only.
5. Re-derive item (a), (b), (c), (d) by hand, writing each step here as it is done.
6. Report verdict per item.

## Log

(entries appended below as work proceeds)

### L1. Sources and setting

- Read: BRIEF.md sections 0-10; ROUND1_SYNTHESIS.md sections 0-8 (sections 4 and 8 used); r1_MOM-BALANCED.md sections 1-6 (identities and Lemmas 2.1-2.2). r3_BAL.md was not opened.
- Setting: H1 = all in-degrees in {25, 26}. H2 = no pair has |D(P)| = 11, so D_P >= 12 and x_P >= 0 (F2 gives |D(P)| >= 11 in general).
- G = V0 (d- = 25, d+ = 26), |G| = 26; H = V1 (d- = 26, d+ = 25), |H| = 26.
- Pair types: GG: C(26,2) = 325 pairs, x = 0. Mixed: 26*26 = 676 pairs = 351 arcs G->H (the M-pairs, x may be > 0) + 325 arcs H->G (x = 0). HH: 325 pairs (the T-pairs, x may be > 0).
- Check: sum_P D_P = sum_w C(d+(w),2) = 26*325 + 26*300 = 8450 + 7800 = 16250. Then sum_P x_P = 16250 - 12*1326 = 16250 - 15912 = 338. VERIFIED.

### L2. Basic identities (re-derived)

**(2.1) L-identity.** Let Y = {y1,y2,y3}, l(Y) = |D+(Y)|, and A_i = N-(y_i) minus Y. An outside vertex lies in D+(Y) iff it is in no A_i, so l = 49 - |A1 u A2 u A3|.
- |A_i| = d-(y_i) - (number of Y-vertices beating y_i). These three counts sum to 3, one per arc of Y. So sum |A_i| = sum d-(y_i) - 3.
- |A_i ∩ A_j| = D_ij - [the third vertex beats both y_i and y_j]. The third vertex beats both only when it is the source of Y. That happens for exactly sigma(Y) of the three pairs.
- A1 ∩ A2 ∩ A3 = D(Y), of size k.
- Inclusion-exclusion: |union| = (sum d- - 3) - (sum D_ij - sigma) + k. Hence k + l = 52 - sum d-(y_i) + sum D_ij - sigma =: L_Y.
- Put d- = 25 + [y in H] and D_ij = 12 + x_ij. Then L_Y = 52 - (75 + a) + (36 + X) - sigma = 13 - a - sigma + X, where a = #H-vertices in Y and X = X_Y. VERIFIED.

**(2.2) Common out-neighbourhoods.** For a pair {a,b}, m_P := |N+(a) ∩ N+(b)| = D_P + 51 - d-(a) - d-(b).
- Proof: the 50 vertices other than a, b split into those beating a or b, and those beaten by both. Exactly one of a, b beats the other, so |N-(a)∪N-(b) minus {a,b}| = d-(a) + d-(b) - 1 - D_P. The complement has 50 - (that) = 51 - d-(a) - d-(b) + D_P elements, and these are the common out-neighbours.
- So m = D+1 (GG), m = D (mixed), m = D-1 (HH). VERIFIED.
- Also cyc(a->b) := |N+(b) ∩ N-(a)| = d+(b) - m_P, since a is not in N+(b).

**(2.3) Lemmas 2.1 and 2.2 (re-derived).**
- v in G. T[N-(v)] has 25 vertices and C(25,2) = 300 arcs. The in-degree of a in it is D({a,v}) >= 12, and the sum is 300 = 25*12, so every D({a,v}) = 12. Hence x(a,v) = 0 for every arc a->v with head in G.
- v in H. The same count gives sum over in-neighbours a of x(a,v) = C(26,2) - 26*12 = 13.
- v in G, out-neighbourhood (26 vertices, 325 internal arcs). For a in N+(v): m(v,a) = 13 if a in G (x = 0), and m = 12 + x if a in H. Writing g+ = |N+(v) ∩ G| and h+ = 26 - g+: 13 g+ + 12 h+ + X+ = 325, so g+ + X+ = 13. Hence X+(v) = d_v := 13 - g+(v) >= 0.
- v in H, out-neighbourhood (25 vertices, 300 internal arcs). For a in G: m = 12 (x = 0). For a in H: m = 11 + x. So 12(25 - h+) + 11 h+ + X+ = 300, i.e. X+(v) = h+(v) =: o_v.
- Consequences: sum_{v in G} d_v = 26*13 - 325 = 13 (GH x-mass). sum_{v in H} o_v = 325 (HH x-mass). Total 338. VERIFIED.
- Let xi_v := sum of x over pairs containing v. Then xi_v = d_v for v in G, and xi_v = 13 + o_v for v in H. VERIFIED.

**(2.4) Cyclic counts through an arc.** cyc = d+(b) - m:
- GG arc: 26 - 13 = 13.
- H->G arc (x = 0): 26 - 12 = 14.
- G->H arc: 25 - (12 + x) = 13 - x.
- HH arc: 25 - (11 + x) = 14 - x.
- Check: 325*13 + 325*14 + (351*13 - 13) + (325*14 - 325) = 4225 + 4550 + 4550 + 4225 = 17550 = 3*5850, where 5850 = 22100 - 16250 is the number of cyclic triples. VERIFIED. (These are the r1 3.1 values.)

**(2.5) STAR re-derived.** Let c_a = number of cyclic triples with a H-vertices.
- Each cyclic triple with a = 0 has 3 GG arcs, and each with a = 1 has 1 GG arc. So sum over GG arcs of cyc = 3 c_0 + c_1 = 325*13 = 4225.
- c_0 = 2600 - sum_{v in G} C(g+(v),2) = 2600 - sum_v C(13 - d_v, 2). Using C(13-d,2) = (156 - 25d + d^2)/2 and sum d_v = 13: sum_v C(13-d_v,2) = (4056 - 325 + sum d^2)/2 = (3731 + sum d^2)/2. So c_0 = (1469 - sum d^2)/2.
- c_1 = 8450 - t_1, where t_1 = number of transitive triples with exactly one H-vertex. Such a triple has source v in G with one G- and one H-out-neighbour, or source v in H with both others in G. So t_1 = sum_{v in G} g+(v) h+(v) + sum_{w in H} C(omega_w, 2), with omega_w = |N+(w) ∩ G| = 25 - o_w.
- sum_{v in G} (13-d_v)(13+d_v) = 26*169 - sum d^2 = 4394 - sum d^2.
- sum_{w in H} C(25 - o_w, 2) = (1/2) sum (600 - 49 o + o^2) = (1/2)(15600 - 49*325 + sum o^2) = (sum o^2 - 325)/2.
- So c_1 = 8450 - 4394 + sum d^2 - (sum o^2 - 325)/2 = 4056 + sum d^2 - (sum o^2 - 325)/2.
- Then 3c_0 + c_1 = 2203.5 - 1.5 sum d^2 + 4056 + sum d^2 - sum o^2/2 + 162.5 = 6422 - (sum d^2 + sum o^2)/2 = 4225.
- Hence **sum_{w in H} o_w^2 + sum_{v in G} d_v^2 = 4394 (STAR)**. VERIFIED. (The sums are taken with o_w directly; no substitution omega = 25 - o is needed.)

### L3. Item (c): the sums

- (c.1) sum_Y X_Y = 50 * sum_P x_P = 50*338 = 16900 (each pair lies in 50 triples). Also sum_Y (k-5) = 127400 - 5*22100 = 127400 - 110500 = 16900. VERIFIED.
- (c.2) sum_Y X_Y^2 = 48 S2 + sum_v xi_v^2, with S2 = sum_P x_P^2. Proof: a pair of distinct pairs lies in a common triple iff they share a vertex, and then in exactly one triple. So sum_Y X^2 = sum_Y sum_{P in Y} x_P^2 + 2 sum_v sum_{ {P,Q} containing v } x_P x_Q = 50 S2 + sum_v (xi_v^2 - sum_{P containing v} x_P^2) = 50 S2 + sum_v xi_v^2 - 2 S2. VERIFIED.
- (c.3) S2 = 338 + 2K. Since x(x-1) = 2 C(x,2), S2 = sum x + sum x(x-1) = 338 + 2K, because only GH and HH pairs carry x > 0 (GG and H->G arcs have head in G). VERIFIED.
- (c.4) sum_v xi_v^2 = sum_{v in G} d_v^2 + sum_{w in H} (13 + o_w)^2 = sum d^2 + [26*169 + 26*325 + sum o^2] = (sum d^2 + sum o^2) + 4394 + 8450 = 4394 + 12844 = 17238 (using STAR). VERIFIED.
- (c.5) Auxiliary sums (for sum L^2):
  - sum_Y a = 8450*1 + 8450*2 + 2600*3 = 33150. sum_Y a^2 = 8450 + 33800 + 23400 = 65650. sum_Y sigma = 16250.
  - sum_Y sigma*a: a transitive triple is counted by its source w, with contribution [w in H] C(d+(w),2) + (d+(w)-1) h+(w), where h+(w) = |N+(w) ∩ H|. For w in G: 25 * (sum h+) = 25*351 = 8775. For w in H: 26*C(25,2) + 24*325 = 7800 + 7800 = 15600. Total 24375. VERIFIED.
  - sum_Y L0^2, where L0 := 13 - a - sigma: expand (13-a-sigma)^2 = 169 + a^2 + sigma - 26a - 26 sigma + 2 a sigma. So sum = 169*22100 + 65650 + 16250 - 26*33150 - 26*16250 + 2*24375 = 3734900 + 65650 + 16250 - 861900 - 422500 + 48750 = 2581150. VERIFIED.
  - sum_Y a X = sum_P x_P (49 a_P + 26) = 26*338 + 49*(13*1 + 325*2) = 8788 + 49*663 = 8788 + 32487 = 41275 (GH pairs have a_P = 1, HH pairs a_P = 2). Cross-check: 75*13 + 124*325 = 975 + 40300 = 41275. VERIFIED.
  - sum_Y sigma X = sum_P x_P (50 - cyc_P), since a pair lies in 50 triples of which cyc_P are cyclic. GH: 37x + x^2; HH: 36x + x^2. So sum = 37*13 + 36*325 + S2 = 481 + 11700 + S2 = 12181 + S2. VERIFIED.
  - sum_Y L0 X = 13*16900 - 41275 - (12181 + S2) = 219700 - 41275 - 12181 - S2 = 166244 - S2. VERIFIED.
- (c.6) sum_Y L_Y^2 = sum L0^2 + 2 sum L0 X + sum X^2 = 2581150 + 2(166244 - S2) + (48 S2 + 17238) = 2930876 + 46 S2. VERIFIED. (For S2 = 338 this is 2946424.)
- (c.7) sum_Y L_Y = 254800, by two routes. Route 1: sum (k+l) = 127400 + 127400. Route 2: 13*22100 - 33150 - 16250 + 16900 = 254800. VERIFIED.

### L4. Items (a) and (b): the certificate constants

- **Cubic identity.** Write k = L/2 + u, l = L/2 - u, p = L/2. With f(t) = t(t-1)(t-2) = t^3 - 3t^2 + 2t: f(p+u) - f(p-u) = 2[(3p^2 - 6p + 2)u + u^3], and C(k,3) - C(l,3) = (f(k) - f(l))/6 = [u^3 + c(L) u]/3, where c(L) = 3p^2 - 6p + 2 = 3(L/2 - 1)^2 - 1 = (3/4)(L-2)^2 - 1. So c(11) = 59.75, c(12) = 74, c(13) = 89.75. VERIFIED.
- **Pair identity.** C(k,2) - C(l,2) = u(L-1), since k + l = L. And u^2 = C(k,2) + C(l,2) + L/2 - L^2/4 (check at (k,l) = (5,8): 10 + 28 + 6.5 - 42.25 = 2.25 = (1.5)^2). VERIFIED.
- **Certificate function.** Define Phi_L(u) := u^2 - (2/3)(u^3 + c u) - (70 - 10L) u. Since (2/3)c = (L-2)^2/2 - 2/3, this is
  Phi_L(u) = -(2/3) u^3 + u^2 + B(L) u, with B(L) = -L^2/2 + 12L - 214/3 = 2/3 - (L-12)^2/2. VERIFIED (the linear coefficient is -(2/3)c - 70 + 10L = -(1/2)(L-2)^2 + 2/3 - 70 + 10L).
- **lambda(L)** := max of Phi_L(u) over admissible u, i.e. u = k - L/2 with k an integer, 5 <= k <= L. (k >= 5 by F1; l = L - k >= 0.) Note L >= 5 for every triple.
- **Hand maxima, L = 5..13** (all admissible u listed):
  - L = 5: k = 5 only, u = 2.5, Phi = -255/4. lambda = -255/4.
  - L = 6: u in {2, 3}: Phi(2) = -36, Phi(3) = -61. lambda = -36.
  - L = 7: u in {1.5, 2.5, 3.5}: Phi = -71/4, -135/4, -231/4. lambda = -71/4.
  - L = 8: u in {1, 2, 3, 4}: Phi(1) = -7, Phi(2) = -16, Phi(3) = -18 + 9 - 22 = -31, Phi(4) < 0. lambda = -7.
  - L = 9: u in {0.5, 1.5, ...}: Phi(0.5) = -7/4, Phi(1.5) = -23/4. lambda = -7/4.
  - L = 10: u in {0, 1, ...}: Phi(0) = 0, Phi(1) = -1, Phi(2) = -4. lambda = 0.
  - L = 11: u in {-1/2, 1/2, 3/2, ...}: Phi = 1/4 at the first three, then negative. lambda = 1/4. Exact: Phi_11(u) - 1/4 = -(2/3)(u+1/2)(u-1/2)(u-3/2). Check at u = 0: LHS -1/4, RHS -(2/3)(1/2)(-1/2)(-3/2) = -1/4. VERIFIED.
  - L = 12: u in {-1, 0, 1, ..., 6}: Phi(-1) = 1, Phi(0) = 0, Phi(1) = 1, Phi(2) = 0, Phi(3) = -7. lambda = 1. Exact: Phi_12(u) - 1 = -(1/3)(u-1)(u+1)(2u-3). Check at u = 0: LHS -1, RHS -(1/3)(-1)(1)(-3) = -1. VERIFIED.
  - L = 13: u in {-3/2, -1/2, 1/2, 3/2, ...}: Phi(-3/2) = 17/4, Phi(-1/2) = Phi(1/2) = Phi(3/2) = 1/4. lambda = 17/4, attained at u = -3/2 (k = 5).
  - In each case L = 5..13, the maximum is attained at k = 5 (u = 5 - L/2) [for L = 12 also at k = 7, equal value 1; for L = 11 also at k = 6, 7, equal value 1/4].
- **L >= 14 (monotonicity).** Phi_L'(u) = -2(u - 1/2)^2 + 1/2 + B(L) <= 1/2 + 2/3 - (L-12)^2/2 <= 7/6 - 2 = -5/6 < 0 when L >= 14. So Phi_L is strictly decreasing and the maximum is at the smallest admissible u, u = 5 - L/2 (k = 5). VERIFIED.
- **Closed form at k = 5.** Put w = L - 10, so u = -w/2. Then B = -w^2/2 + 2w - 4/3, and Phi = w^3/3 - (3/4) w^2 + (2/3) w. This is an identity in w, so it holds for every L. Together with the hand maxima above (k = 5 attains the maximum for every L = 5..13), lambda(L) = w^3/3 - 3w^2/4 + 2w/3 for all L >= 5. Values: lambda(14..18) = 12, 105/4, 49, 329/4, 128. VERIFIED.
- **Lambda and Lambda_q.** Lambda(L) := lambda(L) + L^2/4. Lambda_q(L) := 37 + 8(L-12) + 1.5(L-12)^2 = 1.5 L^2 - 28 L + 157. Check: Lambda_q(12) = 37; Lambda_q(14) = 59.
- **Exact closed form.** With w = L - 10: Lambda = w^3/3 - 3w^2/4 + 2w/3 + (w+10)^2/4 = w^3/3 - w^2/2 + 17w/3 + 25. Also Lambda_q = 27 + 2w + 3w^2/2. Difference: w^3/3 - 2w^2 + 11w/3 - 2 = (w-1)(w-2)(w-3)/3. So
  **Lambda(L) - Lambda_q(L) = (L-11)(L-12)(L-13)/3 for all L >= 5.** VERIFIED.
- **Item (a).** eps(L) = (L-11)(L-12)(L-13)/3 = 2 C(L-11, 3) for L >= 14: eps(14) = 2, eps(15) = 8, eps(16) = 20, eps(17) = 40, eps(18) = 70. Check by direct values: Lambda(14..18) = 61, 82.5, 113, 154.5, 209 against Lambda_q = 59, 74.5, 93, 114.5, 139. VERIFIED.
- **Item (b).** Lambda(L) - Lambda_q(L) for L = 5..13 equals -112, -70, -40, -20, -8, -2, 0, 0, 0 (closed form). All are <= 0, with equality exactly at L = 11, 12, 13. Direct check at L = 9: Lambda = 18.5 <= 26.5 = Lambda_q; at L = 10: 25 <= 27. VERIFIED.
- **Signed master sum.** sum_Y Lambda(L_Y) = sum_Y Lambda_q(L_Y) + sum_Y C3(L_Y), with C3(L) := (L-11)(L-12)(L-13)/3 (exact, all L). Since C3 <= 0 on L <= 11 and C3 = 0 on 11..13, the r1 convention "eps = 0 for L <= 13" gives sum Lambda <= sum Lambda_q + E_tail with E_tail = sum over L >= 14 of C3(L). Valid, and lossy when some L <= 10 occur.

### L5. Item (d): assembly of the master inequality

Hypotheses: H1, H2 (Case A setting). F1 is used only through k >= 5 in the admissible u-set.

- **Step 1 (second moments).** sum_Y C(k,2) = sum_P C(m_P,3) (a pair {w,w'} with Y inside N+(w) ∩ N+(w') is counted once). Expand by pair type:
  - GG: 325 * C(13,3) = 325*286 = 92950.
  - H->G (x = 0, m = 12): 325 * C(12,3) = 325*220 = 71500.
  - GH (m = 12 + x): C(12+x,3) = 220 + 66x + f_G(x). Sum = 351*220 + 66*13 + sum_GH f_G = 77220 + 858 + sum_GH f_G.
  - HH (m = 11 + x): C(11+x,3) = 220 + 66(x-1) + f_H(x). Sum = 325*220 + 66*(325 - 325) + sum_HH f_H = 71500 + sum_HH f_H.
  - Total: 92950 + 71500 + 77220 + 858 + 71500 = 314028, plus ex. So sum_Y C(k,2) = 314028 + ex, where ex = sum_GH f_G + sum_HH f_H. VERIFIED.
  - Check of the f-values: f_G(0..3) = 0, 0, 12, 37 (f_G(x+1) - f_G(x) = C(12+x,2) - 66 >= 0). f_H(0..4) = 11, 0, 0, 12, 37 (f_H(x+1) - f_H(x) = C(11+x,2) - 66, which is -11 at x = 0 and 0 at x = 1). Both are >= 0. VERIFIED.
  - Also 988*220 + 338*286 = 217360 + 96668 = 314028. VERIFIED.
- **Step 2 (difference).** sum_Y [C(k,2) - C(l,2)] = sum_Y u(L-1) = sum_P [C(m_P,3) - C(D_P,3)]. GG: 325*(286 - 220) = 21450. Mixed: 0. HH: -sum_HH C(11+x,2) = -(325*110 + 21*325 + S2_HH)/2 = -(42575 + S2_HH)/2 = -21287.5 - S2_HH/2. Total: 162.5 - S2_HH/2. With S2_HH = sum_HH x^2 = 2 eta_T + 325 (x^2 = x(x-1) + x, sum_HH x = 325), this is -eta_T. So sum_Y (L-1) u = -eta_T, and since sum u = 0, **sum_Y L u = -eta_T**. VERIFIED.
- **Step 3 (second moment of u).** Using the pair identity, sum u^2 = sum C(k,2) + sum C(l,2) + sum L/2 - sum L^2/4, with sum C(l,2) = sum C(k,2) + eta_T = 314028 + ex + eta_T, sum L/2 = 127400. So
  sum_Y u^2 = 755456 + 2 ex + eta_T - (1/4) sum L^2 = 755456 + 2 ex + eta_T - (2930876 + 46 S2)/4 = 22737 + 2 ex + eta_T - 11.5 S2. VERIFIED (755456 - 732719 = 22737).
  - Cross-check of sum C(l,2) = 314028 + ex + eta_T: sum_P C(D_P,3) = sum_P C(m_P,3) + sum_HH [C(12+x,3) - C(11+x,3)] = (314028 + ex) + sum_HH C(11+x,2) - 66*325 = 314028 + ex + (21287.5 + S2_HH/2) - 21450 = 314028 + ex + eta_T. VERIFIED.
- **Step 4 (certificate).** For each triple, u^2 <= (2/3)(u^3 + c u) + (70 - 10L) u + lambda(L), which is Phi_L(u) <= lambda(L) by definition. Sum over all 22100 triples:
  - sum (2/3)(u^3 + c u) = 2 sum [C(k,3) - C(l,3)] = 0 (Step 1 of L4 and sum_Y C(k,3) = sum_W C(l(W),3)). VERIFIED.
  - sum (70 - 10L) u = 70*0 - 10*(-eta_T) = 10 eta_T.
  - So sum u^2 <= sum lambda(L_Y) + 10 eta_T.
- **Step 5 (combine).** 755456 + 2ex + eta_T - (1/4) sum L^2 <= sum lambda + 10 eta_T, i.e. 755456 + 2 ex <= sum_Y Lambda(L_Y) + 9 eta_T. VERIFIED.
- **Step 6 (quadratic majorant).** sum_Y Lambda_q(L_Y) = 1.5 sum L^2 - 28 sum L + 157*22100 = (4396314 + 69 S2) - 7134400 + 3469700 = 731614 + 69 S2. VERIFIED. With L4 (Lambda <= Lambda_q for L <= 13, Lambda - Lambda_q = eps(L) for L >= 14):
  sum Lambda <= 731614 + 69 S2 + E_tail, E_tail = sum over L >= 14 of eps(L).
- **Step 7 (substitute S2).** 755456 - 731614 = 23842, so 23842 + 2 ex <= 69 S2 + 9 eta_T + E_tail. With S2 = 338 + 2(eta_T + eta_M): 69 S2 = 23322 + 138 eta_T + 138 eta_M. Hence
  **520 + 2 ex <= 147 eta_T + 138 eta_M + E_tail.** VERIFIED.
- Here eta_M = sum over GH arcs of C(x,2) = (1/2) G with G = sum over G->H arcs of x(x-1). So 138 eta_M = 69 G, matching the corrected form in r1 sec 5 (synthesis F1). 147 = 138 + 9, coming from the 69 S2 term (coefficient 2*69 on eta_T) plus 9.

### L6. Audit items: confirmed or corrected

- **Synthesis F1 (r1 sec 5, master form): CONFIRMED.** The correct general form is 520 + 2ex <= 147 eta + 69 G + E_tail (here eta = eta_T, G = 2 eta_M). Equivalently 23842 + 2 ex <= 69 S2 + 9 eta + E_tail. The original bullet "(5.1) forces E_tail > 0 or S2 >= 346 (take eta = ex = 0)" is imprecise: if eta_T = eta_M = ex = 0 then S2 = 338 and (5.1) gives E_tail >= 23842 - 23322 = 520 directly. The disjunction is true in that case but is not the sharp statement.
- **Synthesis F4 (r1 sec 3.6 signs): CONFIRMED.** Phi_11(u) - 1/4 = -(2/3)(u+1/2)(u-1/2)(u-3/2) (r1 printed a plus sign), and Phi_12(u) - 1 = -(1/3)(u-1)(u+1)(2u-3) (r1 printed the form without the minus sign). The lambda values are unaffected. Also r1 writes "lambda(13) = 17/4 (zero at u = -3/2)". The correct statement: Phi_13(-3/2) = 17/4, so lambda(13) = 17/4 is attained there; Phi_13 - 17/4 vanishes there.
- **r1 sec 3.1 cyclic counts: CONFIRMED** (GG 13, H->G 14, G->H 13-x, HH 14-x; total 17550 = 3*5850).
- **r1 sec 3.2 STAR and the 17238 value: CONFIRMED** (STAR re-derived in L2.5; xi-sum in L3 (c.4)).
- **r1 sec 3.3 identities: CONFIRMED.** sum L0^2 = 2581150; sum L0 X = 166244 - S2; sum L^2 = 2930876 + 46 S2 (for S2 = 338: 2946424). Also the stated (3.3) check.
- **r1 sec 3.4a and 3.4b: CONFIRMED** (sum (L-1) u = -eta; sum u^2 = 22737 + 2ex - 11.5 S2 + eta).
- **r1 sec 3.6 lambda values: CONFIRMED** for L = 9, 10, 11, 12, 13, 14, 15, 16 (values -7/4, 0, 1/4, 1, 17/4, 12, 105/4, 49). Also lambda(5..8) and lambda(17), lambda(18) (= 329/4, 128) are new here; they agree with the closed form.
- **r1 sec 3.6 list "Lambda(9..16) = 18.5, 25, 30.5, 37, 46.5, 61, 82.5, 113": CONFIRMED.**
- **r1 sec 5 Prop 4.1(c) bound** N^- >= (169 - sum d^2)/25 (synthesis F2): I re-derived it from sum s^2 = 338 - sum d^2 (from STAR and sum o^2 = 4394 - sum d^2 with s = o - 12) and sum s^2 <= 13(13 + N^-) + 12 N^- = 169 + 25 N^- (using s <= 13, s >= -12, sum s = 13). CONFIRMED. The consequence for eta, and whether eta >= 7 or 9 holds, was not checked further (outside the master target).
- **r1 sec 4 Prop 4.3 arithmetic: CONFIRMED** (see L7). Its structural claims in Prop 4.2 were not re-derived.

### L7. Observations (not errors in the master)

1. **Signed (sharper) master.** Because Lambda(L) = Lambda_q(L) + C3(L) for all L >= 5, the master can be written exactly as 520 + 2ex <= 147 eta_T + 138 eta_M + sum over ALL triples of C3(L_Y). C3 is negative for L <= 10, so this is sharper than the E_tail version whenever such triples exist. The E_tail version (sum over L >= 14 only) is valid and is the one stated in the task.
2. **Special triples in the Prop 4.2 family.** In the family of r1 Prop 4.2 (a vertex v0 in G with g+ = 0, and h0 in H with o = 25), the 50 triples {v0, h0, y} have k = l = 12, so L = 24, and C3(24) = 13*12*11/3 = 572 each. In the global master these alone put 28600 into E_tail. Prop 4.3 avoids this by removing them (they have u = 0), which is a valid, different (sharper) argument. I checked its arithmetic: sum over non-special triples of (L-12) = -10400 - 600 = -11000; of (L-12)^2 = (46 S2 - 1924) - 7200 = 46 S2 - 9124; then -11355 + 57.5 S2 + E, and 36536 + 2 ex_H <= 69 S2 + 9 eta + E, giving 2450 + 2 ex_H <= 147 eta + E. CONFIRMED.
3. **Not established: "impossible when eta = 0".** Prop 4.3 says that if every HH arc has x = 1, the family is impossible. Its inequality with eta = ex_H = 0 only gives E >= 2450, where E is the tail over the non-special triples. Impossibility would need an upper bound on E for that family, which the proposition does not provide. Flag for the Prop 4.3 owner.

### L8. Hand checks of the numbers

- 1326 * 12 = 15912; 16250 - 15912 = 338.
- C(26,2) = 325; C(25,2) = 300; C(26,3) = 2600; C(25,3) = 2300; C(51,2) = 1275; C(52,3) = 22100.
- sum_Y k = 26*2600 + 26*2300 = 67600 + 59800 = 127400; minus 5*22100 = 110500 gives 16900.
- sum_Y L = 254800: 52*22100 - 1326*1275 + 50*16250 - 16250 = 1149200 - 1690650 + 812500 - 16250 = 254800.
- 988*220 = 217360; 338*286 = 96668; sum 314028. 2*314028 + 127400 = 755456.
- 755456 / ... : (1/4)*2930876 = 732719; 755456 - 732719 = 22737.
- 1.5*2930876 = 4396314; 28*254800 = 7134400; 157*22100 = 3469700; 4396314 - 7134400 + 3469700 = 731614.
- 755456 - 731614 = 23842; 69*338 = 23322; 23842 - 23322 = 520.
- 169*22100 = 3734900; 26*33150 = 861900; 26*16250 = 422500; 2*24375 = 48750; sum L0^2 = 2581150.
- 13*16900 = 219700; 219700 - 41275 - 12181 = 166244; 2*166244 = 332488; 2581150 + 332488 + 17238 = 2930876.
- 4394 + 8450 + 4394 = 17238 (with 4394 = sum d^2 + sum o^2, 8450 = 26*325, 4394 = 26*169).
- 3*5850 = 17550 = 4225 + 4550 + 4550 + 4225.
- eps(14..18): (3*2*1)/3, (4*3*2)/3, (5*4*3)/3, (6*5*4)/3, (7*6*5)/3 = 2, 8, 20, 40, 70.
- Lambda(14..18) = 61, 82.5, 113, 154.5, 209; Lambda_q(14..18) = 59, 74.5, 93, 114.5, 139.

## Final verdict

- (a) VERIFIED. (b) VERIFIED. (c) VERIFIED, including sum X = 16900, sum X^2 = 48 S2 + sum xi^2, sum xi^2 = 17238 and sum L^2 = 2930876 + 46 S2. (d) VERIFIED: 520 + 2 ex <= 147 eta_T + 138 eta_M + E_tail, under H1 + H2 (the Case A setting). Coefficient 138 = 2*69 matches G = 2 eta_M.
- The master is correct as stated. It does not by itself close Case A: its use relies on the setting (H1, H2) and on controlling E_tail and the ex terms in later lanes.

<!-- END -->

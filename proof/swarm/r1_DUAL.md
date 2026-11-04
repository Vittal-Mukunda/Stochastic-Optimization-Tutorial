# r1_DUAL: systematic certificate hunt (by hand), N = 52, F1-tournaments

## Status (kept current)
- (24 Oct) Section 1 catalogue done (C1-C10). Section 2: moment system in u=(k-m)/2; ideal case n=0 killed (Thm IB0).
- Section 3: general dual certificate "Lemma Theta": for ANY F1-tournament on 52 vertices, A3 + 10 a2 - 70 a1 <= sum_Y Theta(L_Y), Theta = 20,25,31,40,54,75,105 at L=10..16.
  Consequence: ideal case IB-min is impossible (n <= 1625 < 1785). Another arrangement (ARR2: excess pair counts on V_0->V_1 arcs) is NOT killed by this certificate (rough estimate).
- Section 4: exact vertex-local identities V2 (pair counts into v) and V3 (sum over triples through v of k-m = 600 e_v - 300 when e in {0,1}).
- NOT a proof of T1. Open: general arrangements.

## Plan
1. Read BRIEF, [A52], [TP], [52] key formulas.
2. Section 1: catalogue of identities with exact numbers at N=52.
3. Section 2: LP relaxation on types.
4. Section 3: certificate attempt / pseudo-solution.

## 1. Catalogue of universal identities (N = 52, F1-tournament), all checked

Notation: e_v = d-(v) - 25, d+(v) = 26 - e_v, S2 = sum e^2, S3 = sum e^3. For a triple Y: k = |D(Y)|, m = |D+(Y)| (vertices beaten by all
of Y), sigma = 1 transitive / 0 cyclic, D_ij = |D({y_i,y_j})|. For a pair P: lambda_P = |D(P)|. Facts used: sum e = 26 (sum d- = 1326), e >= -1.

**(C1)** sum e = 26 and S2 >= 26 (e^2 >= e for integers, equality iff e in {0,1}).

**(C2)** #transitive triples = sum_w C(26-e_w, 2) = sum_P lambda_P = 16237 + S2/2. [C(26-e,2) = (650 - 51e + e^2)/2, sum = (33800 - 1326 + S2)/2.]
  Also sum_v C(25+e_v,2) = (31200 + 1274 + S2)/2 = 16237 + S2/2 (same number, as it must be). #cyclic = 22100 - 16237 - S2/2 = 5863 - S2/2.

**(C3) Triple-level inclusion-exclusion.** k + m = L_Y := 52 - sum_i d-(y_i) + sum_{i<j} D_ij - sigma(Y)
  = 13 - sigma - sum_i e(y_i) + sum_{i<j} h_ij,   h_ij := D_ij - 12 >= -1.
  Proof (re-done): the 49 outside vertices; |D+(Y)| = 49 - sum|N-(y_i)\Y| + sum_{i<j}|(N-(y_i) cap N-(y_j))\Y| - k.
  sum|N-(y_i)\Y| = sum d- - 3 (three internal arcs). N-(y_i) cap N-(y_j) = D_ij, and a vertex of Y lies in it iff the third vertex beats both:
  that happens for exactly sigma of the three pairs (a transitive triple has one source, a cyclic triple none). So m + k = 49 - sum d- + 3 + sum D_ij - sigma. QED.
  Check: 52 - 75 + 36 = 13.

**(C4) First moments.** sum_Y k = sum_w C(26-e_w,3), sum_Y m = sum_w C(25+e_w,3). With g(e) := C(26-e,3) - C(25+e,3) = 300 - (3601/6)e + e^2/2 - e^3/3
  [(26-e)(25-e)(24-e) = 15600 - 1874e + 75e^2 - e^3; (25+e)(24+e)(23+e) = 13800 + 1727e + 72e^2 + e^3; difference/6; check g(1) = -300, g(2) = -901]:
  sum_Y (k - m) = -13/3 + S2/2 - S3/3 (using sum e = 26: 52*300 - (3601/6)*26 = 15600 - 15604.333). It vanishes iff e in {0,1} everywhere.
  sum_Y L = 254163 + 24.5*S2 (also = sum_w f(e_w), f(e) = 4900 + 24.5(e^2 - e); checked at e = -1,0,1,2,3: 4949, 4900, 4900, 4949, 5047).

**(C5) Second moments.**  sum_Y C(m,2) = sum_P C(lambda_P, 3)   [pairs {w,w'} of Y's dominated vertices: Y subset of N-(w) cap N-(w'), |N-(w) cap N-(w')| = lambda_{ww'}].
  sum_Y C(k,2) = sum_P C(lambda_P + 1 - e_a - e_b, 3), since |N+(a) cap N+(b)| = 51 - d-(a) - d-(b) + lambda (50 outside vertices; |N-(a) cup N-(b)| minus a,b).

**(C6) Cubic identity.** sum_Y C(k,3) = sum_Y C(m,3) (pairs (Y,W) of triples with W beating Y).

**(C7) Vertex-local pair identity (V2) [new, simple].** For every vertex v:  sum over a in N-(v) of lambda_{av} = C(d-(v), 2),
  because lambda_{av} = |N-(a) cap N-(v)| is the in-degree of a inside T[N-(v)]. Hence
  sum_{a -> v} (lambda_{av} - 12) = e_v (25 + e_v) / 2,   sum_{a -> v} (lambda_{av} - 11) = (25 + e_v)(2 + e_v)/2.
  Check: e = -1 gives -12 (so at least 12 tight pairs, the content of Claim Q); sum over v of e_v(25+e_v)/2 = (650 + S2)/2 = 325 + S2/2 = sum_P (lambda_P - 12). OK.
  *Consequence (NT)*: if there is no tight pair then every e_v >= 0 (e = -1 would force deficit), and every vertex with e_v = 0 has lambda_{av} = 12 for ALL a -> v;
  moreover N-(v) is then a 12-regular (hence regular) tournament on 25 vertices in which every pair has >= 5 common in-neighbours (= triples {v,a,a'}, k >= 5).

**(C8) Pair-level excess budget (B_P).** For a pair P = {a,b}, R = D(P): k({a,b,y}) = |R cap N-(y)| for every y not in P (also y in R). Summing over the 50 vertices y:
  sum_y k = sum_{r in R} (d+(r) - 2) = sum_r (24 - e_r). So  sum_{y notin P} (k({a,b,y}) - 5) = 24 lambda_P - 250 - E_R(P) >= 0,  E_R(P) = sum_{r in D(P)} e_r.
  (lambda = 11: 14 - J, the identity (E); lambda = 12: 38 - E_R, or 32 - E_R for y outside R only since T[R] contributes 6.) Summing over P gives 3 sum_Y (k - 5) consistent with (C4): sum_P E_R(P) = sum_r e_r C(26-e_r,2).

**(C9) Vertex-level excess budget (B_v).** sum_{Y contains v} (k(Y) - 5) = sum_{w -> v} C(25 - e_w, 2) - 6375 >= 0 (number of pairs (Y,w) with v in Y subset N+(w): w must beat v; Y\{v} in N+(w)\{v}: C(d+(w)-1,2), d+(w) - 1 = 25 - e_w).
  Total over v gives 3 * [sum_Y k - 5*22100]: consistent.

**(C10) Venn nonnegativity for a triple.** The 8 cell counts n_S (S subset of Y = the set of y_i beaten by... ) satisfy n_{123} = k, n_{ij} = D_ij - [y_l beats both] - k >= 0 etc. These are the Bonferroni-type constraints k <= D_ij', k >= D_ij' + D_il' - d-'(y_i), m >= 0. All slack when degrees ~25 and pair counts ~12 (k <= 12 etc.), so they never bind in the near-regular regime.

Numerical anchor (balanced min case: 26 vertices e=0, 26 with e=1, 338 pairs with lambda=13, rest 12):  E k = E m = 127400/22100 = 98/17 = 5.76471;
  E C(m,2) = 314028/22100 = 14.2095 (338*286 + 988*220 = 96668 + 217360). #transitive 16250, #cyclic 5850.

## 2. The moment system in the variable u = (k - m)/2, and the IDEAL CASE (IB-min)

**Reformulation.** For a triple Y with L = L_Y = k + m put w = k - m = 2u, so k = L/2 + u, m = L/2 - u, and u >= 5 - L/2 (from k >= 5), u in Z + L/2.
Identities (C4)-(C6) become (all sums over the 22100 triples):
 (G1) sum 2u = A1 := sum_w g(e_w)   [= 0 when all e in {0,1}]
 (G2) sum 2u(L-1) = A2 := 2 sum_P [C(x_P,3) - C(lambda_P,3)],  x_P = lambda_P + 1 - e_a - e_b   [= 0 in IB-min]
 (G3) sum [C(k,2) + C(m,2)] = A3 := sum_P [C(x_P,3) + C(lambda_P,3)], and C(k,2)+C(m,2) = L^2/4 - L/2 + u^2, so sum u^2 = A3 - sum L(L-2)/4
 (G4) sum [C(k,3) - C(m,3)] = 0, and C(k,3) - C(L-k,3) = (u^3 + (3L^2/4 - 3L + 2) u)/3 [a = L/2 - 1, (u^3 + (3a^2-1)u)/3], so
      sum u^3 = -(3/4) sum L^2 u + 3 sum L u - 2 sum u.
  (Checks of the algebra: L=11,k=5: C(5,3)-C(6,3) = -10; u=-1/2: 3*121/4 = 90.75, -33, +2 gives 59.75; 59.75*(-1/2) = -29.875; plus u^3 = -0.125 gives -30; /3 = -10. OK.
   L=13,k=5: u=-3/2: 3*169/4 = 126.75 - 39 + 2 = 89.75; 89.75*(-1.5) = -134.625; u^3 = -3.375; sum -138; /3 = -46 = C(5,3) - C(8,3) = 10 - 56. OK.)

**IDEAL CASE (IB-min).** All e in {0,1} (26 vertices each: V_0, V_1); lambda = 13 on all 325 pairs inside V_1, lambda = 12 on all 325 pairs inside V_0, lambda = 12 on mixed pairs
except exactly 13 mixed pairs with lambda = 13 ('bumps'). This is precisely the configuration that minimises BOTH sum_P C(lambda_P,3) and sum_P C(x_P,3) (each = 314028 = 92950 + 71500 + 149578),
and it is forced if both sums attain their convexity minima (x_P and lambda_P all in {12,13}: 00-pairs need lambda=12, 11-pairs need lambda=13, sum lambda = 16250 fixes the 13 mixed bumps).
Then L_Y = 13 - sigma - j + C(j,2) + b_Y with j = |Y cap V_1|, b_Y = number of bump pairs in Y; j(j-3)/2 = 0,-1,-1,0 for j=0..3, so
 L = 13 - sigma  (j=0,3),   L = 12 - sigma (j=1,2),   plus b.
Class sizes: c_j = 2600, 8450, 8450, 2600. Transitive total 16250. Let T03 = transitive triples with j in {0,3}. With n := #triples with L = 13 (cyclic with j in {0,3}, plus cyclic j in {1,2} carrying a bump)
one gets (bumps assumed to hit distinct triples, b <= 1; counts re-derived twice):
 n_11 = 10400 + n,  n_12 = 11700 - 2n,  n_13 = n.   [sum 22100; sum L = 11*10400 + 12*11700 + 0*n + (11+... ) = 254800 OK: 11(10400+n) + 12(11700-2n) + 13n = 114400 + 140400 + n(11-24+13)=254800.]
Then sum L(L-2)/4 = 24.75 n_11 + 30 n_12 + 35.75 n_13 = 608400 + n/2, and **sum u^2 = Q := 628056 - 608400 - n/2 = 19656 - n/2.**
Also (G1),(G2) give class sums U_l := sum over L=l of u: U_11 + U_12 + U_13 = 0 and 11U_11 + 12U_12 + 13U_13 = 0, so (U_11,U_12,U_13) = (t,-2t,t), and sum L^2 u = 2t, so (G4): sum u^3 = -(3/2) t.

**Theorem IB0 (n = 0 version, proved by hand).** If n_13 = 0 the ideal case is impossible. Proof: n_13 = 0 forces t = U_13 = 0, so U_11 = U_12 = 0 and sum u^3 = 0.
 Class 11 (u in {-1/2, 1/2, 3/2, ...}): u^3 - u/4 = (u-1/2) u (u+1/2) >= 0, equality iff u = +-1/2. Class 12 (u in {-1,0,1,...}): u^3 - u = (u-1)u(u+1) >= 0, equality iff u in {-1,0,1}.
 So 0 = sum u^3 >= U_11/4 + U_12 = 0 forces every u to be an equality point; hence sum u^2 <= n_11/4 + n_12 = 2600 + 11700 = 14300 < 19656 = Q. Contradiction. (Same mechanism as DRT(51), margin 5356 in sum u^2.)
 Status: the arithmetic of n_ell and Q was done twice (above and via sum L = 254800, sum L(L-2)/4 = 608400, 628056 - 608400 = 19656). The ideal case itself is NOT a proof of T1.

**Correction note (added later).** In IB-min the value n = 0 is NOT realisable: exact cyclic-triple counts (Section 4, (C12)) give c_0 + c_3 = 1300 cyclic triples inside V_0^3 and V_1^3, so n >= 1300. Theorem IB0 is therefore only an illustration of the mechanism; the real statement is Lemma Theta below.

## 3. Lemma Theta: a universal pointwise certificate (proved)

Fix eps = 3/2 and, for each integer L, s_L := (3/4)(L-12)^2 - 1 = (3/4)L^2 - 18L + 107. For a triple with k + m = L and u = k - L/2 put
 r_L(u) := u^3 - (3/2) u^2 + s_L u + M(L),   M(L) := - min over lattice {u in Z + L/2, u >= 5 - L/2} of [u^3 - (3/2)u^2 + s_L u].
By definition r_L >= 0 on every u allowed by k >= 5. Values (each recomputed): 
 L=10: s=2, min at u=0 is 0, M=0.   L=11: s=-1/4, f(-1/2)=f(1/2)=f(3/2)=-3/8, M=3/8 (r_11 = (u^2-1/4)(u-3/2)).
 L=12: s=-1, f(-1)=f(1)=-3/2, M=3/2 (r_12 = (u^2-1)(u-3/2)).   L=13: s=-1/4, f(-3/2) = -51/8, M=51/8=6.375.
 L=14: s=2, f(-2) = -18, M=18.   L=15: s=23/4, f(-5/2) = -39.375, M=39.375.   L=16: s=11, f(-3) = -73.5, M=73.5.
 L=9: s=23/4, min f(1/2)=21/8, M=-21/8.  L=8: s=11, f(1)=10.5, M=-10.5.  L=7: s=71/4, f(3/2)=26.625, M=-26.625. L=6: s=26, f(2)=54. L=5: s=143/4, f(5/2)=95.625.
Summing r_{L_Y}(u_Y) >= 0 over all triples and using (G1)-(G4): with a1 = sum u = A1/2, a2 = sum L u = (A1+A2)/2,
 sum (u^3 + s_L u) = sum[u^3 + (3L^2/4 - 3L + 2)u] + sum(-15L + 105)u = 0 - 15 a2 + 105 a1.
Hence 0 <= -15 a2 + 105 a1 - (3/2) sum u^2 + sum M(L_Y), and sum u^2 = A3 - sum L(L-2)/4, which gives

 **Lemma Theta.** In every F1-tournament on 52 vertices:   A3  <=  sum_Y Theta(L_Y) - 10 a2 + 70 a1,   Theta(L) := (2/3) M(L) + L(L-2)/4.
 Theta(L) for L = 5..18: -60, -30, -9, 5, 14, 20, 25, 31, 40, 54, 75, 105, 146, 200 (e.g. Theta(13) = 4.25 + 35.75 = 40, Theta(14) = 12 + 42 = 54).
 **Theta is the cubic Theta(L) = 20 + 5z + C(z,2) + 2 C(z,3) with z = L - 10** (checked at every listed value, including negative z: z=-1 gives 20-5+1-2 = 14).
 In the balanced case (all e in {0,1}) a1 = 0 and a2 = A2/2, and A2 = 0 when the x- and lambda- sums coincide (IB-min), so the criterion is: A3 <= sum_Y Theta(L_Y).
 (Sanity check on the other side: for QR_67, L = 15 or 16, sum Theta = 3,968,745 >= A3 = 2,476,320 so no contradiction, as it must be since QR_67 has S_4.)
 Moment form: with z-bar = mean(L) - 10 and delta = L - mean, sum Theta(L) = N Theta(z-bar) + (z-bar - 1/2) sum delta^2 + (1/3) sum delta^3. For the balanced min data
 N Theta(z-bar) = 22100 * 27.925 = 617,150 and A3 = 628,056, so feasibility needs (z-bar - 1/2) sum delta^2 + sum delta^3/3 >= 10,906: the lengths of L must fluctuate.

## 4. New exact identities (all proved in this section)

**(C12) cyclic triples through a vertex.** cyc(v) = sum_{w -> v} d-(w) - C(d-(v),2). Proof: a cyclic triple through v is v -> u -> w -> v; for fixed w in N-(v) the number of u with v -> u -> w is |N-(w) cap N+(v)| = d-(w) - |N-(w) cap N-(v)| (v is not in N-(w) since w -> v) = d-(w) - lambda_{wv}; and sum_{w->v} lambda_{wv} = C(d-(v),2) by (V2).
  For e in {0,1}: cyc(v) = 325 + g(v), g(v) = number of in-neighbours of v in V_1. (Both for e_v = 0: 25*25 + g - 300, and e_v = 1: 25*26 + g - 325.)
  Check: sum_v cyc(v) = 52*325 + (arcs leaving V_1 = 26*25 = 650) = 17550 = 3 * 5850. OK.
**(C12') cyclic triples through a pair** (a -> b): d-(a) - lambda_{ab} (third vertex c with b -> c -> a; |N-(a)| minus |N-(a) cap N-(b)|, b is not in N-(a)). So transitive triples through the pair: 50 - d-(a) + lambda.
**(C13) the cross moment.** sum_Y k(Y) m(Y) = sum over ordered pairs (w,w') of C(c(w,w'),3), c(w,w') = |{z : w -> z -> w'}| = d+(w) - [w -> w'] - x_{ww'}, x_{ww'} = |N+(w) cap N+(w')| = lambda + 1 - e_w - e_w'.
  So per unordered pair {w -> w'}: C(d+(w) - 1 - x, 3) + C(d+(w') - x, 3).  (Test: QR_11 has all 55 cyclic triples with (k,m) = (1,1) and sum km = 55 = C(11,2) * [C(3,3) + C(2,3)]. OK.)
  Consequently **sum_Y L_Y^2 = 2 A3 + sum L + 2 B**, B := sum over pairs of the two terms above. This fixes Var(L) exactly from the pair data.
**(V2) head identity** sum_{a -> v} lambda_{av} = C(d-(v),2), i.e. sum_{a->v} h_{av} = e_v (25 + e_v)/2.   **(V2') tail identity** sum_{b in N+(v)} lambda_{vb} = sum_{b in N+(v)} (24 + e_b) - C(26 - e_v, 2)
  (the in-degree of b inside T[N+(v)] is d-(b) - 1 - lambda_{vb}), i.e. sum_{b in N+(v)} h_{vb} = f+(v) + (26 - e_v)(e_v - 1)/2, f+(v) := sum_{b in N+(v)} e_b.
**(V4) row sums of h.** r_v := sum_u h_{vu} = f+(v) + 26 e_v - 13 (add V2 and V2'; (25e + e^2) + (27e - 26 - e^2) = 52e - 26). Check: sum_v r_v = 650 + S2 = 2 sum_P h_P.
**(V3) vertex sum of k - m** (e in {0,1}): sum_{Y contains v} (k - m) = sum_{w->v} C(25-e_w,2) - sum_{v->w} C(24+e_w,2) = 600 e_v - 300 (the f-terms combine to 24(26 - e_v)). Hence sum_Y (k-m) E_Y = 7800.
  (Used: 300 d-(v) - 276 d+(v) - 624 + 24 e_v with d- = 25+e, d+ = 26-e gives 7500 + 300e - 7176 + 276e - 624 + 24e = 600e - 300. OK)

## 5. Audit of the ideal case with the new identities: IB-min is not a tournament

In IB-min (NT-B structure: heads of excess pairs lie in V_1): c_1 + c_2 = 4550 and c_0 + c_3 = 1300 (cyclic triples by number j of V_1-vertices), from the pair-incidence counts 3c_0 + c_1 = 325*13, 3c_3 + c_2 = 325*13, 2(c_1+c_2) = 338*13 + 13*12 + 325*14 = 9100.
So the L=13 class has n = 1300 + (cyclic j in {1,2} triples through a bump) = 1456 when no triple contains two bumps, and sum L^2 = 2,946,112 + S, S := sum w_v^2 + sum t_v^2 (w_v = bumps with head v, t_v = bumps with tail v).
But (C13) gives sum L^2 = 2,946,424 (A3 = 628,056; B = 717,756; 2A3 + 254,800 + 2B). So S = 338, impossible for 13 distinct bump pairs (max S = 169 + 13 = 182 for a star). Hence **no tournament at all has the IB-min pair data.**
Then Lemma Theta is not needed for IB-min. The meaningful question is the general NT-B family (next section).

## 6. Theorem NT-B01 (proved by hand; F1 is NOT used)

**Theorem NT-B01.** No tournament on 52 vertices has all in-degrees in {25, 26} and all pair counts lambda_P = |D(P)| in {12, 13}.

Proof (each step re-checked, N = 52 throughout). V_0 = {d- = 25}, V_1 = {d- = 26}; sum d- = 1326 = 52*25 + 26 gives |V_1| = 26 = |V_0|. Arcs: inside V_0: 325; inside V_1: 325; V_0 -> V_1: 26*26 - 325 = 351; V_1 -> V_0: 26*25 - 325 = 325.
Write f(v) = |N+(v) cap V_1|. d+ = 26 on V_0, 25 on V_1.
1. (V2) sum_{a->v} lambda_{av} = C(d-(v),2) (lambda_{av} is the in-degree of a in T[N-(v)]). For v in V_0: 300 = 25*12, so lambda_{av} = 12 for every a -> v. For v in V_1: 325 = 26*12 + 13.
   Hence a pair with lambda = 13 has its head (the beaten endpoint) in V_1.
2. (V2') for v: sum_{b in N+(v)} lambda_{vb} = sum_{b in N+(v)} (d-(b) - 1) - C(d+(v),2) [in-degree of b in T[N+(v)] is d-(b) - 1 - lambda_{vb}].
   v in V_1: 24*25 + f(v) - 300 = 300 + f(v), i.e. sum (lambda - 12) = f(v).  v in V_0: 24*26 + f(v) - 325 = 299 + f(v), i.e. sum (lambda - 12) = f(v) - 13.
3. Out-neighbours of v in V_1 lying in V_0 have lambda = 12 (head in V_0). So the f(v) out-arcs of v inside V_1 carry total excess f(v) with each excess in {0,1}: all pairs inside V_1 have lambda = 13.
   For v in V_1, step 1 gives 13 = (25 - f(v)) + w_v, w_v := #{a in V_0, a -> v, lambda_{av} = 13}, so w_v = f(v) - 12 >= 0.  For v in V_0: t_v := #{b in V_1, v -> b, lambda_{vb} = 13} = f(v) - 13 >= 0.
   t_v and w_b are the degrees of the bipartite graph G on V_0 u V_1 formed by the mixed pairs with lambda = 13; |E(G)| = sum t_v = 351 - 338 = 13 = sum w_b (sum_{V_1} f = 325 = 312 + 13).
4. Cyclic triples through an arc a -> b: d-(a) - lambda_{ab} (c in N+(b) cap N-(a); b is not in N-(a)). Let c_j = #cyclic triples with j vertices in V_1. A cyclic triple with j in {1,2} has exactly two mixed pairs, j in {0,3} none. So
   2(c_1 + c_2) = sum over V_0->V_1 arcs (25 - lambda) + sum over V_1->V_0 arcs (26 - 12) = (351*25 - (351*12 + 13)) + 325*14 = (8775 - 4225) + 4550 = 9100, c_1 + c_2 = 4550.
   Total cyclic triples = 22100 - sum_v C(d+(v),2) = 22100 - (26*325 + 26*300) = 22100 - 16250 = 5850. So c_0 + c_3 = 1300.
5. A triple inside V_1 is transitive iff it has a source, so #transitive = sum_{v in V_1} C(f(v),2) and c_3 = 2600 - sum_{V_1} C(f,2). Likewise c_0 = 2600 - sum_{v in V_0} C(26 - f(v), 2).
   So sum_{V_1} C(f,2) + sum_{V_0} C(26 - f,2) = 5200 - 1300 = 3900.
6. Substitute f = 12 + w_v on V_1 and 26 - f = 13 - t_v on V_0: sum_{V_1} C(12+w,2) = 26*66 + 11.5*13 + (sum w^2)/2 = 1865.5 + (sum w^2)/2; sum_{V_0} C(13-t,2) = 26*78 - 12.5*13 + (sum t^2)/2 = 1865.5 + (sum t^2)/2.
   Total 3731 + S/2 with S := sum w_b^2 + sum t_v^2. Setting 3731 + S/2 = 3900 gives S = 338.
7. But S = sum over edges e = (v,b) of G of (t_v + w_b), and t_v + w_b <= |E(G)| + 1 = 14 (the edge vb is counted in both). So S <= 13*14 = 182 < 338. Contradiction. QED.
Cross-checks of the numbers: (a) with the 'spread' choice w, t in {0,1} the left side of step 5 equals 3744 (13*66 + 13*78 = 858 + 1014 = 1872 per class), i.e. S = 26 (3731 + 13 = 3744), consistent. (b) The same S = 338 arises independently from the identity (C13)+(G3): sum L^2 = 2A3 + sum L + 2B (Section 5, A3 = 628056, B = 717756, sum L^2 = 2,946,424 versus structural 2,946,086 + S). Two independent routes agree.
Remark: the proof uses only degrees, V2, V2' and cyclic-triple counts. It shows the 'doubly-regular-like' data (all lambda in {12,13}, balanced degrees) is not realisable by ANY tournament.

**Generalisation (NT-B, proved by the same steps).** If all e in {0,1} and all lambda >= 12 (no tight pair, h = lambda - 12 >= 0 arbitrary), steps 1-2 and 4-5 hold verbatim:
 (a) h = 0 on every pair whose head is in V_0; (b) sum_{b in N+(v)} h_{vb} = f(v) (v in V_1), = f(v) - 13 (v in V_0), so **f(v) >= 13 for every v in V_0** with sum_{V_0}(f - 13) = 13;
 (c) the in-weight at every v in V_1 is exactly 13; (d) c_0 + c_3 = 1300 (step 4 used only sum_{C} lambda = 4225, which follows from (b)), hence sum_{V_1}C(f,2) + sum_{V_0}C(26-f,2) = 3900, equivalently
     **sum_{v} (f(v) - mean of its class)^2 = 325** (classes V_0: mean 13.5, V_1: mean 12.5). Since V_0 contributes at most 162.5 (f >= 13, sum (f-13) = 13), **the 26 vertices of V_1 must have sum (f - 12.5)^2 >= 162.5**, i.e. T[V_1] is far from regular
     (its number of cyclic triples c_3 <= 650 versus the maximum 728).
 (e) the weights d_ab = lambda_ab - 12 on arcs inside V_1 satisfy: out-weight(v) = outdeg_{V_1}(v) = f(v), in-weight(v) = 13 - w_v. So the average lambda over V_1-internal pairs is 13 but individual values must spread (some 12, some >= 14) as soon as f is dispersed.
 So the remaining balanced/no-tight configurations are exactly those with f strongly dispersed on V_1. They are not excluded by Lemma Theta (see Section 7).

<!-- END -->

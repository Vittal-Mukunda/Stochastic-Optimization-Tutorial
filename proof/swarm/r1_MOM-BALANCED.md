# r1_MOM-BALANCED: moment method in the balanced (H1) and no-tight-pair (H2) sub-cases, N = 52

Lane: MOM-BALANCED. Hand derivations only. Written 24 Oct 2026.

## Status (keep current)
- Nothing proved yet. File just created. Plan: (1) exact moment bookkeeping for H1; (2) H2 pair-count constraints; (3) feasibility margin.

## Plan
1. Setup and exact identities for H1 (all in-degrees 25/26).
2. Triple classification by (#V26, sigma), the L_Y formula.
3. H2 refinement.
4. Relaxation, margin.

## 1. Notation and exact H1 bookkeeping (N = 52)

H1: every in-degree is 25 or 26. Sum d- = 1326 = 52*25 + 26, so exactly 26 vertices have d- = 26.
G := V25 (d- = 25, d+ = 26), H := V26 (d- = 26, d+ = 25); |G| = |H| = 26.
Arcs: inside G 325, inside H 325, between 676. Out-degrees of G sum to 26*26 = 676 = 325 + t, so t = #(G->H arcs) = 351, and H->G = 325. (Check: out-degrees of H sum to 650 = 325 + 325. ok)

Triples by a = #H-vertices: 2600, 8450, 8450, 2600 (a = 0,1,2,3). Transitive triples 16250, cyclic 5850.

Pair data: D_P = |D(P)|; m_P = |N+(w) ∩ N+(w')| = D_P + 51 - d-(w) - d-(w') (derived: of the 50 other vertices, those beating at least one
of w,w' number d-(w)+d-(w')-1-D_P, so common out = 50 - that = 51 - d-(w) - d-(w') + D_P). So m = D+1, D, D-1 for (G,G),(G,H),(H,H).
Sum_P D_P = sum_w C(d+(w),2) = 26*325 + 26*300 = 8450 + 7800 = 16250.  Also sum_P m_P = sum_v C(d-(v),2) = 26*300 + 26*325 = 16250.

Triple identity (re-derived): outside vertices 49; D+(Y) = 49 - sum_i |N-(y_i) \ Y| + sum_{i<j} |D(y_i,y_j) \ Y| - |D(Y)|,
sum_i |N-(y_i)\Y| = sum d- - 3, and exactly sigma(Y) of the three pairs have the third vertex among their dominators
(transitive: the top vertex beats the other two: exactly one pair). Hence
   k(Y) + l(Y) = L_Y := 52 - sum_i d-(y_i) + sum_{i<j} D_ij - sigma(Y),   l(Y) := |D+(Y)|.        (1.1)
With the degree pattern a = #H in Y and all D_ij = 12:  L = 88 - (75 + a) - sigma = 13 - a - sigma.  [a=0: 13 - s; a=1: 12 - s; a=2: 11 - s; a=3: 10 - s.]
In general L_Y = 13 - a - sigma + X_Y,  X_Y := sum_{pairs in Y} x_P,  x_P := D_P - 12.

Exact sums (H1; re-checked):
 * sum_Y k = sum_w C(d+(w),3) = 26*C(26,3) + 26*C(25,3) = 26*2600 + 26*2300 = 127400.   mean 5.7647 = 98/17.
 * sum_Y l = sum_z C(d-(z),3) = 26*2300 + 26*2600 = 127400.  Hence sum_Y L_Y = 254800 (checked independently:
   52*22100 - 1326*1275 + 50*16250 - 16250 = 1149200 - 1690650 + 812500 - 16250 = 254800. ok).
 * sum_Y (k-5) = 127400 - 110500 = 16900 = 50*338.
 * sum_Y C(k,2) = sum_P C(m_P,3);  sum_Y C(l,2) = sum_P C(D_P,3).   [l counts z with Y in N-(z); two such z, z' : Y in N-(z) cap N-(z'),
   and |N-(z) cap N-(z')| = D({z,z'}).]   Both >= 314028 for any integers with sum 16250 over 1326 pairs: 988*220 + 338*286 = 217360 + 96668 = 314028.
 * sum_Y C(k(Y),3) = sum_W C(l(W),3): both count pairs (Y,W) of triples with every vertex of W beating every vertex of Y
   (fixed Y: W inside D(Y); fixed W: Y inside D+(W)).  So sum_Y [C(k,3) - C(l,3)] = 0 (the triples W range over all triples as well).

 * 4-set identities. #TT4 (transitive 4-sets) = sum_{Y trans} k(Y) = sum_{Y trans} l(Y)  (a TT4 {w,t,m,s} is counted once by removing its source
   in the k-count and once by removing its sink in the l-count). Since sum k = sum l in H1, also sum_{cyc} k = sum_{cyc} l.
   So in H1:  sum_{trans} (k-l) = 0 and sum_{cyc} (k-l) = 0.                                           (1.2)

 * a-weighted sums.  sum_Y k*a(Y) = sum_w C(d+(w)-1,2) * h+(w), h+(w) := |N+(w) cap H|. Sum over w in G of h+(w) = 351, over w in H = 325 (arcs inside H).
   C(d+-1,2) = C(25,2) = 300 for w in G, C(24,2) = 276 for w in H.  So sum k*a = 300*351 + 276*325 = 105300 + 89700 = 195000.
   sum_Y l*a = sum_z C(d-(z)-1,2) * h-(z): z in G: C(24,2) = 276, sum h-(z) = H->G arcs = 325; z in H: C(25,2) = 300, sum = 325.
   So sum l*a = 276*325 + 300*325 = 89700 + 97500 = 187200.   Hence  sum_Y (k-l) a = 7800, i.e. sum_Y u_Y a_Y = 3900, u := (k-l)/2.   (1.3)
   Cross-check (done, passes): sum_Y (k+l) a = 195000 + 187200 = 382200 must equal sum_Y L_Y a_Y = sum (13 - a - sigma + X) a.
   sum a = 33150; sum a^2 = 8450*1 + 8450*4 + 2600*9 = 65650; sum 13a = 430950; sum sigma*a = (by top vertex w, pairs in N+(w)):
   w in G: 25*h+(w), total 25*351 = 8775; w in H: C(25,2) + 24 h+(w), total 26*300 + 24*325 = 7800 + 7800 = 15600; so 24375.
   sum X*a (section 2 data) = 13*75 + 325*124 = 41275.  Then 430950 - 65650 - 24375 + 41275 = 382200. OK.

## 2. Case H1 + H2: the irregularity x_P = D_P - 12 has a rigid directed structure (NEW, proved)

H2: no tight pair, so D_P >= 12 for all P. Put x_P = D_P - 12 >= 0.  Sum_P x_P = 16250 - 15912 = 338 (12*1326 = 15912).

**Lemma 2.1 (in-neighbourhoods).** Assume H1, H2. For v in G: T[N-(v)] is a 12-regular tournament on 25 vertices, so x(a,v) = 0 for every a in N-(v).
For v in H: sum_{a in N-(v)} x(a,v) = 13.   (x(a,v) := x_{a,v}.)
*Proof.* a in N-(v): the in-degree of a in T[N-(v)] is |N-(a) cap N-(v)| = |D({a,v})| (a vertex beating both a and v lies in N-(v) and beats a;
conversely). The in-degrees in a tournament on d-(v) vertices add to C(d-(v),2). v in G: C(25,2) = 300 = 25*12 and each is >= 12 (H2), so all equal 12.
v in H: C(26,2) = 325 = 26*12 + 13. QED.

So x is supported on pairs {a,h} with a -> h and h in H ("arcs whose head is in H"); G->G, H->G arcs carry x = 0.  Totals: G->H arcs carry 13, H->H arcs carry 325
(338 = 26*13 and H->G, G->G carry 0; the split is Lemma 2.2).

**Lemma 2.2 (out-neighbourhoods).** Assume H1, H2. For v in G: g+(v) + X+(v) = 13, where g+(v) = |N+(v) cap G|, X+(v) = sum_{a in N+(v) cap H} x(v,a).
In particular g+(v) <= 13 for all v in G, sum_{v in G}(13 - g+(v)) = 338 - 325 = 13 = total x on G->H arcs.
For v in H: sum_{a in N+(v) cap H} x(v,a) = h+(v) := |N+(v) cap H|. Total x on H->H arcs = 325.
*Proof.* a in N+(v): out-degree of a inside T[N+(v)] is m(a,v) = D_{av} + 51 - d-(a) - d-(v). Out-degrees add to C(d+(v),2).
v in G (d-=25, d+=26): m = 13 + x(v,a) if a in G (x=0 then), m = 12 + x(v,a) if a in H. Sum = 13 g+ + 12 h+ + X+ = 12*26 + g+ + X+ = 325, so g+ + X+ = 13.
v in H (d-=26, d+=25): m = 12 (a in G, x = 0), m = 11 + x(v,a) (a in H). Sum = 12*(25 - h+) + 11 h+ + X+ = 300 - h+ + X+ = 300. QED.
Consistency: sum_{v in G} g+ = 325, so G->H x-mass = 26*13 - 325 = 13 and H->H x-mass = sum_{v in H} h+(v) = 325. Total 338. ok.

**Consequences.**
(i) T[G] is a 26-vertex tournament with all out-degrees <= 13 (d_v := 13 - g+(v) >= 0, sum d_v = 13). #transitive triples in G = sum C(13 - d_v, 2) = (3731 + sum d_v^2)/2.
   [ (13-d)(12-d)/2 = (156 - 25 d + d^2)/2; 26*156 = 4056; 25*13 = 325; 4056 - 325 = 3731.] Minimum 1872 (13 d_v = 1), so >= 1872.
(ii) G->H x-mass: X+(v) = d_v, so the vertex v in G with g+(v) = 13 sends no weighted arc into H; a vertex with d_v >= 1 has x-weighted out-arcs into H summing to d_v.
(iii) For h in H: sum over in-neighbours of x = 13; sum over HH out-neighbours of x = outdeg_H(h). Writing gamma_h = G->h x-mass (sum_h gamma_h = 13), HH in-mass of h = 13 - gamma_h.
(iv) Every x_P <= 13 (x(a,h) <= in-mass(h) = 13 - gamma_h <= 13).
(v) The minimum 314028 of sum_P C(m_P,3) is attained iff every HH pair has x = 1 and exactly 13 G->H arcs have x = 1 ("pattern M*_min", S2 = 338).
    Section 3 shows that M*_min is impossible.

## 3. More exact identities in H1 + H2 (NEW; each re-derived and cross-checked)

Notation: x_P = D_P - 12; d_v := 13 - g+(v) (v in G, sum d_v = 13); o_w := |N+(w) cap H| (w in H, sum o_w = 325); omega_w := 25 - o_w = |N+(w) cap G|.
Arc types: GG (x=0), H->G (x=0), G->H (x total 13; out-mass of v in G is d_v), HH (x total 325; out-mass of w is o_w; in-mass of h is 13 - gamma_h, gamma_h := G-tail mass into h, sum gamma = 13).

**(3.1) cyclic triples through an arc a->b:** cyc(a->b) = |N+(b) cap N-(a)| = d+(b) - m_P  (a is not in N+(b)).  Values: GG: 26-13 = 13; H->G: 26-12 = 14;
G->H: 25-(12+x) = 13-x; HH: 25-(11+x) = 14-x.   [check: total = 325*13 + 325*14 + (351*13-13) + (325*14-325) = 4225+4550+4550+4225 = 17550 = 3*5850. ok]

**(3.2) Star identity (STAR).** Counting the cyclic triples through GG-arcs in two ways: sum over GG arcs of cyc = 4225 = 3*c_0 + c_1, where c_a = #cyclic triples with a H-vertices.
c_0 = 2600 - sum_v C(13-d_v,2) = (1469 - sum d_v^2)/2;   c_1 = 8450 - t_1, t_1 = sum_{v in G}(13-d_v)(13+d_v) + sum_{w in H} C(omega_w,2) = 4394 - sum d^2 + (sum omega^2 - 325)/2.
Solving:   **sum_{w in H} o_w^2 + sum_{v in G} d_v^2 = 4394.**   (STAR)       (sum o^2 = sum omega^2 because sum omega = 325 = sum o... indeed sum(25-o)^2 = 16250 - 50*325 + sum o^2.)
(The HH-version, 3 c_3 + c_2 = 4225, gives the same equation: verified.)  Consequences: sum (o_w - 12.5)^2 = 331.5 - sum d_v^2 in [162.5, 318.5]: **T[H] is far from regular**.
Also all cyclic counts follow: c_0 = (1469 - sum d^2)/2, c_3 = 1300 - c_0, c_1 = 4225 - 3 c_0, c_2 = 325 + 3 c_0.
(A pattern "d_v, gamma_h in {0,1}" with x = 1 on every HH pair -- which has o_w = 12 + gamma_w -- would need sum gamma^2 + sum d^2 = 338, which for sum d = sum gamma = 13 forces
d = 13*delta_{v0}, gamma = 13*delta_{h0}.  So the naive "minimal excess" pattern M*_01 does not exist; an earlier draft of this section used it; DISCARD any 0/1 pattern.)

**(3.3) Exact sums of L.**  sum L0^2 = 2,581,150 (L0 := 13-a-sigma; from sum a = 33150, sum a^2 = 65650, sum sigma = 16250, sum sigma*a = 24375);
sum L0*X = 13*16900 - 41275 - (12181 + S2) = 166244 - S2 where S2 := sum_P x_P^2 and
sum sigma*X = sum_{GH} x(37+x) + sum_{HH} x(36+x) = 12181 + S2  [trans(P) = 50 - cyc(P)];  sum a*X = 13*75 + 325*124 = 41275;
sum X^2 = 48*S2 + sum_v xi_v^2, xi_v := sum_{P containing v} x_P  (xi_v = d_v for v in G; xi_w = 13 + o_w for w in H)  [X^2 = sum_P x_P^2 + 2 sum over pairs of pairs; pairs of pairs sharing a vertex lie in exactly one triple].
Therefore, using (STAR):
   **sum_Y L_Y^2 = 2,930,876 + 46*S2**,   S2 = sum_P x_P^2 >= 338.                                  (3.3)
[Check: for S2 = 338 this is 2,946,424.]

**(3.4) Second-moment identity in H1+H2.**  With k = L/2 + u (u = (k-l)/2):
   sum C(k,2) - sum C(l,2) = sum (L-1)u = sum_P [C(m_P,3) - C(D_P,3)] = 162.5 - S2_H/2 = -eta,  eta := sum_{HH} C(x,2) >= 0,   (3.4a)
 [GG: 325*(286-220) = 21450; GH, HG: 0; HH: -sum C(11+x,2) = -(21287.5 + S2_H/2).]  Hence sum L u = -eta (as sum u = 0).
   sum_Y u_Y^2 = 755456 + 2 ex - (sum L^2)/4 - sum L u = 22,737 + 2 ex - 11.5 S2 + eta,                      (3.4b)
 where ex := sum_P C(m_P,3) - 314028 = sum_{GH} f_G(x) + sum_{HH} f_H(x) >= 0, f_G(x) = C(12+x,3) - 220 - 66x (0,0,12,37,...), f_H(x) = C(11+x,3) - 220 - 66(x-1) (11,0,0,12,37,...).
 [755456 = 2*314028 + 127400; 2,930,876/4 = 732,719.]

**(3.5) Cubic identity.** sum_Y [u^3 + c(L_Y) u] = 0 with c(L) = (3/4)(L-2)^2 - 1  (c(11)=59.75, c(12)=74, c(13)=89.75). [From C(k,3)-C(l,3) = (u^3+(3a^2-1)u)/3, a = L/2-1.]

**(3.6) A universal pointwise certificate (theta = 2/3).**  For each triple, with (u, L):  u^2 <= (2/3)(u^3 + c(L)u) + (70 - 10L)u + lambda(L)
where lambda(L) := max over admissible u (u = k - L/2, k >= 5, l = L-k >= 0) of [u^2 - (2/3)(u^3 + c(L)u) - (70-10L)u].  Values (hand computed; u-lattice is {5-L/2, 6-L/2, ...}):
 lambda(11) = 1/4 (zeros at u = -1/2, 1/2, 3/2: the polynomial is (2/3)(u+1/2)(u-1/2)(u-3/2)+0),  lambda(12) = 1 (poly (1/3)(u-1)(u+1)(2u-3)),  lambda(13) = 17/4 (zero at u=-3/2, min >= 0 for u >= -3/2),
 lambda(10) = 0, lambda(9) = -7/4, lambda(14) = 12, lambda(15) = 105/4, lambda(16) = 49.
Summing over all triples and using sum(u^3 + c u) = 0 and sum u = 0, sum L u = -eta:
   **sum u^2 <= sum_Y lambda(L_Y) + 10 eta**.                                   (3.6)
Combined with (3.4b): 755456 + 2ex + eta - sum L^2/4 <= sum lambda(L_Y) + 10 eta, i.e.  **755456 + 2 ex <= sum_Y Lambda(L_Y) + 9 eta**, Lambda(L) := lambda(L) + L^2/4:
 Lambda(9..16) = 18.5, 25, 30.5, 37, 46.5, 61, 82.5, 113.   (quadratic majorant 37 + 8(L-12) + 1.5(L-12)^2 touches at 11,12,13; below at L<=10; above by 2, 8, 20 at L=14,15,16.)

## 4. Consequences of (STAR) and the mass conditions (H1 + H2; all proved)

Put s_h := o_h - 12 (h in H), so sum s_h = 13, o_h = 12 + s_h, in-degree of h inside T[H] = 25 - o_h = 13 - s_h.  For an HH arc a->h put y := x - 1.
By Lemma 2.2 (out-mass) and Lemma 2.1 (in-mass), for every h in H:  sum over HH out-arcs of y = 0  and  sum over HH in-arcs of y = (13 - gamma_h) - (13 - s_h) = s_h - gamma_h =: b_h.
Also sum_h b_h = 0, and eta = sum_{HH} C(x,2) = (1/2) sum_{HH} y(y+1).

**Proposition 4.1.** Assume H1 and H2.
 (a) sum_{h in H} (o_h - 12.5)^2 = 331.5 - sum_{v in G} d_v^2 >= 162.5   (d_v >= 0, sum d_v = 13 so sum d_v^2 <= 169).
 (b) Some pair has D_P >= 14 (x_P >= 2).  In particular the "minimal" pattern x in {0,1} (S2 = 338) cannot occur.
 (c) eta >= B := sum_h (-b_h)^+ >= N^- := sum_h s_h^-, and N^- >= (169 - sum d_v^2)/25.
*Proof.* (a) sum o^2 = 4394 - sum d^2 by (STAR); sum (o-12.5)^2 = sum o^2 - 25*325 + 26*156.25 = sum o^2 - 4062.5.
(b) Suppose all x <= 1.  An HH arc has x = 1 or 0; out-mass of w equals the number o_w of its HH out-arcs, so every HH out-arc has x = 1: all HH arcs have x = 1.
 Then in-mass of h = in-degree: 13 - gamma_h = 13 - s_h, so s_h = gamma_h >= 0.  Then sum s^2 <= (sum s)^2 = 169 (s >= 0).  (STAR): 4394 = sum o^2 + sum d^2
 = (26*144 + 24*13 + sum s^2) + sum d^2 = 4056 + sum s^2 + sum d^2, so sum s^2 + sum d^2 = 338, forcing sum s^2 = sum d^2 = 169, hence a single d_{v0} = 13 and a single gamma_{h0} = 13.
 The G->H x-mass 13 sits on the out-arcs of v0 and the in-arcs of h0, so the arc v0->h0 carries x = 13 >= 2.  Contradiction.
(c) sum over HH arcs of y is 0 and y >= -1.  Let Z be the number of arcs with y = -1; then sum_{y>0} y = Z, and C(x,2) = y(y+1)/2 >= y for y >= 1, so eta >= Z.
 Each head h with b_h < 0 has at least -b_h in-arcs with y = -1, so Z >= B.  For s_h < 0, b_h = s_h - gamma_h <= s_h, so B >= N^-.
 Finally sum s = 13 and each s_h^+ <= 13, s_h^- <= 12 give sum s^2 <= 13(13 + N^-) + 12 N^- = 169 + 25 N^-, while sum s^2 = 338 - sum d^2 (STAR). QED.

**Proposition 4.2 (a G-vertex with no out-neighbour in G).**  Assume H1, H2 and that some v0 in G has g+(v0) = 0 (equivalently d_{v0} = 13).  Then
 N+(v0) = H, N-(v0) = G' := G \ {v0}, T[G'] is 12-regular; there is exactly one h0 in H with o_{h0} = 25 (h0 beats all of H' := H \ {h0}, and every vertex of G beats h0),
 every h in H' has o_h = 12 (T[H'] is 12-regular), x(v0,h0) = 13 (D({v0,h0}) = G', 25 vertices), x(v0,h) = 0 for h in H', and every other G->H arc has x = 0.
 Moreover x(h0,h) = 1 for all h in H'.
*Proof.* g+(v0) = 0: every vertex of G beats v0, and d-(v0) = 25 = |G'|, so N-(v0) = G', N+(v0) = H.  For h in H, D({v0,h}) = N-(v0) cap N-(h) = G' cap N-(h).
 |G cap N-(h)| = d-(h) - |H cap N-(h)| = 26 - (25 - o_h) = 1 + o_h, and v0 is one of them (v0 -> h), so |G' cap N-(h)| = o_h.  Thus o_h = 12 + x(v0,h), i.e. s_h = x(v0,h) >= 0.
 Since sum d^2 = 169 (d_{v0} = 13, other d = 0), (STAR) gives sum s^2 = 169; with s >= 0 and sum s = 13 this forces one s_{h0} = 13, others 0.  The G->H x-mass is entirely on arcs out of v0
 (out-mass of v0 is d_{v0} = 13, the others have d = 0) so every G->H arc other than those of v0 has x = 0; x(v0,h) = s_h.  T[G']: each g in G' has g+(g) = 13 - 0 = 13 including v0, so 12 inside G': regular.
 h0 beats the 25 vertices of H' (o = 25), each h in H' has o_h = 12 inside H'.  D({h0,h}) for h in H': vertices beating h0 (= all G, since N-(h0) has 26 = |G| elements all in G) and h:
 = {v0} cup (G' cap N-(h)) of size 1 + 12 = 13, so x(h0,h) = 1.  QED.
(This is the structure "M*_ext": two vertices v0, h0, and 25 + 25 other vertices.)

**Proposition 4.3 (the family of 4.2: a moment contradiction up to HH defects).**  In the situation of 4.2, the 50 triples Y = {v0,h0,y} have k(Y) = l(Y) = 12 (so u = 0, L = 24), and every tournament in this family satisfies
        2450 + 2 ex_H <= 147 eta + E,
 where eta = sum_{HH} C(x,2), ex_H = sum_{HH} f_H(x) >= 0 and E >= 0 is the tail term of the certificate (E = sum over triples with L >= 14 of Lambda(L) - Lambda_q(L); E = 0 if all L <= 13).
 In particular **if every HH arc has x = 1 (eta = 0, no defects) the family is impossible**; in general it needs eta >= 17 (or E >= 2450 - 147 eta).
*Proof.* k({v0,h0,y}) = |D({v0,h0}) cap N-(y)| = |G' cap N-(y)|: for y in G' this is the in-degree of y in the 12-regular T[G'], 12; for y in H' it is o_y = 12 (shown in 4.2).
 l = |D+(Y)|: v0 beats all of H, h0 beats H', so D+(Y) = H' cap N+(y), which has 12 elements for y in G' (y beats h0 and 12 vertices of H', since h+(y) = 13) and for y in H' (o_y = 12 inside H').
 Hence u = 0 on these 50 triples, and they contribute nothing to sum u, sum Lu, sum (u^3 + c u), sum u^2.  Apply (3.6) to the other 22050 triples:
 sum_ns u^2 <= sum_ns lambda(L) + 10 eta.  Now S2 = 169 + (325 + 2 eta) = 494 + 2 eta; sum L^2 = 2,930,876 + 46 S2 (3.3) and the 50 special triples have L = 24 (L = k + l), so
 sum_ns (L-12) = -10400 - 600 = -11000 and sum_ns (L-12)^2 = (46 S2 - 1924) - 7200 = 46 S2 - 9124.  With the quadratic majorant (Lambda <= Lambda_q for L <= 13, plus E for L >= 14),
 sum_ns lambda(L) <= sum_ns Lambda_q - sum_ns L^2/4 + E = (815,850 - 88,000 + 1.5(46 S2 - 9124)) - (2,930,876 + 46 S2 - 28,800)/4 + E = -11,355 + 57.5 S2 + E.
 On the other hand (3.4b): sum u^2 = 22,737 + 2 ex - 11.5 S2 + eta with ex = 1222 + ex_H [f_G(13) = C(25,3) - 220 - 66*13 = 1222].  Hence 22,737 + 2444 + 2 ex_H - 11.5 S2 + eta <= -11,355 + 57.5 S2 + E + 10 eta,
 i.e. 36,536 + 2 ex_H <= 69 S2 + 9 eta + E = 34,086 + 147 eta + E.  QED.
 [Check, defect-free: sum L^2 = 121*12300 + 144*8450 + 169*1300 + 576*50 = 1,488,300 + 1,216,800 + 219,700 + 28,800 = 2,953,600 = 2,930,876 + 46*494. ok.
  Non-special class counts: trans a in{1,2}: 12350 - 50 = 12300 (L = 11), trans a in{0,3}: 3900 and cyc a in {1,2}: 4550 (L = 12), cyc a in {0,3}: 1300 (L = 13); from t_0 = 1950, c_0 = 650, t_1 = t_2 = 6175, c_1 = c_2 = 2275.
  sum_ns u^2 <= (1/4)12300 + 8450 + (17/4)1300 = 3075 + 8450 + 5525 = 17,050 < 19,500 = required.]

## 5. The moment system: master inequality, exact margin, and its limits

**Master inequality (H1+H2, proved).**   755456 + 2 ex <= sum_Y Lambda(L_Y) + 9 eta,   Lambda(L) = lambda(L) + L^2/4 (values in 3.6).
Using Lambda <= Lambda_q := 37 + 8(L-12) + 1.5 (L-12)^2 for L <= 13 and (3.3):  sum Lambda_q = 731,614 + 69 S2, so
        **23,842 + 2 ex <= 69 S2 + 9 eta + E_tail**   (E_tail = sum over L >= 14 of Lambda - Lambda_q;  e(14),e(15),e(16),e(17),e(18) = 2, 8, 20, 40, 70).        (5.1)
A tournament satisfying H1+H2 must satisfy (5.1).  Writing S2 = 338 + sum_{pairs} x(x-1), (5.1) reads
        520 + sum_{pairs} [2 f(x) - 69 x(x-1)] - 9 eta <= E_tail,
with per-pair terms 2f(x) - 69x(x-1) - [HH] 4.5 x(x-1):  HH: x = 0: +22 (since x(x-1) = 0 there), x = 2: -147, x = 3: -417 [24 - 414 - 27], x = 4: -808; GH: x = 2: -114, x = 3: -340 (relative to the baseline x in {0,1}).
[Recomputed: HH x=2: 0 - 69*2 - 9 = -147; x=3: 24 - 69*6 - 27 = -417; GH x=2: 24 - 138 = -114; x=3: 74 - 414 = -340.]

 * **Idealised best case.**  If x were in {0,1} (S2 = 338, ex = eta = 0, all L in {11,12,13}) then the left side of (5.1) is 23,842 and the right side 23,322: margin **520** in sum Lambda
   (equivalently the required sum u^2 = 18,850 versus the certificate bound 18,330; margin 2.8%).  This pattern does not exist (Prop 4.1(b)), so this is only the margin of the *ideal* system.
 * **Cost of spreading the pair counts.**  Each unit of S2 above 338 costs 69 in (5.1); each HH 'defect' (an arc with x = 2 together with an arc x = 0) costs about 125.  Hence (5.1) forces
   either E_tail > 0 or S2 >= 346 (take eta = ex = 0 as the best case).  In particular the certificate rules out only patterns with at most about 3 defects.  Prop 4.1(c) shows that a generic
   H1+H2 tournament has many more defects (e.g. sum d^2 = 13 forces N^- >= 9, hence eta >= 9) or the extreme structure of Prop 4.2 (which Prop 4.3 handles up to eta >= 17).
 * **Hard limit of any argument of this type.**  From (3.4b), sum u^2 = 22,737 + 2 ex - 11.5 S2 + eta >= 0, so the moment identities with u == 0 are consistent as soon as
   S2 >= 1977 + (2 ex + eta)/11.5: if the pair counts D_P are spread enough, k(Y) = L(Y)/2 is not contradicted by anything above (the variance requirement is then met by the variance of L alone).
   Therefore **any proof must control the spread of the pair counts D_P** (show S2 - 338 is small, i.e. D_P in {12,13} for almost all pairs), or must use information beyond sums over all triples.

## 6. The general balanced case H1 (H2 dropped): the same package without H2  (proved formulas; not exploited)

In H1 alone put x_P = D_P - 12 >= -1 (x = -1 iff P is tight).  Still sum x = 338, sum_Y L = 254800, sum_Y (k-l) = 0, and (derived exactly as in sections 1-3):
 * Lemma 2.1 and 2.2 hold verbatim with x allowed to be negative: for v in G, sum_{a->v} x(a,v) = 0 and sum_{v->a} x(v,a) = d_v := 13 - g+(v) (here d_v may be negative);
   for v in H, sum_{a->v} x = 13 and sum_{v->a} x = o_v.  Hence xi_v = sum_{P containing v} x_P equals d_v (v in G) and 13 + o_v (v in H), exactly as before.
 * (STAR') sum d_v^2 + sum o_w^2 = 4394 + 2 X_GG, X_GG := sum over GG pairs of x_P.  [Same derivation: sum over GG arcs of cyc = 8450 - sum(13 + x) = 4225 - X_GG.]
 * sum_Y L^2 = 2,990,806 + 46 S2 + (sum d^2 + sum o^2) - 2[49 X_GH + 48 X_HG + 97 X_HH],  S2 = sum_P x_P^2.  (For H2 this is 2,930,876 + 46 S2: checked.)
   [Uses trans(P) = 62 - d-(tail) + x_P, sum_Y a X = sum_P x_P (49 a_P + 26), sum X^2 = 48 S2 + sum xi^2.]
 * sum_Y L u = 3575 + 11.5 X_GG - 10.5 X_HH + (S2_GG - S2_HH)/2, and sum C(k,2) = sum_P C(m_P,3), with m_P = D_P + (1, 0, -1) for (GG, mixed, HH) pairs.
 * Master inequality (H1):  2 sum_P C(m_P,3) + 127400 + 9 sum L u <= 734,500 + 1.5 (sum L^2 - 2,932,800) + E_tail.
 What is missing for H1 is control of the tight-pair terms (x = -1); local lemmas (SF: a G-dominator r of a tight pair has |D({r,w})| = 12 for all other w in D(P); J >= 5 and >= 4 heavy dominators)
 only say where x = -1 pairs can sit.  No contradiction was derived.

<!-- END -->

# r1_NO-TIGHT: excluding tight pairs at N = 52

## Status
(created; nothing proved yet)

## Plan
1. Read TP, audit files. 2. Check tau_i <= 5 j_i. 3. Table of (J,s) cases. 4. Look for global contradiction.

## 0. Conventions (same as [TP], r1_AUDIT-52-B)
N=52, P={a,b} tight, R=D(P) (11 vertices, T[R] 5-regular), O = V minus (P u R), |O|=39. For y in O: Q_y = R n N^-(y), q_y=|Q_y|>=5,
M_y = R minus Q_y = vertices of R that y BEATS, t_y = |M_y| = 11-q_y, eps_y = q_y-5 = 6-t_y. Heavy: q_y>=6 (eps>=1). j_u = d^-(u)-25 >= 0 (u in R),
J = sum j_u, V_0 = {j=0}, V_+ = {j>0}, s=|V_+|. D_uv=|D({u,v})|, c(u,v) = #{x in R beating u and v} <= 4, s(u,v) = sum_{w in R\{u,v}} (|D({u,v,w})|-5).
Facts used (all verified in r1_AUDIT-52-B sections 2-3 and BRIEF 8): (E) sum eps_y = 14-J; Lemma A (u in V_0: only 5-vertices y beat u; D_uv=12 and s(u,v)=3-c(u,v), c(u,v)<=3 for all v in R);
(PS) sum_{v!=u} D_uv = 120+5j_u - tau_u, tau_u = sum_{y: u in M_y} eps_y; (S) s(u,v)=4D_uv - c - 45 - E_both; (B) s(u,v)<=min(Ex(u),Ex(v));
Ex(u) = 5+10 j_u - sum_{y: u in M_y} lambda(q_y), lambda(5..11)=0,4,7,9,10,10,10; D_uv>=12 for all u,v in R.

## 1. Check of the lead's inequality tau_i <= 5 j_i  (PROVED)
For i in V_+ and v in V_0, D_iv = 12 (Lemma A at v). (PS) at i: sum_{v!=i} D_iv = 120+5j_i-tau_i. The V_0 part contributes 12(11-s); so
 sum_{v in V_+\{i}} D_iv = 120 - 132 + 12 s + 5 j_i - tau_i = 12(s-1) + 5j_i - tau_i.
Each D_iv >= 12 for v in V_+\{i} (s-1 terms), so  sum_{v in V_+\{i}} (D_iv-12) = 5 j_i - tau_i >= 0.  ==> tau_i <= 5 j_i. CONFIRMED.
Summing over i in V_+: sum_i tau_i = sum_{heavy y} t_y*eps_y = sum t(6-t) <= 5J. Also sum_{V_+}(5j_i - tau_i) = 2 * sum_{pairs in V_+}(D-12).
Write f_uv := D_uv - 12 >= 0 (u,v in V_+). Then (S) reads s(u,v) = 4 f_uv + 3 - c(u,v) - E_both(u,v), and s(u,v) in [0, min(Ex(u),Ex(v))].

## 2. Reformulation: nu-invariant
nu_u := j_u - #{heavy y: u in M_y}. Sum over V_+ of nu_u = J - sum_{heavy} t_y = 14 - 6h  (h = # heavy y incl. q=11), since J = 14 - sum(6-t_y).
Ex(u) = 5 + 10 nu_u + (6 n6 + 3 n7 + n8)(u), n_q(u) = #{y: q_y=q, u in M_y}   [since 10-lambda(6,7,8) = 6,3,1, and lambda(q>=9)=10].

## 3. KEY OBSERVATION (the survivors are NOT only small J)
[TP] closes J=3,4 and shows J=5 => s>=4, and s>=4 for all J. It does NOT close J>=5 with s>=4, e.g. J=14 (then h=0: all 39 outside vertices are 5-vertices,
tau=0, Ex(u)=5+10 j_u: the pair budgets (B) are then weak). So the pair-level tools (Lemma A, PS, S, B) can't finish; need a genuinely new tool (triples with a or b, S_4, T[R] structure).

## 4. NEW: global structure of a tight pair (uses a, b themselves; all PROVED, N=52, F1 only)
Orient P={a,b} so that b -> a (WLOG). Let A = O n N^-(a), B = O n N^-(b), C = O \ (A u B) (y beaten by both a and b), m=|A|.
(4.1) N^-(a) = R u {b} u A (R beats a and b; b->a), N^-(b) = R u B (a not in N^-(b) as b->a). Since D(P)=N^-(a) n N^-(b)=R, the in-degree of b in T[N^-(a)] is
 exactly 11 with in-neighbourhood R; so b beats every vertex of A, i.e. A n B = empty. [Proof: a vertex y in A beats a; if y beat b it would lie in D(P)=R.]
(4.2) d^-(a)=12+m, d^-(b)=11+|B|; e(a)=m-13, e(b)=|B|-14. By [A52] Lemma 1 (no in-degree 23) and F3: m>=12, |B|>=13. e(a)+e(b)=12-|C|, so |C|<=14.
(4.3) Sum identity: sum_{y in O} e(y) = 26 - J - e(a) - e(b) = |C| + 14 - J = |C| + sum_y eps_y.   [direct from sum e = 26.]
(4.4) For u in R: D({a,u}) = W_u u {y in A: u in M_y} where W_u = N^-_R(u) (5 vertices; b does not beat u); so D_au = 5 + alpha_u, alpha_u := #{y in A: y beats u}.
 D({b,u}) = W_u u {y in B: y beats u}: D_bu = 5 + beta_u. F2/F3 (|D|>=11) give  alpha_u >= 6 and beta_u >= 6  for every u in R. With gamma_u := #{y in C beating u}:
 alpha_u + beta_u + gamma_u = 20 + j_u.   In particular {a,u} is a tight pair iff alpha_u = 6, {b,u} tight iff beta_u=6.
(4.5) |D({a,u,v})| = c(u,v) + cov_A(u,v), |D({b,u,v})| = c(u,v) + cov_B(u,v), where cov_X(u,v) = #{y in X : y beats u and v}. Hence (>=5)
 cov_A(u,v) >= 5 - c(u,v), cov_B(u,v) >= 5 - c(u,v). And D_uv = c + cov_A + cov_B + cov_C.
 If u in V_0 (D_uv = 12): x_a(u,v) + x_b(u,v) + cov_C(u,v) = c(u,v) + 2, with x_a = |D(a,u,v)|-5 >= 0, x_b = |D(b,u,v)|-5 >= 0. So cov_C(u,v) <= c(u,v)+2.
(4.6) Pairs {a,y}, {b,y} for y in O (using |D|>=11): |D(a,y)| = q_y + [y in A u C] + #{z in A: z->y}; |D(b,y)| = q_y + #{z in B: z->y}.
 Hence for a 5-vertex y: in T[A] in-degree >= 5 (y in A); y in B is beaten by >= 6 vertices of A, y in C by >= 5 vertices of A;
 y in B has in-degree >= 6 in T[B]; y in A u C is beaten by >= 6 vertices of B.
Status: these are consistent with all counts I tried (see sec. 7) - no contradiction yet. They are tools for later.

<!-- END -->

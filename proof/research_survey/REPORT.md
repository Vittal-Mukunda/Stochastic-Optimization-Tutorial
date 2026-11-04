# Analogues of Erdős #902 and how they were solved: a method survey for S_4 at N = 52

Date: 24 Oct 2026. Scope: a survey of literature and methods. No scripts were run. I did a few small calculations by hand, and they are marked as mine.
Status labels used throughout: **[V]** I read the full text, or the specific sections cited, in this survey or in `proof/swarm/r1_LIT.md`. **[P]** I read the abstract plus some sections. **[A]** I read the abstract or metadata only. **[S]** secondary source only.
Nothing below settles Erdős #902 or f(4) >= 53, and no source claims to.

## 0. Main findings

1. **The closest solved analogue is R(5,5) <= 46** (Angeltveit-McKay 2024) [P]. Its proof has the same structure as our setting. A hypothetical extremal object on n vertices has a forced degree window. Every neighbourhood is a smaller extremal object (there, a (4,5)-Ramsey graph; for us, T[N^-(v)] is an S_3 tournament). A triple-counting identity forces a total "excess" of exactly 0. The excess is split into per-vertex terms. Each term is >= 1 unless that vertex's neighbourhood lies in a small, enumerable family E. The few remaining cases are killed by computer "gluing along an edge" (for us: along a pair, especially a tight pair). This is the single most transferable recipe.
2. **SAT with machine-checked certificates is now routine for exact small cases**: Keller dimension 7, the empty hexagon h(6) = 30, Schur number five, Boolean Pythagorean triples, and R(3,8), R(3,9). Each succeeded only after a hand or theory reduction to a compact encoding plus heavy symmetry breaking. A direct SAT encoding of "no S_4 tournament on 52 vertices" (1326 arc variables, 270,725 four-sets × 48 candidate dominators) has no such reduction yet. SAT is realistic for the **local configurations our hand analysis already isolates**: the J = 5 survivors, branch h = 0, and T[D(P)] for a tight pair. It is also realistic for an **existence search for an F1-tournament on 52 vertices**, which decides whether F1-only counting can ever close T1.
3. **Flag-algebra SDP has been made to work at fixed small n** (Lidický-Pfender, Ramsey numbers) [P]. Finite-n symmetric sums of squares are equivalent to flag SOS on 2d-vertex flags (Raymond-Saunderson-Singh-Thomas) [P]. That method is the natural degree-2 upgrade of our failed histogram LP. It can encode the **4-set (S_4) information** that F1 counting ignores, as rooted constraints of the form "the dominator density over a labelled 4-set is >= 1/48".
4. **Covering designs, covering arrays and cover-free families do not see the tournament (skew) constraint**, which carries almost all the strength. My hand check: the Schönheim bound with blocks of size (v-1)/2 (the out-neighbourhoods of a regular tournament) gives v >= 31 at t = 4. That is exactly Erdős's 2^{n+1}-1, far below 47. Roux's covering-array recursion is the same one-step descent. These fields supply vocabulary, not lower-bound strength.
5. **Classification-based rigidity (Wilder's DRT(23) route) cannot reach order 51.** Skew-Hadamard matrices are classified up to order 32 [S], and order 36 only partially (2024) [A], so no catalogue of DRT(51) exists. Our classification-free moment argument for DRT(51) is therefore the right kind of argument at this order.

## 1. Ranked table: most transferable methods

| # | Method | Source | What it could prove for S_4 at N = 52 | Main obstacle | Realistic effort |
|---|---|---|---|---|---|
| 1 | Per-vertex excess decomposition, catalogue of extremal neighbourhoods, gluing along an edge | Angeltveit-McKay, arXiv:2409.15709 (R(5,5) <= 46) | Non-existence, by showing every vertex contributes >= 1 to a slack whose total is fixed (e.g. 338 in Case A, or sum(k-5)), except for vertices whose T[N^-(v)] lies in a small family E, then killing E by gluing along tight or near-tight pairs | Find a per-vertex slack term that is provably >= 1 off a *small* family. T[N^-(v)] (25-27 vertices, S_3, every in-degree >= 11) is far too varied to catalogue in full; R(5,5) needed about 30 CPU-years even with LP pruning | High: months of work; computation from modest to large, depending on the slack found |
| 2 | Cube-and-conquer SAT with LRAT/DRAT proofs, verified checker | Heule-Scheucher arXiv:2403.00737; Brakensiek et al. arXiv:1910.03740; Wilder repo (Cayley families, order 49) | Kill the four J = 5 tight-pair survivors, branch h = 0, and the QR_11 sub-case as finite local problems (P, R = D(P) of size 11, outside q-profile fixed) | Global S_4/F1 must be cut down to local clauses that are valid consequences, and each cut must be justified by hand. The symmetry breaking must itself be certified (Keller left part of it unverified) | Medium: weeks per case family; CPU cost likely small to moderate |
| 3 | SAT or local search for a *witness* F1-tournament on 52 vertices (optionally with a group-invariant ansatz) | Geist arXiv:1402.4303 (SAT finds minimal profiles); Wilder (Cayley SAT) | If one is found: proof that no F1-only argument can give T1, which redirects all effort to S_4. A found witness needs no certificate, only a direct check | If none exists, failure to find one proves nothing. An UNSAT proof for the full F1 problem would be very large | Low to medium: days to weeks |
| 4 | Finite-N flag-algebra / symmetric SOS SDP with rational rounding | Lidický-Pfender SIAM J. DM 2021 (arXiv:1704.03592); Raymond et al. arXiv:1606.05639; Razborov 2007 | A rational PSD certificate that no 52-vertex tournament satisfies S_4 (or F1 plus the 4-set rooted constraints) | Unknown whether flags on 6-8 vertices are strong enough (456 tournaments on 7 vertices, 6880 on 8). Finite-N product corrections must be exact. The blow-up trick used for Ramsey numbers does not stay inside tournaments | Medium-high: 1-2 months to build; SDP of desktop to cluster size |
| 5 | Two-moment rigidity plus divisibility | Wilder N = 47 (r1_LIT §R); our DRT(51) argument | Sub-cases where degrees and pair counts are pinned (already used for NT-B01) | At N = 52, L_Y varies (BRIEF §9), so the polynomial trick needs class weights | Low, but mostly exhausted |
| 6 | 0/1 ILP branch-and-bound with hand case splits | Applegate-Rains-Sloane, J. Combin. Des. 11 (2003), arXiv:math/0205303 | Exact closure of the histogram ILP after adding new cut families (e.g. from 4-sets) | Our LP/ILP relaxations already fail. CPLEX gives no checkable certificate | Medium |
| 7 | Lasserre / Sherali-Adams lift of the histogram LP (Laurent 2003) | — | Same as #4 | Too large without symmetry reduction; with it, it becomes #4 | Subsumed by #4 |
| 8 | Covering-design, covering-array and cover-free bounds (Schönheim, Roux, Kleitman-Spencer, EFF/Füredi) | §2.1-2.2 below | Only Erdős-level bounds (about 31 at n = 4) | They ignore antisymmetry | Not worth pursuing |

## 2. Dictionary: S_n in each language (my derivations, checked by hand)

- **Intersecting families.** w dominates X iff w lies in the intersection of N^-(x) over x in X. This automatically gives w not in X, since x is not in N^-(x), and x' in X cannot beat every x in X because x' is not in N^-(x'). So **S_n means {N^-(x)} is an n-wise intersecting family**, subject to the skew rule: for y ≠ x, exactly one of "y in N^-(x)" and "x in N^-(y)" holds. This is the reformulation used by Borowiecki-Grytczuk-Hałuszczak-Tuza.
- **Covering designs.** S_n means every n-set lies in some out-neighbourhood N^+(w). So the N blocks N^+(w) form an n-covering of the N points, with blocks of average size (N-1)/2, under the same skew rule.
- **Covering arrays.** Take the adjacency matrix (row w, column x, entry 1 if w -> x). *Strong* S_n (n-existentially closed) asks for all 2^n patterns on every n columns, from rows outside X: essentially a binary covering array CA(N; n, N, 2) with rows = columns. Weak S_n asks only for the all-ones pattern.
- **Union-free / cover-free.** S_n means that no n closed out-neighbourhoods N^+[x] cover V.
- **Domination and fault tolerance.** S_n is equivalent to γ(T) > n (Reid et al. 2004). "Every n-set has >= m dominators" (the Szekeres-Szekeres m-fold version, [S] via Jeffries) is equivalent to: **T - Z has S_n for every Z with |Z| = m-1**. In particular, our **F1 says exactly that S_3 survives the deletion of any 4 vertices.**
- **Voting.** γ of a majority tournament is the Condorcet dimension restricted to pairwise majorities. S_n tournaments realised by voters give elections with Condorcet dimension > n.
- **Descent.** Bonato-Cameron (quoted in JLZ 2026 [V]): P_k implies that the neighbourhoods have P_{k-1}. For weak S_k, T[N^-(v)] has S_{k-1}. The covering analogues are Schönheim's recursion and Roux's CAN(t+1, n+1, q) >= q·CAN(t, n, q) (Choi-Kim-Oh Thm 4.1 [P]).

## 3. Cluster sections

### 3.1 Covering designs, covering arrays, combinatorial interaction testing

**(a) Covering numbers C(v,k,t); Schönheim bound; exact values by ILP.**
- *Mapping:* blocks = out-neighbourhoods; t = n; v = N; the number of blocks is forced to equal v; skew rule added.
- *Status:* C(v,k,t) is known exactly only for small parameters. Gordon-Kuperberg-Patashnik tabulate upper bounds for v <= 32, k <= 16, t <= 8 [A]. Applegate-Rains-Sloane determined new exact values (e.g. C(10,5,4) = 51) [P].
- *Lower-bound method:* the Schönheim recursion, then 0/1 ILP with branch and bound. ARS formulate the problem as an IP, solve it with CPLEX, and split by hand into cases ("suppose the code contains a vector u3 of weight 3 with ..."). For banded cases they run two independent branch-and-bound codes, one guided by the LP relaxation.
- *Upper-bound method:* greedy and lexicographic constructions, and recombination of existing coverings (GKP).
- *Proof type:* computer search (CPLEX/AMPL), with **no external certificate**. ARS call it "perfectly rigorous" on the grounds that it could be replaced by hand calculation.
- *What made it work:* small v, plus a hand case split that removes symmetric branches. *Hardest step:* proving the lower bound (for instance, that 57 is impossible for D(8,1)).
- *Transfer:* the covering relaxation of S_4 at N = 52 is trivially feasible. My Schönheim check with k = (v-1)/2 and t = 4: at v = 31 the bound is ⌈31/15·⌈30/14·⌈29/13·⌈28/12⌉⌉⌉⌉ = 31 <= 31, so it is feasible; at v = 29 it is 34 > 29, infeasible. This recovers Erdős's 31 and nothing more. The ILP-with-case-split *workflow* does transfer (row 6), but certificates would be needed.
- *Confidence:* ARS [P]; GKP [A]; Schönheim [S].

**(b) Binary covering arrays CA(m; t, n, 2) and k-independent families.**
- *Mapping:* strong S_n is roughly a CA of strength n with m = n_cols = N (diagonal excluded, skew).
- *Status:* t = 2 is solved exactly (Rényi; Katona; Kleitman-Spencer 1973): the maximal degree is C(m-1, ⌈m/2⌉) [P, quoted in Choi-Kim-Oh], and the maximal arrays are unique (Katona). For t >= 3, only bounds are known. Choi-Kim-Oh improve Roux's bound for t = 3 by a structural and Erdős-Ko-Rado-type argument [P].
- *Methods:* for lower bounds, Sperner/EKR-type extremal set theory (t = 2) and Roux's recursion (t >= 3). For upper bounds, probabilistic constructions (Kleitman-Spencer) and explicit constructions (Alon 1986) [S]. Lawrence et al. survey constructions and search [A].
- *Proof type:* hand.
- *What made it work:* for t = 2 the problem is exactly an antichain problem. *Hardest step:* t >= 3, which is still open in general.
- *Transfer:* low. Weak S_4 needs one pattern, not 16, so CA bounds are not even valid lower bounds for weak S_n beyond the descent. Colbourn-Kéri (IWCC 2009) treat covering arrays and existentially closed graphs together [S, title only], and that would be the bridge for strong S_n.
- *Confidence:* as marked.

### 3.2 Cover-free families, superimposed codes, set-pair methods

**(a) r-cover-free families (Erdős-Frankl-Füredi 1985; Füredi 1996; D'yachkov-Rykov; Kautz-Singleton).**
- *Mapping:* only loose. S_n is a "no n closed out-neighbourhoods cover V" condition, while r-cover-free means "no member is covered by r others". Both are union conditions on a set system, but the quantifiers differ.
- *Status:* log T(n,r)/n is Θ(log r / r^2). Füredi's short hand proof gives (4 log r + O(1))/r^2, "implicitly contained" in EFF [S]. Exact values are known only where Steiner systems exist (EFF, zbMATH review [S]). Constructions are algebraic (Kautz-Singleton) or random.
- *Transfer:* low. These are bounds up to constants in the exponent, nowhere near one-vertex precision at N = 52.

**(b) Bollobás set-pair / Tuza set-pair method; BGHT 2003.**
- *Problem:* BGHT study a bipartite tournament (A, B) in which every k-subset of A and l-subset of B have "conquerors in opposite teams", and estimate f(k,l) = |A| + |B| via intersecting families, with probabilistic and constructive methods [A; full text paywalled].
- *Related:* Nagy-Patkós use Tuza's set-pair method to count maximal intersecting k-uniform families, M(n,k) = n^{Θ(C(2k,k))} [A]. That paper does not mention Schütte.
- *Transfer:* unknown, because the bounds in BGHT are not visible to me. Set-pair inequalities give Bollobás-type exact bounds when the pair structure is rigid. Our tight pairs (P, D(P)) with D(P) 5-regular on 11 vertices are the most rigid objects we have, but I found no source applying set pairs to them.
- *Confidence:* BGHT [A], Nagy-Patkós [A], Bollobás/Lovász exterior-algebra proof [not read].

### 3.3 Tournament domination; multiple and fault-tolerant domination

- **Sources:** Reid-McRae-Hedetniemi-Hedetniemi 2004 [V]; Lee 2001 [V]; Alon-Brightwell-Kierstead-Kostochka-Winkler 2006 [P]; Chudnovsky-Kim-Liu-Seymour-Thomassé 2018 [A]; Ai-Yi 2026 [V]. All from r1_LIT.
- **Mapping:** γ(T) > n iff S_n.
- **Results and methods:** greedy gives γ <= lg(n+1), which is Erdős's lower bound (Lee). The random tournament has γ in {k+1, k+2}. Fisher (unrefereed private communication) found that the smallest *rotational* S_4 tournament is QR_67. Structured classes (k-majority, S-free) are handled by VC-dimension and LP duality (ABKKW, CKLST). Proofs are hand and probabilistic.
- **Multiple domination:** the SS m-fold problem [S via Jeffries] at (k, m) = (3, 5) is exactly our F1, i.e. S_3 tolerating 4 deletions (§2). I found **no** tournament-specific lower-bound technique for it beyond SS-type counting. Graph k-domination work (search snippets only) concerns upper bounds and algorithms.
- **Transfer:** the fault-tolerance view suggests one concrete lemma to test: F1 at N = 52 implies that **every 48-vertex subtournament has S_3 "with room"**. That links to f(3) = 19 and to the T[N^-(v)] catalogue in row 1. No source exploits this.

### 3.4 Intersecting families and Schütte's problem

- **BGHT 2003** (above): bipartite S_{k,l}; intersecting-family reformulation; probabilistic and constructive bounds [A].
- **Jeffries 2026** (sets of tournaments; dice) [V via r1_LIT]: f(m,k) <= f(m1,k1) + f(m2,k2); SAT for small multi-tournament cases; f(4) not starred as exact.
- **JLZ 2026 + Bonato-Cameron** [V via r1_LIT]: descent; "QR_p has S_4 iff its neighbourhoods have S_3"; QR_67 has S_4 because K - K = Z_33.
- **Transfer:** the intersecting-family view makes T1 the statement that **no skew system of 52 sets on 52 points is 4-wise intersecting**. Every proof we have uses only 3-wise information with multiplicity 5. The extra content of S_4 is that each D(Y) is itself undominated (BRIEF F1). Neither the literature nor our files exploit that systematically.

### 3.5 Voting and tournament solutions

**(a) Condorcet dimension (Elkind-Lang-Saffidine 2015; Charikar-Lassota-Ramakrishnan-Vetta-Wang 2025; Geist 2014).**
- *Mapping:* candidates = vertices; a Condorcet winning set is a set S that no outside candidate beats by a majority over every member of S. For the majority tournament, dimension > n means S_n.
- *Status:* every election has Condorcet dimension <= 6 (CLRVW, via the probabilistic method plus minimax, building on stable committees) [P]. A dimension-3 profile with 6 voters and 6 candidates was found by SAT and shown minimal (Geist) [A; size quoted by CLRVW]. Searches for dimension 4 (Geist SAT; Bloks, LSE MSc thesis 2018, via dominating sets in tournaments) found none [S, as reported by CLRVW].
- *Proof types:* probabilistic (upper bound); SAT (small exact cases, no certificate format stated in the abstract).
- *Transfer:* the voter-realisability constraint is extra structure that S_4 does not have, so these bounds do not transfer. The *SAT workflow for minimal witnesses* does (row 3).

**(b) Schwartz's TEQ conjecture (Brandt-Chudnovsky-Kim-Liu-Norin-Scott-Seymour-Thomassé, Soc. Choice Welf. 40 (2013)).**
- *Problem and method:* the conjecture is reduced to "for every partition (A, B), one side contains an undominated transitive subset". That is refuted with an Erdős-Moser random tournament (no transitive subset larger than 3 log n) plus a new vertex v_T dominating each transitive T. The preprint gives about 10^130 vertices. A 24-vertex counterexample was later found by computer (Brandt-Seedig) [S]. The proof is probabilistic. [V]
- *Transfer:* low for lower bounds. It is a reminder that "dominate every small structured subset" problems shrink drastically under computer search.

### 3.6 Exact small cases by SAT/ILP with certificates

| Problem | Result | Encoding and reduction | Certificate and checker | Cost | Status |
|---|---|---|---|---|---|
| Boolean Pythagorean triples | n = 7825 | cube-and-conquer (look-ahead plus CDCL) | DRAT, about 200 TB; 68 GB compressed certificate | 800 cores, about 2 days | [A] arXiv:1605.00723 |
| Schur number five | S(5) = 160 | massively parallel SAT | 2 PB proof, checked by a formally verified checker | — | [A] arXiv:1711.08076 |
| Keller, dim 7 | no 128-clique in G_{7,3}, G_{7,4}, G_{7,6} | compact encoding; hand symmetry breaking fixes 19 coordinates (*not* mechanically checked); further symmetry-breaking clauses checked by DRAT-trim; a DNF tautology proves the cubes cover the space | CaDiCaL DRAT, trimmed by DRAT-trim, certified by **ACL2check**; 224 GB | 20 nodes × 24 cores | [P] arXiv:1910.03740 |
| Empty hexagon | h(6) = 30 | O(n^4)-clause signotope encoding, symmetry breaking, cube partition | CaDiCaL **LRAT piped directly to cakeLPR**; 180 TB LRAT; the encoding was later formalised in Lean (Subercaseaux et al.) | 17,300 CPU hours | [P] arXiv:2403.00737; [A] arXiv:2403.17370 |
| R(3,8), R(3,9) | 28, 36 | SAT plus CAS (MathCheck), orderly generation, cube-and-conquer | "first independently verifiable certificates" | 59 h sequential for R(3,8) | [S] IJCAI 2025 |
| R(5,5) <= 46 | non-existence on 46 vertices | degree window {21..24}; identity (1.2); LP; partial catalogues of R(4,5,n, e >= e0); gluing | no formal certificate; **two disjoint independent implementations** | about 30 + 50 CPU-years | [P] arXiv:2409.15709 |
| Wilder, order-49 Cayley families | no S_4 in Z_49 and F_7^2 Cayley tournaments | group-invariant SAT | DRAT | — | [S] r1_LIT §M-N |

- *What made them work:* in every case, a mathematical reduction came first (Keller graphs; signotopes; neighbourhood degree windows), then symmetry breaking, then cube partitioning. Certification has moved from DRAT to LRAT checked by verified checkers (cakeLPR, ACL2check), and in one case to Lean formalisation of the encoding. *The hardest step* was always the one that is not mechanically checked: Keller's initial symmetry breaking, the hexagon's geometric encoding (closed later in Lean), and for R(5,5) the whole pipeline.
- *Transfer:* our hand reductions play the role of the reduction step. A tight pair fixes 13 vertices with T[D(P)] a regular tournament on 11 vertices: there are **1223** of these up to isomorphism (OEIS A096368 [V]). Each J = 5 survivor fixes the outside q-profile. The local problem "extend this to a 52-vertex tournament satisfying the local consequences of S_4" is a SAT instance of a few thousand variables and is very likely tractable, with LRAT certificates. The missing piece is a hand-proved list of local consequences that suffice; otherwise UNSAT of a weaker local formula proves nothing.

### 3.7 Skew-Hadamard matrices and doubly regular tournaments

- **Reid-Brown 1972** (JCTA 12, 332-338): DRT(n-1) exists iff skew-Hadamard(n) exists [A/S; content confirmed via Nozaki-Suda [V]]. **Blatt-Szekeres 1969**: skew-Hadamard of order 52 exists, hence DRT(51) exists [S].
- **Nozaki-Suda**: T is a DRT iff its spectrum is {(n-1)/2, (-1 ± sqrt(-n))/2} [V].
- **Classification:** order 32 is classified (6662 H-inequivalent; 7227 SH-inequivalent; Hanaki-Kharaghani-Mohammadian-Tayfeh-Rezaie, as reported on a Tayfeh-Rezaie web page whose fetch failed, so [S]). Order 36 is only partly classified, "for some types", by Araya-Harada-Kharaghani-Mohammadian-Tayfeh-Rezaie 2024 [A]. **Order 52 is far out of reach**, so no catalogue of DRT(51) exists.
- *Proof type:* algebraic (equivalence, spectra); exhaustive computer search (classification).
- *Transfer:* Wilder's 48-vertex route forces a DRT(23) core and then uses McKay's catalogue [S]. It cannot be copied at 51/52. What does transfer is the spectral characterisation, which gives eigenvalue-interlacing constraints for near-DRT 52-vertex tournaments. That is unexplored, and it is not the same as the spectral Corollary 3 that BRIEF §8 says fails.

### 3.8 Flag algebras and SDP hierarchies

- **Razborov 2007, "Flag algebras"** (J. Symbolic Logic 72): the general calculus [pointer only, not re-read]. **Coregliano-Razborov** (tournaments): transitive-tournament density is asymptotically minimised by the random tournament, with quasi-random characterisations, all in the flag-algebra language for tournaments [P].
- **Lidický-Pfender** (SIAM J. Discrete Math. 2021, DOI 10.1137/18M1169473) [P]. They prove exact small Ramsey numbers, e.g. R(K_4^-, K_4^-, K_4^-) = 28 and R(K_8, C_5) = 29. *Method:* blow up a hypothetical Ramsey colouring of K_n into independent sets. In the blow-up model, the density of non-edges (pairs inside one blob) is >= 1/n, with equality for balanced blow-ups. The plain flag SDP lower-bounds that density, and **integrality** of n finishes the proof. *Certificate:* the CSDP float solution is rounded through eigen-decomposition to rational PSD matrices, so the bound degrades only slightly, and "due to the discrete nature of the problem, this small difference typically does not change the result". *Scale:* up to about 200,000 graphs, memory up to about 300 GB.
- **Raymond-Saunderson-Singh-Thomas** (arXiv:1606.05639) [P]: symmetric polynomials on the k-subset hypercube of [n]. Every degree-d SOS certificate can be replaced by one built from flags on <= 2d vertices, with size independent of n. This is the rigorous finite-n bridge.
- **Laurent 2003** [A]: Lasserre is the tightest of the Sherali-Adams, Lovász-Schrijver and Lasserre hierarchies. **Schrijver 2005** [A]: Terwilliger-algebra block-diagonalisation makes a Delsarte-strengthening SDP polynomial-size, and it improved concrete A(n,d). This is the template for "exploit the ambient symmetry".
- *Transfer to S_4 at N = 52:*
  - Our histogram LP corresponds roughly to the degree-1 level: linear identities among subtournament counts. The SDP adds Cauchy-Schwarz over rooted flags.
  - S_4 enters as linear rooted constraints. For each labelled 4-set type σ, the rooted density of a dominating fifth vertex is >= 1/48. F1 gives the analogue >= 5/49 on labelled triples. These are multiplied by nonnegative rooted flags and averaged.
  - The blow-up trick does not stay inside tournaments (pairs inside a blob have no orientation), so use the exact finite-N version (Raymond et al.) rather than the asymptotic one.
  - Main risk: 7- or 8-vertex flags may not capture enough of S_4 to reach 53. No tournament S_k result by flag algebras exists in the sources I read.

## 4. What to try first on S_4 at N = 52

1. **Decide the F1-only question by search (row 3), in parallel with local SAT (row 2).** A witness F1-tournament on 52 vertices would show, with a trivially checkable certificate, that every F1-only argument (all of [52], the moment identities, the LP) is doomed, and it would tell us exactly which 4-sets fail S_4. This is cheap. Start with group-invariant ansätze: there are no circulant tournaments of even order, so use a group of order 51 plus a fixed point, or Z_13 × Z_4 orbit structures, as Wilder did at 49. Then use the same encoding with LRAT output on the local tight-pair configurations that the hand analysis already isolated (the four J = 5 survivors; branch h = 0; T[D(P)] ranging over the 1223 regular 11-tournaments). Every UNSAT result is a certified lemma, *provided* the local clauses are hand-proved consequences of S_4.
2. **The Angeltveit-McKay recipe (row 1).** We already have the analogues of their identity (1.2): the head identity sum over pairs of (D_P - 12) = 338 + ..., the triple identities, and the STAR identity sum ξ_v^2 = 17238 (r4_MASTER). What is missing is their key move: rewrite the zero-sum excess as a sum over vertices of terms that are >= 1 unless the vertex's in-neighbourhood is one of a few extremal S_3 tournaments. This route naturally uses **full S_4** (T[N^-(v)] has S_3, which F1 alone does not give), so it attacks exactly the information our counting has ignored. R(5,5) shows the method closes problems that pure counting could not.
3. **An exact finite-N flag SDP with 4-set rooted constraints (row 4).** It is the principled successor to the failed histogram LP. It uses S_4 directly, produces a rational certificate if it succeeds, and the infrastructure has a precedent (Lidický-Pfender's code; Raymond et al.'s reduction). Run a cheap calibration first: check that the SDP with only F1 constraints reproduces f(4) >= 52 (or at least > 47) before spending on S_4 constraints.

## 5. Sources and verification status

| # | Source | Identifier | Status |
|---|---|---|---|
| 1 | Angeltveit, McKay, "R(5,5) <= 46" | arXiv:2409.15709 | [P] intro, §2, §4 |
| 2 | Lidický, Pfender, "Semidefinite programming and Ramsey numbers", SIAM J. Discrete Math. (2021) | DOI 10.1137/18M1169473; arXiv:1704.03592 | [P] §1, §4, rounding and implementation |
| 3 | Raymond, Saunderson, Singh, Thomas, "Symmetric sums of squares over k-subset hypercubes" | arXiv:1606.05639 | [P] abstract, intro |
| 4 | Coregliano, Razborov, "On the density of transitive tournaments" | arXiv:1501.04074 | [P] abstract, §1 |
| 5 | Razborov, "Flag algebras", J. Symbolic Logic 72 (2007) 1239-1282 | standard reference | pointer only, not read here |
| 6 | Laurent, comparison of SA/LS/Lasserre, Math. Oper. Res. 28 (2003) | DOI 10.1287/moor.28.3.470.16391 | [A] |
| 7 | Schrijver, Terwilliger-algebra SDP code bounds, IEEE Trans. IT 51 (2005) | DOI 10.1109/TIT.2005.851748 | [A] |
| 8 | Heule, Scheucher, "Happy ending: an empty hexagon in every set of 30 points" | arXiv:2403.00737 | [P] §7, experiments |
| 9 | Subercaseaux et al., "Formal verification of the empty hexagon number" | arXiv:2403.17370 | [A] |
| 10 | Brakensiek, Heule, Mackey, Narváez, "The resolution of Keller's conjecture" | arXiv:1910.03740 | [P] §1, §5-7 |
| 11 | Heule, "Schur number five" (AAAI 2018) | arXiv:1711.08076 | [A] |
| 12 | Heule, Kullmann, Marek, Boolean Pythagorean triples (SAT 2016) | arXiv:1605.00723 | [A] |
| 13 | Li, Duggan, Bright, Ganesh, verified certificates for R(3,8), R(3,9) (IJCAI 2025) | https://www.ijcai.org/proceedings/2025/292 | [S] search summary and poster |
| 14 | Applegate, Rains, Sloane, "On asymmetric coverings and covering numbers", J. Combin. Des. 11 (2003) 218-228 | arXiv:math/0205303 | [P] method sections |
| 15 | Gordon, Kuperberg, Patashnik, "New constructions for covering designs", J. Combin. Des. (1995) | arXiv:math/9502238 | [A] |
| 16 | Choi, Kim, Oh, "Structures and lower bounds for binary covering arrays" | arXiv:1111.0587 | [P] intro, Thm 4.1 (Roux) |
| 17 | Lawrence, Kacker, Lei, Kuhn, Forbes, "A survey of binary covering arrays", EJC 18 (2011) P84 | combinatorics.org v18i1p84 | [A] |
| 18 | Kleitman, Spencer, "Families of k-independent sets", Discrete Math. 6 (1973) 255-262 | — | [S] via #16 |
| 19 | Colbourn, Kéri, "Binary covering arrays and existentially closed graphs", IWCC 2009, LNCS 5557, 22-33 | — | [S] title/bibliography only |
| 20 | Erdős, Frankl, Füredi, Israel J. Math. 51 (1985) 79-89 | DOI 10.1007/BF02772959 | [S] zbMATH review |
| 21 | Füredi, "On r-cover-free families", JCTA 73 (1996) 172-173 | renyi.hu PDF | [S] abstract via search |
| 22 | Borowiecki, Grytczuk, Hałuszczak, Tuza, CPC 12(4) (2003) 359-364 | DOI 10.1017/S0963548303005674 | [A] (paywalled) |
| 23 | Nagy, Patkós, EJC 22(1) (2015) P1.83 | arXiv:1501.00648 | [A] |
| 24 | Reid, McRae, Hedetniemi, Hedetniemi, Australas. J. Combin. 29 (2004) | ajc_v29_p157 | [V] (r1_LIT) |
| 25 | Lee, "The domination number of a tournament" (2001) | kkms.org | [V] (r1_LIT) |
| 26 | Alon, Brightwell, Kierstead, Kostochka, Winkler, JCTB 96 (2006) | — | [P] (r1_LIT) |
| 27 | Chudnovsky, Kim, Liu, Seymour, Thomassé, "Domination in tournaments", JCTB 130 (2018) | — | [A] (r1_LIT) |
| 28 | Ai, Yi, linear lower bound, k-majority tournaments | arXiv:2607.23148 | [V] (r1_LIT) |
| 29 | Jeffries, "Schütte's property for sets of tournaments" | arXiv:2604.08790 | [V] (r1_LIT); SS m-fold claim [S] |
| 30 | Javier, Llano, Zuazua, Contrib. Discrete Math. 21 (2026) | DOI 10.55016/0sre1423 | [V] (r1_LIT) |
| 31 | Graham, Spencer, Canad. Math. Bull. 14 (1971) | — | [V] (r1_LIT) |
| 32 | Brandt et al., "A counterexample to a conjecture of Schwartz", Soc. Choice Welf. 40 (2013) 739-743 | math.mcgill.ca/snorin/papers/brandt.pdf | [V] |
| 33 | Elkind, Lang, Saffidine, "Condorcet winning sets", Soc. Choice Welf. 44 (2015) 493-517 | — | [S] via #34 |
| 34 | Charikar, Lassota, Ramakrishnan, Vetta, Wang, "Six candidates suffice to win a voter majority" | arXiv:2411.03390 | [P] intro, related work, §3 overview |
| 35 | Geist, "Finding preference profiles of Condorcet dimension k via SAT" | arXiv:1402.4303 | [A] |
| 36 | Bloks, "Condorcet winning sets", MSc thesis, LSE (2018) | — | [S] via #34 |
| 37 | Reid, Brown, JCTA 12 (1972) 332-338 | DOI 10.1016/0097-3165(72)90098-2 | [A] metadata; content via #38 |
| 38 | Nozaki, Suda, skew-Hadamard and DRT characterisation | arXiv:1202.5374 | [V] (r1_LIT) |
| 39 | Blatt, Szekeres, "A skew Hadamard matrix of order 52", CJM 21 (1969) | DOI 10.4153/CJM-1969-144-2 | [S] (r1_LIT) |
| 40 | Araya, Harada, Kharaghani, Mohammadian, Tayfeh-Rezaie, skew Hadamard order 36 | arXiv:2402.11074 | [A] |
| 41 | Tayfeh-Rezaie, "Skew-Hadamard matrices of order 32" web page | math.ipm.ac.ir/~tayfeh-r/SkewHadamard32.htm | [S] search snippet (fetch failed) |
| 42 | OEIS A096368, regular tournaments | https://oeis.org/A096368 | [V] |
| 43 | Wilder, github.com/jaredwilder/erdos902 | — | [S] (r1_LIT, tool summaries) |

*Proved vs computed:* items 1, 8-14 and 43 are computer-assisted. Of these, only 8-12 come with machine-checked certificates (13 claims them). Item 1 relies on independent re-implementation. Items 2 and 3 yield rational certificates that can be checked by hand or by machine. Everything in §2, and the Schönheim figures in §3.1, are my own hand derivations.

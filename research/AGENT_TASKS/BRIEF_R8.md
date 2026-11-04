# Round 8 brief (read fully before working)

Repository root: `C:\Users\vitta\OneDrive\Desktop\stochastic optimization`. Python 3.12 with ortools 9.15 (CP-SAT),
highspy, pulp, pysat, numpy are installed. The machine has 16 cores shared by up to six agents: use at most 3 solver
workers per process and at most 20 minutes of wall time per single solver call. Note: this folder is on OneDrive; a file
written a moment ago may briefly be invisible to a new process, so retry once after a few seconds if a fresh file is
"not found".

## Problem

A tournament T on V: every unordered pair carries one arc; u → v means u beats v. For X ⊆ V,
D(X) = {w ∉ X : w → x for all x ∈ X}. T has S_n if every n-set has D(X) ≠ ∅. f(n) = least |V| admitting S_n.
Erdős 902: estimate f(n). Known: f(1)=3, f(2)=7, f(3)=19; Szekeres (n+2)2^(n-1) − 1 ≤ f(n) ≤ (ln 2 + o(1)) n² 2ⁿ (Erdős).
Repository results (see `proof/ERDOS902_PROOF.md`, `proof/F4_GE_52_HAND_PROOF.md`): f(n) ≥ (c* − o(1)) n 2ⁿ with
c* ≈ 0.7695; f(4) ≥ 52 (hand proof, checked); f(4) ≤ 67 (Paley QR_67).

## Facts from S_4 used everywhere (proved, `proof/ERDOS902_PROOF.md` §1)

(F1) every triple has ≥ 5 dominators and D(triple) is undominated (Lemma 1.2: D(A) undominated for |A| ≤ 3).
(F2) for a pair P and y ∉ P, D(P ∪ {y}) = D(P) ∩ N⁻(y) has ≥ 5 elements; T[D(P)] has min in-degree ≥ 5; |D(P)| ≥ 11.
(F3) T[N⁻(v)] has min in-degree ≥ 11 and in-degree of a inside T[N⁻(v)] equals |D({a, v})|; d⁻(v) ≥ 23.
Tight pair: |D(P)| = 11; then T[D(P)] is 5-regular. Lemma T: every dominator of a tight pair has in-degree ≥ 25.
Claim Q (valid at every N): Z = {d⁻ = 24} has every vertex with ≤ 2 in-neighbours in Z, so |Z| ≤ 5.

## Order-52 tight-pair notation

P = {a, b}, a → b, tight; R = D(P) (11 vertices, 5-regular); O = V \ (P ∪ R), |O| = 39. For y ∈ O: Q_y = R ∩ N⁻(y),
q_y = |Q_y| ≥ 5, M_y = R \ Q_y, e_y = q_y − 5 (heavy if e_y ≥ 1). d⁻(r) = 25 + j_r (j_r ≥ 0), J = Σ j_r,
V_0 = {j = 0}, V_+ = R \ V_0. c(u, v) = #{w ∈ R : w → u, w → v}. E_both(u, v) = Σ_{y : u, v ∈ M_y} e_y.
Identities (each checked): #{y : r ∉ Q_y} = 20 + j_r; Σ_y e_y = 14 − J; |D(u, v)| = c(u, v) + #{y : u, v ∈ M_y};
pair triple-excess s(u, v) := Σ_{w ∈ R∖{u,v}} (|D({u,v,w})| − 5) = 4|D(u,v)| − c(u,v) − 45 − E_both(u,v) ≥ 0;
Ex(u) := Σ_{triples ∋ u}(|D| − 5) = 5 + 10 j_u − Σ_{y : u ∈ M_y} λ(q_y), λ(6..11) = 4, 7, 9, 10, 10, 10; Σ_v s(u,v) = 2Ex(u);
s(u, v) ≤ Ex(u). Lemma A (any J): j_u = 0 ⇒ u ∈ Q_y for every heavy y, c(u, v) ≤ 3 and |D(u, v)| = 12 for all v.
**New (24 Oct): c(u, v) ≥ 1 for all u, v ∈ R** (the dominator of {a, b, u, v} lies in D(P) = R), i.e. T[R] has S_2.

## Current frontier (see `research/N52_TIGHT_J_GE_6.md`)

* J ≤ 5 is impossible for a tight pair at order 52 (hand proof for J = 5 in that note; J ≤ 4 rests on
  `research/AGENT_TASKS/R1-C-n52-j-le-2.report.json` and `R3-C-four-positive.report.json`; all of J ≤ 5 is also
  reproduced by the CP-SAT pair-level model `research/compute/n52_pairlevel.py`, no certificate).
* Pair-level survivors: 206 j-partitions with 6 ≤ J ≤ 14 (`research/compute/n52_pairlevel_6_14.json`). The three J = 6
  survivors (2,2,1,1), (2,1,1,1,1), (1⁶) each use heavy pattern 6+2 (one y with Q_y = R, one y with q_y = 7).
* The no-tight branch (every pair ≥ 12 dominators) is untouched beyond global moments (R4-B, R5-B, R6-B): those show the
  pair/triple moment identities do not by themselves exclude it.
* Exhausted approach keys (do not repeat): claim-L-single-pair-link, one-level-counting-past-cstar,
  two-stage-averaging-second-log, random-cayley-beat-erdos-upper, n51-local-milp-certificates,
  wrong-direction-covering-local48, three-level-count-second-log.

## Rules

Distinguish in your report: proved (full argument written), computationally verified over a stated finite domain (with
the script path), solver output without certificate, conjecture, disproved. A timeout is not infeasibility. A feasible
necessary-condition model is not a tournament. Do not edit `proof/`, `research/FINAL_PROOF.md`, `research/LEMMAS.md`,
`research/STATE.md`, `research/LEDGER.md` or `research/CHECKPOINT.json`. Put new scripts under `research/compute/`
with a prefix equal to your task id in lowercase (e.g. `r8a_*.py`). Write the report JSON exactly where the prompt says.

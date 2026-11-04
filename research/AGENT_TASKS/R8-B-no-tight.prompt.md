Task id: R8-B-no-tight
Role: B
Approach key: n52-no-tight-local-structure
Relation to prior work: R4-B, R5-B, R6-B only used global moments of the margin (26, 338, 5). This task uses local structure at single vertices and at 12-dominator pairs, which those reports did not use.

Write one JSON object to:
C:\Users\vitta\OneDrive\Desktop\stochastic optimization\research\AGENT_TASKS\R8-B-no-tight.report.json

Do not edit files under proof/. Do not edit research/FINAL_PROOF.md.
Do not declare Erdős 902 solved. A status of proved is stored as unreviewed.
Use inconclusive when you have a partial result. Use failed only if you could not start.
Required keys: task_id, agent, claim, status, definitions, argument, evidence, weaknesses, references, next_step, relation_to_prior, novelty.
status is one of proved, disproved, conditional, failed, inconclusive, computed.
task_id must be R8-B-no-tight. agent must be B.
Exhausted approach keys, which this task must not repeat: claim-L-single-pair-link, one-level-counting-past-cstar, two-stage-averaging-second-log, random-cayley-beat-erdos-upper, n51-local-milp-certificates, wrong-direction-covering-local48, three-level-count-second-log.

Read research/AGENT_TASKS/BRIEF_R8.md first. Branch: T has S_4 on 52 vertices and every pair has at least 12 dominators. Deliverables:
1. Prove: every in-degree is 25 or 26, exactly 26 of each (call them L and H); for v in L, T[N^-(v)] is 12-regular on 25 vertices, has S_3, and every pair inside it has at least 5 common in-neighbours inside it; for v in H, T[N^-(v)] has in-degrees 12 + eps with Sum eps = 13. Derive and prove the arc-count identities between L and H (for example, for w in L the number of out-neighbours in L plus the excess carried by its out-arcs into H equals 13; for w in H the excess on its out-arcs inside H equals its out-degree inside H). Check each identity by a short script on random tournaments where it is an identity, or explain why it is not.
2. Study a pair P = {a, v} with v in L and a -> v, so |D(P)| = 12 exactly. Let R = D(P) (12 vertices, T[R] min in-degree >= 5, T[R] has S_2 because the dominator of {a, v, x, y} must lie in R), O = the other 38 vertices. Write the analogues of (I1), Lemma I, s(u,v), Ex(u) and the rounding-mod-4 step for this 12-dominator pair (in-degrees inside R are 5 + t_x with Sum t_x = 6), and determine whether the pair-level system is infeasible, by hand or with a CP-SAT model in which T[R] is a variable 12-vertex tournament (min in-degree >= 5, S_2) and the degrees of R-vertices are 25 or 26. Every row must be a proved consequence; state each.
3. If that model is feasible, extract the surviving structure and try a contradiction from the 12-regular, S_3, pair-common-in-neighbour >= 5 tournament W = N^-(v) on 25 vertices (a Theorem-5-style identity inside W, or a count over all v in L simultaneously).
Status proved only for written proofs; solver verdicts are evidence. Write research/AGENT_TASKS/R8-B-no-tight.report.json.

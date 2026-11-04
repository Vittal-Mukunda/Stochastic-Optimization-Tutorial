Task id: R8-D-spectral
Role: F
Approach key: n52-spectral-threshold-j6
Relation to prior work: R3-F located the first failing bound of Corollary 2 at order 52. This task uses the new bound J >= 6 and asks for the exact threshold of the Gram/Gershgorin step and for a strengthened version.

Write one JSON object to:
C:\Users\vitta\OneDrive\Desktop\stochastic optimization\research\AGENT_TASKS\R8-D-spectral.report.json

Do not edit files under proof/. Do not edit research/FINAL_PROOF.md.
Do not declare Erdős 902 solved. A status of proved is stored as unreviewed.
Use inconclusive when you have a partial result. Use failed only if you could not start.
Required keys: task_id, agent, claim, status, definitions, argument, evidence, weaknesses, references, next_step, relation_to_prior, novelty.
status is one of proved, disproved, conditional, failed, inconclusive, computed.
task_id must be R8-D-spectral. agent must be F.
Exhausted approach keys, which this task must not repeat: claim-L-single-pair-link, one-level-counting-past-cstar, two-stage-averaging-second-log, random-cayley-beat-erdos-upper, n51-local-milp-certificates, wrong-direction-covering-local48, three-level-count-second-log.

Read research/AGENT_TASKS/BRIEF_R8.md and proof/F4_GE_52_HAND_PROOF.md section 3 first. Assume (as an input from research/N52_TIGHT_J_GE_6.md) that every tight pair at N = 52 has J >= 6. Deliverables:
1. Redo Corollary 2 at N = 52: a vertex v of in-degree 23 makes every {a,v} (a in N^-(v)) tight; derive the exact bound on Sum_{a in N^-(v)} e(a) and decide whether J >= 6 (or the per-pair-level facts in the brief) now excludes in-degree 23. Give the full argument.
2. Redo Corollary 3 at N = 52 for a vertex v with in-degree 24: the Gram matrix of the sets D({v,z}) has size 51, rank <= 24. Compute exactly how the off-diagonal row sum of a tight row (14 - J) compares with the diagonal, what threshold of J makes the tight block positive definite, and what bound on W_A = Sum_{x in N^-(v)} max(e(x),0) results. Then look for a strengthening valid for J in {6, 7, 8}: e.g. a weighted Gershgorin (scaling rows), a bound on the number of heavy outside vertices per tight row, use of exact M_{zz'} values from the tight-pair structure (entries are q_{z'} - 5 for z' outside R), or a second-moment bound on M. Prove whatever you claim.
3. Combine with the global budget at N = 52: Sum_v (d^-(v) - 25) = 26, |Z| <= 5, the in-degree of each vertex >= 23. Determine what the tight-pair branch then forces globally (how many tight pairs, which in-degrees), and whether any contradiction follows.
Write research/AGENT_TASKS/R8-D-spectral.report.json.

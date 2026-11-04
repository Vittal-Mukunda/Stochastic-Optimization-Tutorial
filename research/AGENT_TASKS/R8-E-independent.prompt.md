Task id: R8-E-independent
Role: E
Approach key: n52-independent-exhaustive-j-le-5
Relation to prior work: research/compute/n52_pairlevel.py is one CP-SAT implementation without certificates. This builds a separate implementation with different variables and an independently checkable output.

Write one JSON object to:
C:\Users\vitta\OneDrive\Desktop\stochastic optimization\research\AGENT_TASKS\R8-E-independent.report.json

Do not edit files under proof/. Do not edit research/FINAL_PROOF.md.
Do not declare Erdős 902 solved. A status of proved is stored as unreviewed.
Use inconclusive when you have a partial result. Use failed only if you could not start.
Required keys: task_id, agent, claim, status, definitions, argument, evidence, weaknesses, references, next_step, relation_to_prior, novelty.
status is one of proved, disproved, conditional, failed, inconclusive, computed.
task_id must be R8-E-independent. agent must be E.
Exhausted approach keys, which this task must not repeat: claim-L-single-pair-link, one-level-counting-past-cstar, two-stage-averaging-second-log, random-cayley-beat-erdos-upper, n51-local-milp-certificates, wrong-direction-covering-local48, three-level-count-second-log.

Read research/AGENT_TASKS/BRIEF_R8.md first. Do NOT import research/compute/n52_pairlevel.py. Deliverables:
1. Implement from scratch a verifier of the statement 'no tight pair at N = 52 has J <= 5' at the pair level, using T[R] taken from the explicit list of the 551 5-regular S_2 tournaments on 11 vertices in proof/n51_local/reg11_S2.txt (one 55-character upper-triangle string per line, character k for pair (i,j), i<j in lexicographic order, '1' meaning i -> j). Verify first that the file really lists 551 pairwise non-isomorphic 5-regular S_2 tournaments, and if possible that it is complete (the number of 5-regular tournaments on 11 vertices up to isomorphism is 1223; you may cross-check with nauty/pynauty if available, otherwise with a canonical-form routine of your own). For each class and each placement of the j-vector (use automorphisms to cut placements; Lemma A forces every endpoint of a c = 4 pair into V_+), decide the pair-level system with c fixed by the class, using an exact method that does not rely on CP-SAT (for example your own branch-and-bound over heavy patterns and D-values, or HiGHS MILP with the final infeasibility re-checked by an exact rational Farkas certificate). Record counts and runtimes.
2. Produce checkable certificates in research/CERTIFICATES/ (create it): for each infeasible case either a Farkas multiplier vector over integer rows with a small checker script, or a case-split log that a separate 50-line checker replays. Write the checker as research/compute/r8e_check_certificates.py.
3. Validate the encoding on a case known to be feasible (with c >= 0 instead of c >= 1, J = 5 shape (2,1,1,1) must become feasible for some class/placement if R4-C is right; report what you find).
Write research/AGENT_TASKS/R8-E-independent.report.json.

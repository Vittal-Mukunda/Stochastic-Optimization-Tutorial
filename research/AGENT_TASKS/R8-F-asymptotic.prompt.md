Task id: R8-F-asymptotic
Role: A
Approach key: asym-dominator-set-structure-sk
Relation to prior work: The exhausted keys one-level-counting-past-cstar, two-stage-averaging-second-log and three-level-count-second-log concern adding counting levels. This task instead feeds structural properties of dominator sets (T[D(A)] has S_{n-|A|}) into the recursion, which those approaches did not use.

Write one JSON object to:
C:\Users\vitta\OneDrive\Desktop\stochastic optimization\research\AGENT_TASKS\R8-F-asymptotic.report.json

Do not edit files under proof/. Do not edit research/FINAL_PROOF.md.
Do not declare Erdős 902 solved. A status of proved is stored as unreviewed.
Use inconclusive when you have a partial result. Use failed only if you could not start.
Required keys: task_id, agent, claim, status, definitions, argument, evidence, weaknesses, references, next_step, relation_to_prior, novelty.
status is one of proved, disproved, conditional, failed, inconclusive, computed.
task_id must be R8-F-asymptotic. agent must be A.
Exhausted approach keys, which this task must not repeat: claim-L-single-pair-link, one-level-counting-past-cstar, two-stage-averaging-second-log, random-cayley-beat-erdos-upper, n51-local-milp-certificates, wrong-direction-covering-local48, three-level-count-second-log.

Read research/AGENT_TASKS/BRIEF_R8.md, proof/ERDOS902_PROOF.md sections 3-6, and the barrier notes it cites. Deliverables:
1. Identify precisely which inequality in Lemma 3.1 / Lemma 5.2 / the definition of a_j produces the constant c* = 0.7695..., and prove a statement of the form 'any argument using only the inequalities X, Y, Z cannot give a constant above c*' (state X, Y, Z exactly).
2. Use the structure that the method ignores: for |A| = s, T[D(A)] has property S_{n-s} (prove this), so |D(A)| >= f(n-s) and T[D(A)] itself satisfies every lemma recursively; also D(A) is undominated and has the in-degree structure of Lemma 1.3. Derive a recursion that uses f(n-s) (or the bounds on it) inside Lemma 3.1, and compute its limit constant numerically. Either prove an improved constant c' > c* rigorously (with a script verifying the numerics, research/compute/r8f_*.py), or prove that this extra structure provably cannot change the limit, and explain why.
3. On the upper side: state the best explicit upper-bound construction known to you (random tournaments, Paley, Graham-Spencer), check by computation for small n whether any explicit family (e.g. Paley or cyclotomic tournaments on primes p ~ c n^2 2^n with smaller c) beats ln 2 * n^2 2^n heuristically, and state precisely what is proved versus heuristic.
Do not claim the growth rate is determined. Write research/AGENT_TASKS/R8-F-asymptotic.report.json.

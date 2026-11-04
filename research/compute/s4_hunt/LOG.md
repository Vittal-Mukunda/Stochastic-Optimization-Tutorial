# S_4 hunt log (Erdős 902, f(4) <= 66?)

Start 2026-11-04T11:20Z, budget 48h. State in STATE.json; per-run logs in runs/.

- 11:30Z checker_a.py written (40 lines); passes Paley-67 (766480 4-sets, 0 undominated),
  fails Paley-59 (3422 undominated, {0,1,7,19} among them). Log: checker_a_validation.log.
- satgroup.py: lazy SAT (CaDiCaL 1.9.5) with prescribed odd-order automorphism group.
- 11:45Z circ_exh.c: exhaustive over ALL circulant tournaments Z_n, n odd 53..65 (2^((n-1)/2-1) sets each,
  1 in S wlog by unit scaling). Sanity: finds QR19 for S_3 and QR67 for S_4. Result: NO circulant
  tournament of order 53..65 has S_4. (Even N cannot be circulant tournaments.)
- Sanity tests on Z_67: lazy SAT (cadical) too slow even with 33 primary vars; orbit tabu stuck at 2144.
  => prefer exhaustive enumeration over orbit variables when V <= ~36.
- 11:53Z enum_actions.py: 167 actions of odd-order groups (Z_p x| C_e affine, Z_m cyclic) on unions of
  coset spaces, N in 52..66, with V <= 40 arc-orbit variables (actions.json). run_actions.py + orbit_exh.c
  enumerate ALL 2^V invariant tournaments per action (sanity: finds Paley-67 under Z_67 x| C_3).
  Results: runs/actions_results.jsonl. Stages V<=34, then 35-36, then 37-38 (runs/driver.sh).
- sa_cycles.c: SA with 3-/4-cycle reversals (score preserving), exact incremental undominated count
  (recheck matches). From Paley67-minus-vertex (330): at T=2 no move accepted in 157k tries (every cycle
  reversal is uphill); T=40 drifts to ~7800. Needs tuning; secondary method.
- 12:04Z last completed action: 64 group actions (V <= 23) exhausted, none has S_4.
- 12:53Z STOPPED by user. Background jobs not running. To resume: `python3 run_actions.py 24 34`,
  then 35 36 and 37 38 (finished actions are skipped through runs/actions_results.jsonl).
  Removed a stray FOUND_N67.txt left by the Paley-67 sanity test of satgroup.py (N=67, not a result).

# S_4 hunt log (Erdős 902, f(4) <= 66?)

Start 2026-11-04T11:20Z, budget 48h. State in STATE.json; per-run logs in runs/.

- 11:30Z checker_a.py written (40 lines); passes Paley-67 (766480 4-sets, 0 undominated),
  fails Paley-59 (3422 undominated, {0,1,7,19} among them). Log: checker_a_validation.log.
- satgroup.py: lazy SAT (CaDiCaL 1.9.5) with prescribed odd-order automorphism group.
- 11:50Z circ_exh.c: exhaustive over ALL circulant tournaments Z_n, n odd 53..65 (2^((n-1)/2-1) sets each,
  1 in S wlog by unit scaling). Sanity: finds QR19 for S_3 and QR67 for S_4. Result: NO circulant
  tournament of order 53..65 has S_4. (Even N cannot be circulant tournaments.)
- Sanity tests on Z_67: lazy SAT (cadical) too slow even with 33 primary vars; orbit tabu stuck at 2144.
  => prefer exhaustive enumeration over orbit variables when V <= ~36.

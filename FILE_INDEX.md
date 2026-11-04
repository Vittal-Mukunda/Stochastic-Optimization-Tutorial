# File index: everything produced on Erdős #902 (Schütte's tournament problem)

There are two downloads:

* **`schutte_902_results.zip`** is the curated package. It holds the write-ups and the scripts that support each result. Start here.
* **`schutte_902_all_work.zip`** holds the complete working directories: every script, log and intermediate file. It also includes
  dead ends, abandoned attempts and the agents' raw notes. Compiled binaries and Python caches are left out; rebuild the binaries with
  `gcc -O3 -march=native -o NAME NAME.c`.

The workspace path of each item is given in brackets, e.g. [/home/claude/f4/pkg].

---

## A. Curated package (`schutte_902_results.zip`) [/home/claude/f4/pkg]

### Read first
| file | contents |
|---|---|
| `ROUND3_FINDINGS.md` | **All new results**, with proofs and their verification status. §0 is f(4) ≥ 51 by hand. §1 is f(4) ≥ 50. §2 is the hand proof of f(4) ≥ 49. §3 has the sharper explicit bounds. §4 shows the base level is tight. §5 has the barrier theorems for constructions. §6 is the computer searches. §7 is the literature. |
| `LOWER_BOUND_CONSTANT.md` | The main theorem, f(n) ≥ (0.7695… − o(1))·n·2^n: the cross-level lemma, the full proof, the table for n ≤ 26 and the checks. |
| `RESULTS.md` | The history of the f(4) bounds (48 → 49 → 50 → 51). It also has the computer-assisted min-in-degree theorem (round 1) and the upper-bound searches. |
| `ASYMPTOTICS.md` | Theory notes: why the classical methods stop where they do, the structure theorem for the equality case, and lines of attack. |
| `README_original.md` | The README from your original upload. |

### `lower_bound/`: computer-assisted parts of the f(4) work (round 1)
* `drt23_s3.py`, `drt23_all.py`: SAT classification of the doubly regular tournaments on 23 vertices. There are 37, and exactly 2 have S_3.
* `alldrt_classes.txt`, `all_classes.txt`, `drt23_class0.txt` (D₂), `drt23_class1.txt` (QR_23): those tournaments, in digraph6 format.
* `crosscheck.py` / `.out`: cross-check against McKay's catalogue and the 16 skew-Hadamard classes.
* `local48b.c` / `local48b_out.txt`: the covering-budget computation behind "minimum in-degree ≥ 24".
* `verify_cover_py.py` and `verify_class{0,1}.out`: an independent Python re-check of that computation.
* `reg11.txt`, `reg11_S2.txt`: all regular 11-vertex tournaments, and the 551 of them with S_2.
* `sts_identity.py`, `eq4_symbolic.py`, `eq5.py`: symbolic checks for the equality-case structure theorem.
* `tour_util.py`: helper functions.

### `asymptotic_lower_bound/`: the 0.7695 constant and the explicit bounds
* `crosslevel.py` with `table_exact.txt`: the recursion in exact integers, giving f(n) for n ≤ 26.
* `crosscheck_small.py` / `.out`: an independent re-implementation for n ≤ 9.
* `sharpened_small.py`: the sharpened lemma, which gives f(4) ≥ 49, f(5) ≥ 121, f(6) ≥ 281, …
* `crossfloat.py` with `large_n.txt`: numerical runs for n up to 240.
* `limit_const.py` / `.out`: the value of c\*.
* `sanity.py` / `sanity_out.txt`: brute-force checks of each proof step on QR_7, QR_19, QR_67 and random tournaments.
* `szekeres_never_tight.py` / `.out`: the Szekeres bound is not attained for 8 ≤ n ≤ 400.
* `budget_check.py`: my independent re-check that no vertex has in-degree 23 for N ≤ 64.
* `check_planted.py`: independent check of the 70-vertex example in which a triple has only 5 dominators.

### `upper_bound/`: the search for small S_4 tournaments (round 1, all negative)
* `genum2.c`: exhaustive enumerator for group-invariant tournaments.
* `gact.py`, `families.py`, `fams/`: the 138 symmetric families on 48–66 vertices (family generator files plus `index.txt`).
* `fams_log.txt`, `reruns_log.txt`, `runlist.sh`, `rerun_split.sh`: the run logs.
* `s4ls.c` (local search), `qr_analyze.c`, `gen_qr_minus.py`, `fam_test.py`, `sk.h` (S_k checker).

### `round3_agents/`: the six research agents' notes, code and outputs
| folder | what it contains |
|---|---|
| `f4/` | **`FINAL.md`**: f(4) ≥ 51 by hand, the in-degree-23 exclusion up to N = 64, and the reduction of N = 51 to a DRT(51) case plus one pending local claim. `notes.md` is the full log. The LP/MILP scripts include `tight51.py`, `verify_reg51.py`, `class0_split.py` and `portfolio_J.py`. |
| `crosslevel/` | `notes.md`: the round-3 proof of f(4) ≥ 50. `n4/`: local LP/MILP models. |
| `verifier/` | Adversarial verification of the 0.7695 proof (`run_all.sh`, `myrec.py`, `lemcheck.c`, `cstar.py`, `refine.py`). The sharpened lemma came from here. |
| `verifier2/` | `notes.md`: verification of f(4) ≥ 50, the base-level theorem and the barrier theorems. Its scripts include `lemma4.c`, `mckay_s3.py` and `ub_exact.py`. |
| `base/` | `notes.md`: (M1) is tight for every n. It contains the planted examples `thin_S4_N70.txt` and `thin_S5_N335.txt`, their checkers, and `union_bound.py` / `.out`. |
| `uppertheory/` | `THEOREMS.md`: Theorems A–B and Propositions C–E on constructions. `NOTES.md` / `notes.md`: Monte Carlo data on Paley tournaments (`mc_paley_*.txt`). |
| `asym/` | `FINAL.md`: barrier results B1–B5 for the counting method, and Conjecture L3. `code/`: LP/ILP experiments. |
| `smallcon/` | `notes.md`: cyclotomic S_5 searches below 331, with C sources (`cyclo3.c`, `afam2.c`) and logs. |
| `literature/` | `bibliography.md`: annotated bibliography and novelty check. `notes.md`: raw notes. |

---

## B. Complete working directories (`schutte_902_all_work.zip`)

| folder [workspace path] | contents |
|---|---|
| `f4/` [/home/claude/f4] | Your original upload: `README.md`, `cayley.c`, `genum.c`, `gls.c`, `gen_cnf.c`, `verify.c`, `szekeres.c`, `paley_test.c`, `sk.h`, `affgens.py`, `mkgens.py`, `affine_driver2.py`, `equality_case_check.py`, `out_*.txt`, `sat/`. |
| `f4/new/` [/home/claude/f4/new] | Round-1 upper-bound work. It has `genum2.c` (fast enumerator), `gact.py`, `families.py` and `fams/` (216 family files). `fams_log.txt` and the reruns are its run logs. It also has the local and tabu search code `s4ls.c` and `gdfs.c`, the Paley analysis `qr_analyze.c` and `gen_qr_minus.py`, and seed and test files. |
| `f4/lb/` [/home/claude/f4/lb] | Round-1 lower-bound work, including abandoned attempts. **Warning:** `local48.c`, `cover48.c`, `forced48.c`, `m_check.py`, `config_check.py`, `complete48.py` and `qr23_cover*` use the wrong covering direction and are superseded by `local48b.c`. The attempted classification of 24-vertex in-neighbourhoods (`nbhd24*.py`, `pair49.py`, `test24.py`, `probe24*.py`) stalled and is incomplete. |
| `f4/pkg/` [/home/claude/f4/pkg] | Source of the curated package (part A). |
| `asym/` [/home/claude/asym] | `eq4*.py`, `eq5.py`: equality-case computations. `cross/` is the working copy of the cross-level scripts. |
| `agents/` [/home/claude/agents] | The complete working directories of all agents (base, crosslevel, smallcon, uppertheory, literature, verifier, verifier2, f4, asym), including intermediate files that are not in part A. |

**Not included, because they are third-party:**
* A clone of J. Wilder's public repository, at [/home/claude/jaredwilder/erdos902]. It is available at https://github.com/jaredwilder/erdos902.
* The nauty/pynauty source used for tournament generation, at [/home/claude/tools]. It is available at https://pallini.di.uniroma1.it.

## Status of the main results (details in `ROUND3_FINDINGS.md`)
| result | status |
|---|---|
| f(n) ≥ (0.7695… − o(1))·n·2^n | new; adversarially verified |
| f(5) ≥ 121, f(6) ≥ 281, f(7) ≥ 665, …; f(n) ≥ (n + 2.5)·2^(n−1) − 1 for n ≥ 5 | new; verified twice |
| f(4) ≥ 51, by hand | new record; checked by me; an independent check is still pending |
| no vertex of in-degree 23 in S_4 tournaments with N ≤ 64 | computer-assisted; re-checked |
| N = 51 reduces to a DRT(51) case plus one local claim | computer-assisted (exact certificates) and partly pending |
| (M1) is tight for every n; barrier theorems for random symmetric constructions | new; verified |
| f(4) ≥ 48 (Reid et al. 2004), f(4) ≥ 49 (Wilder 2026) | known; not ours |

# Literature

Published results, website statements, and repository claims are kept apart. A row marked "not opened this session" is a pointer, not a verification.

## Retrieved this session

| source | what was actually seen | status |
|---|---|---|
| <https://www.erdosproblems.com/902> | Indexed text via web search on 23 October 2026. Direct HTML fetch timed out. | The indexed statement is quoted in `PROBLEM.md`. It gives \(f(1)=3\), \(f(2)=7\), Erdős (1963) \(2^{n+1}-1 \le f(n) \ll n^2 2^n\), and Szekeres–Szekeres (1965) \(f(3)=19\) and \(n 2^n \ll f(n)\). The snippet does not mention \(f(4)\) or \(c^\ast\). |
| <https://www.erdosproblems.com/latex/902> | Same indexed text. | Same quotation. |
| <https://www.erdosproblems.com/forum/thread/902/proof-claims> | Indexed snippet. | The snippet says "No proof claims have been submitted yet." Direct fetch was not completed. |
| Semantic Scholar query "Schütte Erdős tournament domination Szekeres" | Empty response from the academic-search tool. | Not evidence of absence. |
| arXiv query "tournament every set of vertices dominated" | The tool returned unrelated papers dated 22 October 2026 (differential geometry, cosmology, numerical analysis). | The response is not a literature search. Do not cite those papers for this problem. |

## Standard references cited by the repository

These citations are copied from `proof/ERDOS902_PROOF.md`. The papers were not re-read from the journal in this session unless noted.

| item | bibliographic pointer used here | role |
|---|---|---|
| Erdős 1963 | P. Erdős, On a problem in graph theory, *Math. Gazette* 47 (1963) 220–223. | Upper bound of shape \(n^2 2^n\), and a weaker lower bound \(2^{n+1}-1\). Published. |
| Szekeres–Szekeres 1965 | E. Szekeres and G. Szekeres, On a problem of Schütte and Erdős, *Math. Gazette* 49 (1965) 290–293. | \(f(3)=19\) and \((n+2)2^{n-1}-1 \le f(n)\). Published. |
| Graham–Spencer 1971 | R. L. Graham and J. H. Spencer, A constructive solution to a tournament problem, *Canad. Math. Bull.* 14 (1971) 45–48. | Constructive upper bound, weaker than the random upper bound. The erdosproblems forum snippet says the same. Paper not opened this session. |
| Reid–McRae–Hedetniemi–Hedetniemi 2004 | K. B. Reid, A. A. McRae, S. M. Hedetniemi and S. T. Hedetniemi, Domination and irredundance in tournaments, *Australas. J. Combin.* 29 (2004) 157–172. | The repository attributes \(f(4) \ge 48\) to this paper. Paper not opened this session. |
| Moon 1968 | J. W. Moon, *Topics on Tournaments*, Holt, Rinehart and Winston, 1968. | Background. Not opened this session. |
| Landau 1953 | H. G. Landau, On dominance relations and the structure of animal societies III, *Bull. Math. Biophys.* 15 (1953) 143–148. | Score sequences. Not used in the proof of Lemma S1. Not opened this session. |
| Wilder, GitHub, September 2026 | <https://github.com/jaredwilder/erdos902> | The repository attributes a Lean formalisation of the classical bounds, and a computer-assisted candidate \(f(4) \ge 49\), to this repository. Not a journal article. Not re-fetched this session. |
| Paley tournament of order 67 | Quadratic-residue tournament. | The repository, and today's rerun of `proof/verify_proof.py`, give it property \(S_4\). That supplies the upper bound \(f(4) \le 67\) inside this workspace. It is a construction, not a new paper. |

## Claims that live in this workspace and were not found in the indexed problem page

| claim | where it is written | how to treat it |
|---|---|---|
| \(48 \le f(4) \le 67\) | `proof/ERDOS902_PROOF.md`, citing Reid et al. and the Paley tournament of order 67 | Upper bound \(f(4) \le 67\) was rechecked today by the verifier (QR_67 has \(S_4\)). The lower bound 48 was not re-read from Reid et al. |
| \(f(4) \ge 49\) | Attributed to Wilder, GitHub, September 2026 | Unpublished candidate, as described by the local notes. |
| \(f(4) \ge 51\) | `proof/ERDOS902_PROOF.md` Theorem A | Local hand argument. Arithmetic rechecked. Not on the indexed problem page. |
| \(f(4) \ge 52\) and the strong triple claim | `proof/F4_GE_52_HAND_PROOF.md` | Local hand argument. Not independently audited. Not on the indexed problem page. |
| \(c^\ast \approx 0.76950321915\) | `proof/ERDOS902_PROOF.md` Theorem C | Local hand argument plus a high-precision computation rechecked today. Not on the indexed problem page. |
| \(f(5) \ge 121\), and the rest of the Theorem D table | same, §6 | Finite recursion, rerun today. |

The order of \(f(n)\) is open on the problem page: the published bounds differ by a factor of about \(n\).

## 23 October 2026, after the literature report

`research/AGENT_TASKS/R1-A-literature.report.json` says the problem page, the proof-claims thread, the Reid–McRae–Hedetniemi–Hedetniemi PDF, and a Graham–Spencer text extraction were opened. On that reading, \(f(4) \ge 48\) is Corollary 7 of the 2004 paper together with their equivalence of \(S_4\) and domination number greater than 4, and \(f(4) \le 67\) is the Paley tournament of order 67 as stated by Graham–Spencer. The strings \(f(4) \ge 51\), \(f(4) \ge 52\), and \(c^\ast \approx 0.7695\) were not in the sources that report lists. The orchestrator did not repeat those fetches. The earlier line in this file that attributes a general \(f(4) \ge 49\) to the Wilder repository is not supported by the README and order-49 note named in that report.

## Opened 23 October 2026

Direct fetches of <https://www.erdosproblems.com/902>, <https://www.erdosproblems.com/latex/902>, <https://www.erdosproblems.com/forum/thread/902>, and <https://www.erdosproblems.com/forum/thread/902/proof-claims> succeeded. The statement page gives \(f(1)=3\), \(f(2)=7\), Erdős (1963) \(2^{n+1}-1\le f(n)\ll n^2 2^n\), and Szekeres–Szekeres (1965) \(f(3)=19\) and \(n 2^n\ll f(n)\). It shows Proof claims (0). The proof-claims thread says "No proof claims have been submitted yet." None of those four pages states \(f(4)\ge 51\), \(f(4)\ge 52\), or \(c^\ast\approx 0.7695\).

The PDF <https://ajc.maths.uq.edu.au/pdf/29/ajc_v29_p157.pdf> is Reid, McRae, Hedetniemi, and Hedetniemi, Australas. J. Combin. 29 (2004) 157–172. It states that property \(S_k\) is equivalent to domination number greater than \(k\), writes \(f(4)\ge 47\) from the Szekeres bound, and Corollary 7 says that domination number at least 5 forces at least 48 vertices. Graham and Spencer, Canad. Math. Bull. 14 (1971) 45–48, opened through Cambridge Core, say that \(T_{67}\) has property \(P_4\). The Zenodo dataset <https://doi.org/10.5281/zenodo.23269759>, including the zip, says the bounds \(48\le f(4)\le 67\) are unchanged. The strings \(f(4)\ge 51\), \(f(4)\ge 52\), and \(0.76950321915\) were not in those opened sources. The Wilder README and `ORDER49_MONOLITHIC_ASSAULT.md`, opened from <https://github.com/jaredwilder/erdos902>, state \(48\le f(4)\le 67\) and say the order-49 Cayley eliminations do not decide arbitrary tournaments.

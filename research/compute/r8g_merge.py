"""R8-G: merge per-process bests into r8g_best_N.txt, re-check each with both checkers,
and write r8g_summary.json."""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import r8g_core as C
import r8g_check2 as C2

summary = {}
for N in (52, 60, 63, 66):
    cands = []
    for path in glob.glob(os.path.join(HERE, f"r8g_log_{N}_*.json")):
        tag = path.rsplit("_", 1)[1][:-5]
        if tag == "tune":
            continue
        with open(path, encoding="utf-8") as f:
            log = json.load(f)
        tpath = os.path.join(HERE, f"r8g_best_{N}_{tag}.txt")
        if not os.path.exists(tpath):
            continue
        A = C.load_tournament(tpath)
        pr = C.profile(A)
        cands.append((pr["undominated_4sets"], pr["triple_deficit"], tag, A, pr, log))
    if not cands:
        continue
    cands.sort(key=lambda c: (c[0], c[1]))
    u4, deficit, tag, A, pr, log = cands[0]
    out = os.path.join(HERE, f"r8g_best_{N}.txt")
    C.save_tournament(out, A, [f"R8-G best tournament found at N={N} (source tag {tag})",
                               f"undominated_4sets={u4} triple_deficit={deficit} "
                               f"min_pair_dom={pr['min_pair_dom']} min_triple_dom={pr['min_triple_dom']}",
                               "row w, column x = 1 iff w -> x"])
    chk2 = C2.check(C2.read_rows(out))
    assert chk2["undominated_4sets"] == u4 and chk2["min_triple_dom"] == pr["min_triple_dom"] \
        and chk2["min_pair_dom"] == pr["min_pair_dom"], (N, chk2, pr)
    runs = []
    for c in cands:
        for r in c[5]["runs"]:
            runs.append({"tag": c[2], "lam": c[5]["args"]["lam"], "seed_kind": r["seed_kind"],
                         "seed_undominated": r["seed_undominated"], "seed_cost": r["seed_cost"],
                         "best_cost": r["best_cost"], "best_undominated": r["profile"]["undominated_4sets"],
                         "min_pair_dom": r["profile"]["min_pair_dom"],
                         "min_triple_dom": r["profile"]["min_triple_dom"],
                         "iters": r["iters"], "seconds": r["seconds"]})
    summary[N] = {"best_file": os.path.relpath(out, os.path.dirname(os.path.dirname(HERE))),
                  "profile": pr, "checker2": chk2, "source_tag": tag,
                  "search_seconds": sum(c[5].get("elapsed_seconds", 0) for c in cands),
                  "runs": runs}
    print(N, "U4", u4, "deficit", deficit, "pair", pr["min_pair_dom"], "triple", pr["min_triple_dom"],
          "indeg", pr["indeg_hist"], "check2 ok")
with open(os.path.join(HERE, "r8g_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=1)

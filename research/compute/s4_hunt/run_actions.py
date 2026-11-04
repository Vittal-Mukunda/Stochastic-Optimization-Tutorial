"""Exhaustive orbit-variable search over the group actions in actions.json (V in [vmin, vmax]).
Results appended to runs/actions_results.jsonl; skips actions already done."""
import json, os, subprocess, sys, time
import numpy as np
from gactions import affine_group, cyclic, power, action
from mkorbits import write_instance

HERE = os.path.dirname(os.path.abspath(__file__))
vmin, vmax = int(sys.argv[1]), int(sys.argv[2])
acts = json.load(open(os.path.join(HERE, "actions.json")))
resf = os.path.join(HERE, "runs", "actions_results.jsonl")
done = set()
if os.path.exists(resf):
    for ln in open(resf):
        done.add(json.loads(ln)["key"])


def build(a):
    if a["kind"] == "aff":
        p, e = a["p"], a["e"]
        t, mm = affine_group(p, e)
        subs = []
        for (lab, d), k in a["combo"]:
            gen = [power(mm, e // d)] if d > 1 else []
            if lab == "ZC":
                gen = gen + [t]
            subs += [gen] * k
        return action([t, mm], subs)
    c = cyclic(a["p"])
    subs = []
    for d, k in a["combo"]:
        subs += [[power(c, d)] if d < a["p"] else []] * k
    return action([c], subs)


todo = sorted([a for a in acts if vmin <= a["V"] <= vmax], key=lambda a: (a["V"], -a["N"]))
for a in todo:
    key = f'{a["kind"]}:{a["p"]}:{a["e"]}:{json.dumps(a["combo"])}'
    if key in done:
        continue
    N, P = build(a)
    inst = os.path.join(HERE, "inst", f'act_{a["kind"]}_{a["p"]}_{a["e"]}_N{N}_V{a["V"]}_{abs(hash(key)) % 10**6}.txt')
    V = write_instance(N, P, inst)
    nj = 4 if V >= 12 else 1
    t0 = time.time()
    procs = [subprocess.Popen([os.path.join(HERE, "runs", "orbit_exh"), inst, str(j), str(nj), inst[:-4]],
                              stdout=subprocess.PIPE, text=True) for j in range(nj)]
    outs = [p.communicate()[0] for p in procs]
    found = sum(o.count("FOUND\n") for o in outs)
    rec = {"key": key, "N": N, "V": V, "order": len(P), "found": found, "seconds": round(time.time() - t0),
           "outcome": "FOUND" if found else "none", "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    with open(resf, "a") as f:
        f.write(json.dumps(rec) + "\n")
    if found and N <= 66:
        # copy first found matrix to FOUND_N<N>.txt (verification is done separately)
        for j in range(nj):
            fp = inst[:-4] + f"_found_j{j}.txt"
            if os.path.exists(fp):
                rows = open(fp).read().strip().split("\n\n")[0]
                open(os.path.join(HERE, f"FOUND_N{N}.txt"), "w").write(rows.strip() + "\n")
                break
        open(os.path.join(HERE, "runs", "FOUND_FLAG"), "w").write(key + "\n")
        break

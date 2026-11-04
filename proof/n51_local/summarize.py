"""Build the per-class result table from the checker's output (only 'OK' lines count)."""
import sys, re, ast, collections
ok = collections.defaultdict(dict)
fails = []
for line in open(sys.argv[1]):
    if line.startswith('OK '):
        _, cl, mode, rest = line.split(' ', 3)
        st = ast.literal_eval(rest.strip())
        prev = ok[int(cl)].get(mode)
        if prev is None or st['leaves'] < prev['leaves']:
            ok[int(cl)][mode] = st
    elif line.startswith('FAIL'):
        fails.append(line.strip())
rows = []
cnt = collections.Counter()
for cl in range(551):
    d = ok.get(cl, {})
    inm = 'free' if 'free' in d else ('in' if 'in' in d else None)
    outm = 'free' if 'free' in d else ('out' if 'out' in d else None)
    cnt[('in', inm is not None)] += 1; cnt[('out', outm is not None)] += 1
    cnt['free'] += 'free' in d
    rows.append((cl, inm, outm, d))
print('classes with a type-free certificate:', cnt['free'])
print('in-mode certified:', cnt[('in', True)], ' open:', cnt[('in', False)])
print('out-mode certified:', cnt[('out', True)], ' open:', cnt[('out', False)])
print('checker failures:', len(fails))
for f in fails: print('  ', f)
with open(sys.argv[2], 'w') as f:
    f.write('class\tin_mode\tout_mode\tcertificates (mode: leaves/branch nodes/skeletons)\n')
    for cl, inm, outm, d in rows:
        desc = '; '.join(f"{m}: {s['leaves']}/{s['branch']}" + (f"/K{s['skeletons']}" if 'skeletons' in s else '') for m, s in sorted(d.items()))
        f.write(f"{cl}\t{'CERT('+inm+')' if inm else 'OPEN'}\t{'CERT('+outm+')' if outm else 'OPEN'}\t{desc}\n")

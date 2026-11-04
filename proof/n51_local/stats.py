"""Statistics of the certificates from checker output: python stats.py check_all.out"""
import sys, ast, statistics, collections
rec = []
for line in open(sys.argv[1]):
    if line.startswith('OK '):
        _, cl, mode, rest = line.split(' ', 3)
        rec.append((int(cl), mode, ast.literal_eval(rest.strip())))
free = [r for r in rec if r[1] == 'free']
lv = [r[2]['leaves'] + r[2]['X'] for r in free]
print('type-free certificates:', len(free), ' root-refuted (1 leaf):', sum(1 for x in lv if x == 1))
print('leaves per type-free tree: median', statistics.median(lv), ' mean', round(statistics.mean(lv), 1), ' max', max(lv))
print('total leaves (all certificates):', sum(r[2]['leaves'] + r[2]['X'] for r in rec), ' X-leaves:', sum(r[2]['X'] for r in rec))
print('skeleton-split certificates:', [(r[0], r[1]) for r in rec if 'skeletons' in r[2]])
print('non-free certificates:', [(r[0], r[1], r[2]) for r in rec if r[1] != 'free'])

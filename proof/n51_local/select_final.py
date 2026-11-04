"""Pick one certificate per needed (class, mode) from ctrees/ and write them into a zip (stored, already gzipped)."""
import os, re, sys, zipfile, collections
files = sorted(os.listdir('ctrees'))
by = collections.defaultdict(list)
for f in files:
    m = re.match(r'^(\d+)_(free|in|out|reg)(_.*)?\.json\.gz$', f)
    assert m, f
    by[(int(m.group(1)), m.group(2))].append(f)
chosen = []
for cl in range(551):
    if (cl, 'free') in by:
        chosen.append(sorted(by[(cl, 'free')], key=lambda f: os.path.getsize('ctrees/' + f))[0])
    else:
        for mode in ('in', 'out'):
            assert (cl, mode) in by, (cl, mode)
            chosen.append(sorted(by[(cl, mode)], key=lambda f: os.path.getsize('ctrees/' + f))[0])
for extra in [('0', 'reg')]:
    if (0, 'reg') in by: chosen.append(by[(0, 'reg')][0])
with zipfile.ZipFile(sys.argv[1], 'w', zipfile.ZIP_STORED) as z:
    for f in chosen:
        z.write('ctrees/' + f, f)
print('certificates:', len(chosen), ' bytes:', os.path.getsize(sys.argv[1]))

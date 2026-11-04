import os, sys
from lmodel import *; from skel import *
lines=open('reg11_S2.txt').read().split()
out=parse_class(lines[0]); M=Model(out,'out'); reps=skeleton_list(M,automorphisms(out))
done=set(os.listdir('skelcache'))
rows=[]
for n,(b,j) in enumerate(reps):
    key=f"{b}_{''.join(map(str,j))}.json.gz"
    st='B' if f'0_out_{key}' in done else ('A' if f'0_out_aux_{key}' in done else '.')
    rows.append(st)
print(''.join(rows), ' base:', rows.count('B'), ' aux:', rows.count('A'), ' open:', rows.count('.'))
print('first wave (28-38,40) open:', [n for n in list(range(28,39))+[40] if rows[n]=='.'])

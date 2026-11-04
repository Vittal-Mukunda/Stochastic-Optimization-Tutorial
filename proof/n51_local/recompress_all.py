import sys, os, glob
from multiprocessing import Pool
import recompress
def job(p):
    q = 'ctrees/' + os.path.basename(p)
    if os.path.exists(q): return p, 'skip'
    try:
        recompress.main(p, q + '.tmp'); os.replace(q + '.tmp', q); return p, 'ok'
    except Exception as e:
        return p, 'ERR ' + repr(e)
if __name__ == '__main__':
    files = sorted(glob.glob('trees/*.json.gz'))
    with Pool(int(sys.argv[1])) as P:
        for p, st in P.imap_unordered(job, files):
            if st != 'ok' and st != 'skip': print(p, st, flush=True)
    print('done', len(files), flush=True)

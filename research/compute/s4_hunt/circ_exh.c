/* Exhaustive search over ALL circulant tournaments on Z_n (n odd, n <= 127) for S_k.
 * Connection set S: for each d in 1..(n-1)/2 exactly one of d, n-d is in S;  w -> w+s for s in S.
 * WLOG 1 in S (multiply by a unit: S contains a unit since #unit-pairs > 0).
 * IN(x) = x - S.  X = {0,a,b,c} (k=4) is dominated iff AND of rotations of IN(0) by 0,a,b,c != 0.
 * Usage: circ_exh n k job njobs   (jobs split on the top log2(njobs) free bits; njobs power of 2)
 * Prints every S with property S_k (should be none for n<67, k=4) and a final summary line.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
typedef unsigned __int128 u128;
static int n;
static u128 FULL;
static inline u128 rot(u128 m, int x) { /* shift by x positions mod n */
    if (x == 0) return m;
    return ((m << x) | (m >> (n - x))) & FULL;
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); int k = atoi(argv[2]); long job = atol(argv[3]), njobs = atol(argv[4]);
    FULL = (((u128)1) << n) - 1;
    int h = (n - 1) / 2;
    /* list of k-sets containing 0 */
    int maxq = 1000000; int *Q = malloc(sizeof(int) * 3 * maxq); int nq = 0;
    if (k == 4) {
        for (int a = 1; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
            Q[3*nq] = a; Q[3*nq+1] = b; Q[3*nq+2] = c; nq++; }
    } else if (k == 3) {
        for (int a = 1; a < n; a++) for (int b = a + 1; b < n; b++) { Q[3*nq]=a; Q[3*nq+1]=b; Q[3*nq+2]=0; nq++; }
    }
    int free_bits = h - 1; /* d = 2..h */
    int jb = 0; while ((1L << jb) < njobs) jb++;
    int lowbits = free_bits - jb;
    uint64_t count = 0, found = 0;
    clock_t t0 = clock();
    /* S as in-mask IN(0) = -S: bit (n-s) set for s in S */
    for (uint64_t g = 0; g < (1ULL << lowbits); g++) {
        uint64_t code = ((uint64_t)job << lowbits) | (g ^ (g >> 1)); /* gray code over low bits */
        u128 in0 = 0;
        /* d=1 in S */
        in0 |= ((u128)1) << (n - 1);
        for (int i = 0; i < free_bits; i++) {
            int d = i + 2;
            int s = ((code >> i) & 1) ? d : n - d;
            in0 |= ((u128)1) << (n - s);
        }
        count++;
        int ok = 1;
        for (int qi = 0; qi < nq; qi++) {
            int a = Q[3*qi], b = Q[3*qi+1], c = Q[3*qi+2];
            u128 D = in0 & rot(in0, a) & rot(in0, b);
            if (k == 4) D &= rot(in0, c);
            if (!D) {
                ok = 0;
                if (qi > 0) { /* move failing set to front half */
                    int j = qi / 2; int t0_ = Q[3*j], t1 = Q[3*j+1], t2 = Q[3*j+2];
                    Q[3*j]=a; Q[3*j+1]=b; Q[3*j+2]=c; Q[3*qi]=t0_; Q[3*qi+1]=t1; Q[3*qi+2]=t2; }
                break;
            }
        }
        if (ok) {
            found++;
            printf("FOUND n=%d k=%d S={1", n, k);
            for (int i = 0; i < free_bits; i++) { int d = i + 2; printf(",%d", ((code >> i) & 1) ? d : n - d); }
            printf("}\n"); fflush(stdout);
        }
    }
    printf("DONE n=%d k=%d job=%ld/%ld checked=%llu found=%llu cpu=%.1fs\n", n, k, job, njobs,
           (unsigned long long)count, (unsigned long long)found, (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}

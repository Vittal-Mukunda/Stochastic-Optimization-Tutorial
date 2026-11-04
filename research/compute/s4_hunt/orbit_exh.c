/* Exhaustive enumeration over all assignments of orbit variables (instance from mkorbits.py).
 * Gray code over the low (V - jb) vars, top jb vars fixed by job index.  Prints FOUND assignments.
 * Usage: orbit_exh infile job njobs outprefix   (njobs a power of two)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
typedef unsigned __int128 u128;
static int N, V, Q, T;
static int *vm, **vu, **vv, *qa, *qw;
static u128 IN[128];
static unsigned char val[256];
static void setvar(int i, int b) {
    val[i] = b;
    for (int j = 0; j < vm[i]; j++) {
        int u = vu[i][j], v = vv[i][j];
        if (b) { IN[v] |= ((u128)1) << u; IN[u] &= ~(((u128)1) << v); }
        else   { IN[u] |= ((u128)1) << v; IN[v] &= ~(((u128)1) << u); }
    }
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); long job = atol(argv[2]), njobs = atol(argv[3]); const char *outp = argv[4];
    if (fscanf(f, "%d %d %d %d", &N, &V, &Q, &T) != 4) return 1;
    vm = malloc(V * sizeof(int)); vu = malloc(V * sizeof(int *)); vv = malloc(V * sizeof(int *));
    for (int i = 0; i < V; i++) {
        if (fscanf(f, "%d", &vm[i]) != 1) return 1;
        vu[i] = malloc(vm[i] * sizeof(int)); vv[i] = malloc(vm[i] * sizeof(int));
        for (int j = 0; j < vm[i]; j++) if (fscanf(f, "%d %d", &vu[i][j], &vv[i][j]) != 2) return 1;
    }
    qa = malloc(4 * Q * sizeof(int)); qw = malloc(Q * sizeof(int));
    for (int i = 0; i < Q; i++) if (fscanf(f, "%d %d %d %d %d", qa+4*i, qa+4*i+1, qa+4*i+2, qa+4*i+3, qw+i) != 5) return 1;
    fclose(f);
    int jb = 0; while ((1L << jb) < njobs) jb++;
    int low = V - jb;
    memset(IN, 0, sizeof IN);
    for (int i = 0; i < V; i++) setvar(i, i >= low ? (int)((job >> (i - low)) & 1) : 0);
    uint64_t total = 1ULL << low, found = 0; clock_t t0 = clock();
    char path[1024]; snprintf(path, sizeof path, "%s_found_j%ld.txt", outp, job);
    for (uint64_t g = 0; g < total; g++) {
        if (g) { int b = __builtin_ctzll(g); setvar(b, !val[b]); }
        int qi;
        for (qi = 0; qi < Q; qi++) {
            int *q = qa + 4 * qi;
            if (!(IN[q[0]] & IN[q[1]] & IN[q[2]] & IN[q[3]])) break;
        }
        if (qi == Q) {
            found++;
            FILE *o = fopen(path, "a");
            for (int u = 0; u < N; u++) { for (int v = 0; v < N; v++) fputc((IN[v] >> u) & 1 ? '1' : '0', o); fputc('\n', o); }
            fputc('\n', o); fclose(o);
            printf("FOUND\n"); fflush(stdout);
        } else if (qi > 0) {
            int j = qi / 2, tmp[4];
            memcpy(tmp, qa + 4 * j, sizeof tmp); memcpy(qa + 4 * j, qa + 4 * qi, sizeof tmp); memcpy(qa + 4 * qi, tmp, sizeof tmp);
        }
    }
    printf("DONE %s job=%ld/%ld checked=%llu found=%llu cpu=%.1fs\n", argv[1], job, njobs,
           (unsigned long long)total, (unsigned long long)found, (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}

/* Tabu search for S_4 over orbit variables of a prescribed automorphism group.
 * Input (from mkorbits.py): N V Q T ; then V lines "m u1 v1 ... um vm" (var=1: u->v);
 * then Q lines "a b c d w" (4-set orbit rep, orbit size); then T lines "a b c w" (triples).
 * Cost = sum_w(undominated 4-set orbits) + lam * sum_w max(0, 5-|D(T)|).
 * Usage: orbit_tabu infile seed seconds outprefix [lam] [init_file|-] [mu]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
typedef unsigned __int128 u128;
static int N, V, Q, T;
static int *vm, **vu, **vv;
static int *qa, *qw, *ta, *tw;
static u128 IN[128];
static unsigned char *val;
static double lam = 0.05, mu = 0.0;
static uint64_t rng_s;
static uint64_t rnd(void) { rng_s ^= rng_s << 13; rng_s ^= rng_s >> 7; rng_s ^= rng_s << 17; return rng_s; }
static inline int pc(u128 x) { return __builtin_popcountll((uint64_t)x) + __builtin_popcountll((uint64_t)(x >> 64)); }
static void setvar(int i, int b) {
    val[i] = b;
    for (int j = 0; j < vm[i]; j++) {
        int u = vu[i][j], v = vv[i][j];
        if (b) { IN[v] |= ((u128)1) << u; IN[u] &= ~(((u128)1) << v); }
        else   { IN[u] |= ((u128)1) << v; IN[v] &= ~(((u128)1) << u); }
    }
}
static long und_count;
static double cost(void) {
    long c4 = 0; long c3 = 0; long c1 = 0;
    for (int i = 0; i < Q; i++) {
        int *q = qa + 4 * i;
        u128 D = IN[q[0]] & IN[q[1]] & IN[q[2]] & IN[q[3]];
        if (!D) c4 += qw[i];
        else if (mu > 0 && !(D & (D - 1))) c1 += qw[i];
    }
    for (int i = 0; i < T; i++) {
        int *t = ta + 3 * i;
        int d = pc(IN[t[0]] & IN[t[1]] & IN[t[2]]);
        if (d < 5) c3 += (long)(5 - d) * tw[i];
    }
    und_count = c4;
    return c4 + lam * c3 + mu * c1;
}
static void save(const char *path) {
    FILE *f = fopen(path, "w");
    for (int u = 0; u < N; u++) { for (int v = 0; v < N; v++) fputc((IN[v] >> u) & 1 ? '1' : '0', f); fputc('\n', f); }
    fclose(f);
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); rng_s = 0x9E3779B97F4A7C15ULL ^ (uint64_t)atol(argv[2]) * 2654435761ULL;
    double secs = atof(argv[3]); const char *outp = argv[4];
    if (argc > 5) lam = atof(argv[5]);
    if (argc > 7) mu = atof(argv[7]);
    if (fscanf(f, "%d %d %d %d", &N, &V, &Q, &T) != 4) return 1;
    vm = malloc(V * sizeof(int)); vu = malloc(V * sizeof(int *)); vv = malloc(V * sizeof(int *));
    for (int i = 0; i < V; i++) {
        if (fscanf(f, "%d", &vm[i]) != 1) return 1;
        vu[i] = malloc(vm[i] * sizeof(int)); vv[i] = malloc(vm[i] * sizeof(int));
        for (int j = 0; j < vm[i]; j++) if (fscanf(f, "%d %d", &vu[i][j], &vv[i][j]) != 2) return 1;
    }
    qa = malloc(4 * Q * sizeof(int)); qw = malloc(Q * sizeof(int));
    for (int i = 0; i < Q; i++) if (fscanf(f, "%d %d %d %d %d", qa+4*i, qa+4*i+1, qa+4*i+2, qa+4*i+3, qw+i) != 5) return 1;
    ta = malloc(3 * T * sizeof(int)); tw = malloc(T * sizeof(int));
    for (int i = 0; i < T; i++) if (fscanf(f, "%d %d %d %d", ta+3*i, ta+3*i+1, ta+3*i+2, tw+i) != 4) return 1;
    fclose(f);
    val = malloc(V);
    memset(IN, 0, sizeof IN);
    for (int i = 0; i < V; i++) setvar(i, rnd() & 1);
    if (argc > 6 && strcmp(argv[6], "-") != 0) { /* init from 0/1 string of length V */
        FILE *g = fopen(argv[6], "r"); for (int i = 0; i < V; i++) { int ch = fgetc(g); setvar(i, ch == '1'); } fclose(g); }
    double cur = cost(), best = cur; long bestund = und_count;
    unsigned char *bestval = malloc(V); memcpy(bestval, val, V);
    long *tabu = calloc(V, sizeof(long));
    time_t t0 = time(NULL); long it = 0, last_imp = 0, kicks = 0;
    char path[1024]; snprintf(path, sizeof path, "%s_best.txt", outp);
    char logp[1024]; snprintf(logp, sizeof logp, "%s.log", outp);
    FILE *lg = fopen(logp, "a");
    fprintf(lg, "start N=%d V=%d Q=%d T=%d cost=%.2f und=%ld\n", N, V, Q, T, cur, und_count); fflush(lg);
    int sample = V < 400 ? V : 400;
    while (time(NULL) - t0 < secs) {
        it++;
        int bi = -1; double bc = 1e18;
        for (int s = 0; s < sample; s++) {
            int i = (sample == V) ? s : (int)(rnd() % V);
            setvar(i, !val[i]); double c = cost(); setvar(i, !val[i]);
            if ((tabu[i] > it && c >= best) ) continue;
            if (c < bc || (c == bc && (rnd() & 1))) { bc = c; bi = i; }
        }
        if (bi < 0) continue;
        setvar(bi, !val[bi]); cur = cost();
        tabu[bi] = it + 5 + (long)(rnd() % (V / 8 + 3));
        if (cur < best) {
            best = cur; bestund = und_count; memcpy(bestval, val, V); last_imp = it;
            save(path);
            fprintf(lg, "it=%ld t=%lds best=%.2f und=%ld\n", it, (long)(time(NULL) - t0), best, bestund); fflush(lg);
            if (bestund == 0 && best < 1e-9) break;
            if (bestund == 0) { /* S_4 reached even if triple term > 0 (cannot happen: S_4 => |D(T)|>=5) */ break; }
        }
        if (it - last_imp > 3 * V + 200) { /* kick */
            for (int i = 0; i < V; i++) setvar(i, bestval[i]);
            int nk = 2 + (int)(rnd() % (V / 20 + 3));
            for (int k = 0; k < nk; k++) { int i = (int)(rnd() % V); setvar(i, !val[i]); }
            cur = cost(); last_imp = it; kicks++; memset(tabu, 0, V * sizeof(long));
        }
    }
    fprintf(lg, "END it=%ld kicks=%ld t=%lds best=%.2f best_undominated=%ld\n", it, kicks, (long)(time(NULL) - t0), best, bestund);
    fclose(lg);
    printf("%ld\n", bestund);
    return 0;
}

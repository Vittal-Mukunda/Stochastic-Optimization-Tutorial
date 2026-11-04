/* Simulated annealing for S_4 on an unstructured tournament (N <= 127), multi-arc moves.
 * Cost = number of undominated 4-sets (exact, updated incrementally per arc reversal).
 * Moves: reverse a directed 3-cycle or 4-cycle (score-preserving), or a single arc (rarely).
 * Usage: sa_cycles init_matrix seed seconds outprefix [T0] [p_single]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>
typedef unsigned __int128 u128;
static int N;
static u128 IN[128], OUT[128];
static uint64_t rs;
static uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double urand(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
#define B(x) (((u128)1) << (x))
static inline int has(u128 m, int i) { return (int)((m >> i) & 1); }
/* change in #undominated 4-sets if arc u->v is reversed (current state has u->v) */
static long delta_flip(int u, int v) {
    long d = 0;
    /* X contains v, not u: becomes undominated iff D(X) == {u} */
    u128 P0 = IN[v] & ~B(u);
    for (int a = 0; a < N; a++) {
        if (a == u || a == v || !has(IN[a], u)) continue;
        u128 Pa = IN[v] & IN[a];
        for (int b = a + 1; b < N; b++) {
            if (b == u || b == v || !has(IN[b], u)) continue;
            u128 Pb = Pa & IN[b];
            if (Pb & P0 & ~(OUT[a] | OUT[b]) & 0) {}
            for (int c = b + 1; c < N; c++) {
                if (c == u || c == v || !has(IN[c], u)) continue;
                if ((Pb & IN[c]) == B(u)) d++;
            }
        }
    }
    (void)P0;
    /* X contains u, not v: becomes dominated iff D(X) empty and v -> a,b,c */
    u128 Ov = OUT[v] & ~B(u);
    for (int a = 0; a < N; a++) {
        if (!has(Ov, a)) continue;
        u128 Pa = IN[u] & IN[a];
        for (int b = a + 1; b < N; b++) {
            if (!has(Ov, b)) continue;
            u128 Pb = Pa & IN[b];
            if (!Pb) { /* every c with v->c gives an undominated X */
                for (int c = b + 1; c < N; c++) if (has(Ov, c)) d--;
                continue;
            }
            for (int c = b + 1; c < N; c++) if (has(Ov, c) && !(Pb & IN[c])) d--;
        }
    }
    return d;
}
static void flip(int u, int v) { /* u->v becomes v->u */
    OUT[u] &= ~B(v); IN[v] &= ~B(u); OUT[v] |= B(u); IN[u] |= B(v);
}
static long full_cost(void) {
    long c = 0;
    for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) {
        u128 P = IN[a] & IN[b];
        for (int cc = b + 1; cc < N; cc++) { u128 P3 = P & IN[cc];
            for (int d = cc + 1; d < N; d++) if (!(P3 & IN[d])) c++; }
    }
    return c;
}
static void save(const char *path) {
    FILE *f = fopen(path, "w");
    for (int u = 0; u < N; u++) { for (int v = 0; v < N; v++) fputc(has(OUT[u], v) ? '1' : '0', f); fputc('\n', f); }
    fclose(f);
}
static int pick(u128 m) { /* random set bit */
    int c = __builtin_popcountll((uint64_t)m) + __builtin_popcountll((uint64_t)(m >> 64));
    if (!c) return -1;
    int k = (int)(rnd() % c);
    for (int i = 0; i < N; i++) if (has(m, i)) { if (!k) return i; k--; }
    return -1;
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); rs = 88172645463325252ULL ^ ((uint64_t)atol(argv[2]) * 0x9E3779B97F4A7C15ULL);
    double secs = atof(argv[3]); const char *outp = argv[4];
    double T0 = argc > 5 ? atof(argv[5]) : 3.0; double psingle = argc > 6 ? atof(argv[6]) : 0.05;
    char line[512]; N = 0;
    while (fgets(line, sizeof line, f)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        int L = (int)strcspn(line, "\r\n");
        for (int v = 0; v < L; v++) if (line[v] == '1') { OUT[N] |= B(v); IN[v] |= B(N); }
        N++;
    }
    fclose(f);
    long cur = full_cost(), best = cur;
    char bp[1024], lp[1024]; snprintf(bp, sizeof bp, "%s_best.txt", outp); snprintf(lp, sizeof lp, "%s.log", outp);
    FILE *lg = fopen(lp, "a"); fprintf(lg, "start N=%d cost=%ld T0=%g\n", N, cur, T0); fflush(lg);
    time_t t0 = time(NULL); long it = 0, acc = 0; double T = T0; long since = 0;
    int us[4], vs[4];
    while (1) {
        it++;
        if ((it & 255) == 0) {
            double el = difftime(time(NULL), t0);
            if (el >= secs) break;
            /* cyclic schedule: period 600 s, geometric T0 -> T0/50 */
            double ph = fmod(el, 600.0) / 600.0; T = T0 * pow(0.02, ph);
        }
        int m = 0;
        double r = urand();
        if (r < psingle) { int u = (int)(rnd() % N); int v = pick(OUT[u]); if (v < 0) continue; us[0] = u; vs[0] = v; m = 1; }
        else if (r < 0.7) { /* 3-cycle u->v->w->u */
            int u = (int)(rnd() % N); int v = pick(OUT[u]); if (v < 0) continue;
            int w = pick(OUT[v] & IN[u]); if (w < 0) continue;
            us[0]=u; vs[0]=v; us[1]=v; vs[1]=w; us[2]=w; vs[2]=u; m = 3; }
        else { /* 4-cycle u->v->w->x->u */
            int u = (int)(rnd() % N); int v = pick(OUT[u]); if (v < 0) continue;
            int w = pick(OUT[v] & ~B(u)); if (w < 0) continue;
            int x = pick(OUT[w] & IN[u] & ~B(v)); if (x < 0) continue;
            us[0]=u; vs[0]=v; us[1]=v; vs[1]=w; us[2]=w; vs[2]=x; us[3]=x; vs[3]=u; m = 4; }
        long d = 0;
        for (int i = 0; i < m; i++) { d += delta_flip(us[i], vs[i]); flip(us[i], vs[i]); }
        if (d <= 0 || urand() < exp(-d / T)) {
            cur += d; acc++;
            if (cur < best) {
                best = cur; save(bp); since = 0;
                fprintf(lg, "it=%ld t=%.0fs T=%.3f best=%ld\n", it, difftime(time(NULL), t0), T, best); fflush(lg);
                if (best == 0) break;
            }
        } else {
            for (int i = m - 1; i >= 0; i--) flip(vs[i], us[i]);
        }
        since++;
    }
    long chk = full_cost();
    fprintf(lg, "END it=%ld acc=%ld best=%ld cur=%ld recheck=%ld t=%.0fs\n", it, acc, best, cur, chk, difftime(time(NULL), t0));
    fclose(lg); printf("%ld\n", best);
    return 0;
}

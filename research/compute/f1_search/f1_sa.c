/* f1_sa.c -- [experiment] simulated annealing for tournaments in which every triple has >= T dominators.
 * Not a proof tool. Cost = sum over triples Y of max(0, T - |D(Y)|).
 * usage: f1_sa N T seed iters temp0 temp1 [outfile]
 * Flip of arc u->v into v->u changes k only on triples {u,y,z} (gain 1 iff v beats y,z) and {v,y,z} (lose 1 iff u beats y,z). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
#define MAXN 64
static int N, T;
static u64 inb[MAXN], MASK;
static unsigned char K[MAXN][MAXN][MAXN];
static u64 rs = 88172645463325252ULL;
static inline u64 rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline double urand(void){ return (rnd() >> 11) * (1.0/9007199254740992.0); }
static inline int beats(int a,int b){ return (inb[b] >> a) & 1; }
static inline u64 outb(int v){ return ~inb[v] & MASK & ~(1ULL<<v); }
static inline unsigned char *kp(int a,int b,int c){ /* sort */
  int t; if(a>b){t=a;a=b;b=t;} if(b>c){t=b;b=c;c=t;} if(a>b){t=a;a=b;b=t;} return &K[a][b][c]; }
static long full_cost(void){
  long c=0; for(int a=0;a<N;a++)for(int b=a+1;b<N;b++){u64 ab=inb[a]&inb[b];for(int d=b+1;d<N;d++){
    int k=__builtin_popcountll(ab&inb[d]); K[a][b][d]=(unsigned char)k; if(k<T) c+=T-k;}} return c; }
/* delta of flipping the arc between u and v, where currently u -> v */
static long delta(int u,int v){
  long d=0; u64 A=outb(v), B=outb(u)&~(1ULL<<v);
  /* A: vertices v beats (u not in A since u->v). Triples {u,y,z}, y,z in A gain 1 */
  for(u64 a=A;a;a&=a-1){int y=__builtin_ctzll(a); for(u64 b=a&(a-1);b;b&=b-1){int z=__builtin_ctzll(b);
      if(*kp(u,y,z)<T) d--; }}
  for(u64 a=B;a;a&=a-1){int y=__builtin_ctzll(a); for(u64 b=a&(a-1);b;b&=b-1){int z=__builtin_ctzll(b);
      if(*kp(v,y,z)<=T) d++; }}
  return d; }
static void apply(int u,int v){ /* u->v becomes v->u */
  u64 A=outb(v), B=outb(u)&~(1ULL<<v);
  for(u64 a=A;a;a&=a-1){int y=__builtin_ctzll(a); for(u64 b=a&(a-1);b;b&=b-1){int z=__builtin_ctzll(b); (*kp(u,y,z))++; }}
  for(u64 a=B;a;a&=a-1){int y=__builtin_ctzll(a); for(u64 b=a&(a-1);b;b&=b-1){int z=__builtin_ctzll(b); (*kp(v,y,z))--; }}
  inb[v] &= ~(1ULL<<u); inb[u] |= (1ULL<<v); }
int main(int argc,char**argv){
  if(argc<7){fprintf(stderr,"usage: f1_sa N T seed iters temp0 temp1 [outfile]\n");return 1;}
  N=atoi(argv[1]); T=atoi(argv[2]); rs ^= (u64)atoll(argv[3])*0x9E3779B97F4A7C15ULL; for(int i=0;i<20;i++) rnd();
  long iters=atol(argv[4]); double t0=atof(argv[5]), t1=atof(argv[6]); const char*out=argc>7?argv[7]:NULL;
  MASK = (N==64)?~0ULL:((1ULL<<N)-1);
  memset(inb,0,sizeof inb);
  for(int a=0;a<N;a++)for(int b=a+1;b<N;b++){ if(rnd()&1) inb[b]|=1ULL<<a; else inb[a]|=1ULL<<b; }
  long cost=full_cost(), best=cost; double lr=log(t1/t0);
  for(long it=0; it<iters; it++){
    double temp=t0*exp(lr*(double)it/(double)iters);
    int u=rnd()%N, v=rnd()%N; if(u==v) continue; if(!beats(u,v)){int t=u;u=v;v=t;}
    long d=delta(u,v);
    if(d<=0 || urand()<exp(-(double)d/temp)){ apply(u,v); cost+=d;
      if(cost<best){ best=cost;
        if(best==0){ fprintf(stdout,"FOUND it=%ld\n",it); break; } } }
    if((it & ((1L<<24)-1))==0){ fprintf(stdout,"it=%ld temp=%.4f cost=%ld best=%ld\n",it,temp,cost,best); fflush(stdout); }
  }
  long chk=full_cost(); int mink=99; for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int d=b+1;d<N;d++) if(K[a][b][d]<mink) mink=K[a][b][d];
  int dmin=99,dmax=0; for(int v=0;v<N;v++){int d=__builtin_popcountll(inb[v]); if(d<dmin)dmin=d; if(d>dmax)dmax=d;}
  fprintf(stdout,"END N=%d T=%d final_cost=%ld (recomputed %ld) best=%ld min_k=%d indeg=[%d,%d]\n",N,T,cost,chk,best,mink,dmin,dmax);
  if(out){ FILE*f=fopen(out,"w"); for(int v=0;v<N;v++) fprintf(f,"%llu\n",(unsigned long long)inb[v]); fclose(f); }
  return 0; }

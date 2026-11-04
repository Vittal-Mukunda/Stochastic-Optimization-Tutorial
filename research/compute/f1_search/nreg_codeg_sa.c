/* p25_sa.c -- [experiment] search for (P25): a 12-regular tournament on 25 vertices with every pair having >= 5 common
 * in-neighbours and every triple dominated (S_3).  Moves reverse a directed 3-cycle (keeps all degrees).
 * cost = W1 * sum_pairs max(0, 5 - codeg) + W2 * #{triples with no dominator}.  usage: p25_sa seed iters t0 t1 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#ifndef NV
#define NV 25
#endif
#ifndef CMIN
#define CMIN 5
#endif
typedef uint32_t u32; static u32 inb[NV];
static uint64_t rs=88172645463325252ULL; static inline uint64_t rnd(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static inline double ur(void){return (rnd()>>11)*(1.0/9007199254740992.0);}
static int beats(int a,int b){return (inb[b]>>a)&1;}
static void flip(int a,int b){ /* a->b becomes b->a */ inb[b]&=~(1u<<a); inb[a]|=1u<<b; }
static long cost(int *cd,int *und){ long c=0; int d=0,u=0;
  for(int a=0;a<NV;a++)for(int b=a+1;b<NV;b++){u32 ab=inb[a]&inb[b]; int k=__builtin_popcount(ab); if(k<CMIN){c+=CMIN-k; d+=CMIN-k;}
    if(0) for(int e=b+1;e<NV;e++) if(!(ab&inb[e])){ c+=3; u++; } }
  if(cd)*cd=d; if(und)*und=u; return c; }
int main(int argc,char**argv){ rs^=(uint64_t)atoll(argv[1])*0x9E3779B97F4A7C15ULL; for(int i=0;i<20;i++)rnd();
  long iters=atol(argv[2]); double t0=atof(argv[3]),t1=atof(argv[4]),lr=log(t1/t0);
  for(int a=0;a<NV;a++) for(int s=1;s<=(NV-1)/2;s++) inb[(a+s)%NV]|=1u<<a;   /* rotational start: a -> a+1..a+12 */
  long c=cost(NULL,NULL), best=c;
  for(long it=0;it<iters;it++){ double T=t0*exp(lr*(double)it/iters);
    int a=rnd()%NV,b=rnd()%NV,e=rnd()%NV; if(a==b||b==e||a==e) continue;
    if(!(beats(a,b)&&beats(b,e)&&beats(e,a))) { if(beats(b,a)&&beats(e,b)&&beats(a,e)){int t=a;a=e;e=t;} else continue; }
    flip(a,b); flip(b,e); flip(e,a); long c2=cost(NULL,NULL);
    if(c2<=c || ur()<exp(-(double)(c2-c)/T)){ c=c2; if(c<best){best=c; if(best==0){ printf("FOUND it=%ld\n",it); break; }} }
    else { flip(b,a); flip(e,b); flip(a,e); } }
  int cd,u; cost(&cd,&u); printf("END best=%ld final codeg_deficit=%d undominated_triples=%d\n",best,cd,u);
  if(best==0 && getenv("DUMP")){ for(int v=0;v<NV;v++){ printf("%d:",v); for(int w=0;w<NV;w++) if(beats(v,w)) printf(" %d",w); printf("\n"); } }
  return 0; }

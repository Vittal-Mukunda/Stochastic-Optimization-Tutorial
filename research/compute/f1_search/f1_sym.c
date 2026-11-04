/* f1_sym.c -- [experiment] SA over tournaments invariant under Z_n acting with r orbits of size n (n odd) plus f fixed points.
 * Vertex (i,j) = orbit i, element j in Z_n; index i*n+j; fixed points are r*n .. r*n+f-1.  N = r*n + f <= 64.
 * Bits: within orbit i, for each d in 1..(n-1)/2 a bit says (i,j)->(i,j+d) [else (i,j)->(i,j-d)];
 *       between orbits i<i', for each d in Z_n a bit says (i,j)->(i',j+d) [else reverse];
 *       fixed point p vs orbit i: a bit says p -> whole orbit i [else orbit -> p]; fixed points among themselves: a bit per pair.
 * Cost = sum over triples of max(0, T - k). Full recomputation per move (N <= 64, bitsets).
 * usage: f1_sym n r f T seed iters temp0 temp1 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
static int n,r,f,N,T,NB; static int *bits; static u64 inb[64];
static u64 rs=88172645463325252ULL; static inline u64 rnd(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static inline double urand(void){return (rnd()>>11)*(1.0/9007199254740992.0);}
static void set_arc(int a,int b){ inb[b]|=1ULL<<a; inb[a]&=~(1ULL<<b); }
static void build(void){
  memset(inb,0,sizeof inb); int p=0, h=(n-1)/2;
  for(int i=0;i<r;i++) for(int d=1;d<=h;d++,p++) for(int j=0;j<n;j++){ int a=i*n+j, b=i*n+(j+d)%n; if(bits[p]) set_arc(a,b); else set_arc(b,a); }
  for(int i=0;i<r;i++) for(int i2=i+1;i2<r;i2++) for(int d=0;d<n;d++,p++) for(int j=0;j<n;j++){ int a=i*n+j, b=i2*n+(j+d)%n; if(bits[p]) set_arc(a,b); else set_arc(b,a); }
  for(int q=0;q<f;q++) for(int i=0;i<r;i++,p++) for(int j=0;j<n;j++){ int a=r*n+q, b=i*n+j; if(bits[p]) set_arc(a,b); else set_arc(b,a); }
  for(int q=0;q<f;q++) for(int q2=q+1;q2<f;q2++,p++){ int a=r*n+q,b=r*n+q2; if(bits[p]) set_arc(a,b); else set_arc(b,a); }
}
static long cost(int *mink){ long c=0; int mk=99;
  for(int a=0;a<N;a++)for(int b=a+1;b<N;b++){u64 ab=inb[a]&inb[b]; for(int d=b+1;d<N;d++){int k=__builtin_popcountll(ab&inb[d]); if(k<T)c+=T-k; if(k<mk)mk=k;}}
  if(mink)*mink=mk; return c; }
int main(int argc,char**argv){
  if(argc<9){fprintf(stderr,"usage: f1_sym n r f T seed iters temp0 temp1\n");return 1;}
  n=atoi(argv[1]); r=atoi(argv[2]); f=atoi(argv[3]); T=atoi(argv[4]); rs^=(u64)atoll(argv[5])*0x9E3779B97F4A7C15ULL; for(int i=0;i<20;i++)rnd();
  long iters=atol(argv[6]); double t0=atof(argv[7]), t1=atof(argv[8]); N=r*n+f; if(N>64){fprintf(stderr,"N>64\n");return 1;}
  NB = r*((n-1)/2) + (r*(r-1)/2)*n + f*r + f*(f-1)/2; bits=calloc(NB,sizeof(int));
  for(int i=0;i<NB;i++) bits[i]=rnd()&1;
  if(argc>9){ for(int i=0;i<NB&&argv[9][i];i++) bits[i]=argv[9][i]-48; build(); int m0; long c0=cost(&m0); printf("EVAL cost=%ld min_k=%d\n",c0,m0); return 0; }
  build(); int mk; long c=cost(&mk), best=c; double lr=log(t1/t0);
  int *bestbits=calloc(NB,sizeof(int)); memcpy(bestbits,bits,NB*sizeof(int));
  for(long it=0;it<iters;it++){ double temp=t0*exp(lr*(double)it/(double)iters); int p=rnd()%NB; bits[p]^=1; build();
    long c2=cost(NULL); long d=c2-c; if(d<=0||urand()<exp(-(double)d/temp)){ c=c2; if(c<best){best=c; memcpy(bestbits,bits,NB*sizeof(int)); if(best==0) break;} } else bits[p]^=1;
    if(it%20000==0){ printf("it=%ld temp=%.3f cost=%ld best=%ld\n",it,temp,c,best); fflush(stdout);} }
  memcpy(bits,bestbits,NB*sizeof(int)); build(); c=cost(&mk); int dmin=99,dmax=0; for(int v=0;v<N;v++){int d=__builtin_popcountll(inb[v]); if(d<dmin)dmin=d; if(d>dmax)dmax=d;}
  printf("END n=%d r=%d f=%d N=%d T=%d NB=%d best_cost=%ld min_k=%d indeg=[%d,%d]\nBITS ",n,r,f,N,T,NB,c,mk,dmin,dmax);
  for(int i=0;i<NB;i++) printf("%d",bits[i]); printf("\n"); return 0; }

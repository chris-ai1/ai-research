// print all distance-5 XOR faces at n=5 for G gates (reuses enum5 logic)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define K 5
static uint8_t *bm; static uint32_t nodes[K+16]; static int used[K+16];
static inline void setf(uint32_t f){bm[f>>3]|=1<<(f&7);} static inline int getf(uint32_t f){return (bm[f>>3]>>(f&7))&1;}
static void dfs(int L,int r,int u){for(int i=0;i<L;i++)for(int j=i+1;j<L;j++){int u2=u-(i>=K&&!used[i])-(j>=K&&!used[j])+1;if(u2>r)continue;uint32_t a=nodes[i],b=nodes[j];uint32_t c[5]={a&b,a&~b,~a&b,a|b,a^b};for(int t=0;t<5;t++){uint32_t g=c[t];if(!g)continue;int dup=0;for(int q=0;q<L;q++)if(nodes[q]==g){dup=1;break;}if(dup)continue;if(u2==1){setf(g);setf(~g);}if(r>1){int ui=used[i],uj=used[j];used[i]=used[j]=1;nodes[L]=g;used[L]=0;dfs(L+1,r-1,u2);used[i]=ui;used[j]=uj;}}}}
int main(int argc,char**argv){int G=atoi(argv[1]);bm=calloc(1u<<29,1);for(int i=0;i<K;i++){uint32_t t=0;for(int r=0;r<32;r++)if((r>>i)&1)t|=1u<<r;nodes[i]=t;used[i]=1;setf(t);setf(~t);}setf(0);setf(~0u);for(int g=1;g<=G;g++)dfs(K,g,0);
 uint32_t ma=1u,mb=1u<<31;for(uint64_t f=0;f<(1ull<<32);f++){uint32_t g=(uint32_t)f;if(g&(ma|mb))continue;int e0=getf(g),e1=getf(g|ma),e2=getf(g|mb),e3=getf(g|ma|mb);if(e0+e1+e2+e3==2&&e0==e3)printf("%08x %d\n",g,e0);}return 0;}

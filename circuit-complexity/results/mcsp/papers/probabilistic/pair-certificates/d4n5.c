// n=5, threshold 5: pair a=00000, b=01111 (bits 0..3). For each third point g in the 5-cube (g != a,b), is there an XOR face (L,L')
// with C(L+g) >= 6 and C(L'+g) >= 6 ?
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static uint8_t *bm;
static inline int getf(uint32_t f){return (bm[f>>3]>>(f&7))&1;}
int main(){
    bm = malloc(1u<<29); FILE*fi=fopen("bm5_5.bin","rb"); if(fread(bm,1,1u<<29,fi)!=(1u<<29)) return 1; fclose(fi);
    uint32_t ma=1u, mb=1u<<15; int ok[32]={0}; long faces=0;
    for(uint64_t f=0; f<(1ull<<32); f++){
        uint32_t g=(uint32_t)f; if(g&(ma|mb)) continue;
        int e0=getf(g),e1=getf(g|ma),e2=getf(g|mb),e3=getf(g|ma|mb);
        if(e0+e1+e2+e3!=2||e0!=e3) continue;
        faces++;
        uint32_t L = e0 ? g : (g|ma), L2 = L^ma^mb;
        for(int p=0;p<32;p++){ if(p==0||p==15) continue; if(!getf(L^(1u<<p)) && !getf(L2^(1u<<p))) ok[p]=1; }
    }
    printf("faces %ld\nthird points with no good face:", faces);
    for(int p=0;p<32;p++) if(p!=0&&p!=15&&!ok[p]) printf(" %d", p);
    printf("\n"); return 0;
}

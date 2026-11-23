// All 5-variable functions with at most G gates (B2, free negation), as a bitmap; then face statistics.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define K 5
static uint8_t *bm;            // 2^32 bits
static uint32_t nodes[K + 16];
static int used[K + 16];
static int G;
static inline void setf(uint32_t f) { bm[f >> 3] |= 1 << (f & 7); }
static inline int getf(uint32_t f) { return (bm[f >> 3] >> (f & 7)) & 1; }
static void dfs(int L, int r, int u) {   // L nodes so far, r gates still to add, u = #unused gates
    for (int i = 0; i < L; i++) for (int j = i + 1; j < L; j++) {
        int u2 = u - (i >= K && !used[i]) - (j >= K && !used[j]) + 1;
        if (u2 > r) continue;
        uint32_t a = nodes[i], b = nodes[j];
        uint32_t c[5] = { a & b, a & ~b, ~a & b, a | b, a ^ b };
        for (int t = 0; t < 5; t++) {
            uint32_t g = c[t];
            if (g == 0) continue;
            int dup = 0;
            for (int q = 0; q < L; q++) if (nodes[q] == g) { dup = 1; break; }
            if (dup) continue;
            if (u2 == 1) { setf(g); setf(~g); }
            if (r > 1) {
                int ui = used[i], uj = used[j];
                used[i] = used[j] = 1; nodes[L] = g; used[L] = 0;
                dfs(L + 1, r - 1, u2);
                used[i] = ui; used[j] = uj;
            }
        }
    }
}
int main(int argc, char **argv) {
    G = atoi(argv[1]);
    bm = calloc(1u << 29, 1);
    for (int i = 0; i < K; i++) {
        uint32_t t = 0;
        for (int r = 0; r < 32; r++) if ((r >> i) & 1) t |= 1u << r;
        nodes[i] = t; used[i] = 1; setf(t); setf(~t);
    }
    setf(0); setf(~0u);
    for (int g = 1; g <= G; g++) dfs(K, g, 0);
    uint64_t cnt = 0;
    for (uint64_t f = 0; f < (1ull << 32); f++) cnt += getf((uint32_t)f);
    {char nm[64];sprintf(nm,"bm5_%d.bin",G);FILE*fo=fopen(nm,"wb");fwrite(bm,1,1u<<29,fo);fclose(fo);}
    printf("G=%d functions with <=G gates: %llu\n", G, (unsigned long long)cnt);
    for (int d = 1; d <= K; d++) {
        uint32_t ma = 1u, mb = 1u << ((1u << d) - 1);
        uint64_t xr = 0, odd = 0; uint32_t ex = 0; int have = 0;
        for (uint64_t f = 0; f < (1ull << 32); f++) {
            uint32_t g = (uint32_t)f;
            if (g & (ma | mb)) continue;
            int e0 = getf(g), e1 = getf(g | ma), e2 = getf(g | mb), e3 = getf(g | ma | mb);
            int s = e0 + e1 + e2 + e3;
            if (s == 1 || s == 3) odd++;
            if (s == 2 && e0 == e3) { xr++; if (!have) { have = 1; ex = g; } }
        }
        printf("  distance %d: XOR faces %llu, odd faces %llu, example %08x\n", d,
               (unsigned long long)xr, (unsigned long long)odd, ex);
    }
    return 0;
}

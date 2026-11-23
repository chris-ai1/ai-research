# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
import sys
sys.path.insert(0, '/tmp/andreev_gap/explainer_review')
from fractions import Fraction as F
from build_circuit import formula
allok = True
for k in (1, 2, 4, 8, 16, 32, 64, 128):
    N = 1 << k; m = N // k; n = N + k * m; assert k * m == N and n == 2 * N
    total = formula(k, m) + 1
    resid = F(total) - (F(5, 16) * n * n - F(n * k, 4))      # log2(n/2) = k exactly
    allok &= resid == 3 * n - 2 * k - 1
    print(k, 'resid == 3n-2k-1:', resid == 3 * n - 2 * k - 1, ' resid/n =', float(resid / n))
print('PASS' if allok else 'FAIL', ' exact balance: total = 5/16 n^2 - (n/4) log2(n/2) + 3n - 2 log2(n/2) - 1')

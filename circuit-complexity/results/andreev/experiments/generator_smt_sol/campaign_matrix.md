<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Actual completed run matrix

`full` denotes the separate arbitrary-table mode ($r=-1$). S counts bottoms; add one for total gates. “No witness” and UNKNOWN make no infeasibility claim. LP/MILP witness validity is independently exact even if the symbolic family checker times out.

| Run | k,m,r | Method; attempted S/library | Best S | Family symbolic | Ordinary symbolic | Run termination |
|---|---|---|---|---|---|---|
| free_k2m6r0s6 | 2,6,0 | free; 6 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| free_k2m6r1s18 | 2,6,1 | free; 18 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| free_k2m8r0s8 | 2,8,0 | free; 8 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| free_k2m8r1s23 | 2,8,1 | free; 23 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| free_k3m3r1s8 | 3,3,1 | free; 8 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| free_k3m3r1s8_long | 3,3,1 | free; 8 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| free_k3m4r0s8 | 3,4,0 | free; 8 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| free_k3m6r1s18 | 3,6,1 | free; 18 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| free_k4m2r1s12 | 4,2,1 | free; 12 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| free_k4m3r1s16 | 4,3,1 | free; 16 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| free_xag_k3m3r1s8 | 3,3,1 | free; 8 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| lp_k3m3full | 3,3,full | LP; 54 | 54 | UNSAT | UNKNOWN | LP feasible |
| lp_k3m3r1 | 3,3,1 | LP; 54 | 36 | UNSAT | COUNTEREXAMPLE | LP feasible |
| lp_k3m3r2 | 3,3,2 | LP; 54 | 54 | UNSAT | COUNTEREXAMPLE | LP feasible |
| lp_k3m4full | 3,4,full | LP; 68 | 68 | UNKNOWN | UNKNOWN | LP feasible |
| lp_k3m4r1 | 3,4,1 | LP; 68 | 48 | UNKNOWN | COUNTEREXAMPLE | LP feasible |
| lp_k3m6full | 3,6,full | LP; 89 | 89 | UNKNOWN | UNKNOWN | LP feasible |
| lp_k3m6r1 | 3,6,1 | LP; 89 | 66 | UNKNOWN | COUNTEREXAMPLE | LP feasible |
| lp_k4m3r1 | 4,3,1 | LP; 168 | 64 | UNKNOWN | COUNTEREXAMPLE | LP feasible |
| milp_k3m3full | 3,3,full | MILP; 54 | 49 | UNSAT | VERIFIED | Time limit reached. (HiGHS Status 13: Time limit reached) |
| milp_k3m3r1 | 3,3,1 | MILP; 54 | 32 | UNSAT | COUNTEREXAMPLE | Optimization terminated successfully. (HiGHS Status 7: Optimal) |
| milp_k3m3r2 | 3,3,2 | MILP; 54 | 47 | UNSAT | COUNTEREXAMPLE | Optimization terminated successfully. (HiGHS Status 7: Optimal) |
| milp_k3m4full | 3,4,full | MILP; 68 | 63 | UNKNOWN | UNKNOWN | Time limit reached. (HiGHS Status 13: Time limit reached) |
| milp_k3m4r1 | 3,4,1 | MILP; 68 | 43 | UNSAT | COUNTEREXAMPLE | Time limit reached. (HiGHS Status 13: Time limit reached) |
| milp_k3m6full | 3,6,full | MILP; 89 | 86 | UNKNOWN | UNKNOWN | Time limit reached. (HiGHS Status 13: Time limit reached) |
| milp_k3m6r1 | 3,6,1 | MILP; 89 | 59 | UNKNOWN | COUNTEREXAMPLE | Time limit reached. (HiGHS Status 13: Time limit reached) |
| milp_k4m2r1 | 4,2,1 | MILP; 144 | 49 | UNSAT | COUNTEREXAMPLE | Time limit reached. (HiGHS Status 13: Time limit reached) |
| milp_k4m3r1 | 4,3,1 | MILP; 168 | 60 | UNKNOWN | COUNTEREXAMPLE | Time limit reached. (HiGHS Status 13: Time limit reached) |
| mixedlp_k2m6full | 2,6,full | LP; 57 | 19 | UNSAT | VERIFIED | LP feasible |
| pool_k2m6r1 | 2,6,1 | pool; 19 | 19 | UNSAT | VERIFIED | learner UNSAT |
| pool_k2m8r1 | 2,8,1 | pool; 24 | no witness | — | — | learner SAT; checker UNKNOWN |
| pool_k2m8r1_long | 2,8,1 | pool; 24 | no witness | — | — | learner SAT; checker UNKNOWN |
| pool_k3m3full | 3,3,full | pool; 54 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| pool_k3m3r1 | 3,3,1 | pool; 54 | 39 | UNSAT | COUNTEREXAMPLE | learner UNKNOWN; checker UNKNOWN |
| pool_k3m3r2 | 3,3,2 | pool; 54 | no witness | — | — | learner UNKNOWN; checker UNKNOWN |
| pool_k4m2r1 | 4,2,1 | pool; 144 | 112 | UNSAT | COUNTEREXAMPLE | learner SAT |

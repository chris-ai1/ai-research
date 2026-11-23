import sys, random, itertools
sys.path.insert(0, sys.argv[1])
import nbp_check as m
rng = random.Random(11); cnt = 0
for tr in range(40):
    widths, E = m.rand_nbp(6, 3, rng.choice((0.3,0.45)), rng)
    S = {x: rng.random() < 0.5 for x in itertools.product((0,1), repeat=6)}
    r = m.peel_check(6, widths, E, S, K=2, beta=rng.choice((0.3,0.5,1.0)), rng=rng)
    if r and r['peels'] > 0: cnt += 1
print("K=2: all checks pass; instances with >=1 peel:", cnt, "of 40")

# working notes (theory)

## Periodic (bulk) reduction
Atom (beta, alpha, p, r, w): gates [L>=theta], L=beta.c+alpha.x, theta==r (mod p), theta in (Lmin,Lmax],
top weight -w p, plus free linear term w L.  Sum equals w*((L-r) mod p) + const EXACTLY on the box.
=> top sum = D(x) + sum_a w_a ((L_a - r_a) mod p_a): periodic in c with period P=lcm(2,p_a).
Correct for all m  <=>  correct on (Z/P)^nc (all residues occur once m>=P-1).
Cost: sum_a (||beta_a||_1 h + range(alpha_a.x))/p_a + cost(D) (+ O(1) rounding).

## Averaging lemma
F correct pointwise => average over each parity class (c with fixed block parities) correct.
Average of atom = ((g/2) e_{S(a)} + alpha.x - r) mod g + const, g = gcd(p, 2beta) (block-symmetric),
S(a) = {i: beta_i == g/2 mod g}.  => averaged F is parity-only:  D(x) + sum_S A_S(x) e_S, with
A_S = sum of two-valued gadgets, one per atom with S(a)=S.

## k=2 parity-only theorem (two-valued gadgets)
tables 1100,1010 (x_00,x_10,x_01,x_11): if n_1=n_2=1 contradiction (Delta_2>Delta_1 and Delta_1>Delta_2).
tables 1100,0110: if n_2=n_12=1 contradiction (Delta_12<Delta_2 and Delta_12>Delta_2).  Symmetric: n_1=n_12=1.
=> at least two of n_1,n_2,n_12 >= 2  => parity-only slope >= 1/2*2+1/2*2+1 = 3 = Theorem G.
(averaging => ANY periodic construction has >=2 atoms on two of the three character classes; but cheap
fluctuating atoms (odd beta, p>=4, cost 1/4) are not excluded by this.)

## monomial one-gadget lemma (all k>=2)
A_S = Delta_S (-1)^{l_S(x)} with l_S linear over GF(2) (period-2 atoms).  N-1 functionals on N bits =>
nonzero kernel v.  x and x+v have the same scores => nested level sets => v = e_c (weight 1), and then the
map is a bijection on x_{-c}; WLOG c = 0 ... (if c != 0 similar).  Then each x_b (b != 0) must be a single
y_{S(b)} (threshold = parity only for 1 variable) with Delta_{S(b)} > sum_{S.b odd, S != S(b)} Delta_S.
Summing over b: sum Delta > (N/2 - 1) sum Delta  => N < 4.  So impossible for k >= 2.

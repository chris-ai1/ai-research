# Four changes to a parity extension

Two changes to an easy truth table can together stay within the gate budget even when either change alone exceeds it. This note asks when two such pairs can be combined. For pairs in different coordinate directions the union exceeds the budget at every separation. The proof also covers overlapping directions when at least three other coordinates separate the pairs.

## Setup

Write $C(f)$ for the gate count over the full binary basis with free signs and constants. Use the baseline $B_m=h(y)\oplus\operatorname{Par}_m(z)$ from the [odd-error manuscript](../../../results/circuit-complexity/mcsp/papers/probabilistic/main.tex). It ignores $l\ge1$ selector bits $q$. Fix one fiber $(y,q)=(u,1^l)$. For $E\subseteq\{0,1\}^m$, write $B_m[E]$ for the result of flipping exactly the entries in $E$ in this fiber. Write $A_m$ for the minimum cost of an odd number of flips there, at the specified $h,l,u$.

The manuscript proves that a singleton attains $A_m$, that its position in the fiber is arbitrary, and that $A_m=A_{m-1}+2$ for $m\ge2$. We use the threshold $s=A_m-1$. Fixing a selector of a singleton circuit to its inactive value shows $C(B_m)\le s$ when $m\ge2$.

## Two disjoint pairs

Let the four distinct points be $a,a+d,b,b+e$, with addition over $\mathbb F_2$. The directions $d,e$ are nonzero and distinct. Put $I=\operatorname{supp}(d)\cup\operatorname{supp}(e)$. Call an index outside $I$ a separating coordinate if $a$ and $b$ differ there.

**Theorem.** The four flips have cost at least $A_m$ if either condition holds.

1. The supports of $d$ and $e$ are disjoint.
2. At least three separating coordinates exist.

In particular, two edges of the address cube in different coordinate directions are individually affordable and have an unaffordable union, however far apart the edges lie. The same holds for two individually affordable pairs with overlapping directions under condition 2.

### A circuit reduction

Choose a set $I$ of at least two parity coordinates. Write $W$ for the remaining parity coordinates and $x=(y,q,W)$. During the reduction a change of variables may translate the $I$-coordinates separately at each $x$. Retain each translation signal as an auxiliary output. These signals depend syntactically only on $x$. The baseline acquires their XOR as an extra summand, and the faults translate with the variables. On a clean selector fiber the main output is still full parity on $I$, up to a sign at each fixed $x$.

Suppose no translation by $e_i+e_j$ for distinct $i,j\in I$ preserves the current fault set. Here $e_i$ denotes a unit vector. The following operations either remove one gate in preparation or give a restriction fixing one $I$-coordinate and saving at least two gates.

- If some $I$-input has two gate readers, fix it to either value. Each reader becomes unary or constant.
- Otherwise each $I$-input has exactly one reader. Take the earliest gate depending on any of these inputs. If it reads two of them, freeze a clean $x$ and the other $I$-inputs. Both inputs reach the output only through this gate, so its truth table must be XOR or XNOR. This would make the whole output invariant under flipping those two inputs. The baseline and every tag are invariant under that flip, contradicting the assumption on the faults.
- The earliest gate therefore reads one $I$-input $z_i$ and a signal $H(x)$. For XOR or XNOR, use its output as the new raw $z_i$, retain the signed partner as a tag, and remove the gate. A projection can be bypassed. If the gate is nonlinear, fix $z_i$ to its canalizing value, so that the gate becomes constant. Its reader also becomes unary or constant. Such a reader exists since a clean fiber depends on at least two $I$-inputs, and no tag reads this gate.

Each preparation removes a gate. As long as the two-coordinate invariance remains excluded, a two-gate restriction must eventually occur. Restore ordinary parity after the restriction by feeding one surviving $I$-input its XOR with the sum of the tags. This costs at most one gate per preceding shear, and the tags have no dependency on that input. The net saving is at least two gates. Both the shears and the restoration are translations on each fixed $x$. In particular, the restoration preserves the number of remaining faults and their $W$-coordinates. All faults still lie in the original core/selector fiber.

### Cost of a single pair

For two flipped points at Hamming distance at least three, take $I$ to be their differing coordinates. They lie at the same $W$, so every shear translates them together. No two-coordinate flip preserves the pair, and fixing any $I$-coordinate always leaves a singleton. The reduced circuit costs at least $A_{m-1}$, giving the lower bound $A_m$.

At distance one, add an output XOR with the differing raw to a minimizing singleton circuit on $m-1$ parity bits. At distance two, substitute the XOR of the two differing raws for one parity input in that singleton circuit. Free signs place the points as prescribed. Each construction costs $A_{m-1}+1=s$. Conversely, fixing a differing raw in any pair circuit leaves a singleton and saves at least one gate, since the raw is essential on a clean fiber with $m\ge2$. Thus a pair costs exactly $s$ at distances one and two, and exceeds $s$ at all larger distances.

Wittcop's Lemma 4.2 gives the distance-one-or-two criterion for a table supported on two points at threshold $n-1$. Here the two changes are measured from the parity extension at the threshold set by its odd faults. [Wittcop, *2N Circuit Lower Bounds for the Minimum Circuit Size Problem*](https://www.academia.edu/180415409/2N_Circuit_Lower_Bounds_for_the_Minimum_Circuit_Size_Problem)

There is also a matching upper bound $A_m=s+1$ at distances three and four. More generally, at distance $D\ge2$ the pair costs at most

$$
 A_m+\lceil D/2\rceil-2.
$$

Translate the two sites to zero and the indicator of their $D$ differing coordinates. Group those coordinates into $t=\lfloor D/2\rfloor$ disjoint pairs and use the XOR of each pair as one new parity input. Keep all parity coordinates outside this group. Start with a minimizing singleton at zero on the resulting $m-D+t\ge1$ parity inputs. To make all $D$ original bits equal at the faults, pick one representative of each pair, and also the unpaired bit when $D$ is odd. Test a representative against each other representative for equality and AND these tests into an existing selector. Each comparison added to the selector costs two gates. The singleton forces equality within every pair and fixes the outside coordinates. The selector enforces equality between the pairs. Exactly the desired two faults remain.

For even $D=2t$ the baseline is unchanged and the construction adds $t+2(t-1)$ gates to $A_{m-t}$. For odd $D=2t+1$ append one final XOR with the unpaired bit to restore the baseline, giving $t+2t+1$ gates beyond $A_{m-t-1}$. The odd-error recurrence gives the displayed bound in both cases. Together with the distance-three lower bound this determines the cost exactly for $D=3,4$.

**Affine planes on four varying axes.** Any four-point affine plane varying in at most four coordinates stays within $s$, for every core. Its three nonzero directions have total Hamming weight at most eight, since every varying coordinate occurs in exactly two directions. Pick a direction of weight one or two. Quotienting by it maps the plane to two distinct points differing in at most three surviving coordinates. At weight one drop that axis and restore it by an output XOR. At weight two replace the two coordinates by their XOR, substituting this one gate into the quotient circuit. The original plane is the full preimage of the pair. The pair on $m-1$ bits costs at most $A_{m-1}$ and the added gate gives at most $s$. For $m=2$ the quotient pair is the whole one-bit fiber; fixing the parity raw in a minimizing one-fault circuit to the value retaining its fault saves a gate and computes $h$ with that fiber toggled, and appending the raw by XOR costs one. Thus this quotient also costs at most $A_1$.

### Proof for the union

Apply the circuit reduction with $I=\operatorname{supp}(d)\cup\operatorname{supp}(e)$. Each pair shares its own $W$-value, so throughout preparation the two directions remain $d$ and $e$. The XOR of the four addresses remains $d+e\ne0$. A four-element set invariant under any nonzero translation consists of two pairs with the same displacement and has XOR zero. This verifies the required exclusion after every shear.

If the coordinate fixed in the reduction belongs to just one direction, that pair leaves one fault, and the other leaves zero or two. The residual has odd size on either branch, including a branch forced by a canalizing gate. Its cost after restoration is at least $A_{m-1}$.

If the coordinate belongs to both directions, one fault from each pair survives. Under condition 2 the survivors still differ on at least three $W$-coordinates after restoration. The single-pair lower bound again gives $A_{m-1}$. Condition 1 only permits the odd case. Adding back the two saved gates gives $A_m$.

### Two distance-two pairs with a common coordinate

Suppose $d=e_c+e_i$ and $e=e_c+e_j$, with $c,i,j$ distinct. Write $t$ for the number of separating coordinates. The same lower bound holds if $t\ge2$, or if $t=1$ and the two pairs have opposite address parities. Both points of each pair have the same parity.

Use $I=\{c,i,j\}$. When $t\ge1$ the two pairs have different $W$-values. At every fixed $x=(y,q,W)$ the function is three-bit parity up to a sign and at most two faults. Each active raw is essential on every such slice, since a function independent of it would differ from parity on exactly four positions. This persists after all shears. A private nonlinear gate with partner $H(x)$ is now impossible unless $H$ is constant. Otherwise $H$ attains its own canalizing value on some slice and the raw is inessential there. A constant partner can be bypassed with a signed wire. Consequently the terminal restriction in the circuit reduction fixes a raw with at least two readers, and we may choose either branch.

Fixing $i$ or $j$ leaves an odd number of faults. If the raw is $c$, apply the same tag correction on a surviving input in both branches. From one branch to the other the survivor of the first pair changes in coordinate $i$, and that of the second changes in coordinate $j$. The two residual distances are therefore $t+v$ and $t+2-v$ for some $0\le v\le2$. Their maximum is at least three if $t\ge2$.

For $t=1$, the parity of these distances is the original cross-pair parity difference. Indeed the preliminary translations have total parity shift equal to the tag sum on each slice. The correction on the surviving raw adds that same sum, so the effective translation, including the subsequently fixed coordinate $c$, preserves address parity. Dropping $c$ does not affect distances within a branch. Opposite pair parities thus force distances one and three. Take the branch of distance three and apply the single-pair lower bound.

## Consequences at a quadratic budget

One can realize $s=n^2$ for all sufficiently large $n$, with $m=n-O(\log n)$ parity coordinates in the same baseline. Use the [threshold interpolation in the odd-error manuscript](../../../results/circuit-complexity/mcsp/papers/probabilistic/main.tex) with $r=\lceil4\log_2 n\rceil$ core bits. The path of cores starts with $A_1(1)=O(r)$, ends with $A_1(1)=\Omega(2^r/r)$, and has upward steps bounded by an absolute constant. Here $A_1(1)$ is minimized over $u$ with one selector. At each core, varying $l$ over the integers from 3 to a sufficiently large absolute constant gives a consecutive interval of budgets

$$
  A_1(1)+2(n-r)-l-4,\qquad m=n-r-l .
$$

This follows from the manuscript's selector and parity recurrences for the fiber minimum over $u$. The interval width exceeds the maximum upward step, so some core and minimizing fiber attain $n^2$.

Take four distinct neighbors of one parity address in this fiber. Their six pairs have distance two. Any partition into two pairs gives disjoint direction supports. On this four-site restriction the accepted inputs flip exactly zero or two entries. Across a split into two sites on each side, the left weights 0, 1 and 2 give three different functions of the right pair. A single bit computed from the left pair cannot carry all three possibilities. A lower bound on total outer gates would require showing that many such restrictions force distinct branching gates.

## The remaining local configurations

For individually affordable pairs, different overlapping directions share exactly one coordinate. A distance-one and a distance-two pair then vary on at most four axes unless there are three separating coordinates. Two distance-two pairs sharing a coordinate can have at most one separating coordinate left to consider. All the constant parity coordinates can be moved into the core by replacing $h$ with its XOR with their parity and fixing the enlarged core value. The baseline and the one-fault functions there are identical as functions of the original inputs, so the threshold remains the same.

Up to translating and permuting the varying axes, only the following three configurations still need an arbitrary-core proof.

| Pair distances | Separating coordinates | Four addresses |
| --- | --- | --- |
| 1 and 2 | 1 | 000, 001, 010, 111 |
| 1 and 2 | 2 | 0000, 0001, 1100, 1111 |
| 2 and 2 | 1, all four addresses of the same parity | 0000, 0011, 1010, 1100 |

For the first two rows the shared coordinate runs along the edge. Flipping it preserves that edge as a set and interchanges the two placements of the other pair's diagonal once its passive coordinates are fixed. With zero separators, four distinct sites cannot fit this pattern in two dimensions. For the last row, translate one pair to $\{0,d\}$. Translation by $d$ still preserves that pair and lets one choose the constant value of the $i$-coordinate on the other pair. Its address parity then specifies its diagonal on $(c,j)$. With zero separators, regroup the sites by their $c$ value. The other two coordinates each vary in exactly one of the two new pairs, giving disjoint supports.

A tempting shortcut is to fix a coordinate leaving three faults and charge an extra gate for the triple. Three faults can attain the odd minimum. With three parity inputs $x,y,z$, a constant zero core and one selector $q$, the five-gate function

$$
 (x\oplus y)\oplus\bigl(z\lor(q\land\neg(x\land y))\bigr)
$$

differs from parity precisely when $q=1$, $z=0$ and $(x,y)\ne(1,1)$. Here $A_1=1$ and $A_3=5$.

For comparison, take four parity bits, a single selector, and a constant zero core. The threshold is six. Exact synthesis on the selector-one fiber finds that all 140 four-point affine planes stay within budget and all 1,680 other quadruples exceed it. Address translations and permutations give 19 cases in total. The [synthesis script](check_four_flips.py) checks all cases, including the case verdicts underlying both counts. The computation treats this one core and budget. The arbitrary-core assertion for the remaining nearby pairs is open.

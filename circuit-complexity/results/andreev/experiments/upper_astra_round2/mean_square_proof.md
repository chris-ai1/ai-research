<!-- Copyright (c) 2026 Christian Reitwiessner. -->
Authors: Christian Reitwiessner

# Random-mask mean-square calculation (working proof)

Fix $r\le k$, $t=2^r$, and $\mathcal S=2^{[r]}\setminus\{\varnothing\}$. Write $\xi_c=2x_c-1$, $X_S=\sum_c\chi_S(c)\xi_c$. For each nonempty $S$, independently choose a uniform mask $z_S$ on its $M_S=m|S|$ active bits. Put $h_S=\lfloor M_S/2\rfloor$, $D_S=|a_S\oplus z_S|-h_S$, $\sigma_S=(-1)^{|z_S|+h_S}$, $\phi(u)=(-1)^u u$, and $f_R(u)=\phi(u)\mathbf1[|u|\le R]$.

Because $X_S$ is even,
$$\sigma_S(\phi(X_S+D_S)+\phi(X_S-D_S))=2X_S\chi_S(b).$$
Use score
$$P_z=2X_\varnothing+\sum_{S\in\mathcal S}\sigma_S(f_R(X_S+D_S)+f_R(X_S-D_S)).$$
The exact score is $P_*=2t\sum_{c\in Q(b)}\xi_c$.

Let $e_S$ denote the clipped-minus-exact error for one character. Conditional on fixed $x,a$, $D_S$ has the distribution $\operatorname{Bin}(M_S,1/2)-h_S$, independent of the raw address, and
$$\sigma_S=\chi_S(b)(-1)^{D_S}.$$
Thus $\mathbb E_z e_S=\chi_S(b)g_S(X_S)$ for a table-only function $g_S$. Different characters use independent masks. Since uniform raw blocks have independent uniform parities, for $S\ne T$,
$$\mathbb E_{x,a,z}e_Se_T=\mathbb E_x[g_S(X_S)g_T(X_T)]\mathbb E_a\chi_{S\triangle T}(b)=0.$$
In particular no independence between Walsh coefficients is asserted. Therefore
$$\mathbb E_{z,x,a}(P_z-P_*)^2=\sum_S\mathbb E e_S^2.$$

For $U=X_S\pm D_S$, its centered version $Y$ is a sum of independent centered variables with subgaussian variance proxy $V_S=N+M_S/4$. Its mean has absolute value at most $1/2$. For integer $R\ge1$, put $q=R/2$. Then
$$\mathbb E U^2\mathbf1[|U|>R]\le (R^2+8V_S+1)e^{-R^2/(8V_S)}\le16V_S e^{-R^2/(16V_S)}.$$
The first inequality follows from $U^2\le2Y^2+1/2$, the implication $|U|>R\Rightarrow|Y|>R/2$, and integration of $\Pr(|Y|>u)\le2e^{-u^2/(2V_S)}$. For the second put $v=R^2/(8V_S)$ and use $(v+2)e^{-v/2}\le2$ and $V_S\ge1$.
Since $e_S^2\le2(U_+^2\mathbf1[|U_+|>R]+U_-^2\mathbf1[|U_-|>R])$, for $V=N+rm/4$,
$$\mathbb E(P_z-P_*)^2\le64(t-1)V e^{-R^2/(16V)}.$$

For $t=N$ the exact score has absolute value $2t$; test $P_z\ge0$. For $t<N$, the subcube size is even and $P_*$ is a multiple of $4t$; test $P_z\ge-2t$, reproducing majority with ties positive whenever $|P_z-P_*|<2t$. Markov's inequality and averaging over the masks give a deterministic mask choice whose probability of disagreement with that majority is at most
$$\frac{16V}{t}e^{-R^2/(16V)}.$$
Choose
$$R=\left\lceil4\sqrt{V\log\frac{16V}{t\delta}}\right\rceil.$$
The resulting agreement with ordinary Andreev is at least $1/2+p(N/t)/2-\delta$ (where $p(1)=1$). The case $t=1$ is exact subcube majority with zero bottoms, handled separately.

Each $f_R(U)$ is exactly
$$\sum_{\ell=-R}^{R+1}(f_R(\ell)-f_R(\ell-1))[U\ge\ell],$$
so the circuit needs at most $4(t-1)(R+1)$ bottoms plus one top. Both $U_+$ and $U_-$ are affine forms in raw table/address bits; no parity or other computed inputs are supplied.

At balance $V\le5N/4$, $t=N$ yields $O(n^{3/2}\sqrt{\log(1/\delta)})$ gates. For $N^{-1/2}\le\varepsilon\le1/8$, choose the least power of two $t\ge32\varepsilon^2N$ and $\delta=\varepsilon$. Then $t<64\varepsilon^2N$, $t\le N$, majority advantage is at least $2\varepsilon$, and the bound is $O(\varepsilon^2 n^{3/2}\sqrt{\log(1/\varepsilon)})$ bottoms, with support wires at most $n$ times this plus top wires. This is a logarithmic improvement over the read baseline when $\log(1/\varepsilon)=o(\log n)$, including constant advantage. It does not remove the logarithm at polynomially small advantage.

Mixed masks: a union bound gives probability at most $rt2^{-m}$ that any active block of any mask is constant. Conditioning on the complementary event multiplies the average error bound by at most $1/(1-rt2^{-m})$. Taking a smaller error budget before conditioning preserves the bound whenever this probability is bounded away from one. In the balanced growing-$k$ regime it tends to zero rapidly. This is conditioning a distribution over fixed circuits, not changing the uniform raw input measure.

import Mathlib.Algebra.Polynomial.Coeff
import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Algebra.BigOperators.Group.Finset.Piecewise

/-!
For finite row, copy and mask alphabets, pulling back a monomial through row-local
shifts can identify sites within a row but never across rows. Its actual Bernoulli
expectation is therefore a power of the thinning parameter. Matching the marginals
of two finite label laws implies divisibility of the difference interpolation by
a power of the polynomial variable. Finite signed weights are allowed, so ordinary
probability weights over the reals are a special case.
-/
namespace ShiftMask

open scoped BigOperators
open Finset Polynomial

variable {Row Copy Loc Label K : Type*} [DecidableEq Row] [DecidableEq Loc]

/-- Indices of the original, independently sampled mask bits required by a monomial. -/
def privateSites (shift : Label → Copy → Loc → Loc) (y : Row → Label)
    (S : Finset (Row × Copy × Loc)) : Finset (Row × Loc) :=
  S.image fun s => (s.1, shift (y s.1) s.2.1 s.2.2)

theorem private_exponent_bounds (shift : Label → Copy → Loc → Loc) (y : Row → Label)
    (S : Finset (Row × Copy × Loc)) :
    (S.image Prod.fst).card ≤ (privateSites shift y S).card ∧
      (privateSites shift y S).card ≤ S.card := by
  constructor
  · have h := Finset.card_image_le (s := privateSites shift y S) (f := Prod.fst)
    simpa [privateSites, Finset.image_image, Function.comp_def] using h
  · exact Finset.card_image_le

theorem privateSites_local (shift : Label → Copy → Loc → Loc) {a b : Row → Label}
    (S : Finset (Row × Copy × Loc))
    (h : ∀ i ∈ S.image Prod.fst, a i = b i) :
    privateSites shift a S = privateSites shift b S := by
  apply Finset.image_congr
  intro s hs
  simp [h s.1 (Finset.mem_image_of_mem _ hs)]

/-- The jointly weighted probability that all specified independent bits are true.
Each unconstrained bit contributes its two possible weights. This identity is
polynomial in t and holds over any commutative ring, without positivity hypotheses. -/
theorem bernoulli_monomial {ι : Type*} [Fintype ι] [DecidableEq ι] [CommRing K]
    (t : K) (S : Finset ι) :
    (∑ mask : ι → Bool, ∏ i,
      (if mask i then t else 1 - t) * (if i ∈ S ∧ mask i = false then 0 else 1)) =
      t ^ S.card := by
  rw [← Fintype.prod_sum fun (i : ι) (b : Bool) =>
    (if b then t else 1 - t) * (if i ∈ S ∧ b = false then 0 else 1)]
  have bit (i : ι) : (∑ b : Bool, (if b then t else 1 - t) *
      (if i ∈ S ∧ b = false then 0 else 1)) = if i ∈ S then t else 1 := by
    rw [Fintype.sum_bool]
    by_cases hi : i ∈ S <;> simp [hi]
  simp_rw [bit]
  simp [Finset.prod_ite_mem]

/-- Finite marginal equality in its test-function form: integrating any statistic
which depends only on at most D row labels gives the same result. -/
def Matches [Fintype Row] [Fintype Label] [CommRing K] (D : ℕ)
    (μ ν : (Row → Label) → K) : Prop :=
  ∀ (R : Finset Row), R.card ≤ D → ∀ (f : (Row → Label) → K),
    (∀ a b, (∀ i ∈ R, a i = b i) → f a = f b) →
      ∑ y, μ y * f y = ∑ y, ν y * f y

/-- Pointwise equality of the usual finite marginals implies test-function matching. -/
theorem matches_of_marginals [Fintype Row] [Fintype Label] [DecidableEq Label]
    [CommRing K] (μ ν : (Row → Label) → K) {D : ℕ}
    (hm : ∀ (R : Finset Row), R.card ≤ D → ∀ z : R → Label,
      (∑ y : Row → Label with (fun i : R => y i) = z, μ y) =
      (∑ y : Row → Label with (fun i : R => y i) = z, ν y)) : Matches D μ ν := by
  classical
  intro R hR f hf
  let restrict (y : Row → Label) : R → Label := fun i => y i
  rw [← Finset.sum_fiberwise univ restrict (fun y => μ y * f y),
      ← Finset.sum_fiberwise univ restrict (fun y => ν y * f y)]
  apply Finset.sum_congr rfl
  intro z _
  by_cases liftable : ∃ u, restrict u = z
  · obtain ⟨u, hu⟩ := liftable
    have factor (w : (Row → Label) → K) :
        (∑ y : Row → Label with restrict y = z, w y * f y) =
        (∑ y : Row → Label with restrict y = z, w y) * f u := by
      rw [Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro y hy
      congr 1
      apply hf
      intro i hi
      exact congrFun ((Finset.mem_filter.mp hy).2.trans hu.symm) ⟨i, hi⟩
    rw [factor μ, factor ν]
    exact congrArg (fun a => a * f u) (hm R hR z)
  · have empty : (univ.filter (fun y : Row → Label => restrict y = z)) = ∅ := by
      apply Finset.eq_empty_iff_forall_notMem.mpr
      intro y hy
      exact liftable ⟨y, (Finset.mem_filter.mp hy).2⟩
    simp [empty]

noncomputable def monomialPoly [Fintype Row] [Fintype Label] [CommRing K]
    (shift : Label → Copy → Loc → Loc) (μ : (Row → Label) → K)
    (S : Finset (Row × Copy × Loc)) : K[X] :=
  ∑ y, C (μ y) * X ^ (privateSites shift y S).card

/-- Evaluation agrees with the actual finite sum over labels and independent
mask assignments, with repeated requirements on the same mask bit counted once. -/
theorem monomialPoly_eval [Fintype Row] [Fintype Label] [Fintype Loc] [CommRing K]
    (shift : Label → Copy → Loc → Loc) (μ : (Row → Label) → K)
    (S : Finset (Row × Copy × Loc)) (t : K) :
    (monomialPoly shift μ S).eval t =
      ∑ y, μ y * ∑ mask : Row × Loc → Bool, ∏ i,
        (if mask i then t else 1 - t) *
        (if i ∈ privateSites shift y S ∧ mask i = false then 0 else 1) := by
  classical
  simp_rw [bernoulli_monomial t]
  simp [monomialPoly, Polynomial.eval_finsetSum]

theorem monomialPoly_dvd [Fintype Row] [Fintype Label] [CommRing K]
    (shift : Label → Copy → Loc → Loc) (μ ν : (Row → Label) → K) {D : ℕ}
    (matchLaw : Matches D μ ν) (S : Finset (Row × Copy × Loc)) :
    (X : K[X]) ^ (D+1) ∣ monomialPoly shift μ S - monomialPoly shift ν S := by
  classical
  by_cases low : (S.image Prod.fst).card ≤ D
  · have equal : monomialPoly shift μ S = monomialPoly shift ν S := by
      ext j
      simp only [monomialPoly, finsetSum_coeff, coeff_C_mul]
      apply matchLaw (S.image Prod.fst) low
      intro a b hab
      rw [privateSites_local shift S hab]
    simp [equal]
  · have high (w : (Row → Label) → K) : (X : K[X]) ^ (D+1) ∣ monomialPoly shift w S := by
      apply Finset.dvd_sum
      intro y _
      apply dvd_mul_of_dvd_right
      exact pow_dvd_pow _ (le_trans (Nat.lt_of_not_ge low) (private_exponent_bounds shift y S).1)
    exact dvd_sub (high μ) (high ν)

/-- The difference interpolation of any finite real multilinear polynomial has
zero coefficients in degrees through D, stated as divisibility by X^(D+1). -/
theorem polynomial_dvd [Fintype Row] [Fintype Label] [CommRing K]
    (shift : Label → Copy → Loc → Loc) (μ ν : (Row → Label) → K) {D : ℕ}
    (matchLaw : Matches D μ ν) (terms : Finset (Finset (Row × Copy × Loc)))
    (coefficient : Finset (Row × Copy × Loc) → K) :
    (X : K[X]) ^ (D+1) ∣
      (∑ S ∈ terms, C (coefficient S) * monomialPoly shift μ S) -
      (∑ S ∈ terms, C (coefficient S) * monomialPoly shift ν S) := by
  rw [← Finset.sum_sub_distrib]
  apply Finset.dvd_sum
  intro S _
  rw [← mul_sub]
  exact dvd_mul_of_dvd_right (monomialPoly_dvd shift μ ν matchLaw S) _

end ShiftMask

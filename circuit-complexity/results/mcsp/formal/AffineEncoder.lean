import Mathlib.LinearAlgebra.LinearIndependent.Basic
import Mathlib.LinearAlgebra.Basis.VectorSpace
import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Linarith

/-! Two steps of the common affine encoder proof. A pivot can be read by a
linear form vanishing on the retained columns outside its block. Replacement
columns independent after these tests are independent of the retained columns.
The last lemma converts per-leaf lower bounds into overlap of probability laws. -/
namespace AffineEncoder
open scoped BigOperators

section Pivots
variable {K V W I J : Type*} [Field K] [AddCommGroup V] [Module K V]
  [AddCommGroup W] [Module K W]

/-- Linear coordinates for the current pivots jointly annihilate all other
retained columns, including earlier encoded replacements. -/
theorem pivot_forms (old : I → V) (pivot : J → V)
    (hi : LinearIndependent K (Sum.elim old pivot)) [DecidableEq J] :
    ∃ read : J → V →ₗ[K] K, (∀ j i, read j (old i) = 0) ∧
      (∀ j k, read j (pivot k) = if j = k then 1 else 0) := by
  classical
  let v := Sum.elim old pivot
  obtain ⟨g, hg⟩ := hi.repr.exists_extend
  have hs (a : I ⊕ J) : g (v a) = Finsupp.single a 1 := by
    let x : Submodule.span K (Set.range v) :=
      ⟨v a, Submodule.subset_span (Set.mem_range_self a)⟩
    have he := DFunLike.congr_fun hg x
    exact he.trans (hi.repr_eq_single a x rfl)
  refine ⟨fun j => (Finsupp.lapply (R := K) (Sum.inr j)).comp g, ?_, ?_⟩
  · intro j i
    change (g (v (.inl i))) (.inr j) = 0
    rw [hs]
    simp
  · intro j k
    change (g (v (.inr k))) (.inr j) = _
    rw [hs]
    by_cases e : j = k
    · subst k
      simp
    · simp [e]

/-- A surjective local test can supply columns independent in the quotient.
This lemma states the precise invariant after those columns have been selected. -/
theorem replace_block [Fintype I] [Fintype J] (old : I → V) (new : J → V)
    (read : V →ₗ[K] W) (ho : LinearIndependent K old)
    (hz : ∀ i, read (old i) = 0)
    (hn : LinearIndependent K (fun j => read (new j))) :
    LinearIndependent K (Sum.elim old new) := by
  classical
  apply Fintype.linearIndependent_iff.mpr
  intro c h a
  rw [Fintype.sum_sum_type] at h
  simp only [Sum.elim_inl, Sum.elim_inr] at h
  have test := congrArg read h
  simp [map_sum, hz] at test
  have right : ∀ j, c (.inr j) = 0 :=
    Fintype.linearIndependent_iff.mp hn (fun j => c (.inr j)) test
  simp [right] at h
  cases a with
  | inl i => exact Fintype.linearIndependent_iff.mp ho _ h i
  | inr j => exact right j
end Pivots

/-- A leaf of uniform mass u receives at least (1-e)u under the code whenever
it is shallow. Only the *total uniform mass* of the remaining leaves is lost. -/
theorem overlap [Fintype I] (uniform easy : I → ℝ) (shallow : Finset I)
    (e : ℝ) (he : 0 ≤ e)
    (hu : ∀ i, 0 ≤ uniform i) (hc : ∀ i, 0 ≤ easy i)
    (good : ∀ i ∈ shallow, (1-e) * uniform i ≤ easy i) :
    (1-e) * (∑ i ∈ shallow, uniform i) ≤ ∑ i, min (uniform i) (easy i) := by
  classical
  rw [Finset.mul_sum]
  calc
    _ ≤ ∑ i ∈ shallow, min (uniform i) (easy i) := by
      apply Finset.sum_le_sum
      intro i hi
      exact le_min (by nlinarith [mul_nonneg he (hu i)]) (good i hi)
    _ ≤ _ := Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _) <| by
      intro i _ _
      exact le_min (hu i) (hc i)

end AffineEncoder

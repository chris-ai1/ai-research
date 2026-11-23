import Std

/-!
The counting step for disjoint translates. Let `changed x i` mean that
table `x` differs from the starting pattern on copy `i`. If an accepted
table can change any untouched copy alone, accepted tables realize every
mask on the copies. The MCSP note supplies the change rule by contradiction.
-/

namespace LocalIsolation

variable {α ι : Type} (accepted : α → Prop) (changed : α → ι → Prop)

private theorem realize (start : ∃ x, accepted x ∧ ∀ i, ¬ changed x i)
    (step : ∀ x, accepted x → ∀ i, ¬ changed x i →
      ∃ y, accepted y ∧ ∀ j, changed y j ↔ j = i ∨ changed x j)
    (copies : List ι) :
    ∃ x, accepted x ∧ ∀ j, changed x j ↔ j ∈ copies := by
  classical
  induction copies with
  | nil =>
    obtain ⟨x, hx, h⟩ := start
    exact ⟨x, hx, fun j => by simp [h j]⟩
  | cons i copies ih =>
    obtain ⟨x, hx, h⟩ := ih
    by_cases hi : changed x i
    · refine ⟨x, hx, fun j => ?_⟩
      rw [List.mem_cons]
      exact ⟨fun hj => Or.inr ((h j).mp hj),
        fun hj => hj.elim (fun e => e ▸ hi) (h j).mpr⟩
    · obtain ⟨y, hy, update⟩ := step x hx i hi
      exact ⟨y, hy, fun j => by rw [update j, h j, List.mem_cons]⟩

/-- Distinct masks on the m copies give distinct accepted tables. -/
theorem inject_masks {m : Nat} (accepted : α → Prop) (changed : α → Fin m → Prop)
    (start : ∃ x, accepted x ∧ ∀ i, ¬ changed x i)
    (step : ∀ x, accepted x → ∀ i, ¬ changed x i →
      ∃ y, accepted y ∧ ∀ j, changed y j ↔ j = i ∨ changed x j) :
    ∃ f : (Fin m → Bool) → α, (∀ b, accepted (f b)) ∧
      ∀ b b', f b = f b' → b = b' := by
  classical
  have witness (b : Fin m → Bool) :
      ∃ x, accepted x ∧ ∀ j, changed x j ↔ b j = true := by
    obtain ⟨x, hx, h⟩ := realize accepted changed start step ((List.finRange m).filter b)
    exact ⟨x, hx, fun j => by simpa using h j⟩
  let f (b : Fin m → Bool) := (witness b).choose
  have spec (b : Fin m → Bool) := (witness b).choose_spec
  refine ⟨f, fun b => (spec b).1, ?_⟩
  intro b b' heq
  funext j
  have h : (b j = true) ↔ (b' j = true) := calc
    b j = true ↔ changed (f b) j := ((spec b).2 j).symm
    _ ↔ changed (f b') j := by rw [heq]
    _ ↔ b' j = true := (spec b').2 j
  simpa using h

end LocalIsolation

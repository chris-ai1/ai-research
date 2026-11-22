import Std

/-! Best-case teaching and signed equality projections, with no dependencies beyond Lean. -/
namespace TeachingProjection

abbrev Word (ι : Type) := ι → Bool

def Teaches (A : List (Word ι)) (x : Word ι) (J : List ι) : Prop :=
  ∀ y ∈ A, (∀ i ∈ J, y i = x i) → y = x

private theorem split_length (A : List (Word ι)) (i : ι) :
    (A.filter (fun y => y i)).length + (A.filter (fun y => !(y i))).length = A.length := by
  induction A with
  | nil => simp
  | cons y A ih => cases h : y i <;> simp [h, ih, Nat.succ_add] <;> omega

/-- The exponential form also works for an enumeration with repeated members. -/
theorem teaching_pow (A : List (Word ι)) (hn : A ≠ []) :
    ∃ x ∈ A, ∃ J : List ι, 2 ^ J.length ≤ A.length ∧ Teaches A x J := by
  classical
  by_cases hs : ∃ i, (∃ x ∈ A, x i = true) ∧ (∃ y ∈ A, y i = false)
  · obtain ⟨i, ⟨x,hx,hi⟩, y,hy,hj⟩ := hs
    let P := A.filter (fun z => z i)
    let M := A.filter (fun z => !(z i))
    have hp : x ∈ P := List.mem_filter.mpr ⟨hx,hi⟩
    have hm : y ∈ M := List.mem_filter.mpr ⟨hy, by simp [hj]⟩
    have hsum : P.length + M.length = A.length := split_length A i
    have select : ∃ b : Bool, let B := A.filter (fun z => z i == b); B ≠ [] ∧ 2*B.length ≤ A.length := by
      by_cases h : P.length ≤ M.length
      · refine ⟨true, ?_⟩
        simpa [P] using And.intro (List.ne_nil_of_mem hp) (show 2*P.length ≤ A.length by omega)
      · refine ⟨false, ?_⟩
        simpa [M] using And.intro (List.ne_nil_of_mem hm) (show 2*M.length ≤ A.length by omega)
    obtain ⟨b,hb,hsmall⟩ := select
    let B := A.filter (fun z => z i == b)
    have hpos : 0 < B.length := List.length_pos_iff.mpr hb
    have hlt : B.length < A.length := by change 2*B.length ≤ A.length at hsmall; omega
    obtain ⟨z,hz,J,hJ,hTeach⟩ := teaching_pow B hb
    obtain ⟨hzA,hzi⟩ := List.mem_filter.mp hz
    refine ⟨z,hzA,i::J, ?_, ?_⟩
    · simp only [List.length_cons, Nat.pow_succ]
      change 2*B.length ≤ A.length at hsmall
      omega
    · intro w hw heq
      apply hTeach w
      · apply List.mem_filter.mpr
        exact ⟨hw, (heq i (by simp)) ▸ hzi⟩
      · intro j hj
        exact heq j (by simp [hj])
  · obtain ⟨x,hx⟩ := List.exists_mem_of_ne_nil A hn
    refine ⟨x,hx,[],by have := List.length_pos_iff.mpr hn; simp; omega, ?_⟩
    intro y hy _
    funext i
    cases h₁ : y i <;> cases h₂ : x i <;> first | rfl | exact False.elim (hs ⟨i,⟨x,hx,h₂⟩,y,hy,h₁⟩) | exact False.elim (hs ⟨i,⟨y,hy,h₁⟩,x,hx,h₂⟩)
termination_by A.length
decreasing_by exact hlt

/-- A teacher using at most floor(log₂ |A|) queries. A duplicate-free list
    enumerating any finite family gives its ordinary set cardinality. -/
theorem teaching_log (A : List (Word ι)) (hn : A ≠ []) :
    ∃ x ∈ A, ∃ J : List ι, J.length ≤ A.length.log2 ∧ Teaches A x J := by
  obtain ⟨x,hx,J,hJ,ht⟩ := teaching_pow A hn
  exact ⟨x,hx,J,(Nat.le_log2 (by have := List.length_pos_iff.mpr hn; omega)).2 hJ,ht⟩

def flip (x : Word ι) : Word ι := fun i => !(x i)

noncomputable def project (x : Word ι) (J : List ι) (b : Bool) (u : {i // i ∉ J} → Bool) : Word ι :=
  fun i => open Classical in if h : i ∈ J then x i ^^ b else x i ^^ u ⟨i,h⟩

/-- Each untaught coordinate has its own input, and the taught ones share b.
    The projected membership predicate tests whether every free input equals b. -/
theorem signed_projection (A : List (Word ι)) (x : Word ι) (J : List ι)
    (hx : x ∈ A) (ht : Teaches A x J) (hc : ∀ y ∈ A, flip y ∈ A)
    (b : Bool) (u : {i // i ∉ J} → Bool) :
    project x J b u ∈ A ↔ ∀ j, u j = b := by
  classical
  constructor
  · intro hp
    cases b with
    | false =>
      have e := ht _ hp (by intro i hi; simp [project,hi])
      intro ⟨i,hi⟩
      have h := congrFun e i
      cases hv : u ⟨i,hi⟩ <;> cases hz : x i <;> simp_all [project]
    | true =>
      have e := ht _ (hc _ hp) (by intro i hi; simp [project,flip,hi])
      intro ⟨i,hi⟩
      have h := congrFun e i
      cases hv : u ⟨i,hi⟩ <;> cases hz : x i <;> simp_all [project,flip]
  · intro h
    cases b with
    | false =>
      have e : project x J false u = x := by
        funext i; by_cases hi : i ∈ J <;> simp [project,hi,h]
      rwa [e]
    | true =>
      have e : project x J true u = flip x := by
        funext i; by_cases hi : i ∈ J <;> simp [project,flip,hi,h]
      exact e ▸ hc x hx

/-- A single-output straight-line program over the full binary basis. The first
    gate adds a fresh register indexed by none; some retains earlier wires.
    Edge signs and output signs are free. -/
structure Literal (ι : Type) where
  wire : ι
  sign : Bool

def Literal.eval (l : Literal ι) (a : Word ι) := a l.wire ^^ l.sign

inductive Program : Type → Type 1 where
  | constant (b : Bool) : Program ι
  | output (l : Literal ι) : Program ι
  | gate (op : Bool → Bool → Bool) (l r : Literal ι) (tail : Program (Option ι)) : Program ι

def extend (a : Word ι) (v : Bool) : Word (Option ι)
  | none => v
  | some i => a i

def Program.eval : Program ι → Word ι → Bool
  | .constant b, _ => b
  | .output l, a => l.eval a
  | .gate op l r tail, a => tail.eval (extend a (op (l.eval a) (r.eval a)))

def Program.size : Program ι → Nat
  | .constant _ => 0
  | .output _ => 0
  | .gate _ _ _ tail => tail.size + 1

def Literal.subst (l : Literal ι) (σ : ι → Literal κ) : Literal κ :=
  ⟨(σ l.wire).wire, (σ l.wire).sign ^^ l.sign⟩

def liftSubst (σ : ι → Literal κ) : Option ι → Literal (Option κ)
  | none => ⟨none,false⟩
  | some i => ⟨some (σ i).wire,(σ i).sign⟩

def Program.subst : Program ι → (ι → Literal κ) → Program κ
  | .constant b, _ => .constant b
  | .output l, σ => .output (l.subst σ)
  | .gate op l r tail, σ => .gate op (l.subst σ) (r.subst σ) (tail.subst (liftSubst σ))

@[simp] theorem size_subst (c : Program ι) (σ : ι → Literal κ) :
    (c.subst σ).size = c.size := by
  induction c generalizing κ with
  | constant => rfl
  | output => rfl
  | gate _ _ _ _ ih => simp [Program.subst,Program.size,ih]

@[simp] theorem literal_eval_subst (l : Literal ι) (σ : ι → Literal κ) (a : Word κ) :
    (l.subst σ).eval a = l.eval (fun i => (σ i).eval a) := by
  simp [Literal.subst,Literal.eval]

theorem eval_subst (c : Program ι) (σ : ι → Literal κ) (a : Word κ) :
    (c.subst σ).eval a = c.eval (fun i => (σ i).eval a) := by
  induction c generalizing κ with
  | constant => rfl
  | output => exact literal_eval_subst _ _ _
  | gate op l r tail ih =>
    simp only [Program.subst,Program.eval,literal_eval_subst,ih]
    congr 1
    funext i; cases i <;> simp [liftSubst,Literal.eval,extend]

noncomputable def projectionSubst (x : Word ι) (J : List ι) (i : ι) :
    Literal (Option {i // i ∉ J}) :=
  open Classical in if h : i ∈ J then ⟨none,x i⟩ else ⟨some ⟨i,h⟩,x i⟩

/-- An actual unchanged-size program for equality on the selector and the
    untaught indices, obtained from a program deciding membership in A. -/
theorem equality_program (A : List (Word ι)) (hn : A ≠ [])
    (hc : ∀ y ∈ A, flip y ∈ A) (c : Program ι)
    (hdec : ∀ a, c.eval a = true ↔ a ∈ A) :
    ∃ J : List ι, J.length ≤ A.length.log2 ∧
      ∃ d : Program (Option {i // i ∉ J}), d.size = c.size ∧
        ∀ a, d.eval a = true ↔ ∀ i, a (some i) = a none := by
  classical
  obtain ⟨x,hx,J,hJ,ht⟩ := teaching_log A hn
  refine ⟨J,hJ,
    c.subst (projectionSubst x J),size_subst ..,?_⟩
  intro a
  rw [eval_subst,hdec]
  have heq : (fun i => (projectionSubst x J i).eval a) =
      project x J (a none) (fun i => a (some i)) := by
    funext i; by_cases hi : i ∈ J <;> simp [projectionSubst,Literal.eval,project,hi,Bool.xor_comm]
  rw [heq]
  exact signed_projection A x J hx ht hc _ _

private theorem filter_lengths (xs : List ι) (p : ι → Bool) :
    (xs.filter p).length + (xs.filter (fun i => !(p i))).length = xs.length := by
  induction xs with
  | nil => simp
  | cons i xs ih => cases h : p i <;> simp [h] <;> omega

/-- Actual dimension of the equality instance (including the selector). -/
def eqArity {n : Nat} (J : List (Fin n)) : Nat :=
  ((List.finRange n).filter (fun i => !decide (i ∈ J))).length + 1

theorem arity_lower {n : Nat} (J : List (Fin n)) : n + 1 ≤ eqArity J + J.length := by
  let p := fun i : Fin n => decide (i ∈ J)
  have hdup : ((List.finRange n).filter p).Nodup :=
    (List.filter_sublist ..).nodup (List.nodup_finRange n)
  have hle : ((List.finRange n).filter p).length ≤ J.length :=
    hdup.length_le_of_subset (by intro i hi; simpa [p] using (List.mem_filter.mp hi).2)
  have hsum := filter_lengths (List.finRange n) p
  rw [List.length_finRange] at hsum
  unfold eqArity
  dsimp [p] at *
  omega

/-- External mathematical input: Schnorr's lower bound 2m−3 for testing if
    all m wires agree. The additive form handles arity one without subtraction. -/
def SchnorrBound : Prop :=
  ∀ (n : Nat) (J : List (Fin n)) (d : Program (Option {i // i ∉ J})),
    (∀ a, d.eval a = true ↔ ∀ i, a (some i) = a none) →
    2 * eqArity J ≤ d.size + 3

/-- Every deciding program has size at least 2n−2 floor(log₂ |A|)−1,
    taking a duplicate-free enumeration of A for its true cardinality. -/
theorem complement_family_lower (schnorr : SchnorrBound)
    (A : List (Word (Fin n))) (hn : A ≠ []) (hc : ∀ y ∈ A, flip y ∈ A)
    (c : Program (Fin n)) (hdec : ∀ a, c.eval a = true ↔ a ∈ A) :
    2*n ≤ c.size + 2*A.length.log2 + 1 := by
  obtain ⟨J,hJ,d,hs,heq⟩ := equality_program A hn hc c hdec
  have := schnorr n J d heq
  have := arity_lower J
  omega

end TeachingProjection

#print axioms TeachingProjection.teaching_log
#print axioms TeachingProjection.signed_projection
#print axioms TeachingProjection.size_subst
#print axioms TeachingProjection.eval_subst
#print axioms TeachingProjection.equality_program
#print axioms TeachingProjection.complement_family_lower

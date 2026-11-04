# The factor-n gap, written as far as the counting goes

*Hand derivation. No computation. This does not remove the factor n. It records the sharp form of the bound the dominator count actually gives, and two attempts that cannot improve the coefficient of the second logarithm.*

## 1. Domination form

In a tournament, a set D is dominating when every vertex outside D is beaten by some vertex of D. The domination number is γ(T). Property S_k is exactly γ(T) > k, so f(k) is the least order of a tournament with γ > k, and

  γ_max(N) = max { γ(T) : |V(T)| = N }

is the inverse: f(k) > N if and only if γ_max(N) ≤ k.

Theorem C of `ERDOS902_PROOF.md` says f(k) ≥ (c\* − o(1)) k 2^k with c\* ≈ 0.7695 the limit defined there by Φ(a_j, a_{j−1}) = ln 2. Inverting the inequality gives the following.

**Theorem.** For every tournament T on n vertices,

  γ(T) ≤ log₂ n − log₂ log₂ n − log₂(c\*) + o(1).

Since log₂(c\*) ≈ −0.377, the additive constant is about +0.38. Szekeres–Szekeres, whose leading term is (1/2) k 2^k, gives the same expression with additive constant +1. The gain from c\* over that leading term is a constant, about 0.62, not a second logarithm.

*Proof.* Let ε > 0 and let k be large. If a tournament has γ > k, it has S_k, so its order is at least (c\* − ε) k 2^k. Contrapositively, every tournament on fewer than (c\* − ε) k 2^k vertices has γ ≤ k. Given n, choose k so that (c\* − ε) k 2^k ≥ n and k is minimal with that property. Then log₂ n ≤ log₂(c\* − ε) + log₂ k + k, hence

  k ≥ log₂ n − log₂ log₂ n − log₂(c\* − ε) + o(1),

and the minimal such k is at most one more than this. Let ε → 0. ∎

The matching construction is still the random tournament: on N vertices a random tournament has γ at least log₂ N − 2 log₂ log₂ N − O(1), so

  f(k) ≤ (ln 2 + o(1)) k² 2^k.

The unsolved gap is precisely the coefficient 1 or 2 of log₂ log₂ N.

## 2. Two-stage averaging does not change the coefficient

Let B(m) be any function satisfying B(m) ≤ log₂ m − log₂ log₂ m + C for an absolute C and all large m. This covers the Szekeres bound and the bound in §1.

**Lemma.** Fix a tournament on n vertices in which every out-degree is at most (1/2 + δ)n. Let s ≥ 1 with s = o(n^{1/2}). Then there is a set S of s vertices such that the set W of vertices beating every member of S satisfies |W| ≤ n · 2^{−s} · e^{O_δ(s²/n)}, and

  γ(T) ≤ s + B(|W| + s).

Substituting the shape of B, the s terms cancel:

  γ(T) ≤ log₂ n − log₂(log₂ n − s) + C + o(1).

Choosing s = α log₂ log₂ n, for any fixed α, leaves the coefficient of log₂ log₂ n equal to 1. Choosing s = log₂ n − β log₂ log₂ n replaces the bound by log₂ n − log₂ log₂ log₂ n + O(1), which is weaker than §1.

*Proof.* Let d⁺(v) ≤ (1/2 + δ)n. For a uniform s-set S and a vertex v ∉ S,

  P(S ⊆ N⁺(v)) = C(d⁺(v), s) / C(n − 1, s) ≤ prod_{i=0}^{s−1} ((1/2 + δ)n − i) / (n − 1 − i).

Each factor is at most (1/2 + δ)(1 + O(s/n)), so the product is at most 2^{−s} e^{O_δ(s²/n)}. Averaging over S, some S has at most n · 2^{−s} e^{O_δ(s²/n)} vertices that beat every member of S. Every other vertex outside S is beaten by S. A dominating set of the tournament induced by W ∪ S, together with nothing else, dominates T: vertices outside W ∪ S are already beaten by S. Thus γ(T) ≤ γ(T[W ∪ S]) ≤ B(|W| + s).

Now |W| + s ≤ n 2^{−s} e^{o(1)} for s = o(n^{1/2}). Hence

  log₂(|W| + s) ≤ log₂ n − s + o(1),

and

  s + log₂(|W| + s) − log₂ log₂(|W| + s) + C ≤ log₂ n − log₂(log₂ n − s) + C + o(1). ∎

The same cancellation occurs if the first stage is iterated. A proof of the coefficient 2 has to count all k-sets in one step, as the random tournament does, rather than by deleting a short set and applying a one-logarithm bound to the remainder.

## 3. A quadratic witness does not pass the first-moment threshold

Let κ(S) be the number of vertices that beat every member of a k-set S. The tournament has γ ≤ k as soon as κ(S) = 0 for some S. For every integer m ≥ 0,

  1_{m = 0} ≥ 1 − m,

so the number of dominating k-sets is at least C(n, k) − Σ_S κ(S) = C(n, k) − Σ_v C(d⁺(v), k). This is positive when the average out-degree is at most (n − 1)/2 and n < 2^k, and only then. It is the bound γ ≤ log₂ n.

A quadratic correction does not extend the range. Suppose f(0) = 1, f(m) ≤ 0 for every integer m ≥ 1, and f(m) = 1 − a m + b m(m − 1). Then a ≥ 1, because f(1) = 1 − a. If b > 0 then f(m) → +∞, so f(m) > 0 for large m. Thus b ≤ 0, and

  E[f(κ)] = 1 − a μ + b β ≤ 1 − μ

whenever μ = E[κ] ≥ 1 and β = E[κ(κ − 1)] ≥ 0. The resulting lower bound on the number of zeros is no larger than the linear one, and is negative throughout the range n ≫ 2^k where the factor n² would have to appear.

## 4. Where a proof of the coefficient 2 has to work

In a doubly regular tournament the same two moments can be computed exactly. Every out-degree is 2t + 1 and every pair has t common out-neighbours, with n = 4t + 3. For a uniform s-set,

  E[κ] = n C(2t + 1, s) / C(n, s),  E[κ(κ − 1)] = n(n − 1) C(t, s) / C(n, s).

The ratio of these two quantities is prod_{i < s} (t − i)(4t + 3 − i) / (2t + 1 − i)² < 1, so the dominator-indicators are pairwise negatively correlated, and the variance is the Poisson variance μ + o(μ) when s = o(t^{1/2}). A distribution with these two moments can still live on the positive integers: for mean 2 and second factorial moment 4, the law (2/3)δ_1 + (1/3)δ_4 does. So the moments of a doubly regular tournament do not by themselves force a k-set with no dominator once the mean exceeds 1.

The random-tournament calculation succeeds because it uses the whole tail, not two moments: there are C(n, k) candidate sets and each survives with probability about exp(−n 2^{−k}). That product exceeds 1 down to n = (ln 2 + o(1)) k² 2^k and fails below it. Carrying the same estimate over to every tournament, with an error small enough to keep the constant ln 2, is the missing step. Section 2 says the step will not come from splitting off o(log n) vertices and quoting §1 on what remains.

# What is computed here, and what is quoted

Condensed mathematics is foundational. Almost every statement in the lectures
is about a whole category, and no finite program checks a statement about a
category. This file lists every claim the three articles make and marks it:

* **computed** means this repository works it out, and `make test` re-checks
  it on your machine;
* **finite shadow** means the repository computes a finite instance of a
  statement whose content is genuinely infinite, and the article says so
  where it appears;
* **quoted** means the article states a result of the lectures and does not
  attempt to verify it.

The source throughout is Peter Scholze, *Lectures on Condensed Mathematics*,
[arXiv:2605.03658v1](https://arxiv.org/abs/2605.03658), May 2026, joint work
with Dustin Clausen. Page numbers are the printed pages of that PDF and are
recorded once in `src/condensed_guide/examples.py`.

---

## Part one, shapes you can only see by probing them

| claim in the article | status | where |
|---|---|---|
| the discrete reals and the usual reals have empty kernel and cokernel as point sets, and are still not isomorphic | quoted | Example 1.9, page 9 |
| topological abelian groups do not form an abelian category | quoted | the problem list, page 6 |
| the halving probe's stages double: 1, 2, 4, 8, 16, ... | computed | `core.cantor`, `tests/test_core.py` |
| the approaching probe separates one more point per stage | computed | `core.convergent_sequence` |
| the base-p probe's stages multiply by p | computed | `core.p_adic` |
| every stored probe is an inverse system with surjective transition maps | computed | `Profinite.check` |
| a space with a distance is determined by which sequences converge | quoted | Remark 1.6, page 9 |
| the two sheaf conditions define a condensed set | quoted | Definition 1.2, page 6 |
| the set-theoretic size bound does not change the theory | quoted | Remark 1.4, page 7, and the appendix to Lecture II |
| condensed abelian groups form an abelian category with the strong axioms | quoted | Theorem 1.10, page 9; Theorem 2.2, page 11 |
| a continuous map from the halving probe need not be locally constant | computed | the ghost figure builds one explicitly |
| unfoldable probes: every surjection onto one splits | quoted | Definition 2.4, page 11 |
| the smallest compactification of a discrete set is unfoldable | quoted | Example 2.5, page 11 |
| a convergent sequence in an unfoldable probe is eventually constant | quoted | Warning 2.6, page 12, citing Gleason 1958 |
| a product of two infinite unfoldable probes is never unfoldable | quoted | Warning 2.6, page 12 |
| an answer sheet is determined by its values on unfoldable probes | quoted | Proposition 2.8, page 12 |
| compact shapes correspond exactly to the compact answer sheets | quoted | Theorem 2.16, page 17 |
| the translation is faithful on compactly generated spaces | quoted | Proposition 1.7, page 9 |
| a space with a non-closed point is never an answer sheet | quoted | Warning 2.14, page 16 |
| the hole counts of a stack of n circles are the binomial coefficients | computed | `core.exterior_ranks`, checked against Pascal's rule |
| counting holes inside answer sheets agrees with the classical count | quoted | Theorem 3.2, page 21 |
| real-valued hole counting vanishes above degree zero | quoted | Theorem 3.3, page 22 |
| a loop's winding number is a whole number unchanged by deformation | computed | `core.winding_number` |

## Part two, infinite sums that finally land

| claim in the article | status | where |
|---|---|---|
| the doubling sum's totals run away in ordinary size | computed | `core.geometric_partial_sums`, exact fractions |
| the same totals converge in base-two size, to minus one | computed | `core.p_adic_abs` and `core.geometric_limit` |
| the ordinary distance doubles and the base-two distance halves, every step | computed | `tests/test_core.py` |
| a weighting is a compatible family of integer weights | computed | `core.Measure`, with `check` enforcing the rule |
| integrating against a weighting does not depend on the level read | computed | `Measure.integrate` at two levels, checked equal |
| a single point of the dust carries a legal weighting | computed | `core.dirac` |
| the free solid group on a probe is the limit of the finite stages | quoted | Definition 5.1, page 33 |
| Bergman's construction produces one basis element per box | finite shadow | `core.nobeling_basis`; freeness is automatic at a finite stage |
| continuous integer functions on any probe form a free group | quoted | Theorem 5.4, page 34, Nöbeling after Specker |
| a homomorphism out of an endless product reads only finitely many slots | quoted | Specker 1950, used throughout Lecture V |
| the weightings on a probe form an endless product of copies of Z | quoted | Corollary 5.5, page 34 |
| the solid rule: a unique extension to weightings | quoted | Definition 5.1, page 33 |
| solid groups are closed under everything, with products of Z as blocks | quoted | Theorem 5.8, page 35; Corollary 6.1, page 42 |
| the ruler is divisible and the whole numbers are not | computed | the divisibility figure, exact arithmetic |
| a divisible group maps to zero in every copy of Z | computed | stated and checked as arithmetic in the tests |
| the solidified ruler is zero | quoted | Corollary 6.1 (iii), page 42 |
| the completed tensor product is symmetric monoidal | quoted | Theorem 6.2, page 43 |
| index sets multiply under completed tensor | quoted | Proposition 6.3, page 43 |
| the five entries of the multiplication table | quoted | Example 6.4, page 44 |
| the other cells of the guide's table | derived | the same rule with variables renamed; `core.quoted_tensor` marks which is which |
| a two-variable series' monomials pair off with two one-variable series' | computed | `core.tensor_index`, `core.double_series_monomials` |
| the holes of the circle, figure eight, sphere, torus and Klein bottle | computed | `core.Complex.homology` by Smith normal form over Z |
| the Klein bottle carries a hole of order two | computed | same, and pinned by name in the tests |
| solidifying a shape returns its holes | quoted | Example 6.5, page 44 |

## Part three, rings that know how to integrate

| claim in the article | status | where |
|---|---|---|
| a theory of measures is a functor with unit weights | quoted | Definition 7.1, page 45 |
| an analytic ring is such a pair passing a further test | quoted | Definition 7.4, page 46 |
| the base-p rule and the solid rule over a plain ring both pass | quoted | Proposition 7.8, page 48 |
| a rule can be attached to any ring with a chosen small subring | quoted | Remark 7.9, page 49 |
| merging boxes must not increase a measure's size | computed | `core.merge_ratio` |
| merging n equal boxes changes the size by n to the power one minus one over the exponent | computed | `core.worst_merge_ratio`, checked against the direct computation |
| that ratio is at most one exactly when the exponent is at most one | computed | `tests/test_core.py` sweeps the exponent |
| the unit ball is convex at and above exponent one and not below | computed | `core.is_convex` |
| the exponent-one rule fails, because of Ribe's extension | quoted | Example 7.10, page 49, citing Ribe 1979 |
| sweeping the exponents gives a rule that works | quoted | Theorem 7.11, page 50 |
| functions near the edge are series in the inverse coordinate | quoted | Lecture VIII, page 53 onward |
| the quotient on the line keeps exactly the tails | computed | `core.line_edge_quotient_rank`, stable in the truncation |
| the quotient on the cross keeps both tails plus one | computed | `core.cross_edge_quotient_rank` |
| the extra piece is the shared value at the crossing point | computed | the count is derived from that constraint and checked |
| the compactly supported pushforward exists and has a counterweight | quoted | Theorem 8.1 and Theorem 8.2, page 53 |
| its counterweight applied to the simplest input is the dualizing complex | quoted | Theorem 8.2, page 53 |
| the lectures compute the cross's dualizing complex from its tails | quoted | Remark 8.5, page 54 |
| the compactly supported operation does not preserve discrete objects | quoted | the discussion under Theorem 8.2, page 53 |
| finiteness of coherent cohomology is recovered | quoted | Remark 8.3, page 54 |
| subrings declared small correspond exactly to regions of valuations | quoted | Proposition 9.2, page 63 |
| the theory of modules glues over patches | quoted | Theorem 9.8, page 65 |
| gluing needs the higher-categorical version of the derived category | quoted | the discussion before Theorem 9.8, page 65 |
| the six operations, and that the third pair is the hard one | quoted | the discussion after Theorem 11.1, page 72 |
| proper and open behaviour force the definition | quoted | same passage, via Nagata compactification |
| duality with a trace map, for a smooth separated map | quoted | Theorem 11.1, page 71 |
| the two sides of the pairing have matching dimensions on a curve | computed | the pairing figure, classical dimensions |

---

## Things the guide deliberately does not claim

**No claim is made that the finite computations here establish the lectures'
theorems.** Every one of the theorems is a statement about a category or about
genuinely infinite objects. What the computations establish is that the
concrete machinery the theorems are about behaves as the article describes it.

**Bergman's basis construction is only run at finite stages**, where the group
is free for trivial reasons. The article says this in its own words at the
point the figure appears. Nöbeling's theorem is the infinite statement and is
quoted.

**Specker's theorem is quoted, not computed.** At a finite stage a product and
a sum are the same object, so the finite computation would be vacuous, and the
guide does not present one.

**The Klein bottle is drawn as a doughnut** in the part two simulation, since
it does not embed in three-dimensional space. The gluing rule, not the
picture, is what makes it a Klein bottle, and the page says so on screen.

**The valuation-space picture in part three, section 6 is schematic.** Its two
directions stand for independent ways a valuation can vary and not for
coordinates on any particular ring. The figure carries that caption.

**The lectures themselves flag a gap in the literature** that this guide
repeats rather than resolves: the universal resolution of Lecture IV has no
published proof, which is why the lectures supply one in an appendix
(Remark 4.6, page 25).

**These notes record a 2019 course.** The preface says the material has been
carried much further since, in later work by Clausen and Scholze, and this
guide does not cover any of it.

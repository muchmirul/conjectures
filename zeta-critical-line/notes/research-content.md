# Research notes: the mathematical content, and where each claim comes from

The source is the paper "More than two thirds of the zeros of the Riemann zeta
function lie on the critical line" (Claude, Anthropic, dated 10 August 2026),
kept in `docs/zeta-critical-line/paper/more-than-two-thirds.pdf` and published
at
[www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf).

Every factual claim in the guide is listed here with its source and, where it
applies, the test that re-checks it. Claims fall into three buckets:

- **[computed]** this repo derives it from scratch and checks it in `tests/`
- **[classical]** a theorem from the literature, quoted, not verified here
- **[recent]** the 2026 result the article is about

---

## History and attribution

| year | claim | bucket | source |
|---|---|---|---|
| 1859 | Riemann's eight-page memoir; the hypothesis stated as "sehr wahrscheinlich", not pursued because it was not needed for his immediate purpose | [classical] | Riemann 1859, cited in the paper as [Rie59]; the paper's section 1.1 |
| 1914 | infinitely many zeros lie on the line | [classical] | Hardy 1914, cited as [Har14] |
| 1921 | the count on the line up to height T grows at least linearly in T | [classical] | Hardy and Littlewood 1921, cited as [HL21] |
| 1942 | a positive (small, inexplicit) proportion lies on the line | [classical] | Selberg 1942, cited as [Sel42] |
| 1974 | Levinson: at least one third, by mollifying zeta near the line | [classical] | Levinson 1974, cited as [Lev74] |
| 1979 | Levinson's zeros are in fact simple (Heath-Brown, and independently Selberg) | [classical] | Heath-Brown 1979, cited as [HB79] |
| 1989 | Conrey: more than two fifths | [classical] | Conrey 1989, cited as [Con89] |
| 2011-2020 | refinements: Bui-Conrey-Young 41%, Feng, then Pratt-Robles-Zaharescu-Zeindler reach 5/12 = 0.4166..., the record since 2020, all by Levinson's method | [classical] | [BCY11], [Fen12], [PRZZ20], as cited in the paper's section 1.2 |
| 1995, 2015 | distinct zeros: Farmer 0.6395 unconditionally, Wu 0.6603 | [classical] | Farmer 1995 [Far95], Wu 2015 [Wu15] |
| 1973 | Montgomery's pair correlation: under RH, at least 2/3 of zeros are simple | [classical] | Montgomery 1973, cited as [Mon73] |
| 1975 | Montgomery-Taylor: under RH the simple proportion rises to 0.6725... | [classical] | Montgomery 1975 [Mon75], Cheer-Goldston [CG93] |
| 2024-2026 | the prime side of Montgomery's argument is unconditional (Baluyot, Goldston, Suriajaya, Turnage-Butterbaugh), and Goldston-Suriajaya ask what would follow if RH could be removed from the zero side | [classical] | [BGSTB24], [GS25], [GS26], the paper's sections 1.2 and 7.4 |
| 2026 | unconditionally, at least 2/3 of the zeros are simple and on the critical line, and at least 5/6 are distinct | [recent] | the paper, Theorems A, B, C |
| 2004 | the first 10^13 zeros are on the line, numerically | [classical] | Gourdon 2004; not cited by the paper, quoted by this guide for context only |

The numerical-verification claim, that 10^13 zeros have been checked, is the
only claim in the guide that does not come from the paper or from a source the
paper cites. The guide marks it as outside the paper.

## The named constants

| claim | value | bucket | test |
|---|---|---|---|
| the previous record proportion | 5/12 = 0.416666... | [classical] | `test_the_record_race_numbers` |
| the new proportion, flat window | 2/3, from the shape function at dial value one | [recent], arithmetic [computed] | `test_the_shape_function_gives_the_papers_constants` |
| simple-zero proportion, flat window | also 2/3 (Theorem B) | [recent] | same |
| distinct-zero proportion | 5/6 = (1 + 2/3) / 2 (Theorem C) | [recent], arithmetic [computed] | same |
| the shape function | two, minus one over the dial, minus a third of the dial; equation (1.3), page 3 of the paper | [computed] | same |
| the distinct-shape and Cauchy-Schwarz shapes agree/cross at dial = 3 minus root 6 = 0.5505... | [computed] | equation (1.3) | `test_the_crossover_dial_value` |
| the Cauchy-Schwarz shape at dial one | 3/4 | [computed] | `test_the_shape_function_gives_the_papers_constants` |
| the optimised window constant | 0.7532960..., from the Montgomery-Taylor window; equation (7.4), page 21 | [computed] numerically from the paper's formula | `test_the_optimised_window_constant` |
| the optimised proportions | 0.67250... on-line and simple, 0.83625... distinct (Theorem D) | [computed] arithmetic from the constant | same |
| the method's ceiling for this kind of certificate | 0.68185 (Remark 1.1, page 4) | [recent] quoted; the paper's "within 0.016" is the gap from the flat-window 2/3, and the optimised 0.6725 sits within a hundredth | `test_the_ceiling_and_the_gap` |
| bandwidths needed for 0.70, 0.80, 0.90 | roughly 1.04, 1.26, 1.70 (Remark 1.1) | [recent] quoted | `test_the_numbers_in_the_prose_match_the_code` (prose pin) |
| prime-side energy at dial one | 4/3 (the Montgomery second moment; Remark 5.10, page 19) | [computed] via the Fejer integral | `test_the_fejer_integral_gives_four_thirds` |
| the assembly | 4 - 2 - 4/3 = 2/3 at dial one | [computed] | `test_the_budget_assembly` |
| the flat window's mean-absolute-gap value | 1/3 (makes the Cauchy-Schwarz shape 3/4 at dial one) | [computed] | `test_the_window_functional_at_the_flat_window` |

## The zeta computations this repo performs

| claim | bucket | test |
|---|---|---|
| the first 300 zero heights (14.1347..., 21.0220..., 25.0108..., ...) | [computed] by mpmath, shipped in `src/zeta_guide/data/zeros300.txt`, spot-rechecked live | `test_the_zero_table_matches_mpmath_and_the_classical_values` |
| every one of those zeros sits on the line to high precision | [computed]: zeta at each shipped height has modulus below 10^-9 | `test_zeta_vanishes_at_the_shipped_heights` |
| the guide's own Euler-Maclaurin zeta agrees with mpmath | [computed] | `test_the_guides_zeta_agrees_with_mpmath` |
| the zero-counting formula (equation (1.2), page 3) predicts the true counts | [computed]: main term vs the shipped zeros in [T, 2T] for several T | `test_the_counting_formula_matches_the_zero_table` |
| adding zero-waves rebuilds the prime staircase (the explicit formula in its psi form) | [computed]: the error falls as waves are added | `test_adding_zero_waves_improves_the_prime_staircase` |
| the prime-built density spikes at the true zero heights | [computed]: local maxima of the prime sum align with shipped zeros | `test_the_prime_density_peaks_at_the_zero_heights` |

## The paper's toy-scale moving parts this repo re-checks

Checking these does not verify the theorem; it verifies that the article
describes the parts correctly, at sizes a laptop can hold. The paper's own
numerical illustrations (section 8, pages 25-27) do the same at larger sizes
and state, as we repeat, that no theorem in the paper depends on them.

| ingredient | bucket | test |
|---|---|---|
| the matrix built from zeros equals the matrix built from primes (the paper's section 8 item (1), which reports agreement 10^-6 to 10^-8; our toy height reaches the same order) | [computed] at toy height, stretch 100 to 200 | `test_prime_side_equals_zero_side_at_toy_height` |
| the sampling identity (Lemma 2.2, page 8): summed over the whole microphone grid, the squared responses to a zero total the same constant wherever the zero sits | [computed] numerically at toy scale, in Python and in the page's JavaScript | `test_the_array_shares_every_zero_fairly`, `test_the_pages_array_total_is_constant` |
| the trace of the matrix is close to the zero count N, whatever the window | [computed] | same test, plus `test_the_trace_tracks_the_zero_count` |
| the rank-trace inequality (Lemma 3.2, equation (3.1), page 9) on random instances | [computed]: random P, Q plus the stated equality case | `test_the_rank_trace_inequality_on_random_instances` |
| the thresholded Cauchy-Schwarz count (Lemma 3.3, page 10) on random instances | [computed] | `test_the_cauchy_schwarz_count_on_random_instances` |
| Weyl's eigenvalue-stability lemma (Lemma 3.4, page 10) on random instances | [computed] | `test_weyls_lemma_on_random_instances` |
| the inertia certificate never exceeds the truth on synthetic configurations (the paper's section 8 item (5)): all-paired, half-paired, doubled zeros | [computed] at toy height | `test_the_certificate_never_exceeds_the_truth_on_synthetic_configurations` |
| an off-line pair contributes a saddle: its two-by-two block has one positive and one negative direction | [computed] | `test_an_off_line_pair_makes_a_saddle` |
| an on-line zero contributes a bowl: its contribution is a nonnegative rank-one form | [computed] | `test_an_on_line_zero_makes_a_bowl` |
| the whole-number trick: m squared is at least 3m - 2, with equality only at 1 and 2 | [computed] | `test_the_whole_number_trick` |
| the optimised window beats the flat window in the paper's functional (equation (7.3), page 20) and small perturbations do not beat the optimiser | [computed] numerically | `test_the_optimised_window_constant` |

## What the 2026 paper proves, quoted not verified

- **Theorem A** (page 3): for the window between heights T and 2T, the number
  of distinct zeros on the critical line is at least the shape function times
  the total count, up to an explicit error; in particular at least 2/3 of all
  zeros, in the limit, are on the line, counted as distinct points.
- **Theorem B** (page 4): the same bound holds for zeros that are simple and
  on the line.
- **Theorem C** (page 4): at least 5/6 of the zeros are distinct.
- **Theorem D** (page 21): with the optimised (Montgomery-Taylor) window the
  three constants become 0.67250..., 0.67250..., 0.83625....
- **Theorem E** (page 22): all of the above holds for the L-function of any
  fixed primitive Dirichlet character, with the same constants.
- Remark 7.3 (page 23): applied to the derivative of the completed zeta
  function, the same machine gives 0.85838 simple-and-on-the-line and 0.92919
  distinct, unconditionally (0.86864 and 0.93432 with a quartic window).
- Section 7.5 (f), (g) (pages 24-25): conditional side-results, quoted in the
  article's section 12: under RH the distinct proportion rises to 0.85082,
  and hypothetical higher-moment laws would push the certified proportion
  toward one. None of the stronger inputs is proven; the paper records these
  as measurements of the remaining distance.
- The inputs are: Weil's explicit formula, the functional equation, mean
  values of Dirichlet polynomials of length up to T (Montgomery's first and
  second moments in the unconditional form of [BGSTB24]), and linear algebra.
  No mollifier, no zero-density estimate, no zero-free region (section 1.3).
- Appendix B: a Lean 4 formalisation of Theorems A-E accompanies the paper
  (repository `github.com/anthropics/zeta-23-lean`), stated against Mathlib's
  definition of zeta; the audit records no hypotheses and no `sorry`, only
  the three standard axioms. The main-term constants were separately verified
  symbolically (SymPy, 31 checks).
- Appendix C: the account of how the argument was found (twenty-three
  parallel research agents, adversarial review, the "E2" agent noticing the
  dual of a vacuous bound, ten independent review passes, handover to human
  analytic number theorists).

## Correctness traps the article must avoid

- **The result says nothing about RH itself, in either direction.** The
  paper's section 1.5 is explicit: lower bounds only; the remaining third is
  not shown to be off the line, it is simply not certified. The article must
  carry this early and plainly.
- **"Two thirds" is a limit statement.** Effectivity Remark 5.9 (page 19):
  the certificate at any computationally accessible height is below the
  Cauchy-Schwarz value, and the constants converge like 1 over the window
  length. Our toy tables show certificates around 0.4 to 0.6 of N, not 2/3,
  and the article says so.
- **The proportions are of zeros in [T, 2T] counted with multiplicity**, and
  "on the line" means counted as distinct points (Theorem A) or simple points
  (Theorem B). The four counters must never be blurred.
- **The method has a ceiling below 1.** Remark 1.1: no certificate of this
  kind (bandwidth one, two moments) can pass 0.68185. Do not let the reader
  think the same machine will creep to 100%.
- **Montgomery 1973 already had 2/3 under RH.** The new content is removing
  RH from the zero side by inertia and rank, not the number 2/3 itself. Credit
  must flow to Montgomery and to [BGSTB24]/[GS25]/[GS26] exactly as the paper
  insists (sections 1.2, 7.4, Acknowledgments).
- **The numerics prove nothing.** Section 8's own preamble: "no theorem,
  proposition or lemma depends on any computation reported here". Same for
  ours: the tests check the article's numbers and toy models, not the theorem.
- **The paper's authorship claim must be reported exactly**: the mathematics
  is the model's, obtained in one interactive session with subsequent review
  by further model instances; Jarred Sumner posed the problem; Ralph Furman
  and Levent Alpöge studied, contextualised, and took responsibility for
  communicating it; the Lean formalisation was orchestrated by Eric Easley.
  Brian Conrey and Daniel Goldston read the manuscript. The result had been
  studied by human mathematicians before release.
- **Off-line zeros are hypothetical.** Every off-line pair drawn in the guide
  is a synthetic illustration; none has ever been found. Figures must label
  synthetic configurations as synthetic.
- **The Gram matrix is real symmetric** because the zero multiset is
  symmetric under both reflections (section 2.1); the article's "one row per
  microphone" story must not accidentally claim entries are probabilities or
  correlations.

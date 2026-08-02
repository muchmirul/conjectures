# Research notes: the mathematical content, and where each claim comes from

The source is chapter 9 of *Ten Advances in Mathematics and Theoretical
Computer Science* (OpenAI), "Super-exponential lower bounds for R(3, ..., 3)",
together with its reasoning walkthrough (chapter 10 of the walkthroughs
document), both kept in `docs/ten-proofs/09-multicolor-ramsey/`.

Every factual claim in the guide is listed here with its source and, where it
applies, the test that re-checks it. Claims fall into three buckets:

- **[computed]** this repo derives it from scratch and checks it in `tests/`
- **[classical]** a theorem from the literature, quoted, not verified here
- **[recent]** the 2026 result the article is about

---

## History and attribution

| year | claim | bucket | source |
|---|---|---|---|
| 1955 | two colors force at six people, three colors at seventeen | [classical] statement; the six case and both safe colorings are [computed] | Greenwood and Gleason 1955, cited in the source chapter as [GG55] |
| 1955 | the sixteen-vertex three-coloring from the sixteen-element field | [computed] the coloring is rebuilt and verified here | Greenwood and Gleason 1955 |
| 1971 | the connection to Shannon capacity | [classical] | Erdős, McEliece and Taylor 1971, cited as [EMT71] |
| 1973 | four colors force at fifty one or more | [classical] | Chung 1973, cited as [Chu73] |
| 2004 | four colors force at sixty two or fewer | [classical] | Fettes, Kramer and Radziszowski 2004, as reported in Radziszowski's dynamic survey of small Ramsey numbers, cited as [Rad] |
| 1983 | Erdős's prizes: 250 dollars for the growth rate, 100 dollars for whether it is finite | [classical] | Chung and Grinstead 1983 and the Erdős problem lists, cited as [CG83], [Blo183], [CG] |
| 1990 | the superexponential-growth question recorded in the standard reference | [classical] | Graham, Rothschild and Spencer 1990, page 146, cited as [GRS90] |
| 1995 | the capacity connection made explicit, and the analogous question for larger forbidden groups | [classical] | Alon and Orlitsky 1995, cited as [AO95] |
| 2020 | the saturated matrix and the coordinate cover, from hat-guessing games | [classical] ingredients; the two-color instances are [computed] | Alon, Ben-Eliezer, Shangguan and Tamo 2020, cited as [ABST20]; the family goes back to Chakraborty, Radhakrishnan, Raghunathan and Sasatte 2006, cited as [CRRS06] |
| 2021 | the best fixed base before this work, 380 to the one fifth | [classical] | Ageron, Casteras, Pellerin, Portella, Rimmel and Tomasik 2021 with the Erdős problem list, cited as [ACPPRT21], [Blo183] |
| 2026 | the growth question answered: the base grows without bound | [recent] | the source chapter, Theorem 1.1 |

The source chapter states the record upper bound as e minus one sixth, times k
factorial, plus one, for four or more colors, credited to a chain of
refinements it cites as [Whi73], [Wan97], [XXC02], [Blo183], [Rad]. The guide
quotes the record without re-deriving it and re-derives only the simple
staircase.

## The numbers

| claim | value | bucket | test |
|---|---|---|---|
| one color forces at three people | 3 | [computed] (it is the base of the staircase) | `test_the_upper_staircase_reproduces_the_settled_values` |
| two colors: five people can stay safe | the pentagon coloring | [computed] | `test_the_pentagon_coloring_is_safe_and_uses_two_colors` |
| two colors: six people cannot | all 32768 colorings checked | [computed] | `test_six_people_with_two_colors_always_force_a_triangle` |
| six people always contain at least two one-color triangles | 2 | [computed]; classically Goodman 1959 | `test_six_people_always_produce_at_least_two_one_color_triangles` |
| three colors: sixteen people can stay safe | the field coloring | [computed] | `test_the_sixteen_vertex_three_coloring_is_safe` |
| three colors: seventeen cannot | 17 | [classical] Greenwood-Gleason; far beyond exhaustive checking here | quoted only |
| four colors | between 51 and 62 | [classical] | quoted only, `test_the_known_forcing_sizes_match_the_safe_tables_built_here` pins the quoted range |
| the simple staircase | 3, 6, 17, 66, 327, ... | [computed] | `test_the_upper_staircase_reproduces_the_settled_values` |
| pentagon times pentagon | 25 vertices, 4 colors, safe | [computed] | `test_pentagon_times_pentagon_is_a_safe_four_coloring_of_twenty_five` |
| the sixteen coloring times the pentagon | 80 vertices, 5 colors, safe | [computed] | `test_sixteen_times_pentagon_is_a_safe_five_coloring_of_eighty` |
| a fixed product's rate never moves | root five, or cube root of sixteen | [computed] | `test_a_fixed_product_keeps_the_same_rate_forever` |
| the best fixed base before 2026 | 380 to the one fifth, about 3.28 | [classical] | `test_the_old_base_and_the_bases_of_the_small_records` pins the digits |
| that base is asymptotic only: no literal five-color block reaches it | the staircase caps five colors at 327, under 380 | [computed] | `test_no_literal_five_color_block_could_reach_the_quoted_rate` |
| the honest per-count floor from multiplying record tables | blocks of 2, 5, 16 and 50 people | [computed], the 50 quoted from Chung 1973 | `test_the_block_product_floor_stays_under_the_ceiling` |
| the record upper bound factor | e minus one sixth | [classical] | `test_the_record_upper_bound_is_the_quoted_multiple_of_factorial` |

## The construction's parts this repo re-checks

These are the small moving parts of the 2026 argument that can be built and
verified directly at toy size. Checking them does not verify the theorem; it
verifies that the article describes the parts correctly.

| ingredient | bucket | test |
|---|---|---|
| the matrix sizes the paper's formula gives at alphabet two and three | (3, 13) and (7, 57) | `test_the_two_color_matrix_parameters_are_the_papers_formula` |
| the smallest real stage uses 342 colors | [computed] from the paper's formula | same test |
| a saturated matrix exists at alphabet two, and is verified over all seventy column sets | [computed] | `test_the_found_matrix_is_saturated_for_every_column_set` |
| the property is not automatic: a lazy matrix fails it | [computed] | `test_the_saturated_property_is_not_automatic` |
| no word has more exceptional columns than the proof allows, over all 8192 words | [computed] | `test_no_word_has_more_exceptional_columns_than_the_proof_allows` |
| the two fixed answer maps meet every pair of words | [computed], exhaustively at alphabet two | `test_the_two_fixed_maps_meet_every_pair_of_words` |
| the three-block parity rule: no membership pattern allows a three-block triangle | [computed], all eight cases | `test_no_membership_pattern_lets_a_color_reach_all_three_blocks` |
| the two-block trap: breaking the label rule makes a triangle, obeying it does not | [computed] | `test_breaking_the_label_rule_makes_a_triangle_and_obeying_it_does_not` |
| the permutation shortcut fails: three orderings, one color, one triangle | [computed] | `test_the_first_difference_shortcut_makes_a_one_color_triangle` |

At alphabet size two almost every random matrix happens to pass the saturated
test, because the failure probability the union bounds control is already
astronomically small there. The two union bounds earn their keep at the real
sizes, where nothing could ever be checked case by case. The article says
this plainly rather than pretending the toy search is dramatic.

## What the 2026 chapter proves, quoted not verified

- The forcing size at k colors is at least (c times the cube root of k, over
  the logarithm of k) to the k-th power, for an absolute constant c and every
  k from 2 up (Theorem 1.1).
- With the factorial upper bound, the forcing size is k to the power
  (a constant times k): the answer to Erdős's growth question is that the
  per-color base grows without bound.
- The explicit all-k constant is one over (six times e to the 38th); with it
  the bound is trivial below 342 colors and only overtakes the old fixed-base
  record at around ten to the sixtieth colors
  (`test_the_explicit_bound_is_trivial_at_every_drawable_size` checks the
  crossover estimate; the paper says the constants were not optimized).
- Equivalent formulation: there are graphs in which no three vertices are
  pairwise unlinked, whose Shannon capacity is as large as you like.

## Correctness traps the article must avoid

- The theorem is about the *growth rate*. At every drawable size the older
  constructions give larger safe tables. Say so.
- The product construction proves the limit exists (by Fekete); it does not
  compute it. The 2026 result says the limit is infinite; before it, even
  finiteness was open.
- The toy matrix search succeeding on the first seed is not evidence the
  property is easy at real sizes; the union-bound arithmetic is what carries
  it there.
- The trap demo is a miniature: the real construction never hand-picks cross
  edges; the fixed maps decide them. The miniature shows only why the label
  rule matters.
- "Triangle" in this guide always means a one-color triangle among three
  people; the article must not drift into using it for the drawn shape only.

# Research notes: the mathematical content, and where each claim comes from

The source is chapter 1 of *Ten Advances in Mathematics and Theoretical
Computer Science* (OpenAI), "Exponential Growth Rate of the Cohn-Elkies Sphere
Packing Linear Program", together with its reasoning walkthrough, both kept in
`docs/ten-proofs/01-sphere-packing-linear-program/`.

Every factual claim in the guide is listed here with its source and, where it
applies, the test that re-checks it. Claims fall into three buckets:

- **[computed]** this repo derives it from scratch and checks it in `tests/`
- **[classical]** a theorem from the literature, quoted, not verified here
- **[recent]** the 2026 result the article is about

---

## History and attribution

| year | claim | bucket | source |
|---|---|---|---|
| 1611 | Kepler guesses the greengrocer's stack is optimal in space | [classical] | Kepler, *Strena seu de nive sexangula* |
| 1910 | Thue's proof that the hexagonal packing is best in the plane | [classical] | Thue 1910; a complete proof is usually credited to Fejes Toth 1943 |
| 1978 | Kabatianskii and Levenshtein prove the exponent 0.59905576 | [classical] | Kabatianskii-Levenshtein 1978, with Levenshtein 1979 |
| 2000 | Gorbachev writes down the Fourier certificate method | [classical] | Gorbachev 2000 |
| 2002-2003 | Cohn, then Cohn and Elkies, publish the method and compute with it | [classical] | Cohn 2002; Cohn-Elkies, Ann. of Math. 157 (2003) |
| 2005 | Hales's proof of the Kepler conjecture appears in print | [classical] | Hales 1998, published 2005 |
| 2014 | Cohn and Zhao: the method is at least as strong as the 1978 bound | [classical] | Cohn-Zhao 2014 |
| 2017 | Viazovska settles dimension 8 | [classical] | Viazovska, Ann. of Math. 185 (2017) |
| 2017 | Cohn, Kumar, Miller, Radchenko and Viazovska settle dimension 24 | [classical] | Cohn-Kumar-Miller-Radchenko-Viazovska 2017 |
| 2020 | Afkhami-Jeddi, Cohn, Hartman, de Laat and Tajdini conjecture the exact rate | [recent] | Afkhami-Jeddi-Cohn-Hartman-de Laat-Tajdini 2020, Conjectures 3.1-3.2 |
| 2010, 2019 | the sign uncertainty problems | [classical] | Bourgain-Clozel-Kahane 2010; the anti-self-Fourier version is Cohn-Goncalves 2019 |
| 2026 | the exact rate is proved, and the exponent is replaced | [recent] | chapter 1 of the source document, Theorems 1.1 and 1.2 |

The article names 1978 as the last time the general exponent moved. The source
says the same, and adds that later work (Cohn-Zhao 2014 and others) improved
only lower order factors, not the exponent.

## The numbers

| claim | value | bucket | test |
|---|---|---|---|
| unit ball volume in dimension d | pi to the d over two, over gamma of d over two plus one | [computed] | `test_low_dimensional_ball_volumes_are_the_familiar_ones` |
| the ball's own volume peaks at dimension 5 | | [computed] | `test_the_ball_volume_peaks_at_dimension_five_then_falls` |
| the ball fills less and less of its box | 0.19 % by dimension 10 | [computed] | `test_the_ball_eventually_fills_almost_none_of_its_box` |
| best density in dimension 2 | 0.9068996 | [classical] value, [computed] from the lattice | `test_the_known_densities_come_back_out_of_their_lattices` |
| best density in dimension 3 | 0.7404804 | [classical] | same |
| best density in dimension 8 | 0.2536695 | [classical] | same |
| best density in dimension 24 | 0.0019295 | [classical] | same |
| the exact rate of the method | root of e over two pi, 0.6577446 | [recent] | `test_the_rate_is_root_e_over_two_pi` |
| the new exponent | 0.604400544291677695 | [recent] | `test_the_exponent_matches_the_digits_the_paper_prints` |
| the exponent it replaces | 0.59905576 | [classical] | `test_the_new_exponent_beats_the_one_from_1978` |
| the sharp sign radius constant | one over pi | [recent] | `test_the_gaussian_radius_moves_exactly_to_one_over_pi` |
| the new bound is 40.6 times smaller in dimension 1000 | | [computed] | `test_how_much_the_improvement_is_worth_in_high_dimensions` |

## The proof ingredients this repo re-checks

These are steps of the 2026 argument that happen to be checkable by direct
computation. Checking them does not verify the theorem; it verifies that the
article describes the pieces correctly.

| ingredient | bucket | test |
|---|---|---|
| the Fourier eigenfunction basis flips sign with its index | [computed] | `test_the_building_blocks_are_their_own_fourier_transforms_up_to_sign` |
| the Mellin multiplier has size one on the real axis | [computed] | `test_the_mellin_multiplier_only_rotates_on_the_real_axis` |
| the limiting weight is a probability density with characteristic function t over sinh t | [computed] | `test_the_logistic_density_has_the_stated_fourier_side` |
| its logarithmic potential is a digamma value plus log two | [computed] | `test_the_log_potential_has_the_digamma_closed_form` |
| the harmonic measure carries mass one minus sigma over two, not one | [computed] | `test_harmonic_measure_carries_the_stated_non_unit_mass` |
| Wallis's integral equals the log of pi over two | [computed] | `test_wallis_gives_the_saddle_displacement` |
| the Gaussian radius times that displacement is exactly one over pi | [computed] | `test_the_gaussian_radius_moves_exactly_to_one_over_pi` |
| the pieces multiply to the stated rate | [computed] | `test_the_pieces_multiply_to_the_stated_rate` |

## This repository's own certificates

| claim | bucket | test |
|---|---|---|
| the simplest certificate exists only up to dimension 6 | [computed] | `test_the_simple_certificate_breaks_in_dimension_seven` |
| it proves something only in dimensions 4 and 5 | [computed] | `test_the_simple_certificate_is_useless_in_four_of_its_six_dimensions` |
| a hill climb finds a certificate proving 0.911648 in the plane | [computed] | `test_the_found_certificates_prove_the_bounds_the_article_quotes` |
| and 0.784806 in space | [computed] | same |
| both obey the sign rules on a grid 30 times finer than the search used | [computed] | `test_the_found_certificates_obey_both_rules_at_high_resolution` |
| the starting family runs out before dimension 6, so the search cannot begin in dimension 8 | [computed] | `test_the_starting_certificate_runs_out_before_dimension_six` |

**What this repo does not do.** The sign conditions are checked by sampling a
fine grid plus a leading term argument for the tail. That is a numerical check,
not a proof, and the article says so where the numbers appear. The optimised
certificates in the literature are found with semidefinite programming and
forced roots; nothing of that kind is implemented here.

## Where the guide deliberately simplifies

- The wall animation in chapter 9 draws an exponentially small allowance with a
  made up decay rate. The shape is the content, the constant is not, and the
  chapter says so.
- Chapter 11 draws the two directions closing at a rate chosen for legibility.
  The real error terms are the o(1) in the source's statements, not this.
- The Mellin transform, the strip, the maximum principle and the saddle point
  analysis are described in words and pictures. None of them is implemented.

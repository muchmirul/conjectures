"""Every number and construction the guide leans on, re-checked from scratch.

The tests are organised the way the article is: the small answers first, then
the two staircases, then each small part of the 2026 construction.  Anything
these tests cannot reach (the full recursion, the theorem itself) is not
claimed by the article either; `notes/research-content.md` keeps the ledger.
"""

import itertools
import math

import numpy as np
import pytest

from ramsey_guide import core as C
from ramsey_guide.examples import (FIRST_STAGE_COLORS, FOUR_COLOR_RANGE,
                                   GF16_BASE, H2_PARAMS, H3_PARAMS,
                                   KNOWN_FORCING, PENTAGON_BASE,
                                   PRE_2026_BASE, SAFE_TABLES)


# --- the small answers -------------------------------------------------------

def test_the_pentagon_coloring_is_safe_and_uses_two_colors():
    p = C.pentagon_coloring()
    assert C.is_complete(p)
    assert C.colors_used(p) == 2
    assert C.is_triangle_free(p)


def test_each_pentagon_color_is_a_five_cycle():
    """Both color graphs are rings of five, and a ring has no triangle."""
    p = C.pentagon_coloring()
    for color in (0, 1):
        degrees = [(p[i] == color).sum() for i in range(5)]
        assert degrees == [2, 2, 2, 2, 2]


def test_six_people_with_two_colors_always_force_a_triangle():
    """The forcing at six, verified over all 32768 colorings, not argued.

    Every one of the 2 to the 15 ways to two-color the fifteen edges of a
    six-person table is checked.  None of them is safe, so the guide's
    statement that six people force a one-color triangle is exhaustively
    verified rather than quoted.
    """
    n, edges = 6, list(itertools.combinations(range(6), 2))
    for bits in range(2 ** len(edges)):
        coloring = C.empty_coloring(n)
        for e, (i, j) in enumerate(edges):
            C.color_edge(coloring, i, j, (bits >> e) & 1)
        if C.is_triangle_free(coloring):
            pytest.fail(f"a safe two-coloring of six people exists: {bits}")


def test_six_people_always_produce_at_least_two_one_color_triangles():
    """Goodman's refinement, found here by the same exhaustive sweep."""
    n, edges = 6, list(itertools.combinations(range(6), 2))
    fewest = min(
        len(C.monochromatic_triangles(_from_bits(bits, edges, n)))
        for bits in range(2 ** len(edges)))
    assert fewest == 2


def _from_bits(bits, edges, n):
    coloring = C.empty_coloring(n)
    for e, (i, j) in enumerate(edges):
        C.color_edge(coloring, i, j, (bits >> e) & 1)
    return coloring


def test_the_sixteen_vertex_three_coloring_is_safe():
    g = C.gf16_coloring()
    assert C.is_complete(g)
    assert C.colors_used(g) == 3
    assert C.is_triangle_free(g)


def test_the_three_cube_classes_split_the_field_evenly_and_are_sum_free():
    """The reason the sixteen-vertex coloring works, checked directly."""
    sizes = [sum(1 for v in range(1, 16) if C.gf16_cube_class(v) == cls)
             for cls in range(3)]
    assert sizes == [5, 5, 5]
    assert all(C.class_is_sum_free(cls) for cls in range(3))


def test_the_known_forcing_sizes_match_the_safe_tables_built_here():
    assert KNOWN_FORCING[2][0] == 6 and SAFE_TABLES[2] == 5
    assert KNOWN_FORCING[3][0] == 17 and SAFE_TABLES[3] == 16
    assert len(C.pentagon_coloring()) == SAFE_TABLES[2]
    assert len(C.gf16_coloring()) == SAFE_TABLES[3]
    assert FOUR_COLOR_RANGE == (51, 62)


# --- the product construction --------------------------------------------------

def test_pentagon_times_pentagon_is_a_safe_four_coloring_of_twenty_five():
    p = C.pentagon_coloring()
    pp = C.product_coloring(p, p, 2)
    assert len(pp) == 25
    assert C.colors_used(pp) == 4
    assert C.is_triangle_free(pp)


def test_sixteen_times_pentagon_is_a_safe_five_coloring_of_eighty():
    pg = C.product_coloring(C.gf16_coloring(), C.pentagon_coloring(), 3)
    assert len(pg) == 80
    assert C.colors_used(pg) == 5
    assert C.is_triangle_free(pg)


def test_a_fixed_product_keeps_the_same_rate_forever():
    """Multiplying the pentagon k/2 times gives root-five per color, always."""
    tower = C.product_tower_sizes(5, 2, 8)
    rates = [size ** (1 / colors) for colors, size in tower]
    assert all(abs(r - PENTAGON_BASE) < 1e-9 for r in rates)
    tower16 = C.product_tower_sizes(16, 3, 6)
    rates16 = [size ** (1 / colors) for colors, size in tower16]
    assert all(abs(r - GF16_BASE) < 1e-9 for r in rates16)


def test_the_block_product_floor_stays_under_the_ceiling():
    """The chart of chapter 7 must never show the floor above the ceiling.

    A smooth fixed-base curve does exactly that at small color counts,
    which is why the honest floor is the block-product value.  The floor
    must also agree with the record blocks themselves.
    """
    ceiling = C.upper_staircase(14)
    for k in range(1, 15):
        assert C.best_product_lower(k) < ceiling[k - 1]
    assert C.best_product_lower(2) == 5
    assert C.best_product_lower(3) == 16
    assert C.best_product_lower(4) == 50
    assert C.best_product_lower(8) == 50 * 50
    # per color, the floor approaches the four-color block's rate from below,
    # which stays under the asymptotic Schur rate the article quotes
    assert C.best_product_lower(40) ** (1 / 40) == pytest.approx(
        50 ** 0.25, rel=1e-6)
    assert 50 ** 0.25 < PRE_2026_BASE


def test_no_literal_five_color_block_could_reach_the_quoted_rate():
    """The 3.28 rate is asymptotic: a real 380-person five-color table would
    contradict the staircase, which caps five colors at 327."""
    assert C.upper_staircase(5)[-1] == 327 < 380
    assert PRE_2026_BASE ** 5 == pytest.approx(380, rel=1e-12)


# --- the two staircases ----------------------------------------------------------

def test_the_upper_staircase_reproduces_the_settled_values():
    assert C.upper_staircase(4) == [3, 6, 17, 66]


def test_the_upper_staircase_is_at_most_a_constant_times_factorial():
    values = C.upper_staircase(12)
    for k, v in enumerate(values, start=1):
        assert v <= 3 * math.factorial(k)


def test_the_record_upper_bound_is_the_quoted_multiple_of_factorial():
    assert C.factorial_record(4) == (math.e - 1 / 6) * 24 + 1


def test_the_old_base_and_the_bases_of_the_small_records():
    assert abs(PENTAGON_BASE - 2.2360680) < 1e-6
    assert abs(GF16_BASE - 2.5198421) < 1e-6
    assert abs(PRE_2026_BASE - 3.2806260) < 1e-6
    # each is genuinely better than the one before
    assert PENTAGON_BASE < GF16_BASE < PRE_2026_BASE


# --- the permutation shortcut fails -----------------------------------------------

def test_the_first_difference_shortcut_makes_a_one_color_triangle():
    """Three orderings that pairwise first-disagree at the same position."""
    perms, coloring = C.first_difference_coloring(3)
    triangles = C.monochromatic_triangles(coloring)
    assert triangles, "the shortcut should fail, and visibly"
    i, j, k = triangles[0]
    a, b, c = perms[i], perms[j], perms[k]
    d = next(p for p in range(3) if a[p] != b[p])
    assert a[d] != b[d] and b[d] != c[d] and a[d] != c[d]


# --- the saturated matrix and the meeting guarantee --------------------------------

@pytest.fixture(scope="module")
def matrix():
    return C.find_saturated_matrix(2, seed=0)


def test_the_two_color_matrix_parameters_are_the_papers_formula():
    assert H2_PARAMS == (3, 13)
    assert H3_PARAMS == (7, 57)
    assert FIRST_STAGE_COLORS == 342 == C.stage_colors(3)


def test_the_found_matrix_is_saturated_for_every_column_set(matrix):
    """All seventy ways to pick four of the eight columns, no exceptions."""
    assert matrix.shape == (13, 8)
    assert C.is_saturated(matrix, 2, 3)


def test_no_word_has_more_exceptional_columns_than_the_proof_allows(matrix):
    """|E_y| is at most m, checked for every one of the 8192 words."""
    worst = max(len(C.exceptional_columns(matrix, y, 2, 3))
                for y in itertools.product(range(2), repeat=13))
    assert worst <= 3


def test_the_two_fixed_maps_meet_every_pair_of_words(matrix):
    """The meeting guarantee, exhaustively: no pair of words escapes."""
    assert C.cover_holds_everywhere(matrix, 2, 3)


def test_the_saturated_property_is_not_automatic():
    """A deliberately bad matrix fails, so the check is doing real work.

    At this toy size almost every random matrix happens to pass, which is
    why the article says the two union bounds earn their keep at the real
    sizes, not here.  But the property is still a property: a matrix whose
    rows all repeat the same left-right pattern misses whole column sets,
    and `is_saturated` catches it.
    """
    lazy = np.array([[z % 2 for z in range(8)] for _ in range(13)], dtype=int)
    assert not C.is_saturated(lazy, 2, 3)


# --- palettes: the parity rule and the trap ------------------------------------------

def test_no_membership_pattern_lets_a_color_reach_all_three_blocks():
    """The three-block argument, by exhaustion over all eight cases."""
    for p, q, r in C.three_block_patterns():
        assert not C.pattern_allows_triangle(p, q, r)


def test_the_ring_labels_are_a_proper_labeling_of_the_ring_color():
    p = C.pentagon_coloring()
    for i in range(5):
        for j in range(i + 1, 5):
            if p[i, j] == 0:
                assert C.RING_LABELS[i] != C.RING_LABELS[j]


def test_breaking_the_label_rule_makes_a_triangle_and_obeying_it_does_not():
    broken = C.trap_coloring(obey_rule=False)
    obeyed = C.trap_coloring(obey_rule=True)
    assert C.monochromatic_triangles(broken) == [(0, 1, 5)]
    assert C.is_triangle_free(obeyed)


# --- the five-symbol channel ------------------------------------------------------------

def test_single_letters_over_the_noisy_pentagon_allow_only_two_words():
    """Any three symbols contain a confusable pair, so codes of length one
    stop at two words."""
    best = max(
        sum(1 for a in combo for b in combo
            if a < b and not C.pentagon_confusable(a, b))
        for combo in itertools.combinations(range(5), 3))
    # no triple is pairwise safe: at most one safe pair inside any three
    for combo in itertools.combinations(range(5), 3):
        safe_pairs = [(a, b) for a in combo for b in combo
                      if a < b and not C.pentagon_confusable(a, b)]
        assert len(safe_pairs) < 3


def test_the_five_two_letter_codewords_are_pairwise_safe():
    """Shannon's 1956 example, checked pair by pair: five words of length
    two, though single letters only ever gave two."""
    book = C.C5_CODEBOOK
    for u, v in itertools.combinations(book, 2):
        assert C.words_distinguishable(u, v)


# --- the final bound's shape -----------------------------------------------------------

def test_the_explicit_bound_is_trivial_at_every_drawable_size():
    """Honesty check: with the printed constant, the new bound only beats
    the old fixed-base record at around ten to the sixtieth colors."""
    assert C.explicit_new_base(342) < 1
    crossover = C.crossover_estimate()
    assert 1e55 < crossover < 1e65
    assert C.explicit_new_base(crossover * 10) > PRE_2026_BASE


def test_the_new_base_eventually_grows_without_bound():
    ks = [1e70, 1e80, 1e100, 1e150]
    bases = [C.explicit_new_base(k) for k in ks]
    assert all(b < a for b, a in zip(bases, bases[1:]))
    assert bases[-1] > 1e10

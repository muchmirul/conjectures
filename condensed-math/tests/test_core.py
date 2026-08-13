"""Recompute every number the three articles quote.

What can be checked here is the finite machinery: probes as real inverse
systems, weightings as compatible integer families, homology by Smith normal
form, the norms and ranks and truncations.  What cannot be checked is any
statement about a category, and `notes/research-content.md` marks those as
quoted.  These tests never pretend otherwise.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
import pytest

from condensed_guide import core as C
from condensed_guide.examples import (CANTOR_LEVEL_SIZES,
                                      MEASURE_EXPONENT_CEILING,
                                      SHAPE_HOMOLOGY, SOURCE, TENSOR_CLAIMS)


# --- part one: probes -------------------------------------------------------

def test_the_halving_probe_doubles():
    S = C.cantor(5)
    assert S.sizes() == CANTOR_LEVEL_SIZES
    assert S.sizes() == [2 ** i for i in range(6)]


def test_the_approaching_probe_separates_one_point_per_stage():
    S = C.convergent_sequence(6)
    assert S.sizes() == [1, 2, 3, 4, 5, 6, 7]
    # every stage holds the points separated so far plus one box for the rest
    for i in range(1, 7):
        assert "oo" in S.levels[i]
        assert sorted(x for x in S.levels[i] if x != "oo") == list(range(i))


@pytest.mark.parametrize("p", [2, 3, 5])
def test_the_base_p_probe_multiplies_by_p(p):
    S = C.p_adic(p, 4)
    assert S.sizes() == [p ** i for i in range(5)]


@pytest.mark.parametrize("S", [C.cantor(4), C.convergent_sequence(5),
                               C.p_adic(3, 3), C.finite_set(6)])
def test_every_probe_is_an_inverse_system(S):
    """Surjective transition maps, defined on the whole of each stage."""
    S.check()


def test_projecting_down_the_probe_is_consistent():
    S = C.cantor(4)
    for label in S.levels[4]:
        # projecting in one jump agrees with projecting one level at a time
        step = label
        for i in range(3, -1, -1):
            step = S.parents[i][step]
            assert step == S.project(label, 4, i)


def test_a_boxs_fibre_is_everything_inside_it():
    S = C.cantor(4)
    for label in S.levels[2]:
        inside = S.fibre(label, at=4, over=2)
        assert len(inside) == 4          # two more splits below level two
        assert all(x.startswith(label) for x in inside)


# --- part one and two: weightings -------------------------------------------

@pytest.mark.parametrize("S", [C.cantor(4), C.p_adic(3, 3),
                               C.convergent_sequence(5)])
def test_a_counting_weighting_obeys_the_agreement_rule(S):
    m = C.counting_measure(S)
    m.check()
    assert m.total() == S.size(S.depth)


@pytest.mark.parametrize("S", [C.cantor(4), C.p_adic(2, 4)])
def test_a_single_point_carries_a_weighting(S):
    point = S.levels[S.depth][3]
    m = C.dirac(S, point)
    m.check()
    assert m.total() == 1


def test_an_uneven_weighting_still_agrees():
    S = C.cantor(4)
    rng = np.random.default_rng(0)
    leaves = {lab: int(v) for lab, v in
              zip(S.levels[4], rng.integers(-5, 9, S.size(4)))}
    m = C.measure_from_leaves(S, leaves)
    m.check()
    assert m.total() == sum(leaves.values())


def test_a_broken_weighting_is_caught():
    S = C.cantor(3)
    m = C.counting_measure(S)
    m.weights[1][S.levels[1][0]] += 1        # break the rule by one
    with pytest.raises(AssertionError):
        m.check()


@pytest.mark.parametrize("S,read", [(C.cantor(5), 2), (C.cantor(5), 3),
                                    (C.p_adic(3, 3), 1)])
def test_the_level_you_read_at_makes_no_difference(S, read):
    """The property that makes integrating against a weighting well posed."""
    rng = np.random.default_rng(7)
    leaves = {lab: int(v) for lab, v in
              zip(S.levels[S.depth], rng.integers(-4, 7, S.size(S.depth)))}
    m = C.measure_from_leaves(S, leaves)
    f = {lab: int(v) for lab, v in
         zip(S.levels[read], rng.integers(-3, 8, S.size(read)))}
    coarse = m.integrate(f, read)
    for finer in range(read + 1, S.depth + 1):
        assert m.integrate(C.refine(S, f, read, finer), finer) == coarse


def test_locally_constant_rank_is_the_box_count():
    S = C.cantor(4)
    for i in range(5):
        assert C.locally_constant_rank(S, i) == S.size(i)


# --- part two: Bergman's construction ---------------------------------------

@pytest.mark.parametrize("depth", [1, 2, 3, 4])
def test_the_basis_construction_finds_one_element_per_box(depth):
    """A finite shadow of Nöbeling's theorem.

    At a finite stage the group is free for trivial reasons; what this checks
    is that the construction of the lectures produces a basis of the right
    size rather than over- or under-shooting.
    """
    points = C.cantor_points(depth)
    basis = C.nobeling_basis(points)
    assert len(basis) == len(points) == 2 ** depth
    assert len(set(basis)) == len(basis)


def test_the_basis_construction_spans():
    """The kept products really do span every function on the stage."""
    depth = 3
    points = C.cantor_points(depth)
    basis = C.nobeling_basis(points)
    rows = [[int(all(pt[c] == 1 for c in subset)) for pt in points]
            for subset in basis]
    assert C._rank_over_q(rows) == len(points)


def test_the_basis_construction_on_a_proper_subset():
    """Fewer points means fewer basis elements, and exactly as many."""
    points = [p for p in C.cantor_points(3) if p != (1, 1, 1)]
    assert len(C.nobeling_basis(points)) == len(points)


# --- part two: the doubling sum ---------------------------------------------

@pytest.mark.parametrize("p", [2, 3, 5])
def test_the_geometric_sum_lands_on_one_over_one_minus_p(p):
    lim = C.geometric_limit(p)
    assert lim == Fraction(1, 1 - p)
    sums = C.geometric_partial_sums(p, 10)
    # the gap to the limit is exactly the next power, up to sign
    for n, s in enumerate(sums):
        assert s - lim == Fraction(p ** (n + 1), p - 1)


def test_base_two_gives_minus_one():
    assert C.geometric_limit(2) == -1
    assert C.geometric_partial_sums(2, 5) == [1, 3, 7, 15, 31]


@pytest.mark.parametrize("p", [2, 3, 5])
def test_the_two_distances_move_in_opposite_directions(p):
    lim = C.geometric_limit(p)
    sums = C.geometric_partial_sums(p, 9)
    ordinary = [abs(s - lim) for s in sums]
    padic = [C.p_adic_abs(s - lim, p) for s in sums]
    for k in range(1, len(sums)):
        assert ordinary[k] == ordinary[k - 1] * p
        assert padic[k] == pytest.approx(padic[k - 1] / p)
    assert padic[-1] == pytest.approx(float(p) ** -9)


def test_the_p_adic_size_of_a_power():
    for k in range(6):
        assert C.p_adic_abs(Fraction(2 ** k), 2) == pytest.approx(2.0 ** -k)
    assert C.p_adic_abs(Fraction(0), 2) == 0.0
    assert C.p_adic_abs(Fraction(1, 8), 2) == pytest.approx(8.0)


# --- part two: products, sums, tensor ---------------------------------------

def test_index_sets_multiply():
    I, J = list("abc"), list("xy")
    assert len(C.tensor_index(I, J)) == len(I) * len(J)


def test_a_two_variable_series_pairs_off_with_two_one_variable_ones():
    """The one entry of the multiplication table this repository derives."""
    order = 5
    one = C.power_series_monomials(order)
    both = C.double_series_monomials(order)
    assert sorted(C.tensor_index(one, one)) == sorted(both)
    assert len(both) == order * order


@pytest.mark.parametrize("a,b,expected", TENSOR_CLAIMS)
def test_the_quoted_multiplication_table(a, b, expected):
    assert C.solid_tensor(a, b) == expected
    assert C.quoted_tensor(a, b)


def test_the_multiplication_rule_is_symmetric():
    names = [n for n in C.ADIC_DIRECTIONS]
    for a in names:
        for b in names:
            assert C.solid_tensor(a, b) == C.solid_tensor(b, a)


def test_the_ruler_annihilates_and_two_primes_annihilate():
    for other in C.ADIC_DIRECTIONS:
        assert C.solid_tensor("R", other) == "0"
    assert C.solid_tensor("Z_p", "Z_l") == "0"
    assert C.solid_tensor("Z_p[[T]]", "Z_l") == "0"


def test_the_whole_numbers_are_the_unit_of_the_rule():
    for other in C.ADIC_DIRECTIONS:
        if other == "R":
            continue
        assert C.solid_tensor("Z", other) == other


def test_naming_a_set_of_directions():
    assert C.name_directions([]) == "Z"
    assert C.name_directions(["p"]) == "Z_p"
    assert C.name_directions(["T", "U"]) == "Z[[T,U]]"
    assert C.name_directions(["U", "T"]) == "Z[[T,U]]"      # order-free
    assert C.name_directions(["p", "T"]) == "Z_p[[T]]"


# --- part two: holes --------------------------------------------------------

@pytest.mark.parametrize("name", sorted(SHAPE_HOMOLOGY))
def test_the_holes_of_each_shape(name):
    got = C.SHAPES[name]().homology()
    assert got == SHAPE_HOMOLOGY[name]


def test_the_klein_bottle_has_a_hole_of_order_two():
    free, torsion = C.klein_bottle().homology()[1]
    assert free == 1
    assert torsion == [2]


def test_the_torus_and_the_klein_bottle_differ_only_in_the_gluing():
    """Same cells, one sign changed, and the homology moves."""
    assert C.torus().cell_counts == C.klein_bottle().cell_counts
    assert C.torus().homology() != C.klein_bottle().homology()


def test_smith_normal_form_on_known_matrices():
    assert C.smith_normal_form([[2]]) == [2]
    assert C.smith_normal_form([[0]]) == []
    assert C.smith_normal_form([[2, 0], [0, 3]]) == [1, 6]
    assert C.smith_normal_form([[1, 2], [3, 4]]) == [1, 2]


def test_the_hole_counts_of_a_stack_of_circles():
    for n in range(1, 8):
        ranks = C.exterior_ranks(n)
        assert len(ranks) == n + 1
        assert ranks == [math.comb(n, i) for i in range(n + 1)]
        assert sum(ranks) == 2 ** n
        assert ranks == ranks[::-1]                       # Pascal is symmetric


def test_the_stack_of_two_circles_matches_the_doughnut():
    """The article says a doughnut is two circles; the counts must agree."""
    free = [f for f, _ in C.torus().homology()]
    assert free == C.exterior_ranks(2)


# --- part one: winding ------------------------------------------------------

@pytest.mark.parametrize("turns", [-3, -1, 0, 1, 2, 5])
def test_the_winding_number_counts_the_turns(turns):
    t = np.linspace(0, 2 * np.pi, 4001)
    assert C.winding_number(turns * t) == turns


@pytest.mark.parametrize("wobble", [0.0, 0.3, 0.9, 1.6])
def test_the_winding_number_survives_a_wobble(wobble):
    t = np.linspace(0, 2 * np.pi, 4001)
    assert C.winding_number(2 * t + wobble * np.sin(5 * t)) == 2


# --- part three: the exponent -----------------------------------------------

@pytest.mark.parametrize("boxes", [2, 3, 4, 9, 16])
@pytest.mark.parametrize("p", [0.4, 0.7, 1.0, 1.3, 2.0, 3.0])
def test_the_closed_form_for_merging_equal_boxes(boxes, p):
    values = [1.0] * boxes
    direct = C.merge_ratio(values, [list(range(boxes))], p)
    assert direct == pytest.approx(C.worst_merge_ratio(boxes, p), rel=1e-12)


@pytest.mark.parametrize("boxes", [2, 4, 9])
def test_merging_only_shrinks_below_the_ceiling(boxes):
    for p in np.linspace(0.3, 2.5, 45):
        ratio = C.worst_merge_ratio(boxes, float(p))
        if p <= MEASURE_EXPONENT_CEILING + 1e-12:
            assert ratio <= 1 + 1e-9
        else:
            assert ratio > 1


def test_the_ratio_is_exactly_one_at_the_ceiling():
    for boxes in (2, 3, 7, 40):
        assert C.worst_merge_ratio(boxes, 1.0) == pytest.approx(1.0)


@pytest.mark.parametrize("p", [0.3, 0.5, 0.8, 1.0])
def test_below_the_ceiling_merging_shrinks_whatever_the_weights(p):
    """The statement the theory actually needs, for every configuration."""
    rng = np.random.default_rng(3)
    for _ in range(300):
        n = int(rng.integers(2, 9))
        values = list(rng.uniform(0.01, 4.0, n))
        assert C.merge_ratio(values, [list(range(n))], p) <= 1 + 1e-9


@pytest.mark.parametrize("p", [1.2, 1.5, 2.0, 3.0])
def test_above_the_ceiling_equal_weights_grow_the_most(p):
    """Above the ceiling merging can grow, and the equal case is the extreme."""
    rng = np.random.default_rng(3)
    worst = C.worst_merge_ratio(5, p)
    assert worst > 1
    for _ in range(300):
        values = list(rng.uniform(0.05, 1.0, 5))
        assert C.merge_ratio(values, [list(range(5))], p) <= worst + 1e-9


@pytest.mark.parametrize("p,convex", [(0.4, False), (0.5, False), (0.8, False),
                                      (1.0, True), (1.5, True), (2.0, True),
                                      (3.0, True)])
def test_where_the_unit_ball_is_convex(p, convex):
    assert C.is_convex(p) is convex


def test_the_unit_ball_really_has_unit_size():
    for p in (0.5, 1.0, 2.0):
        pts = C.lp_ball(p, 361)
        for pt in pts[::17]:
            assert C.lp_size(pt, p) == pytest.approx(1.0, rel=1e-9)


def test_merging_adds_the_weights():
    assert C.merge([1, 2, 3, 4], [[0, 1], [2, 3]]) == [3.0, 7.0]
    assert C.merge([1, 2, 3], [[0, 1, 2]]) == [6.0]


# --- part three: functions near the edge ------------------------------------

@pytest.mark.parametrize("tails", range(1, 9))
def test_the_line_keeps_exactly_its_tails(tails):
    for top in range(1, 10):
        assert C.line_edge_quotient_rank(top, tails) == tails


@pytest.mark.parametrize("tails", range(1, 9))
def test_the_cross_keeps_both_tails_and_one_more(tails):
    for top in range(1, 10):
        assert C.cross_edge_quotient_rank(top, tails) == 2 * tails + 1


def test_the_cross_beats_two_copies_of_the_line_by_exactly_one():
    for top in range(1, 8):
        for tails in range(1, 8):
            line = C.line_edge_quotient_rank(top, tails)
            cross = C.cross_edge_quotient_rank(top, tails)
            assert cross - 2 * line == 1


def test_the_truncation_does_not_move_the_answer():
    """Pushing the polynomial part further out changes nothing."""
    got = {C.line_edge_quotient_rank(top, 4) for top in range(1, 30)}
    assert got == {4}


# --- the article's own bookkeeping ------------------------------------------

def test_every_cited_result_has_a_page():
    for key, (plain, label, page) in SOURCE.items():
        assert plain and label
        assert 5 <= page <= 78, f"{key} cites page {page}, outside the PDF"

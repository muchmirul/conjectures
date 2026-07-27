"""The exact geometry the guide leans on: unions, merges and Perron trees."""

import random
from fractions import Fraction

import pytest

from kakeya_guide.core import (direction_cover, elementary_slivers,
                               extrusion_holds_direction,
                               holds_every_direction, is_translate,
                               merged_pair_area, perron_tree, ramped_alphas,
                               sliver, union_area, union_area_numeric,
                               union_area_reference, union_length, width_at)
from kakeya_guide.examples import (FAN, PERRON_STALL_LIMIT, RAMPED_AREAS,
                                   RAMPED_AREAS_DECIMAL, THE_TRIANGLE,
                                   steady_area, tree)


# --- slivers and their areas (chapters 3 and 5) ----------------------------

def test_the_triangle_has_area_one_half():
    assert THE_TRIANGLE.area == Fraction(1, 2)
    assert union_area([THE_TRIANGLE]) == Fraction(1, 2)


def test_sliding_changes_nothing_but_position():
    moved = THE_TRIANGLE.translate(Fraction(-7, 3))
    assert moved.area == THE_TRIANGLE.area
    assert is_translate(moved, THE_TRIANGLE)
    assert moved.direction_interval() == THE_TRIANGLE.direction_interval()


def test_cutting_the_base_conserves_area():
    for k in range(5):
        pieces = elementary_slivers(k, (0, 1), Fraction(1, 2), 1)
        assert len(pieces) == 2 ** k
        assert sum(p.area for p in pieces) == Fraction(1, 2)
        assert union_area(pieces) == Fraction(1, 2)


def test_overlap_is_counted_once():
    a = sliver(0, 1, Fraction(1, 2))
    assert union_area([a, a, a]) == a.area                    # exact copies
    b = a.translate(Fraction(1, 2))
    assert union_area([a, b]) < 2 * a.area                    # partly stacked
    far = a.translate(10)
    assert union_area([a, far]) == 2 * a.area                 # nothing shared


def test_union_length_merges_touching_intervals():
    assert union_length([(Fraction(0), Fraction(1)),
                         (Fraction(1), Fraction(2))]) == 2
    assert union_length([(Fraction(0), Fraction(2)),
                         (Fraction(1), Fraction(3))]) == 3
    assert union_length([(Fraction(0), Fraction(9)),
                         (Fraction(1), Fraction(2))]) == 9


# --- the one merge that everything is built from (chapter 5) ---------------

@pytest.mark.parametrize("t", [Fraction(n, 12) for n in range(0, 13)])
def test_merged_pair_matches_the_closed_form(t):
    # two halves of a triangle of base 2 and height 1, right half slid left by t
    assert merged_pair_area(t) == 1 - t + 3 * t * t / 4


def test_the_best_single_merge_keeps_two_thirds():
    areas = {t: merged_pair_area(t) for t in
             (Fraction(n, 60) for n in range(0, 121))}
    best_t = min(areas, key=lambda t: areas[t])
    assert best_t == Fraction(2, 3)
    assert areas[best_t] == Fraction(2, 3)          # of the original area 1


# --- the fast sweep, checked against the slow obvious method ---------------

def test_sweep_agrees_with_reference_on_random_figures():
    rng = random.Random(20250224)
    for _ in range(12):
        pieces = []
        for _ in range(6):
            b0 = Fraction(rng.randint(-8, 8), 4)
            w = Fraction(rng.randint(1, 8), 4)
            pieces.append(sliver(b0, b0 + w, Fraction(rng.randint(-9, 9), 4)))
        assert union_area(pieces) == union_area_reference(pieces)


def test_sweep_agrees_with_reference_on_a_real_tree():
    for k in range(4):
        t = tree(k)
        assert union_area(t) == union_area_reference(t)


def test_numeric_estimate_tracks_the_exact_area():
    for k in range(7):
        t = tree(k)
        assert union_area_numeric(t) == pytest.approx(float(union_area(t)),
                                                      abs=2e-6)


def test_width_at_matches_a_slice_by_hand():
    # THE_TRIANGLE at half height is the interval [1/4, 3/4]
    assert width_at([THE_TRIANGLE], Fraction(1, 2)) == Fraction(1, 2)
    assert width_at([THE_TRIANGLE], 0) == 1
    assert width_at([THE_TRIANGLE], 1) == 0


# --- Perron trees: the steady squeeze stalls (chapter 5) -------------------

@pytest.mark.parametrize("k", range(7))
def test_steady_squeeze_has_an_exact_closed_form(k):
    assert union_area(perron_tree(k, Fraction(2, 3))) == steady_area(k)


def test_steady_squeeze_never_gets_past_a_sixth():
    for k in range(7):
        assert union_area(perron_tree(k, Fraction(2, 3))) > PERRON_STALL_LIMIT
    assert steady_area(40) - PERRON_STALL_LIMIT < Fraction(1, 10 ** 12)


# --- Perron trees: the varying squeeze keeps going -------------------------

@pytest.mark.parametrize("k", sorted(RAMPED_AREAS))
def test_ramped_tree_areas_are_what_the_guide_quotes(k):
    assert union_area(tree(k)) == RAMPED_AREAS[k]


@pytest.mark.parametrize("k", range(7))
def test_ramped_decimals_are_what_the_guide_quotes(k):
    assert round(float(union_area(tree(k))), 6) == RAMPED_AREAS_DECIMAL[k]


@pytest.mark.parametrize("k", range(7, 10))
def test_deeper_ramped_decimals_hold_up_numerically(k):
    assert union_area_numeric(tree(k)) == pytest.approx(
        RAMPED_AREAS_DECIMAL[k], abs=2e-6)


def test_every_cut_shrinks_the_figure():
    areas = [union_area(tree(k)) for k in range(7)]
    assert all(b < a for a, b in zip(areas, areas[1:]))


def test_varying_the_squeeze_breaks_the_one_sixth_wall():
    # the steady squeeze can never get here, however deep it goes
    assert union_area(tree(7)) < steady_area(60)
    assert union_area_numeric(tree(9)) < float(PERRON_STALL_LIMIT)


def test_the_alphas_are_the_advertised_sequence():
    assert ramped_alphas(5) == [Fraction(1, 4), Fraction(2, 5), Fraction(1, 2),
                                Fraction(4, 7), Fraction(5, 8)]


# --- and it is still a Kakeya figure (chapters 5 and 6) --------------------

@pytest.mark.parametrize("k", range(7))
def test_the_tree_still_holds_a_needle_in_every_direction(k):
    t = tree(k)
    assert direction_cover(t) == [FAN]
    assert holds_every_direction(t, *FAN)
    assert FAN == (Fraction(-1, 2), Fraction(1, 2))


@pytest.mark.parametrize("k", range(7))
def test_nothing_was_rotated_or_resized_along_the_way(k):
    t = tree(k)
    originals = elementary_slivers(k, (0, 1), Fraction(1, 2), 1)
    assert len(t) == 2 ** k
    for moved, original in zip(t, originals):
        assert is_translate(moved, original)


def test_a_tree_that_loses_a_sliver_loses_directions():
    t = tree(3)
    assert not holds_every_direction(t[1:], *FAN)


# --- pushed sideways into space (chapter 12) -------------------------------

def test_the_extruded_tree_holds_space_directions_over_its_fan():
    """A slab holds every direction whose shadow lies in the flat fan."""
    t = tree(4)
    for run in (Fraction(-1, 2), Fraction(-1, 5), Fraction(0),
                Fraction(1, 3), Fraction(1, 2)):
        for rise in (Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3, 2)):
            assert extrusion_holds_direction(t, (run, -1, rise),
                                             half_height=Fraction(1, 2))


def test_the_extruded_tree_misses_what_the_flat_fan_misses():
    t = tree(4)
    # a shadow steeper than the fan, and one lying flat along the ground line
    assert not extrusion_holds_direction(t, (2, -1, 0), Fraction(1, 2))
    assert not extrusion_holds_direction(t, (1, 0, 0), Fraction(1, 2))


def test_straight_up_needs_only_thickness():
    t = tree(2)
    assert extrusion_holds_direction(t, (0, 0, 1), half_height=Fraction(1, 2))
    assert not extrusion_holds_direction(t, (0, 0, 1), half_height=Fraction(1, 4))


def test_the_needle_drawn_in_the_3d_figure_really_is_inside_the_slab():
    """The blue needle in guide/12-the-proof/kakeya3d.gif, checked point by
    point: its shadow stays inside a sliver and its height stays in the slab."""
    import math

    t = tree(4)
    half = 0.5
    widest = max(t, key=lambda s: s.ax)
    lo, hi = (float(v) for v in widest.direction_interval())
    run, rise = (lo + hi) / 2, 0.5
    flat = math.sqrt(1 - rise ** 2) / math.hypot(run, 1.0)
    start = (float(widest.ax), 1.0, -rise / 2)
    step = (run * flat, -flat, rise)
    assert math.isclose(math.hypot(*step), 1.0, abs_tol=1e-12)   # a unit needle

    def in_some_sliver(x, y):
        for s in t:
            h = float(s.h)
            if not -1e-9 <= y <= h + 1e-9:
                continue
            u = y / h
            left = float(s.b0) + (float(s.ax) - float(s.b0)) * u
            right = float(s.b1) + (float(s.ax) - float(s.b1)) * u
            if left - 1e-9 <= x <= right + 1e-9:
                return True
        return False

    for i in range(41):
        p = [start[j] + step[j] * i / 40 for j in range(3)]
        assert in_some_sliver(p[0], p[1])
        assert abs(p[2]) <= half + 1e-9

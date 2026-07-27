"""The rooms people tried before Besicovitch, and what a motion costs."""

import math

import pytest

from kakeya_guide.shapes import (DELTOID_A, DELTOID_AREA, DISC_AREA,
                                 TRIANGLE_AREA, deltoid, deltoid_needle,
                                 deltoid_tangent_chord, disc, equilateral,
                                 equilateral_turn, fits_every_direction,
                                 longest_chord,
                                 needle_in_polygon, pal_join_area,
                                 pal_join_travel, polygon_area, sector_area)


def inside(poly, p, pad=1e-9):
    """Is the point in the convex polygon?  Touching an edge counts as in."""
    x, y = p
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        cross = (x1 - x0) * (y - y0) - (y1 - y0) * (x - x0)
        if cross < -pad:
            return False
    return True


# --- how big the three classical rooms are (chapter 2) ---------------------

def test_the_three_rooms_have_the_areas_the_guide_quotes():
    assert polygon_area(disc(0.5, 4000)) == pytest.approx(DISC_AREA, rel=1e-6)
    assert polygon_area(equilateral(1.0)) == pytest.approx(TRIANGLE_AREA,
                                                           rel=1e-12)
    assert polygon_area(deltoid(n=4000)) == pytest.approx(DELTOID_AREA,
                                                          rel=1e-5)


def test_each_room_beats_the_last():
    assert DELTOID_AREA < TRIANGLE_AREA < DISC_AREA
    assert DELTOID_AREA == pytest.approx(TRIANGLE_AREA * 0.68, rel=0.01)


def test_the_disc_is_the_lazy_answer():
    assert DISC_AREA == pytest.approx(math.pi / 4)
    # a needle spun about its middle stays in the disc of diameter 1
    assert all(math.hypot(0.5 * math.cos(a), 0.5 * math.sin(a)) <= 0.5 + 1e-12
               for a in [i * math.pi / 180 for i in range(180)])


# --- the equilateral triangle of height 1 (Pal, 1921) ----------------------

def test_the_triangle_of_height_one_fits_the_needle_every_way():
    assert fits_every_direction(equilateral(1.0), 1.0, samples=720)


def test_a_slightly_shorter_triangle_does_not():
    assert not fits_every_direction(equilateral(0.99), 1.0, samples=720)


def test_the_tightest_direction_is_exactly_the_height():
    poly = equilateral(1.0)
    lengths = [math.dist(*longest_chord(poly, math.pi * i / 720))
               for i in range(720)]
    assert min(lengths) == pytest.approx(1.0, abs=1e-6)


def test_pals_turn_stays_inside_and_turns_a_full_half_circle():
    poly = equilateral(1.0)
    angles = []
    for i in range(600):
        p, q = equilateral_turn(i / 600)
        assert math.dist(p, q) == pytest.approx(1.0, abs=1e-9)
        assert inside(poly, p, 1e-9) and inside(poly, q, 1e-9)
        angles.append(math.atan2(q[1] - p[1], q[0] - p[0]))
    turned = 0.0
    for a, b in zip(angles, angles[1:]):
        turned += (b - a + math.pi) % (2 * math.pi) - math.pi
    assert abs(turned) == pytest.approx(math.pi, abs=1e-6)


def test_the_needle_really_sits_inside_the_triangle():
    poly = equilateral(1.0)
    for i in range(120):
        p, q = needle_in_polygon(poly, math.pi * i / 120)
        assert math.dist(p, q) == pytest.approx(1.0)
        assert inside(poly, p, 1e-9) and inside(poly, q, 1e-9)


# --- the deltoid, Kakeya's own guess (chapter 2) ---------------------------

def test_the_tangent_chord_is_always_one_unit_long():
    for i in range(200):
        t = 2 * math.pi * i / 200
        p, q = deltoid_tangent_chord(t)
        assert math.dist(p, q) == pytest.approx(4 * DELTOID_A, abs=1e-12)


def test_the_needle_turns_a_full_half_circle_inside_the_deltoid():
    angles = [deltoid_needle(2 * math.pi * i / 400)[1] for i in range(401)]
    unwrapped, shift = [angles[0]], 0.0
    for a, b in zip(angles, angles[1:]):
        if b - a > math.pi / 2:
            shift -= math.pi
        elif a - b > math.pi / 2:
            shift += math.pi
        unwrapped.append(b + shift)
    turned = abs(unwrapped[-1] - unwrapped[0])
    assert turned == pytest.approx(math.pi, abs=1e-6)   # a needle's full turn


def test_the_deltoid_is_smaller_than_anything_convex_can_be():
    # so the deltoid is not convex: it beats Pal's convex minimum
    assert DELTOID_AREA < TRIANGLE_AREA


# --- what turning and sliding cost (chapter 4) ----------------------------

def test_pivoting_sweeps_a_sector():
    assert sector_area(math.pi) == pytest.approx(math.pi / 2)
    assert sector_area(math.pi / 2, 2.0) == pytest.approx(math.pi)


def test_pals_join_costs_as_little_as_you_like_and_travels_as_far():
    areas = [pal_join_area(t) for t in (0.1, 0.01, 0.001)]
    travels = [pal_join_travel(1.0, t) for t in (0.1, 0.01, 0.001)]
    assert areas == sorted(areas, reverse=True)
    assert travels == sorted(travels)
    assert areas[-1] < 0.003 and travels[-1] > 900
    assert pal_join_area(0.02) == pytest.approx(0.02)


def test_sliding_along_your_own_line_is_free():
    # a needle sliding along its own direction sweeps no new area at all:
    # the swept region is the segment it already occupies, area zero
    assert sector_area(0.0) == 0.0

"""Zero size, positive dimension: the measurements behind chapter 7."""

import math
from fractions import Fraction

import numpy as np
import pytest

from kakeya_guide.dimension import (box_count, box_count_2d, box_dimension,
                                    cantor_box_dimension,
                                    cantor_intervals,
                                    cantor_length_and_dimension,
                                    project_to_3d, rotate_4d,
                                    similarity_dimension, sphere_directions,
                                    total_length)


# --- the Cantor set loses all its length ----------------------------------

@pytest.mark.parametrize("m", range(9))
def test_the_middle_thirds_set_keeps_two_thirds_of_its_length_each_round(m):
    length, _ = cantor_length_and_dimension(m)
    assert length == Fraction(2, 3) ** m


def test_the_length_falls_to_nothing():
    assert cantor_length_and_dimension(60)[0] < Fraction(1, 10 ** 10)
    assert total_length(cantor_intervals(4)) == Fraction(16, 81)


def test_the_pieces_multiply_while_the_length_dies():
    for m in range(7):
        assert len(cantor_intervals(m)) == 2 ** m


# --- but it keeps its dimension -------------------------------------------

def test_box_counting_recovers_the_textbook_dimension():
    measured = cantor_box_dimension(2, Fraction(1, 3), levels=9)
    assert measured == pytest.approx(math.log(2) / math.log(3), abs=1e-12)
    assert measured == pytest.approx(0.6309297, abs=1e-6)


@pytest.mark.parametrize("pieces,ratio,expected", [
    (2, Fraction(1, 3), math.log(2) / math.log(3)),
    (2, Fraction(1, 4), 0.5),
    (3, Fraction(1, 5), math.log(3) / math.log(5)),
    (4, Fraction(1, 9), math.log(4) / math.log(9)),
])
def test_measured_dimension_matches_the_similarity_dimension(pieces, ratio,
                                                             expected):
    assert cantor_box_dimension(pieces, ratio, levels=6) == pytest.approx(
        expected, abs=1e-9)
    assert similarity_dimension(pieces, ratio) == pytest.approx(expected)


def test_the_box_counts_are_exactly_what_the_construction_says():
    ivals = cantor_intervals(7)
    for m in range(1, 8):
        assert box_count(ivals, Fraction(1, 3) ** m) == 2 ** m


def test_dimension_zero_and_dimension_one_bracket_it():
    assert 0 < similarity_dimension(2, Fraction(1, 3)) < 1


# --- the point of the chapter: small area, big dimension ------------------

def test_a_set_of_zero_length_can_still_be_more_than_a_dot():
    length, dim = cantor_length_and_dimension(30)
    assert length < Fraction(1, 10 ** 5)      # heading for zero
    assert dim > 0.63                         # and yet nowhere near a dot


def test_a_zero_area_set_in_the_plane_can_have_dimension_over_one():
    """Cantor set x interval: zero area, dimension 1 + log2/log3 = 1.63.

    A Besicovitch set does the same trick harder: zero area, dimension 2.
    """
    xs = cantor_intervals(7)
    ys = [(Fraction(0), Fraction(1))]
    counts = [(Fraction(1, 3) ** m, box_count_2d(xs, ys, Fraction(1, 3) ** m))
              for m in range(1, 8)]
    assert [c for _, c in counts] == [6 ** m for m in range(1, 8)]
    assert box_dimension(counts) == pytest.approx(
        1 + math.log(2) / math.log(3), abs=1e-9)
    # area = length(x) * length(y) -> 0
    assert total_length(xs) * 1 == Fraction(2, 3) ** 7


# --- directions in n dimensions, and looking at four of them ---------------

@pytest.mark.parametrize("n", [2, 3, 4, 5, 6, 10])
def test_sphere_directions_are_unit_vectors_in_any_dimension(n):
    v = sphere_directions(n, 200)
    assert v.shape == (200, n)
    assert np.allclose(np.linalg.norm(v, axis=1), 1.0)
    assert (v[:, -1] >= 0).all()          # one representative per direction


def test_the_four_dimensional_turn_really_is_a_rotation():
    v = sphere_directions(4, 300)
    for angle in (0.0, 0.4, 1.7, math.pi, 5.9):
        turned = rotate_4d(v, angle)
        assert np.allclose(np.linalg.norm(turned, axis=1), 1.0)
        # angles between vectors are preserved, which is what "rotation" means
        assert np.allclose(turned @ turned.T, v @ v.T, atol=1e-9)


def test_the_four_dimensional_turn_is_visible_after_projecting():
    """The chapter 8 figure claims you can see the fourth axis.  Check it.

    If the projected picture were the same shape at every angle, the animation
    would be showing a 3D rotation wearing a 4D costume.  It is not: the
    projected lengths genuinely change.
    """
    v = sphere_directions(4, 300)
    spans = []
    for i in range(12):
        p = project_to_3d(rotate_4d(v, 2 * math.pi * i / 12))
        spans.append(np.linalg.norm(p, axis=1).mean())
    assert max(spans) - min(spans) > 0.02


def test_projection_is_the_usual_perspective_one():
    flat = np.array([[1.0, 0.0, 0.0, 0.0]])
    assert np.allclose(project_to_3d(flat), [[1.0, 0.0, 0.0]])
    near = np.array([[1.0, 0.0, 0.0, 1.0]])       # closer in w: drawn bigger
    assert project_to_3d(near)[0, 0] > 1.0


def test_two_cantor_sets_multiply_their_dimensions_by_addition():
    xs = ys = cantor_intervals(7)
    counts = [(Fraction(1, 3) ** m, box_count_2d(xs, ys, Fraction(1, 3) ** m))
              for m in range(1, 8)]
    assert box_dimension(counts) == pytest.approx(
        2 * math.log(2) / math.log(3), abs=1e-9)

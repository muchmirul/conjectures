"""Kakeya on the grid, and Dvir's proof run step by step (chapter 10).

Each test below is one link of the 2008 argument.  Together they are the proof
that a Kakeya set in F_q^n cannot have fewer than C(q+n-1, n) points, carried
out in exact arithmetic on small grids.
"""

import itertools
import random

import pytest

from kakeya_guide.examples import GRID_SIZES, blokhuis_mazzocca
from kakeya_guide.finite import (directions, dvir_bound, dvir_report,
                                 evaluation_rank, greedy_kakeya_size, grid,
                                 is_kakeya, line, lines_in_direction,
                                 min_kakeya_size, missing_directions,
                                 monomials, poly_degree, poly_eval,
                                 restrict_to_line, tangent_line_kakeya,
                                 top_part, vanishing_polynomial)


# --- the grid and its lines ------------------------------------------------

@pytest.mark.parametrize("q", GRID_SIZES)
def test_the_plane_grid_has_q_plus_one_directions(q):
    assert len(directions(q, 2)) == q + 1
    assert len(grid(q, 2)) == q * q


@pytest.mark.parametrize("q,n", [(2, 3), (3, 3), (5, 3), (3, 4)])
def test_direction_count_in_higher_dimensions(q, n):
    assert len(directions(q, n)) == (q ** n - 1) // (q - 1)


@pytest.mark.parametrize("q", GRID_SIZES)
def test_a_line_has_q_points_and_lives_in_a_parallel_family(q):
    for b in directions(q, 2):
        fam = lines_in_direction(b, q, 2)
        assert len(fam) == q                       # q parallel lines
        assert all(len(L) == q for L in fam)
        assert set().union(*fam) == set(grid(q, 2))   # they tile the grid


# --- how small a Kakeya set can be ----------------------------------------

@pytest.mark.parametrize("q", GRID_SIZES)
def test_the_tangent_line_construction_is_a_kakeya_set(q):
    K = tangent_line_kakeya(q)
    assert is_kakeya(K, q, 2)
    assert missing_directions(K, q, 2) == []


@pytest.mark.parametrize("q", GRID_SIZES)
def test_brute_force_matches_blokhuis_and_mazzocca(q):
    assert min_kakeya_size(q, 2) == blokhuis_mazzocca(q)
    assert len(tangent_line_kakeya(q)) == blokhuis_mazzocca(q)


@pytest.mark.parametrize("q", GRID_SIZES)
def test_the_smallest_set_found_really_is_kakeya(q):
    size, K = min_kakeya_size(q, 2, return_set=True)
    assert len(K) == size
    assert is_kakeya(K, q, 2)


@pytest.mark.parametrize("q", GRID_SIZES)
def test_dvirs_bound_holds_and_is_nearly_tight(q):
    assert dvir_bound(q, 2) == q * (q + 1) // 2
    assert min_kakeya_size(q, 2) >= dvir_bound(q, 2)
    # off by (q-1)/2 for odd q, exactly right for even q
    assert min_kakeya_size(q, 2) - dvir_bound(q, 2) == (q - 1) // 2 * (q % 2)


def test_a_kakeya_set_is_a_vanishing_fraction_of_the_big_grid():
    # half the plane, but only a q^(1-n) sliver of higher dimensional grids
    assert min_kakeya_size(2, 3) >= dvir_bound(2, 3)
    assert greedy_kakeya_size(5, 3) < 5 ** 3 / 2


# --- step 1: a small set always has a low-degree polynomial through it ------

@pytest.mark.parametrize("q,n", [(3, 2), (5, 2), (3, 3)])
def test_any_set_below_the_bound_carries_a_vanishing_polynomial(q, n):
    rng = random.Random(2008)
    pts = grid(q, n)
    for _ in range(5):
        S = rng.sample(pts, dvir_bound(q, n) - 1)
        g = vanishing_polynomial(S, q, n, q - 1)
        assert g, "a nonzero polynomial must exist"
        assert poly_degree(g) <= q - 1
        assert all(poly_eval(g, p, q) == 0 for p in S)


def test_the_count_that_makes_step_one_work():
    for q, n in [(2, 2), (3, 2), (5, 2), (3, 3), (5, 3)]:
        assert len(monomials(n, q - 1)) == dvir_bound(q, n)


# --- step 2: a line inside the set kills the top part in its direction -----

@pytest.mark.parametrize("q,n", [(3, 2), (5, 2), (3, 3)])
def test_vanishing_on_a_whole_line_zeroes_the_restriction(q, n):
    rng = random.Random(1999)
    for _ in range(5):
        b = rng.choice(directions(q, n))
        a = rng.choice(grid(q, n))
        L = sorted(line(a, b, q))
        g = vanishing_polynomial(L, q, n, q - 1)
        assert g
        # q points, degree < q: the restriction is not just zero at q places,
        # it is the zero polynomial
        assert all(c == 0 for c in restrict_to_line(g, a, b, q))


@pytest.mark.parametrize("q,n", [(3, 2), (5, 2), (3, 3)])
def test_the_top_coefficient_along_a_line_is_the_top_part_at_the_direction(q, n):
    rng = random.Random(7)
    for _ in range(20):
        g = {m: rng.randrange(q) for m in monomials(n, q - 1)}
        if poly_degree(g) < 0:
            continue
        d = poly_degree(g)
        a, b = rng.choice(grid(q, n)), rng.choice(directions(q, n))
        coeffs = restrict_to_line(g, a, b, q)
        got = coeffs[d] if len(coeffs) > d else 0
        assert got == poly_eval(top_part(g), b, q)


# --- step 3: nothing of low degree vanishes on the whole grid --------------

@pytest.mark.parametrize("q,n", [(2, 2), (3, 2), (5, 2), (2, 3), (3, 3)])
def test_no_low_degree_polynomial_vanishes_everywhere(q, n):
    assert evaluation_rank(q, n, q - 1) == dvir_bound(q, n)
    assert vanishing_polynomial(grid(q, n), q, n, q - 1) is None


# --- the three steps together ----------------------------------------------

@pytest.mark.parametrize("q", (3, 5))
def test_a_real_kakeya_set_is_too_big_for_step_one(q):
    r = dvir_report(tangent_line_kakeya(q), q, 2)
    assert r["kakeya"]
    assert not r["too_small"]          # exactly what the theorem promises
    assert not r["contradiction"]


@pytest.mark.parametrize("q", (3, 5))
def test_sets_below_the_bound_always_miss_a_direction(q):
    """The theorem, checked the brute way: nothing smaller than the bound can
    hold every direction, so the polynomial argument never has to be believed
    on trust."""
    budget = dvir_bound(q, 2) - 1
    dirs = directions(q, 2)
    reachable = 0
    for how_many in range(len(dirs), 0, -1):
        for subset in itertools.combinations(dirs, how_many):
            best = _cheapest_cover(subset, q)
            if best <= budget:
                reachable = max(reachable, how_many)
                break
        if reachable:
            break
    assert reachable < len(dirs)


def _cheapest_cover(dirs, q):
    """Fewest points covering one line in each of these directions."""
    pts = grid(q, 2)
    idx = {p: i for i, p in enumerate(pts)}
    best = 10 ** 9

    def walk(i, mask):
        nonlocal best
        size = mask.bit_count()
        if size >= best:
            return
        if i == len(dirs):
            best = size
            return
        for L in lines_in_direction(dirs[i], q, 2):
            m = mask
            for p in L:
                m |= 1 << idx[p]
            walk(i + 1, m)

    walk(0, 0)
    return best

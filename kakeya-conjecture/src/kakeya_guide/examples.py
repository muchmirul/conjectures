"""The named objects the guide keeps coming back to.

    from kakeya_guide.examples import THE_TRIANGLE, FAN, tree, TIMELINE

Nothing here is decorative: every constant is used by a figure script in
src/viz/ and pinned by a test in tests/.
"""

from __future__ import annotations

from fractions import Fraction

from .core import (elementary_slivers, perron_tree, ramped_alphas, sliver,
                   union_area)

# --- the triangle everything is cut from -----------------------------------

#: Base [0, 1] on the ground, apex at (1/2, 1).  Height 1 is not a detail: a
#: segment leaving the apex reaches the ground after at least one unit of
#: travel, so a *unit* needle fits inside in every direction the triangle
#: holds.  Area 1/2.
THE_TRIANGLE = sliver(0, 1, Fraction(1, 2), 1)

#: The directions it holds, measured as sideways run per unit of drop:
#: everything from -1/2 to 1/2, a fan of 2*arctan(1/2) = 53.13 degrees.
FAN = THE_TRIANGLE.direction_interval()

#: The steady squeeze: overlap every pair of neighbours to two thirds.
#: Simple, and it stalls (see PERRON_STALL_LIMIT).
STEADY_ALPHA = Fraction(2, 3)

#: With the steady squeeze the exact area of the order-k tree is
#: 1/6 + 1/(3 * 2**k), so no matter how many slivers you cut, a third of the
#: triangle survives.  This is the wall that a varying squeeze walks through.
PERRON_STALL_LIMIT = Fraction(1, 6)


def steady_area(k: int) -> Fraction:
    """The closed form for the steady-squeeze tree of order k."""
    return PERRON_STALL_LIMIT + Fraction(1, 3 * 2 ** k)


def tree(k: int, steady: bool = False):
    """The guide's Perron tree of order k (ramped squeeze unless told otherwise)."""
    return perron_tree(k, STEADY_ALPHA if steady else ramped_alphas(k))


def slivers(k: int):
    """The 2**k elementary slivers, before anything is slid."""
    return elementary_slivers(k, (0, 1), Fraction(1, 2), 1)


#: Exact areas of the ramped trees, small orders.  Past order 4 the exact
#: value is still a rational, but one with a hundred digits underneath, so the
#: guide quotes decimals from RAMPED_AREAS_DECIMAL instead.
#: tests/test_core.py recomputes both from scratch rather than trusting this.
RAMPED_AREAS = {
    0: Fraction(1, 2),
    1: Fraction(15, 32),
    2: Fraction(629, 1600),
    3: Fraction(3029, 9600),
    4: Fraction(13133, 53760),
}

#: The same areas as decimals, orders 0 to 9, each the exact value rounded.
RAMPED_AREAS_DECIMAL = {
    0: 0.500000, 1: 0.468750, 2: 0.393125, 3: 0.315521, 4: 0.244289,
    5: 0.197952, 6: 0.166697, 7: 0.145032, 8: 0.129469, 9: 0.118088,
}


def area(figure) -> Fraction:
    return union_area(figure)


# --- the finite grid --------------------------------------------------------

#: Primes small enough to search exhaustively in the plane.
GRID_SIZES = (2, 3, 5, 7)

#: Blokhuis and Mazzocca's exact answer for the plane: the smallest Kakeya set
#: in F_q^2 has this many points.  min_kakeya_size() recomputes it by brute
#: force for the sizes above.
def blokhuis_mazzocca(q: int) -> int:
    return q * (q + 1) // 2 + ((q - 1) // 2 if q % 2 else 0)


# --- what happened, and when ------------------------------------------------

#: (year, who, what) for the history figure in chapter 11.  Sources and page
#: references live in notes/research-content.md.
TIMELINE = [
    (1917, "Kakeya", "asks for the smallest room a needle can turn in"),
    (1919, "Besicovitch", "builds a set of area zero holding every direction"),
    (1921, "Pal", "smallest convex room: the triangle of height 1"),
    (1928, "Besicovitch", "turns the needle in a room of any size you name"),
    (1928, "Perron", "the tree: a short proof anyone can draw"),
    (1971, "Davies", "in the plane, area zero still means dimension 2"),
    (1971, "Cunningham", "arbitrarily small rooms with no holes, inside a disc"),
    (1991, "Bourgain", "dimension beats (n+1)/2, the modern assault begins"),
    (1995, "Wolff", "the hairbrush: dimension at least (n+2)/2, so 5/2 in 3D"),
    (1999, "Wolff", "poses the finite field version"),
    (2008, "Dvir", "finite fields fall to the polynomial method, in half a page"),
    (2019, "Katz-Zahl", "3D nudged past 5/2, by a ten-billionth"),
    (2025, "Wang-Zahl", "every Kakeya set in 3D has dimension 3"),
]

#: Where the conjecture stands as this guide is written (July 2026).
STATUS = {
    1: "trivial: a segment is one-dimensional",
    2: "proved by Davies in 1971",
    3: "proved by Wang and Zahl, February 2025",
    4: "open",
    5: "open",
}

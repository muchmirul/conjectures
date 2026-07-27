"""The classical needle-turning rooms: the disc, the triangle, the deltoid.

These are the shapes people tried before Besicovitch, together with the actual
motion of the needle inside each one, so the animations show a real turn and
not a suggestive cartoon.  Areas here are floating point on purpose: they
involve pi and sqrt(3).  The exact rational machinery lives in `core`.
"""

from __future__ import annotations

import math

Point = tuple[float, float]

# --- the three rooms, and how big they are --------------------------------

#: A disc of diameter 1: spin the needle about its middle.  Area pi/4.
DISC_AREA = math.pi / 4

#: The equilateral triangle of height 1, the smallest *convex* room there is
#: (Pal, 1921).  Area 1/sqrt(3).
TRIANGLE_AREA = 1 / math.sqrt(3)

#: The deltoid whose tangent chord has length 1, Kakeya's own guess at the
#: answer.  Area pi/8, half of the triangle.
DELTOID_AREA = math.pi / 8

#: Radius of the small rolling circle that traces that deltoid.
DELTOID_A = 0.25


def disc(radius: float = 0.5, n: int = 240) -> list[Point]:
    return [(radius * math.cos(2 * math.pi * i / n),
             radius * math.sin(2 * math.pi * i / n)) for i in range(n)]


def equilateral(height: float = 1.0) -> list[Point]:
    """The equilateral triangle of the given height, centred on the origin."""
    half = height / math.sqrt(3)
    cy = height / 3
    return [(-half, -cy), (half, -cy), (0.0, height - cy)]


def polygon_area(pts: list[Point]) -> float:
    """Shoelace area of a simple polygon."""
    s = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        s += x0 * y1 - x1 * y0
    return abs(s) / 2


# --- the deltoid, and the needle that slides inside it --------------------

def deltoid_point(t: float, a: float = DELTOID_A) -> Point:
    """The 3-cusped hypocycloid traced by a circle of radius a rolling inside
    a circle of radius 3a."""
    return (2 * a * math.cos(t) + a * math.cos(2 * t),
            2 * a * math.sin(t) - a * math.sin(2 * t))


def deltoid(a: float = DELTOID_A, n: int = 480) -> list[Point]:
    return [deltoid_point(2 * math.pi * i / n, a) for i in range(n)]


def deltoid_tangent_chord(t: float, a: float = DELTOID_A) -> tuple[Point, Point]:
    """The needle: the tangent line at parameter t, cut off by the curve.

    Its ends sit at parameters -t/2 and pi - t/2, and it is 4a long no matter
    where you are on the curve, which is exactly why a deltoid with a = 1/4
    turns a unit needle.  As t runs once round the curve the needle turns
    through a half circle, which is a full turn for a needle.
    """
    return (deltoid_point(-t / 2, a), deltoid_point(math.pi - t / 2, a))


def deltoid_needle(t: float, a: float = DELTOID_A) -> tuple[Point, float]:
    """The needle inside the deltoid as (midpoint, angle) at time t."""
    (x0, y0), (x1, y1) = deltoid_tangent_chord(t, a)
    return ((x0 + x1) / 2, (y0 + y1) / 2), math.atan2(y1 - y0, x1 - x0)


def equilateral_turn(t: float, height: float = 1.0) -> tuple[Point, Point]:
    """Pal's turn: the needle really does rotate inside the triangle.

    Three pivots about the three corners, 60 degrees each, joined by three
    slides along the sides.  Sliding a needle along its own line sweeps no new
    area, so the whole half turn happens inside the triangle.  t runs from 0
    to 1 for one full cycle, at the end of which the needle is where it
    started, reversed: a needle's full turn.
    """
    v = equilateral(height)
    side = 2 * height / math.sqrt(3)
    run = side - 1.0                       # how far to slide after each pivot
    pivot_share = 0.75 / 3                 # of the cycle, per pivot
    slide_share = 0.25 / 3
    corners = [(0, 1, 2), (2, 0, 1), (1, 2, 0)]   # pivot at a, from b, to c
    t = t % 1.0
    for a, b, c in corners:
        A, B, C = v[a], v[b], v[c]
        if t < pivot_share:
            u = t / pivot_share
            ab = math.atan2(B[1] - A[1], B[0] - A[0])
            ac = math.atan2(C[1] - A[1], C[0] - A[0])
            d = (ac - ab + math.pi) % (2 * math.pi) - math.pi
            ang = ab + d * u
            return A, (A[0] + math.cos(ang), A[1] + math.sin(ang))
        t -= pivot_share
        if t < slide_share:
            u = t / slide_share
            dx = (C[0] - A[0]) / side, (C[1] - A[1]) / side
            s = run * u
            return ((A[0] + dx[0] * s, A[1] + dx[1] * s),
                    (A[0] + dx[0] * (s + 1), A[1] + dx[1] * (s + 1)))
        t -= slide_share
    return v[0], (v[0][0] + 1, v[0][1])


# --- chords of a convex polygon, for placing a needle at a given angle ----

def clip_chord(poly: list[Point], through: Point, angle: float
               ) -> tuple[Point, Point] | None:
    """The line through a point at a given angle, cut down to the polygon."""
    dx, dy = math.cos(angle), math.sin(angle)
    lo, hi = -1e9, 1e9
    px, py = through
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        ex, ey = x1 - x0, y1 - y0
        nx, ny = ey, -ex                    # inward or outward normal
        denom = nx * dx + ny * dy
        num = nx * (px - x0) + ny * (py - y0)
        if abs(denom) < 1e-15:
            if num > 1e-12:
                return None                 # parallel and outside this edge
            continue
        s = -num / denom
        if denom > 0:
            hi = min(hi, s)
        else:
            lo = max(lo, s)
    if hi < lo:
        return None
    return ((px + lo * dx, py + lo * dy), (px + hi * dx, py + hi * dy))


def longest_chord(poly: list[Point], angle: float) -> tuple[Point, Point]:
    """The longest chord of a convex polygon in a given direction.

    For a convex polygon it always runs through a vertex, so checking the
    vertices is enough.
    """
    best, best_len = None, -1.0
    for v in poly:
        seg = clip_chord(poly, v, angle)
        if seg is None:
            continue
        length = math.dist(*seg)
        if length > best_len:
            best, best_len = seg, length
    return best


def needle_in_polygon(poly: list[Point], angle: float, length: float = 1.0
                      ) -> tuple[Point, Point] | None:
    """A unit needle at the given angle inside the polygon, or None if it will
    not fit.  Centred on the polygon's longest chord in that direction."""
    seg = longest_chord(poly, angle)
    if seg is None or math.dist(*seg) < length - 1e-12:
        return None
    (x0, y0), (x1, y1) = seg
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = math.cos(angle) * length / 2, math.sin(angle) * length / 2
    return ((cx - dx, cy - dy), (cx + dx, cy + dy))


def fits_every_direction(poly: list[Point], length: float = 1.0,
                         samples: int = 360) -> bool:
    """Does a needle of this length fit inside the shape at every angle?"""
    return all(needle_in_polygon(poly, math.pi * i / samples, length)
               for i in range(samples))


# --- sliding and turning: what a motion costs -----------------------------

def sector_area(angle: float, length: float = 1.0) -> float:
    """Area swept by pivoting a needle about one end through `angle`."""
    return abs(angle) * length ** 2 / 2


def pal_join_area(theta: float, length: float = 1.0) -> float:
    """Cost of Pal's trick for moving a needle onto a parallel line.

    Slide out along the needle's own line (free), pivot through theta, slide
    along the slanted line (free), pivot back through theta.  Two pivots, so
    the area is theta * length^2, as small as you like, and the price is the
    distance travelled: `pal_join_travel`.
    """
    return 2 * sector_area(theta, length)


def pal_join_travel(gap: float, theta: float) -> float:
    """How far the needle must wander to make that join, for a given gap."""
    return gap / math.tan(theta)

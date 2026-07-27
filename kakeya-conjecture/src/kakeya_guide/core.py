"""Exact geometry for Kakeya's needle problem: slivers, unions, Perron trees.

Every figure in this guide is built from **slivers**: triangles standing on the
x-axis, all with the same height.  That one restriction is what makes exact
area computation cheap.  At height y a sliver cuts out a single interval whose
two endpoints move *linearly* in y, so the total width covered at height y is a
piecewise-linear function of y, and the area is the exact integral of it.

    from fractions import Fraction
    from kakeya_guide.core import sliver, union_area

    T = sliver(0, 1, Fraction(1, 2))        # base [0,1], apex (1/2, 1)
    union_area([T])                          # -> Fraction(1, 2)

Everything here runs in exact rational arithmetic, so the shrinking areas the
guide quotes are not rounded estimates: they are the numbers themselves.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence


def F(x) -> Fraction:
    """Coerce to an exact Fraction (ints, Fractions, and 'p/q' strings)."""
    return x if isinstance(x, Fraction) else Fraction(x)


# ---------------------------------------------------------------------------
# Slivers
# ---------------------------------------------------------------------------

@dataclass(frozen=True, order=True)
class Sliver:
    """A triangle with base [b0, b1] on the x-axis and apex at (ax, h)."""

    b0: Fraction
    b1: Fraction
    ax: Fraction
    h: Fraction

    @property
    def area(self) -> Fraction:
        return (self.b1 - self.b0) * self.h / 2

    @property
    def apex(self) -> tuple[Fraction, Fraction]:
        return (self.ax, self.h)

    def translate(self, dx) -> "Sliver":
        dx = F(dx)
        return Sliver(self.b0 + dx, self.b1 + dx, self.ax + dx, self.h)

    def interval(self, y) -> tuple[Fraction, Fraction]:
        """The horizontal slice of the sliver at height y."""
        y = F(y)
        t = y / self.h
        return (self.b0 + (self.ax - self.b0) * t,
                self.b1 + (self.ax - self.b1) * t)

    def direction_interval(self) -> tuple[Fraction, Fraction]:
        """Which directions the sliver holds, as 'sideways run per unit drop'.

        A segment from the apex down to the base point (x, 0) has direction
        vector (x - ax, -h), i.e. run (x - ax)/h per unit of drop.  Slopes,
        not angles, keep this exact.
        """
        return ((self.b0 - self.ax) / self.h, (self.b1 - self.ax) / self.h)

    def polygon(self) -> list[tuple[Fraction, Fraction]]:
        return [(self.b0, F(0)), (self.b1, F(0)), (self.ax, self.h)]

    def shape(self) -> tuple[Fraction, Fraction]:
        """Width and apex offset: what a translation cannot change."""
        return (self.b1 - self.b0, self.ax - self.b0)


def sliver(b0, b1, ax, h=1) -> Sliver:
    """Build a Sliver, coercing every coordinate to an exact Fraction."""
    b0, b1, ax, h = F(b0), F(b1), F(ax), F(h)
    if b1 <= b0:
        raise ValueError(f"empty base [{b0}, {b1}]")
    if h <= 0:
        raise ValueError(f"height must be positive, got {h}")
    return Sliver(b0, b1, ax, h)


def is_translate(s: Sliver, t: Sliver) -> bool:
    """True if s and t are the same triangle up to a horizontal shift."""
    return s.h == t.h and s.shape() == t.shape()


# ---------------------------------------------------------------------------
# Exact area of a union of slivers
# ---------------------------------------------------------------------------

def union_length(intervals: Iterable[tuple[Fraction, Fraction]]) -> Fraction:
    """Total length of a union of intervals: overlap is counted once."""
    total = F(0)
    cur_l = cur_r = None
    for l, r in sorted(intervals):
        if cur_r is None or l > cur_r:
            if cur_r is not None:
                total += cur_r - cur_l
            cur_l, cur_r = l, r
        elif r > cur_r:
            cur_r = r
    if cur_r is not None:
        total += cur_r - cur_l
    return total


def width_at(slivers: Sequence[Sliver], y) -> Fraction:
    """Exact total width the figure covers at height y (overlap counted once)."""
    y = F(y)
    return union_length(s.interval(y) for s in slivers
                        if F(0) <= y <= s.h)


def _endpoint_lines(slivers: Sequence[Sliver]):
    """Each sliver as two moving endpoints x(y) = x0 + slope * y."""
    x0, slope, kind = [], [], []
    for s in slivers:
        x0.append(s.b0)
        slope.append((s.ax - s.b0) / s.h)
        kind.append(1)          # a left edge opens the interval
        x0.append(s.b1)
        slope.append((s.ax - s.b1) / s.h)
        kind.append(-1)         # a right edge closes it
    return x0, slope, kind


def union_area(slivers: Sequence[Sliver]) -> Fraction:
    """The exact area of the union of slivers of equal height.

    Sweeps upward, keeping the endpoints sorted.  Between two consecutive
    crossings of endpoints the covered width is a straight line in y, so the
    area of that horizontal slab is an exact trapezoid.  Cost is one step per
    crossing, which is what makes trees of hundreds of slivers computable in
    exact arithmetic.
    """
    slivers = [s for s in slivers if s.b1 > s.b0]
    if not slivers:
        return F(0)
    h = slivers[0].h
    if any(s.h != h for s in slivers):
        raise ValueError("union_area needs slivers of equal height")
    return _sweep(*_endpoint_lines(slivers), h, F(0))


def union_area_numeric(slivers: Sequence[Sliver], samples: int = 2049) -> float:
    """A quick numerical estimate of the same area: for searching, not quoting.

    Slices the figure at `samples` heights, merges the intervals at each one
    and integrates.  Deliberately not the exact sweep: the sweep leans on
    exact ties (heaps of endpoints in these trees cross at the very same
    height), and in floating point those ties decay into nonsense.  Anything
    this guide states out loud is recomputed with `union_area`.
    """
    import numpy as np

    slivers = [s for s in slivers if s.b1 > s.b0]
    if not slivers:
        return 0.0
    h = float(slivers[0].h)
    b0 = np.array([float(s.b0) for s in slivers])
    b1 = np.array([float(s.b1) for s in slivers])
    ax = np.array([float(s.ax) for s in slivers])
    ys = np.linspace(0.0, h, samples)
    t = (ys / h)[:, None]
    left = b0[None, :] + (ax - b0)[None, :] * t
    right = b1[None, :] + (ax - b1)[None, :] * t
    order = np.argsort(left, axis=1)
    left = np.take_along_axis(left, order, axis=1)
    right = np.take_along_axis(right, order, axis=1)
    reach = np.maximum.accumulate(right, axis=1)
    before = np.concatenate(
        [np.full((len(ys), 1), -np.inf), reach[:, :-1]], axis=1)
    fresh = np.clip(right - np.maximum(left, before), 0.0, None)
    return float(np.trapezoid(fresh.sum(axis=1), ys))


def _sweep(x0, slope, kind, h, zero):
    """Kinetic sweep shared by the exact and floating-point area routines."""
    m = len(x0)
    order = sorted(range(m), key=lambda i: (x0[i], slope[i]))
    pos = [0] * m
    for j, i in enumerate(order):
        pos[i] = j

    # depth[j] = how many slivers cover the gap between order[j], order[j+1]
    depth, d = [0] * (m - 1), 0
    for j in range(m - 1):
        d += kind[order[j]]
        depth[j] = d

    def gap(j):
        """Gap j's contribution to width(y) = A + B*y, or zero if uncovered."""
        if depth[j] <= 0:
            return (zero, zero)
        a, b = order[j], order[j + 1]
        return (x0[b] - x0[a], slope[b] - slope[a])

    A = B = zero
    for j in range(m - 1):
        dA, dB = gap(j)
        A += dA
        B += dB

    y = zero
    area = zero
    heap: list = []

    def schedule(j):
        """Queue the moment the two endpoints bounding gap j swap over."""
        a, b = order[j], order[j + 1]
        if slope[a] > slope[b]:                       # they must converge
            t = (x0[b] - x0[a]) / (slope[a] - slope[b])
            if y <= t <= h:
                heapq.heappush(heap, (t, a, b))

    for j in range(m - 1):
        schedule(j)

    while heap:
        t, a, b = heapq.heappop(heap)
        j = pos[a]
        if j + 1 >= m or order[j + 1] != b:
            continue                                   # stale: they parted ways
        if t > y:
            area += A * (t - y) + B * (t * t - y * y) / 2
            y = t
        touched = [g for g in (j - 1, j, j + 1) if 0 <= g < m - 1]
        for g in touched:
            dA, dB = gap(g)
            A -= dA
            B -= dB
        order[j], order[j + 1] = b, a
        pos[b], pos[a] = j, j + 1
        depth[j] = (depth[j - 1] if j > 0 else 0) + kind[b]
        for g in touched:
            dA, dB = gap(g)
            A += dA
            B += dB
        if j - 1 >= 0:
            schedule(j - 1)
        if j + 1 <= m - 2:
            schedule(j + 1)

    area += A * (h - y) + B * (h * h - y * y) / 2
    return area


def union_area_reference(slivers: Sequence[Sliver]) -> Fraction:
    """The same area, computed the slow obvious way (used to check the fast one).

    Collects every height where two endpoints cross, then adds up exact
    trapezoids between consecutive heights.  O(n^2) heights, each costing a
    full re-scan, so this is only usable on small figures, which is exactly
    what a reference implementation is for.
    """
    slivers = [s for s in slivers if s.b1 > s.b0]
    if not slivers:
        return F(0)
    h = slivers[0].h
    x0, slope, _ = _endpoint_lines(slivers)
    cuts = {F(0), h}
    for i in range(len(x0)):
        for j in range(i + 1, len(x0)):
            if slope[i] != slope[j]:
                t = (x0[j] - x0[i]) / (slope[i] - slope[j])
                if 0 < t < h:
                    cuts.add(t)
    ys = sorted(cuts)
    area = F(0)
    prev_w = width_at(slivers, ys[0])
    for y0, y1 in zip(ys, ys[1:]):
        w1 = width_at(slivers, y1)
        area += (y1 - y0) * (prev_w + w1) / 2
        prev_w = w1
    return area


# ---------------------------------------------------------------------------
# Perron trees
# ---------------------------------------------------------------------------

def elementary_slivers(k: int, base=(0, 1), apex_x=None, h=1) -> list[Sliver]:
    """Cut a triangle's base into 2**k equal pieces: 2**k slivers, one apex.

    Sliver i keeps exactly the directions pointing from the apex into its own
    piece of the base, so together they hold every direction of the triangle,
    and each one keeps holding them wherever you slide it.
    """
    b_lo, b_hi = F(base[0]), F(base[1])
    apex_x = (b_lo + b_hi) / 2 if apex_x is None else F(apex_x)
    n = 2 ** k
    w = (b_hi - b_lo) / n
    return [sliver(b_lo + i * w, b_lo + (i + 1) * w, apex_x, h) for i in range(n)]


def perron_tree(k: int, alpha=Fraction(2, 3), base=(0, 1), apex_x=None,
                h=1) -> list[Sliver]:
    """Perron's tree: cut a triangle into 2**k slivers and slide them together.

    Stage by stage, neighbouring bunches of slivers are pushed into each other
    until each pair overlaps in a copy of itself scaled by `alpha`.  Nothing is
    ever rotated, so the pile still holds a segment in every direction of the
    original triangle, while its area keeps dropping (see `perron_areas`).

    alpha = 2/3 minimises the area of the very first merge (see the closed form
    in tests/test_core.py); alpha closer to 1 wastes less at the deep stages,
    so `alpha` may also be a list with one value per stage.
    """
    alphas = [F(alpha)] * k if not isinstance(alpha, (list, tuple)) else \
        [F(a) for a in alpha]
    if len(alphas) < k:
        raise ValueError(f"need {k} alphas, got {len(alphas)}")
    if any(not 0 < a < 1 for a in alphas):
        raise ValueError("every alpha must lie strictly between 0 and 1")
    b_lo, b_hi = F(base[0]), F(base[1])
    groups = [[s] for s in elementary_slivers(k, (b_lo, b_hi), apex_x, h)]
    width = (b_hi - b_lo) / 2 ** k          # base width of one group's triangle
    for stage in range(k):
        shift = 2 * width * (1 - alphas[stage])   # push the right bunch left
        merged = []
        for left, right in zip(groups[0::2], groups[1::2]):
            merged.append(left + [s.translate(-shift) for s in right])
        groups = merged
        width *= 2
    return [s for g in groups for s in g]


def perron_stages(k: int, alpha=Fraction(2, 3), base=(0, 1), apex_x=None,
                  h=1) -> list[list[Sliver]]:
    """Every intermediate figure: the cut pieces, then one list per merge.

    Stage 0 is the untouched triangle in 2**k pieces and stage k is the
    finished tree, with the slivers in the same order throughout so an
    animation can slide each one from where it was to where it goes.
    """
    alphas = [F(alpha)] * k if not isinstance(alpha, (list, tuple)) else \
        [F(a) for a in alpha]
    b_lo, b_hi = F(base[0]), F(base[1])
    groups = [[s] for s in elementary_slivers(k, (b_lo, b_hi), apex_x, h)]
    stages = [[s for g in groups for s in g]]
    width = (b_hi - b_lo) / 2 ** k
    for stage in range(k):
        shift = 2 * width * (1 - alphas[stage])
        groups = [left + [s.translate(-shift) for s in right]
                  for left, right in zip(groups[0::2], groups[1::2])]
        stages.append([s for g in groups for s in g])
        width *= 2
    return stages


def ramped_alphas(k: int, c=Fraction(3), s: int = 4) -> list[Fraction]:
    """A squeeze that varies with scale: alpha_j = 1 - c/(j+s).

    A single alpha stalls: the tree's area falls to 1/6 + 1/(3*2^k) and stops
    (see tests/test_core.py).  Squeezing hard where the slivers are thin and
    gently where they are fat keeps it falling, which is the whole point of
    Besicovitch's theorem.  These constants come from the scan in
    notes/research-perron.md, not from theory.

    With the defaults this is just alpha_j = (j+1)/(j+4): a quarter at the
    finest stage, then 2/5, 1/2, 4/7, ... easing towards 1 as the pieces being
    merged get fat.
    """
    c = F(c)
    return [max(Fraction(1, 8), min(Fraction(19, 20), 1 - c / (j + s)))
            for j in range(k)]


def perron_areas(k_max: int, alpha=Fraction(2, 3), **kw) -> list[Fraction]:
    """Exact areas of the Perron trees of order 0, 1, ..., k_max."""
    return [union_area(perron_tree(k, alpha, **kw)) for k in range(k_max + 1)]


def best_alpha(k: int, candidates: Sequence[Fraction] | None = None,
               **kw) -> tuple[Fraction, Fraction]:
    """The (alpha, area) pair with the smallest area at order k.

    Scans numerically, then recomputes the winner exactly.
    """
    if candidates is None:
        candidates = [Fraction(i, 48) for i in range(24, 48)]
    best = min(candidates,
               key=lambda a: union_area_numeric(perron_tree(k, a, **kw)))
    return best, union_area(perron_tree(k, best, **kw))


def direction_cover(slivers: Sequence[Sliver]) -> list[tuple[Fraction, Fraction]]:
    """Merge the direction intervals of the slivers into maximal runs.

    A figure holds a unit segment in every direction listed here, provided the
    slivers are one unit tall: a segment leaving the apex at run r per unit
    drop reaches the base after sqrt(1 + r^2) >= 1 of travel, so a whole unit
    of it fits inside the sliver.
    """
    merged: list[list[Fraction]] = []
    for lo, hi in sorted(s.direction_interval() for s in slivers):
        if merged and lo <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    return [(lo, hi) for lo, hi in merged]


def holds_every_direction(slivers: Sequence[Sliver], lo, hi) -> bool:
    """True if the figure holds a segment in every direction from lo to hi."""
    cover = direction_cover(slivers)
    return any(c_lo <= F(lo) and F(hi) <= c_hi for c_lo, c_hi in cover)


def extrusion_holds_direction(slivers: Sequence[Sliver], d, half_height=1) -> bool:
    """Does the figure, pushed out sideways into space, hold this direction?

    Take a flat figure in the xy plane and extrude it along z, from -half_height
    to +half_height.  A unit segment of space pointing along d = (a, b, c) has a
    shadow in the xy plane of length sqrt(a^2 + b^2) <= 1, pointing the flat way
    (a, b), and rises by |c| <= 1.  So the solid holds that direction whenever
    the flat figure holds the shadow's direction and the slab is thick enough:
    a shorter shadow fits inside the unit segment the figure already holds.

    Straight up (a = b = 0) needs only thickness, since the figure is not empty.
    Flat directions (b = 0, a nonzero) are the ones a triangle's fan never
    covers, which is why the plane needs several rotated copies and space
    needs the same.

    d is any nonzero vector; only its direction matters, so the height test is
    written as c^2 <= (2*half_height)^2 * |d|^2, which stays exact.
    """
    a, b, c = (F(v) for v in d)
    if a == b == c == 0:
        raise ValueError("a direction cannot be the zero vector")
    thickness = 2 * F(half_height)
    if c * c > thickness * thickness * (a * a + b * b + c * c):
        return False                      # the slab is too thin to lean that far
    if a == 0 and b == 0:
        return bool(slivers)
    if b == 0:
        return False                      # a shadow along the ground line
    run = a / b
    return holds_every_direction(slivers, run, run)


# ---------------------------------------------------------------------------
# The two-sliver merge, in closed form (chapter 3)
# ---------------------------------------------------------------------------

def merged_pair_area(shift, half_width=1, h=1) -> Fraction:
    """Exact area of two half-slivers of a triangle pushed together by `shift`.

    For a triangle of base 2w and height h split down the middle, sliding the
    right half left by shift = t*w leaves area h*w*(1 - t + 3*t^2/4), which is
    smallest at t = 2/3, where two thirds of the original area survives.
    """
    w, h = F(half_width), F(h)
    left = sliver(0, w, w, h)
    right = sliver(w, 2 * w, w, h).translate(-F(shift))
    return union_area([left, right])

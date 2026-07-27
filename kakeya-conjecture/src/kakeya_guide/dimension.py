"""Box counting: how a set can have zero area and still be big.

Area answers "how much paint?".  Dimension answers "how much room does it fill
as you zoom in?", and the two answers can disagree wildly: the Cantor set has
length 0 and dimension 0.63, and a Besicovitch set has area 0 while (in the
plane) still having dimension 2.  This module measures both, exactly, on sets
made of intervals and boxes.

Counting is done on interval lists rather than sampled points, so the counts
here are integers, not estimates that drift with the sample size.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
from typing import Sequence

Interval = tuple[Fraction, Fraction]


def F(x) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(x)


# --- Cantor sets ------------------------------------------------------------

def cantor_intervals(level: int, pieces: int = 2,
                     ratio=Fraction(1, 3)) -> list[Interval]:
    """Level-`level` approximation of a self-similar Cantor set in [0, 1].

    `pieces` copies of the whole, each shrunk by `ratio`, spread evenly with
    the first flush left and the last flush right.  pieces=2, ratio=1/3 is the
    classic middle-thirds set.
    """
    ratio = F(ratio)
    if pieces < 2 or not 0 < ratio <= Fraction(1, pieces):
        raise ValueError("need pieces >= 2 and 0 < ratio <= 1/pieces")
    gap = (1 - pieces * ratio) / (pieces - 1) if pieces > 1 else F(0)
    out: list[Interval] = [(F(0), F(1))]
    for _ in range(level):
        nxt = []
        for lo, hi in out:
            span = hi - lo
            for i in range(pieces):
                start = lo + i * (ratio + gap) * span
                nxt.append((start, start + ratio * span))
        out = nxt
    return out


def total_length(intervals: Sequence[Interval]) -> Fraction:
    """Total length, overlap counted once."""
    total, cur = F(0), None
    for lo, hi in sorted(intervals):
        if cur is None or lo > cur[1]:
            if cur:
                total += cur[1] - cur[0]
            cur = [lo, hi]
        elif hi > cur[1]:
            cur[1] = hi
    if cur:
        total += cur[1] - cur[0]
    return total


def similarity_dimension(pieces: int, ratio) -> float:
    """log(pieces) / log(1/ratio): the dimension a self-similar set should have."""
    return math.log(pieces) / math.log(1 / float(ratio))


# --- box counting -----------------------------------------------------------

def box_count(intervals: Sequence[Interval], eps) -> int:
    """How many boxes of side eps on a fixed grid the set touches."""
    eps = F(eps)
    hit = set()
    for lo, hi in intervals:
        first = math.floor(lo / eps)
        last = math.ceil(hi / eps) - 1
        if last < first:                     # a point sitting on a grid line
            last = first
        hit.update(range(first, last + 1))
    return len(hit)


def box_count_2d(x_intervals: Sequence[Interval],
                 y_intervals: Sequence[Interval], eps) -> int:
    """Boxes touched by the product set (a rectangle grid, so it factorises)."""
    return box_count(x_intervals, eps) * box_count(y_intervals, eps)


def box_dimension(counts: Sequence[tuple[float, int]]) -> float:
    """Least-squares slope of log(count) against log(1/eps)."""
    xs = [math.log(1 / float(e)) for e, _ in counts]
    ys = [math.log(c) for _, c in counts]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den


def cantor_box_dimension(pieces: int = 2, ratio=Fraction(1, 3),
                         levels: int = 8) -> float:
    """Measure the box dimension of a Cantor set by counting boxes.

    At scale ratio^m the set is covered by exactly pieces^m boxes, so the
    measured slope should land on log(pieces)/log(1/ratio) to the last digit.
    """
    ratio = F(ratio)
    ivals = cantor_intervals(levels, pieces, ratio)
    data = [(ratio ** m, box_count(ivals, ratio ** m))
            for m in range(1, levels + 1)]
    return box_dimension(data)


# --- directions in n dimensions, and how to look at four of them ------------

def sphere_directions(n: int, count: int, seed: int = 8) -> np.ndarray:
    """`count` unit vectors spread evenly over the unit sphere of R^n.

    Works for any n: normalised Gaussians are uniform on the sphere in every
    dimension, which is the whole point of drawing it this way.  Only half the
    sphere is kept, because a needle pointing one way and the other way is the
    same needle.
    """
    rng = np.random.default_rng(seed)
    v = rng.normal(size=(count, n))
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    v[v[:, -1] < 0] *= -1                      # one representative per direction
    return v


def rotate_4d(v: np.ndarray, angle: float) -> np.ndarray:
    """Turn 4D vectors in the x-w and y-z planes at once.

    This is a rotation no 3D scene can imitate.  Watch the projected picture
    breathe: that breathing is the fourth axis.
    """
    c, s = math.cos(angle), math.sin(angle)
    x, y, z, w = v.T
    return np.stack([c * x - s * w, c * y - s * z,
                     s * y + c * z, s * x + c * w], axis=1)


def project_to_3d(v: np.ndarray, eye: float = 3.2) -> np.ndarray:
    """Perspective projection from 4D to 3D, the way tesseracts are drawn."""
    scale = eye / (eye - v[:, 3])
    return v[:, :3] * scale[:, None]


# --- the punchline: length zero, dimension positive -------------------------

def cantor_length(level: int, pieces: int = 2, ratio=Fraction(1, 3)) -> Fraction:
    """Exact length left after `level` rounds: (pieces * ratio)**level.

    Computed from the recipe rather than from the intervals, so that "what is
    left after sixty rounds" costs nothing to ask.
    """
    return (pieces * F(ratio)) ** level


def cantor_length_and_dimension(level: int, pieces: int = 2,
                                ratio=Fraction(1, 3)) -> tuple[Fraction, float]:
    """(exact length at this level, dimension of the limit set)."""
    return (cantor_length(level, pieces, ratio),
            similarity_dimension(pieces, ratio))

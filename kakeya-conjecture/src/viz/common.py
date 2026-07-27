"""Shared drawing helpers for the chapter figure scripts.

Run any chapter script from this folder and it writes straight into the
matching guide/ chapter:

    cd src/viz && python ch05_perron_tree.py
"""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from kakeya_guide.plotting import (BASELINE, BLUE, GRIDLINE, GREEN, INK, INK2,
                                   MUTED, RED, SURFACE, VIOLET, YELLOW, ease,
                                   readout, save_anim, save_fig, sliver_patch,
                                   style_axes, title)

GUIDE = Path(__file__).resolve().parents[2] / "guide"


def out_dir(chapter_folder: str) -> Path:
    d = GUIDE / chapter_folder
    d.mkdir(parents=True, exist_ok=True)
    return d


def fnum(x) -> float:
    return float(x)


# --- slivers ---------------------------------------------------------------

def sliver_xy(s, dx=0.0):
    """The triangle's corners as two lists, ready for set_xy on a Polygon."""
    return [(float(s.b0) + dx, 0.0), (float(s.b1) + dx, 0.0),
            (float(s.ax) + dx, float(s.h))]


def add_slivers(ax, slivers, color=GREEN, alpha=0.3, zorder=3, lw=0.0):
    """Add one patch per sliver and hand back the patches for animating."""
    patches = []
    for s in slivers:
        p = sliver_patch(s, color=color, alpha=alpha, lw=lw, zorder=zorder)
        ax.add_patch(p)
        patches.append(p)
    return patches


def morph_slivers(patches, start, end, t):
    """Slide every sliver from its stage-start place to its stage-end place."""
    for patch, a, b in zip(patches, start, end):
        dx = (1 - t) * float(a.b0) + t * float(b.b0) - float(a.b0)
        patch.set_xy(sliver_xy(a, dx))


# --- needles ---------------------------------------------------------------

def apex_needle(s, run):
    """The unit needle hanging from a sliver's apex at the given run."""
    ax_, h = float(s.ax), float(s.h)
    norm = math.hypot(run, 1.0)
    return (ax_, h), (ax_ + run / norm, h - 1.0 / norm)


def needle_line(ax, color=BLUE, lw=3.2, zorder=9):
    line, = ax.plot([], [], color=color, lw=lw, solid_capstyle="round",
                    zorder=zorder)
    dots, = ax.plot([], [], "o", ms=lw * 1.5, color=color, zorder=zorder + 1)
    return line, dots


def place(line, dots, p, q):
    line.set_data([p[0], q[0]], [p[1], q[1]])
    dots.set_data([p[0], q[0]], [p[1], q[1]])


def turn_schedule(slivers, per_sliver=6, per_jump=3):
    """Frames for a needle that pivots inside each sliver, then hops to the next.

    Returns a list of (kind, sliver_index, t) with kind in {"pivot", "jump"}.
    """
    plan = []
    order = sorted(range(len(slivers)),
                   key=lambda i: slivers[i].direction_interval())
    for n, i in enumerate(order):
        for f in range(per_sliver):
            plan.append(("pivot", i, f / max(per_sliver - 1, 1)))
        if n + 1 < len(order):
            for f in range(per_jump):
                plan.append(("jump", (i, order[n + 1]), f / max(per_jump - 1, 1)))
    return plan


def needle_at(slivers, step):
    """Where the needle is at one step of `turn_schedule`."""
    kind, idx, t = step
    if kind == "pivot":
        s = slivers[idx]
        lo, hi = (float(v) for v in s.direction_interval())
        return apex_needle(s, lo + (hi - lo) * t)
    i, j = idx
    a = apex_needle(slivers[i], float(slivers[i].direction_interval()[1]))
    b = apex_needle(slivers[j], float(slivers[j].direction_interval()[0]))
    return (tuple((1 - t) * u + t * v for u, v in zip(a[0], b[0])),
            tuple((1 - t) * u + t * v for u, v in zip(a[1], b[1])))


# --- little widgets --------------------------------------------------------

def bar(ax, x, height, width=0.6, color=RED, alpha=0.85, zorder=4):
    return ax.bar([x], [height], width=width, color=color, alpha=alpha,
                  zorder=zorder)[0]


def steps_text(ax, lines, x=0.02, y=0.97, fontsize=11, color=INK2):
    return ax.text(x, y, "\n".join(lines), transform=ax.transAxes, va="top",
                   ha="left", fontsize=fontsize, color=color, zorder=10,
                   family="monospace")


def fade_in(artist, t):
    artist.set_alpha(min(1.0, max(0.0, t)))


def hold(frames, n):
    """Repeat the last frame n times so a GIF pauses before looping."""
    return list(frames) + [frames[-1]] * n


def end_pad(fps, seconds=2.5):
    """How many extra frames to ask for so the last one stays up to be read.

    Every animation here ends on the frame that carries the point, usually a
    number or a filled dial.  The update functions clamp their index, so any
    frames past the end simply repeat that last one.  Without a pause of a
    couple of seconds the loop wipes the answer away mid-sentence, which is
    the single most irritating thing an explanatory GIF can do.
    """
    return max(1, round(fps * seconds))

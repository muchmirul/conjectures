"""Shared drawing helpers for the chapter figure scripts.

Run any chapter script from this folder and it writes straight into the
matching guide/ chapter:

    cd src/viz && python ch04_the_certificate.py
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from sphere_packing_guide.plotting import (BASELINE, BLUE, GOOD, GREEN,
                                           GRIDLINE, INK, INK2, MUTED, RED,
                                           SURFACE, VIOLET, YELLOW, arrow,
                                           axes_3d, ball_3d, card, compass_3d,
                                           disc, ease, plot_axes,
                                           project_to_3d, readout, rotate_4d,
                                           save_anim, save_fig, spin_gif,
                                           style_axes, title, wire_cube)

GUIDE = Path(__file__).resolve().parents[2] / "guide"


def out_dir(chapter_folder: str) -> Path:
    d = GUIDE / chapter_folder
    d.mkdir(parents=True, exist_ok=True)
    return d


def end_pad(fps: int, seconds: float = 2.5) -> int:
    """How many extra frames to ask for so the last one stays up to be read.

    Every animation here ends on the frame that carries the point, usually a
    number or a finished picture.  The update functions clamp their index, so
    any frames past the end simply repeat that last one.  Without a pause of a
    couple of seconds the loop wipes the answer away mid-sentence, which is the
    single most irritating thing an explanatory GIF can do.

    Rotating camera shots are the exception and must not use this: they loop
    seamlessly, because there the motion is the content.
    """
    return max(1, round(fps * seconds))


# --- packing layouts the chapters keep reusing -----------------------------

def square_centres(n: int, spacing: float = 1.0) -> list[tuple[float, float]]:
    """Ball centres on a square grid: the obvious way to stack, and not the best."""
    return [(i * spacing, j * spacing) for i in range(n) for j in range(n)]


def hex_centres(n: int, spacing: float = 1.0) -> list[tuple[float, float]]:
    """Ball centres on the hexagonal grid: the best possible way in the plane."""
    out = []
    for j in range(n):
        for i in range(n):
            x = (i + 0.5 * (j % 2)) * spacing
            y = j * spacing * math.sqrt(3) / 2
            out.append((x, y))
    return out


def lerp_centres(a, b, t):
    """Slide one layout into another, so the reader sees the rearrangement."""
    return [((1 - t) * p[0] + t * q[0], (1 - t) * p[1] + t * q[1])
            for p, q in zip(a, b)]


def fcc_centres(n: int = 2) -> np.ndarray:
    """Ball centres of the greengrocer's stack, in three dimensions.

    The face centred cubic lattice: every point whose three whole number
    coordinates add up to an even number.
    """
    pts = []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(-n, n + 1):
                if (i + j + k) % 2 == 0:
                    pts.append((i, j, k))
    return np.array(pts, dtype=float)


def shade_forbidden(ax, x0, x1, y0, y1, color=RED, alpha=0.07, zorder=0):
    """Wash over the region where a rule says a curve is not allowed to go."""
    ax.axvspan(x0, x1, ymin=0, ymax=1, color=color, alpha=alpha, zorder=zorder)
    return ax


def note_below(fig, x=0.012, y=0.022, fontsize=11, color=INK2, ha="left"):
    """A live readout placed under the drawing, never on top of it.

    A number that changes has to sit somewhere, and inside the axes it will
    eventually land on a curve, a dot or another label, because the picture
    moves and the text does not.  Putting it in reserved space below the axes
    makes an overlap impossible rather than unlikely.  Call
    `fig.subplots_adjust(bottom=...)` first so the space is really there.
    """
    return fig.text(x, y, "", ha=ha, va="bottom", fontsize=fontsize,
                    color=color, family="monospace", zorder=20)

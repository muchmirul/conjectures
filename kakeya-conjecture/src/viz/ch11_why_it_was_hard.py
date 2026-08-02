"""Figures for chapter 11: a century of climbing, and the shapes that resist."""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    out_dir, save_fig, title)
from kakeya_guide.plotting import axes_3d, spin_gif

OUT = out_dir("11-why-it-was-hard")

#: Lower bounds on the dimension of a Kakeya set in three dimensions.
#: Only bounds whose 3D value is unambiguous in the literature are plotted;
#: Bourgain's 1991 advance is quoted in the chapter as (n+1)/2 plus a constant,
#: which is how his paper states it.  Sources in notes/research-content.md.
BOUNDS = [
    (1919, 2.0, "Besicovitch\nat least 2"),
    (1995, 2.5, "Wolff\nthe hairbrush"),
    (2000, 2.5, "Katz, Laba, Tao\n+ a ten billionth"),
    (2019, 2.5, "Katz, Zahl\n+ epsilon, Hausdorff"),
    (2025, 3.0, "Wang, Zahl\nall of it"),
]


def bounds_png():
    """A century of pushing a number from 2 up to 3."""
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.set_xlim(1908, 2042)
    ax.set_ylim(1.86, 3.2)
    ax.set_yticks([2.0, 2.5, 3.0])
    ax.set_yticklabels(["2", "5/2", "3"], fontsize=11)
    ax.set_xlabel("year", color=INK2, fontsize=10)
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("bottom", "left"):
        ax.spines[s].set_color(BASELINE)
    ax.grid(True, color=GRIDLINE, lw=0.8, zorder=0)
    ax.axhline(3.0, color=GREEN, lw=1.4, ls="--", zorder=2)
    ax.text(1911, 3.05, "what the conjecture asked for", color=GREEN,
            fontsize=9.5)
    title(ax, "best proved dimension of a Kakeya set in 3D")

    xs = [b[0] for b in BOUNDS] + [2040]
    ys = [b[1] for b in BOUNDS] + [BOUNDS[-1][1]]
    ax.plot(xs, ys, drawstyle="steps-post", color=RED, lw=2.4, zorder=4)
    ax.plot([b[0] for b in BOUNDS], [b[1] for b in BOUNDS], "o", color=RED,
            ms=6, zorder=5)
    # each label is parked in the empty quadrant next to its own step
    places = [(10, 10, "left"), (-10, 24, "right"), (16, -46, "left"),
              (34, -46, "left"), (-12, 6, "right")]
    for (year, value, label), (dx, dy, ha) in zip(BOUNDS, places):
        ax.annotate(f"{year}\n{label}", (year, value),
                    textcoords="offset points", xytext=(dx, dy), ha=ha,
                    fontsize=9, color=INK2, linespacing=1.35)
    ax.text(2007, 2.56, "thirty years stuck here", ha="center", fontsize=9.5,
            color=MUTED)
    save_fig(fig, OUT / "bounds.png")


def hairbrush_gif(n=34, frames=28, fps=11):
    """Wolff's idea: don't count tubes through a point, count them through a line.

    Both arguments live in three dimensional space, and the whole force of the
    hairbrush is that the tubes hanging off the spine spread into the third
    dimension.  Flat pictures hide exactly that, so the camera goes round.
    """
    fig = plt.figure(figsize=(8.2, 4.2))
    axL = axes_3d(fig, 121, box=1.0, elev=16)
    axR = axes_3d(fig, 122, box=1.0, elev=16)
    axL.text2D(0.5, 0.98, "a bush: tubes through one point", ha="center",
               transform=axL.transAxes, fontsize=11.5, color=INK2)
    axR.text2D(0.5, 0.98, "a hairbrush: tubes through one whole tube",
               ha="center", transform=axR.transAxes, fontsize=11.5, color=INK2)

    golden = math.pi * (3 - math.sqrt(5))
    rng = np.random.default_rng(1995)
    for j in range(n):
        z = 1 - (j + 0.5) * 2 / n                 # spread over the sphere
        r = math.sqrt(max(0.0, 1 - z * z))
        phi = golden * j
        d = np.array([r * math.cos(phi), r * math.sin(phi), z])
        axL.plot(*zip(-0.9 * d, 0.9 * d), color=BLUE, lw=2.4, alpha=0.3,
                 solid_capstyle="round", zorder=3)

        # the hairbrush: every tube crosses the spine, but points its own way
        foot = np.array([-0.85 + 1.7 * j / (n - 1), 0.0, 0.0])
        e = rng.normal(0, 1, 3)
        e[0] *= 0.35                              # keep them off the spine
        e = e / np.linalg.norm(e)
        axR.plot(*zip(foot - 0.75 * e, foot + 0.75 * e), color=VIOLET, lw=2.2,
                 alpha=0.3, solid_capstyle="round", zorder=3)
    axR.plot([-0.95, 0.95], [0, 0], [0, 0], color=RED, lw=5, alpha=0.9,
             solid_capstyle="round", zorder=5)
    spin_gif(fig, [axL, axR], OUT / "hairbrush.gif", frames=frames, fps=fps,
             elev=16)



if __name__ == "__main__":
    bounds_png()
    hairbrush_gif()
    print(f"wrote figures to {OUT}")

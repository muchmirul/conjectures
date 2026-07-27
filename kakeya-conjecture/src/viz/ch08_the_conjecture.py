"""Figures for chapter 8: what the conjecture asks, in every dimension.

The statement itself is typed into the chapter, not drawn: a picture of four
boxes of text is just text that cannot be selected, searched or read aloud.

What is drawn is the thing words cannot carry: the set of directions a needle
can point in, in 2, 3 and 4 dimensions.  Each panel is a real 3D scene with the
camera going round it, so the flat one is visibly flat, and the four
dimensional one is turned in the fourth axis before being projected, which is
the honest way to look at something you cannot look at.
"""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    out_dir, readout, save_fig, style_axes, title)
from kakeya_guide.dimension import (project_to_3d, rotate_4d,
                                    sphere_directions)
from kakeya_guide.plotting import axes_3d, save_anim

OUT = out_dir("08-the-conjecture")


def what_it_forbids_png():
    """In the plane every value below 2 is ruled out.  That is the whole claim."""
    fig, ax = plt.subplots(figsize=(8.0, 3.4))
    ax.set_xlim(-0.05, 2.35)
    ax.set_ylim(-1.0, 1.25)
    ax.set_yticks([])
    ax.set_xticks([0, 0.5, 1, 1.5, 2])
    ax.set_xlabel("dimension of a set holding every direction, in the plane",
                  color=INK2, fontsize=10)
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    title(ax, "what the conjecture rules out")
    ax.axvspan(0, 2, color=RED, alpha=0.13, zorder=2)
    ax.plot([2], [0.12], "o", ms=13, color=GREEN, zorder=5)
    ax.text(1.0, 0.62, "no set can live here", ha="center", fontsize=12,
            color=RED)
    ax.text(2.0, 0.62, "only this", ha="center", fontsize=12, color=GREEN)
    ax.text(1.16, -0.62,
            "area can still be zero: dimension is a different question",
            ha="center", fontsize=11, color=INK2)
    save_fig(fig, OUT / "what_it_forbids.png")


def dimensions_gif(count=72, frames=36, fps=11):
    """One needle, three homes: the plane, space, and four dimensional space."""
    from mpl_toolkits.mplot3d.art3d import Line3DCollection

    fig = plt.figure(figsize=(10.4, 3.7))
    axes = [axes_3d(fig, 131 + i, box=0.72, elev=16) for i in range(3)]
    fig.subplots_adjust(left=0.0, right=1.0, top=0.90, bottom=0.0, wspace=0.0)
    names = ["2 dimensions\nthe directions make a circle",
             "3 dimensions\nthey make a sphere",
             "4 dimensions\nturned in the fourth axis, then projected"]
    for ax, name in zip(axes, names):
        ax.text2D(0.5, 1.02, name, ha="center", va="top",
                  transform=ax.transAxes, fontsize=10, color=INK2,
                  linespacing=1.4)

    def segments(dirs, length=0.62):
        return [(-length * d, length * d) for d in dirs]

    flat = sphere_directions(2, count // 2)
    flat3 = np.column_stack([flat, np.zeros(len(flat))])
    axes[0].add_collection3d(Line3DCollection(segments(flat3), colors=BLUE,
                                              lw=1.6, alpha=0.5))
    space = sphere_directions(3, count)
    axes[1].add_collection3d(Line3DCollection(segments(space), colors=VIOLET,
                                              lw=1.6, alpha=0.4))
    hyper = sphere_directions(4, count)
    # seeded with frame zero: an empty 3D collection has nothing to autoscale on
    coll4 = Line3DCollection(segments(project_to_3d(hyper), 0.45), colors=GREEN,
                             lw=1.6, alpha=0.4)
    axes[2].add_collection3d(coll4)

    def update(i):
        azim = 360 * i / frames
        for ax in axes:
            ax.view_init(elev=16, azim=azim)
        turned = rotate_4d(hyper, 2 * math.pi * i / frames)
        coll4.set_segments(segments(project_to_3d(turned), 0.45))
        return []

    save_anim(fig, update, frames, OUT / "dimensions.gif", fps=fps)


if __name__ == "__main__":
    what_it_forbids_png()
    dimensions_gif()
    print(f"wrote figures to {OUT}")

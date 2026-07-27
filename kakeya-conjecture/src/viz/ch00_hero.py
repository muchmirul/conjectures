"""Figure for chapter 0: the hero turn."""

import matplotlib.pyplot as plt
import numpy as np

from common import (BLUE, GREEN, GRIDLINE, INK, INK2, MUTED, RED, SURFACE,
                    VIOLET, YELLOW, add_slivers, ease, end_pad, needle_at,
                    needle_line, out_dir, place, readout, save_anim,
                    save_fig, style_axes, turn_schedule)
from kakeya_guide.core import union_area
from kakeya_guide.examples import tree
from kakeya_guide.shapes import DISC_AREA, disc

OUT = out_dir("00-start-here")


def thumbnail_png(k=4, dpi=150):
    """A 5:2 card for link previews: the turning needle, then the title.

    Saved without a tight bounding box on purpose, so the file comes out at
    exactly 1500 x 600 pixels and the 5:2 ratio survives.
    """
    figure = tree(k)
    fig = plt.figure(figsize=(10, 4))

    xs = [float(v) for s in figure for v in (s.b0, s.b1, s.ax)]
    lo, hi = min(xs) - 0.05, max(xs) + 0.05
    ax = fig.add_axes([0.03, 0.06, 0.34, 0.88])
    ax.set_anchor("C")
    style_axes(ax, (lo, hi), (-0.04, 1.06))
    add_slivers(ax, figure, color=GREEN, alpha=0.45, zorder=3)

    # a fan of faint needles for the directions already covered, then one
    # solid needle for the direction being pointed in right now.  Only the
    # pivot frames are drawn: on a jump frame the needle is mid-slide and
    # outside the set, which would be a lie in a still picture.
    plan = [s for s in turn_schedule(figure, per_sliver=3, per_jump=2)
            if s[0] == "pivot"]
    ghosts = [plan[round(t * (len(plan) - 1))] for t in np.linspace(0, 1, 13)]
    for step in ghosts[:-1]:
        p, q = needle_at(figure, step)
        ax.plot([p[0], q[0]], [p[1], q[1]], color=BLUE, lw=1.7, alpha=0.3,
                solid_capstyle="round", zorder=4)
    p, q = needle_at(figure, ghosts[-1])
    ax.plot([p[0], q[0]], [p[1], q[1]], color=BLUE, lw=4.0,
            solid_capstyle="round", zorder=9)
    ax.plot([p[0], q[0]], [p[1], q[1]], "o", ms=6, color=BLUE, zorder=10)

    # the words live in their own axes, so nothing can land on the picture
    text = fig.add_axes([0.40, 0.06, 0.57, 0.88])
    text.set_axis_off()
    text.text(0, 0.82, "Playing needle with\nKakeya Conjecture", fontsize=34,
              color=INK, va="top", ha="left", linespacing=1.15)
    text.text(0, 0.33, "A needle turns through every direction there is,\n"
                       "inside a room with almost no area at all.",
              fontsize=15, color=INK2, va="top", ha="left", linespacing=1.5)

    out = OUT / "thumbnail.png"
    fig.savefig(out, dpi=dpi, facecolor=SURFACE)
    plt.close(fig)
    return out


def hero_gif(k=4, fps=14):
    """A needle turning through every direction inside a spiky little room."""
    figure = tree(k)
    area = float(union_area(figure))
    xs = [float(v) for s in figure for v in (s.b0, s.b1, s.ax)]
    lo, hi = min(xs) - 0.06, max(xs) + 0.06
    fig, ax = plt.subplots(figsize=(5.6, 5.6 * 1.1 / (hi - lo)))
    style_axes(ax, (lo, hi), (-0.05, 1.05))

    add_slivers(ax, figure, color=GREEN, alpha=0.45, zorder=3)
    plan = turn_schedule(figure, per_sliver=3, per_jump=2)
    trail = [ax.plot([], [], color=BLUE, lw=1.1, alpha=0.22, zorder=4)[0]
             for _ in plan]
    line, dots = needle_line(ax, color=BLUE, lw=3.4)
    readout(ax, (0.02, 0.98),
            f"needle  length 1\nroom    area {area:.3f}", color=INK2,
            fontsize=11)

    def update(i):
        idx = min(i, len(plan) - 1)
        p, q = needle_at(figure, plan[idx])
        place(line, dots, p, q)
        trail[idx].set_data([p[0], q[0]], [p[1], q[1]])
        return [line]

    save_anim(fig, update, len(plan) + end_pad(fps), OUT / "hero.gif", fps=fps)



if __name__ == "__main__":
    hero_gif()
    thumbnail_png()
    print(f"wrote figures to {OUT}")

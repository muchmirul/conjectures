"""Figures for chapter 3: the three-color record, and the four-color unknown."""

import matplotlib.pyplot as plt

from common import (BLUE, EDGE_COLORS, GRIDLINE, INK2, MUTED, RED,
                    draw_coloring, draw_vertices, out_dir, plot_axes,
                    ring_positions, save_fig, style_axes, title)
from ramsey_guide.core import gf16_coloring, is_triangle_free
from ramsey_guide.examples import FOUR_COLOR_RANGE, KNOWN_FORCING

OUT = out_dir("03-more-crayons")


def layers_png():
    """The record coloring taken apart: each color's own net, alone.

    Every panel is one color's connections from the sixteen-person table.
    Each net joins each person to exactly five others and contains no
    triangle at all, which is the entire secret: a net with no triangle can
    never hold a one-color one.
    """
    coloring = gf16_coloring()
    assert is_triangle_free(coloring)
    pos = ring_positions(16, radius=1.0)
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.2))
    for c, ax in enumerate(axes):
        style_axes(ax, (-1.22, 1.22), (-1.22, 1.22))
        draw_coloring(ax, coloring, pos, lw=1.5, only_color=c)
        draw_vertices(ax, pos, r=0.045)
        title(ax, f"color {c + 1} alone: no triangle", size=11)
    save_fig(fig, OUT / "layers.png")


def records_png():
    """What is actually known, color count by color count.

    Three bars are exact.  The fourth is not a bar but a bracket: the answer
    for four colors is only known to lie somewhere between 51 and 62, and
    that range has not moved in decades.
    """
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ks = [1, 2, 3]
    values = [KNOWN_FORCING[k][0] for k in ks]
    ax.bar(ks, values, width=0.55, color=BLUE, alpha=0.8)
    for k, v in zip(ks, values):
        ax.text(k, v + 1.2, str(v), ha="center", fontsize=11, color=INK2)
    lo, hi = FOUR_COLOR_RANGE
    ax.bar([4], [hi - lo], bottom=lo, width=0.55, color=MUTED, alpha=0.45,
           hatch="//")
    ax.plot([3.72, 4.28], [lo, lo], color=INK2, lw=1.4)
    ax.plot([3.72, 4.28], [hi, hi], color=INK2, lw=1.4)
    ax.text(4, hi + 1.2, f"somewhere from {lo} to {hi}", ha="center",
            fontsize=10, color=INK2)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(["1 color", "2 colors", "3 colors", "4 colors"],
                       fontsize=10)
    ax.set_ylim(0, 74)
    plot_axes(ax, ylabel="party size that forces a one-color triangle")
    title(ax, "the exact answers stop at three colors")
    save_fig(fig, OUT / "records.png")


if __name__ == "__main__":
    layers_png()
    records_png()
    print("wrote", OUT)

"""Figures for chapter 6: rooms of any size you name, and area zero."""

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    add_slivers, needle_at, needle_line, out_dir, place,
                    readout, save_anim, save_fig, style_axes, title, turn_schedule)
from kakeya_guide.core import union_area, union_area_numeric
from kakeya_guide.examples import RAMPED_AREAS_DECIMAL, tree

OUT = out_dir("06-area-zero")


def shrink_png(ks=(1, 3, 5, 7, 9)):
    """Same fan of directions, less and less area, one frame per tree."""
    figs = [tree(k) for k in ks]
    fig, axes = plt.subplots(1, len(ks), figsize=(2.05 * len(ks), 3.4))
    for ax, k, figure in zip(axes, ks, figs):
        xs = [float(v) for s in figure for v in (s.b0, s.b1, s.ax)]
        style_axes(ax, (min(xs) - 0.04, max(xs) + 0.04), (-0.05, 1.16))
        add_slivers(ax, figure, color=GREEN, alpha=0.5, zorder=3)
        title(ax, f"{2 ** k} slivers\narea {RAMPED_AREAS_DECIMAL[k]:.4f}",
              size=10)
    fig.tight_layout()
    save_fig(fig, OUT / "shrink.png")


def turn_gif(k=4, fps=12):
    """The needle turning through the whole fan, sliver by sliver.

    Between slivers it takes a Pal join, drawn as a dashed hop: those joins
    cost area, but as little as you care to pay.
    """
    figure = tree(k)
    area = float(union_area(figure))
    xs = [float(v) for s in figure for v in (s.b0, s.b1, s.ax)]
    lo, hi = min(xs) - 0.06, max(xs) + 0.06

    fig, (ax, dial) = plt.subplots(1, 2, figsize=(7.8, 3.9),
                                   gridspec_kw={"width_ratios": [1.5, 1]})
    style_axes(ax, (lo, hi), (-0.06, 1.08))
    add_slivers(ax, figure, color=GREEN, alpha=0.4, zorder=3)
    plan = turn_schedule(figure, per_sliver=3, per_jump=1)
    trail = [ax.plot([], [], color=BLUE, lw=1.0, alpha=0.2, zorder=4)[0]
             for _ in plan]
    line, dots = needle_line(ax, lw=3.2)
    note = readout(ax, (0.02, 0.99), "", fontsize=11)

    style_axes(dial, (-1.2, 1.2), (-0.3, 1.2))
    dial.add_patch(plt.Circle((0, 0), 1.0, fc="none", ec=GRIDLINE, lw=1.4))
    title(dial, "directions covered so far", size=11.5)
    arcs = [dial.plot([], [], color=GREEN, lw=7, solid_capstyle="butt",
                      alpha=0.9)[0] for _ in plan]

    def update(i):
        j = min(i, len(plan) - 1)
        p, q = needle_at(figure, plan[j])
        place(line, dots, p, q)
        trail[j].set_data([p[0], q[0]], [p[1], q[1]])
        ang = np.arctan2(q[1] - p[1], q[0] - p[0]) % np.pi
        arcs[j].set_data(np.cos([ang - 0.03, ang + 0.03]),
                         np.sin([ang - 0.03, ang + 0.03]))
        kind = plan[j][0]
        note.set_text(f"area  {area:.4f}\n"
                      f"{'pivoting inside a sliver' if kind == 'pivot' else 'hopping to the next sliver'}")
        return []

    save_anim(fig, update, len(plan) + 10, OUT / "turn.gif", fps=fps)


def to_zero_png():
    """How the area falls as the cutting goes on, and where it is heading."""
    ks = list(range(10))
    areas = [RAMPED_AREAS_DECIMAL[k] for k in ks]
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    ax.set_xlim(-0.4, 9.4)
    ax.set_ylim(0, 0.55)
    # one row of tick labels, not two: the sliver count IS the x axis here
    ax.set_xticks(ks)
    ax.set_xticklabels([str(2 ** k) for k in ks])
    ax.set_xlabel("slivers the triangle was cut into", color=INK2, fontsize=10)
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("bottom", "left"):
        ax.spines[s].set_color(BASELINE)
    ax.grid(True, color=GRIDLINE, lw=0.8, zorder=0)
    title(ax, "the area keeps falling, and never stops")
    for k in ks:
        ax.bar([k], [areas[k]], width=0.6, color=GREEN, alpha=0.8, zorder=3)
        ax.text(k, areas[k] + 0.012, f"{areas[k]:.3f}", ha="center",
                fontsize=8.5, color=INK2, zorder=4)
    ax.annotate("", xy=(9.3, 0.02), xytext=(9.3, 0.16),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2),
                annotation_clip=False)
    ax.text(9.2, 0.185, "and on, to zero", color=RED, fontsize=10, ha="right")
    save_fig(fig, OUT / "to_zero.png")


if __name__ == "__main__":
    shrink_png()
    turn_gif()
    to_zero_png()
    print(f"wrote figures to {OUT}")

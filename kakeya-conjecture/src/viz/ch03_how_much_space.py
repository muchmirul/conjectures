"""Figures for chapter 3: what area is, and why overlapping is the loophole."""

from fractions import Fraction

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED,
                    VIOLET, YELLOW, add_slivers, ease, end_pad, out_dir,
                    readout, save_anim, sliver_xy, style_axes, title)
from kakeya_guide.core import merged_pair_area, sliver, union_area, width_at
from kakeya_guide.plotting import area_curve

OUT = out_dir("03-how-much-space")

LEFT = sliver(0, 1, 1, 1)                 # left half of a triangle, base [0,1]
RIGHT = sliver(1, 2, 1, 1)                # right half, base [1,2]


def overlap_gif(n=42, fps=12):
    """Slide the two halves together: the area drops because overlap is free."""
    shifts = [Fraction(i, 3 * (n - 1)) * 2 for i in range(n)]     # 0 .. 2/3
    areas = [merged_pair_area(s) for s in shifts]

    fig, (ax, axp) = plt.subplots(1, 2, figsize=(9.8, 4.3),
                                  gridspec_kw={"width_ratios": [1.25, 1]})
    style_axes(ax, (-0.15, 2.15), (-0.1, 1.25))
    title(ax, "slide the right half onto the left half")
    ghost = add_slivers(ax, [LEFT, RIGHT], color=GRIDLINE, alpha=1.0, zorder=1)
    patches = add_slivers(ax, [LEFT, RIGHT], color=GREEN, alpha=0.42, zorder=3)
    note = readout(ax, (0.02, 0.98), "", fontsize=11.5)

    axp.set_xlim(0, 0.7)
    axp.set_ylim(0.6, 1.05)
    axp.set_xlabel("how far it slid", color=INK2, fontsize=10)
    area_curve(axp, [], [], color=RED)
    curve, = axp.plot([], [], color=RED, lw=2.2, zorder=4)
    dot, = axp.plot([], [], "o", ms=6, color=RED, zorder=5)
    title(axp, "area of the two halves together", size=11.5)
    axp.axhline(2 / 3, color=BASELINE, lw=1, ls="--", zorder=2)
    axp.text(0.02, 0.675, "two thirds", color=MUTED, fontsize=9)

    def update(i):
        j = min(i, n - 1)
        dx = float(shifts[j])
        patches[1].set_xy(sliver_xy(RIGHT, -dx))
        note.set_text(f"slid   {dx:.3f}\narea   {float(areas[j]):.4f}")
        curve.set_data([float(s) for s in shifts[:j + 1]],
                       [float(a) for a in areas[:j + 1]])
        dot.set_data([dx], [float(areas[j])])
        return []

    save_anim(fig, update, n + end_pad(fps), OUT / "overlap.gif", fps=fps)


def slices_gif(n=46, fps=12):
    """How area is actually measured here: add up the widths, slice by slice."""
    shifted = RIGHT.translate(Fraction(-2, 3))
    figure = [LEFT, shifted]
    total = union_area(figure)
    heights = [Fraction(i, n - 1) for i in range(n)]
    widths = [float(width_at(figure, y)) for y in heights]

    fig, (ax, axp) = plt.subplots(1, 2, figsize=(9.8, 4.3),
                                  gridspec_kw={"width_ratios": [1.2, 1]})
    style_axes(ax, (-0.35, 1.55), (-0.1, 1.15))
    title(ax, "one horizontal slice at a time")
    add_slivers(ax, figure, color=GREEN, alpha=0.32, zorder=2)
    cut, = ax.plot([], [], color=VIOLET, lw=2.2, zorder=6)
    rule, = ax.plot([], [], color=BASELINE, lw=0.9, ls="--", zorder=3)
    note = readout(ax, (0.02, 0.98), "", fontsize=11.5)

    axp.set_xlim(0, 1.05)
    axp.set_ylim(0, 1.02)
    area_curve(axp, [], [], color=VIOLET)
    prof, = axp.plot([], [], color=VIOLET, lw=2.2, zorder=4)
    fillp = [None]
    axp.set_xlabel("width covered", color=INK2, fontsize=10)
    title(axp, "widths stacked up = the area", size=11.5)

    def update(i):
        j = min(i, n - 1)
        y = float(heights[j])
        w = widths[j]
        left = min(float(s.interval(heights[j])[0]) for s in figure)
        cut.set_data([left, left + w], [y, y])
        rule.set_data([-0.35, 1.55], [y, y])
        note.set_text(f"height {y:.2f}\nwidth  {w:.3f}\n"
                      f"area   {float(total):.4f}" if j == n - 1 else
                      f"height {y:.2f}\nwidth  {w:.3f}")
        prof.set_data(widths[:j + 1], [float(h) for h in heights[:j + 1]])
        if fillp[0] is not None:
            fillp[0].remove()
        fillp[0] = axp.fill_betweenx([float(h) for h in heights[:j + 1]], 0,
                                     widths[:j + 1], color=VIOLET, alpha=0.18,
                                     zorder=3)
        return []

    save_anim(fig, update, n + end_pad(fps), OUT / "slices.gif", fps=fps)


if __name__ == "__main__":
    overlap_gif()
    slices_gif()
    print(f"wrote figures to {OUT}")

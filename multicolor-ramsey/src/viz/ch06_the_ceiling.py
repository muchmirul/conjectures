"""Figures for chapter 6: the sorting argument and the factorial ceiling."""

import math

import matplotlib.pyplot as plt

from common import (BLUE, EDGE_COLORS, GREEN, INK2, MUTED, RED, draw_edge,
                    draw_vertices, ease, end_pad, note_below, out_dir,
                    plot_axes, ring_positions, save_anim, save_fig,
                    style_axes, title)
from ramsey_guide.core import factorial_record, gf16_coloring, upper_staircase

OUT = out_dir("06-the-ceiling")


def sort_gif(fps=16):
    """One person's view of the sixteen-person table, sorted by color.

    Fifteen connections, three colors: the three groups land at exactly five
    each here.  Inside the red group, no connection back to the middle is
    red, and no connection between two of its members can be red either
    without closing a red triangle: red is used up.  The biggest group is a
    smaller party with one color effectively gone, which is the step the
    ceiling repeats.
    """
    coloring = gf16_coloring()
    centre_edges = [(v, int(coloring[0, v])) for v in range(1, 16)]
    start = ring_positions(15, radius=0.9)
    groups = {0: [], 1: [], 2: []}
    for v, c in centre_edges:
        groups[c].append(v)
    target = {}
    anchors = {0: (-1.05, 0.72), 1: (1.05, 0.72), 2: (0.0, -1.05)}
    for c, members in groups.items():
        ax0, ay0 = anchors[c]
        spots = ring_positions(len(members), radius=0.34, centre=(ax0, ay0))
        for v, p in zip(members, spots):
            target[v] = p

    fig, ax = plt.subplots(figsize=(6.6, 6.9))
    fig.subplots_adjust(bottom=0.10, top=0.94)
    style_axes(ax, (-1.62, 1.62), (-1.5, 1.35))
    title(ax, "one person's fifteen connections, sorted by color")
    note = note_below(fig, x=0.5, ha="center", fontsize=11.5)

    lines, dots = {}, {}
    for idx, (v, c) in enumerate(centre_edges):
        (x1, y1) = start[idx]
        (ln,) = ax.plot([0, x1], [0, y1], color=EDGE_COLORS[c], lw=1.8,
                        alpha=0.85, zorder=3)
        lines[v] = ln
        dots[v] = ax.plot([x1], [y1], "o", ms=7, mfc="white", mec=INK2,
                          zorder=8)[0]
    ax.plot([0], [0], "o", ms=10, mfc="white", mec=INK2, zorder=9)

    frames = 46

    def update(i):
        t = ease(min(i, frames - 1) / (frames - 1))
        for idx, (v, c) in enumerate(centre_edges):
            (x0, y0), (x1, y1) = start[idx], target[v]
            x, y = (1 - t) * x0 + t * x1, (1 - t) * y0 + t * y1
            lines[v].set_data([0, x], [0, y])
            dots[v].set_data([x], [y])
        if i < frames - 1:
            note.set_text("everyone slides toward the color of their connection")
            note.set_color(INK2)
        else:
            note.set_text("15 people, 3 colors: some group has at least 5\n"
                          "inside that group, its color is used up")
            note.set_color(INK2)
        return []

    save_anim(fig, update, frames + end_pad(fps, 3.0), OUT / "sort.gif",
              fps=fps)


def staircase_png():
    """The forcing sizes the sorting step proves, next to plain factorials.

    Each step multiplies by roughly the number of colors, which is what
    "factorial growth" means.  The refined record from the literature runs
    parallel to the simple staircase: better constants, same shape.
    """
    ks = list(range(1, 11))
    stair = upper_staircase(10)
    record = [factorial_record(k) for k in ks]
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.plot(ks, stair, "o-", color=BLUE, lw=1.8, ms=4,
            label="the sorting staircase")
    ax.plot(ks[3:], record[3:], "s--", color=MUTED, lw=1.5, ms=4,
            label="the record bound (quoted)")
    ax.plot(ks, [math.factorial(k) for k in ks], ":", color=RED, lw=1.4,
            label="plain factorial, for scale")
    ax.set_yscale("log")
    ax.set_xticks(ks)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    plot_axes(ax, xlabel="colors",
              ylabel="party size that surely forces")
    title(ax, "the ceiling grows like a factorial")
    save_fig(fig, OUT / "staircase.png")


if __name__ == "__main__":
    sort_gif()
    staircase_png()
    print("wrote", OUT)

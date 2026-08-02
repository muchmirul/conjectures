"""Figures for chapter 5: multiplying safe tables, and the rate that will not move."""

import math

import matplotlib.pyplot as plt

from common import (BLUE, EDGE_COLORS, GREEN, INK2, MUTED, draw_vertices,
                    ease, end_pad, note_below, out_dir, plot_axes,
                    ring_positions, save_anim, save_fig, style_axes, title)
from ramsey_guide.core import (is_triangle_free, pentagon_coloring,
                               product_coloring, product_tower_sizes)

OUT = out_dir("05-multiply")


def blowup_gif(fps=16):
    """Each of five people becomes a five-person room, live.

    The connections between two rooms keep the color the two original people
    used.  The connections inside a room use two fresh colors.  Nothing else
    happens, and the result is a safe table five times the size for two more
    colors.  The tests verify the resulting twenty-five-person coloring cold.
    """
    outer = pentagon_coloring()
    product = product_coloring(outer, outer, 2)
    assert is_triangle_free(product)

    big = ring_positions(5, radius=0.95)
    mini_r = 0.30
    frames = 40

    def positions(t):
        out = []
        for p, (cx, cy) in enumerate(big):
            for (ux, uy) in ring_positions(5, radius=mini_r * t,
                                           centre=(cx, cy)):
                out.append((ux, uy))
        return out

    fig, ax = plt.subplots(figsize=(6.4, 6.9))
    fig.subplots_adjust(bottom=0.10, top=0.94)
    style_axes(ax, (-1.55, 1.55), (-1.55, 1.55))
    title(ax, "five people become five rooms of five")
    note = note_below(fig, x=0.5, ha="center", fontsize=12)

    n = 25
    lines = {}
    start = positions(0.0)
    for a in range(n):
        for b in range(a + 1, n):
            c = int(product[a, b])
            (x0, y0), (x1, y1) = start[a], start[b]
            cross = a // 5 != b // 5
            (ln,) = ax.plot([x0, x1], [y0, y1], color=EDGE_COLORS[c],
                            lw=0.9 if cross else 1.8,
                            alpha=0.35 if cross else 0.95,
                            zorder=3, solid_capstyle="round")
            lines[a, b] = ln
    dots = ax.scatter(*zip(*start), s=26, facecolor="white", edgecolor=INK2,
                      lw=1.0, zorder=8)

    def update(i):
        t = ease(min(i, frames - 1) / (frames - 1))
        pos = positions(t)
        for (a, b), ln in lines.items():
            (x0, y0), (x1, y1) = pos[a], pos[b]
            ln.set_data([x0, x1], [y0, y1])
        dots.set_offsets(pos)
        if i < frames - 1:
            note.set_text("rooms grow; colors between rooms never change")
            note.set_color(INK2)
        else:
            note.set_text("25 people, 4 colors, still safe (the tests check it)")
            note.set_color(GREEN)
        return []

    save_anim(fig, update, frames + end_pad(fps), OUT / "blowup.gif", fps=fps)


def tower_png():
    """Repeating the trick forever: big tables, and a rate stuck flat.

    The line through the pentagon's repeated products is straight on this
    plot, and a straight line here means the same people-per-color rate at
    every step.  The sixteen-person table gives a straight line with a
    better slope, and no fixed recipe's line ever curves upward.
    """
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    for base_size, base_colors, label, colour in (
            (5, 2, "pentagon, multiplied", BLUE),
            (16, 3, "sixteen table, multiplied", GREEN)):
        tower = product_tower_sizes(base_size, base_colors, 8)
        ks = [c for c, _ in tower]
        sizes = [s for _, s in tower]
        ax.plot(ks, sizes, "o-", color=colour, lw=1.8, ms=4, label=label)
    ax.set_yscale("log")
    ax.set_xlabel("colors spent", color=INK2, fontsize=10)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    plot_axes(ax, ylabel="safe table size")
    title(ax, "straight lines: the rate per color never climbs")
    save_fig(fig, OUT / "tower.png")


if __name__ == "__main__":
    blowup_gif()
    tower_png()
    print("wrote", OUT)

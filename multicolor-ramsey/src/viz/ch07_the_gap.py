"""Figures for chapter 7: the gap, and the shortcut that fails on camera."""

import math

import matplotlib.pyplot as plt

from common import (BLUE, EDGE_COLORS, GREEN, INK2, MUTED, RED, VIOLET,
                    draw_edge, draw_vertices, end_pad, flash_triangle,
                    note_below, out_dir, plot_axes, ring_positions, save_anim,
                    save_fig, style_axes, title)
from ramsey_guide.core import (best_product_lower, first_difference_coloring,
                               monochromatic_triangles, upper_staircase)

OUT = out_dir("07-the-gap")


def orderings_gif(fps=10):
    """The tempting shortcut, and the triangle that sinks it.

    The six orderings of three letters are the vertices; each pair is
    colored by the first position where the two orderings disagree.  Six
    tables from two colors would beat the pentagon, but the coloring is not
    safe: three orderings can all first-disagree in the same position, and
    the sweep finds them.
    """
    perms, coloring = first_difference_coloring(3)
    labels = ["".join("ABC"[x] for x in p) for p in perms]
    tri = monochromatic_triangles(coloring)[0]
    pos = ring_positions(6, radius=0.9)
    edges = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    edges.sort(key=lambda e: coloring[e[0], e[1]])

    fig, ax = plt.subplots(figsize=(6.2, 6.7))
    fig.subplots_adjust(bottom=0.12, top=0.93)
    style_axes(ax, (-1.42, 1.42), (-1.42, 1.42))
    title(ax, "orderings, colored by first disagreement")
    draw_vertices(ax, pos, r=0.0, labels=labels, label_offset=1.22,
                  fontsize=11)
    for i, (x, y) in enumerate(pos):
        ax.plot([x], [y], "o", ms=9, mfc="white", mec=INK2, zorder=8)
    note = note_below(fig, x=0.5, ha="center", fontsize=11.5)

    build = len(edges)
    flash = []

    def update(i):
        if i < build:
            a, b = edges[i]
            c = int(coloring[a, b])
            draw_edge(ax, pos, a, b, EDGE_COLORS[c], lw=2.4)
            note.set_text("red: differ at the first letter\n"
                          "blue: differ at the second only")
            note.set_color(INK2)
        elif i == build:
            note.set_text("six tables from two colors would beat the pentagon...")
        else:
            if not flash:
                flash.extend(flash_triangle(ax, pos, tri, EDGE_COLORS[0],
                                            lw=6.0))
            a, b, c = (labels[v] for v in tri)
            note.set_text(f"{a}, {b}, {c} all differ at the first letter:\n"
                          "a one-color triangle, and the shortcut is dead")
            note.set_color(EDGE_COLORS[0])
        return []

    frames = build + 3 + end_pad(fps, 3.0)

    def slow(i):
        return update(i if i < build else build + max(0, (i - build) // 3))

    save_anim(fig, slow, frames + 4, OUT / "orderings.gif", fps=fps)


def gap_png():
    """Everything known before 2026, drawn as one widening band.

    The floor is what the multiplication recipe proves from the record
    blocks, computed honestly at every color count rather than smoothed.
    The ceiling is the sorting staircase.  The truth lives in the shaded
    band, and the band widens without end.
    """
    ks = list(range(2, 13))
    floor = [best_product_lower(k) for k in ks]
    ceiling = upper_staircase(12)[1:]
    assert all(f < c for f, c in zip(floor, ceiling))
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ax.plot(ks, ceiling, "o-", color=BLUE, lw=1.8, ms=4,
            label="forced for sure (the ceiling)")
    ax.plot(ks, floor, "o-", color=GREEN, lw=1.8, ms=4,
            label="safe for sure (multiplying the record tables)")
    ax.fill_between(ks, floor, ceiling, color=MUTED, alpha=0.14)
    ax.text(9.9, 5.0e5, "the answer is\nin here somewhere", ha="center",
            va="top", fontsize=10, color=INK2)
    ax.set_yscale("log")
    ax.set_xticks(ks)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    plot_axes(ax, xlabel="colors", ylabel="party size")
    title(ax, "an exponential floor under a factorial ceiling")
    save_fig(fig, OUT / "gap.png")


if __name__ == "__main__":
    orderings_gif()
    gap_png()
    print("wrote", OUT)

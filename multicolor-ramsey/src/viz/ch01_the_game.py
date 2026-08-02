"""Figures for chapter 1: the coloring game, and the pentagon that wins it."""

import matplotlib.pyplot as plt

from common import (EDGE_COLORS, GREEN, INK2, MUTED, RED, draw_coloring,
                    draw_edge, draw_vertices, end_pad, flash_triangle,
                    note_below, out_dir, ring_positions, save_anim, save_fig,
                    style_axes, title)
from ramsey_guide.core import (color_edge, empty_coloring,
                               monochromatic_triangles, pentagon_coloring)

OUT = out_dir("01-the-game")


def rules_png():
    """Two four-person tables: one loses the game, one survives it."""
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.6))
    pos = ring_positions(4, radius=0.92)

    losing = empty_coloring(4)
    for (i, j), c in {(0, 1): 0, (1, 2): 0, (0, 2): 0,
                      (2, 3): 1, (1, 3): 1, (0, 3): 1}.items():
        color_edge(losing, i, j, c)
    style_axes(axes[0], (-1.35, 1.35), (-1.35, 1.35))
    draw_coloring(axes[0], losing, pos, lw=2.6)
    tri = monochromatic_triangles(losing)[0]
    flash_triangle(axes[0], pos, tri, EDGE_COLORS[0], lw=6)
    draw_vertices(axes[0], pos, r=0.075)
    title(axes[0], "three connections, one color: a one-color triangle")

    safe = empty_coloring(4)
    for (i, j), c in {(0, 1): 0, (1, 2): 1, (2, 3): 0,
                      (0, 3): 1, (0, 2): 1, (1, 3): 0}.items():
        color_edge(safe, i, j, c)
    assert not monochromatic_triangles(safe)
    style_axes(axes[1], (-1.35, 1.35), (-1.35, 1.35))
    draw_coloring(axes[1], safe, pos, lw=2.6)
    draw_vertices(axes[1], pos, r=0.075)
    title(axes[1], "every triangle mixes its colors: safe")

    save_fig(fig, OUT / "rules.png")


def pentagon_gif(fps=14):
    """Color the five-person table, then check all ten triangles one by one.

    The build is the easy half; the sweep afterwards is the content.  Each of
    the ten triangles lights up in turn and every one of them shows two
    colors, which is what "safe" means and what the tests verify.
    """
    coloring = pentagon_coloring()
    pos = ring_positions(5, radius=0.95)
    edges = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    edges.sort(key=lambda e: coloring[e[0], e[1]])
    triples = [(i, j, k) for i in range(5) for j in range(i + 1, 5)
               for k in range(j + 1, 5)]
    build, hold, check = len(edges), 4, 3 * len(triples)

    fig, ax = plt.subplots(figsize=(5.8, 6.3))
    fig.subplots_adjust(bottom=0.11, top=0.93)
    style_axes(ax, (-1.3, 1.3), (-1.3, 1.3))
    title(ax, "five people, two colors")
    draw_vertices(ax, pos, r=0.065)
    note = note_below(fig, x=0.5, ha="center", fontsize=12)

    drawn, sweep = [], []

    def update(i):
        if i < build:
            a, b = edges[i]
            c = int(coloring[a, b])
            drawn.append(draw_edge(ax, pos, a, b, EDGE_COLORS[c], lw=2.8))
            note.set_text(f"connections colored  {i + 1} / {len(edges)}")
            note.set_color(INK2)
        elif i < build + hold:
            note.set_text("now check every possible triangle")
        elif i < build + hold + check:
            step = i - build - hold
            t, phase = divmod(step, 3)
            if phase == 0:
                for artist in sweep:
                    artist.remove()
                sweep.clear()
                tri = triples[t]
                for a, b in ((tri[0], tri[1]), (tri[1], tri[2]),
                             (tri[0], tri[2])):
                    c = int(coloring[a, b])
                    sweep.append(draw_edge(ax, pos, a, b, EDGE_COLORS[c],
                                           lw=6.5, zorder=6))
                note.set_text(f"triangle {t + 1} of 10: two colors, harmless")
        else:
            for artist in sweep:
                artist.remove()
            sweep.clear()
            note.set_text("all 10 triangles mix colors: five people are safe")
            note.set_color(GREEN)
        return []

    frames = build + hold + check + 1 + end_pad(fps)
    save_anim(fig, update, frames, OUT / "pentagon.gif", fps=fps)


if __name__ == "__main__":
    rules_png()
    pentagon_gif()
    print("wrote", OUT)

"""Figures for chapter 2: why six people always lose the two-color game."""

import itertools

import matplotlib.pyplot as plt

from common import (BLUE, EDGE_COLORS, GREEN, INK2, MUTED, RED, draw_edge,
                    draw_vertices, end_pad, flash_triangle, note_below,
                    out_dir, plot_axes, ring_positions, save_anim, save_fig,
                    style_axes, title)
from ramsey_guide.core import (color_edge, empty_coloring,
                               monochromatic_triangles)

OUT = out_dir("02-six-is-forced")


def pigeonhole_gif(fps=10):
    """The whole proof, played out on one honest example.

    Watch one person's five connections: three of them must share a color.
    Then any same-colored connection among those three people closes a
    triangle with the middle, and if all three avoid it, they close one
    among themselves.  The animation walks the second case, testing each
    disputed connection both ways.
    """
    pos = ring_positions(6, radius=0.95)
    centre = 0
    others = [1, 2, 3, 4, 5]
    reds = [1, 3, 5]                      # the three same-colored connections
    blues = [2, 4]

    fig, ax = plt.subplots(figsize=(6.0, 6.6))
    fig.subplots_adjust(bottom=0.13, top=0.93)
    style_axes(ax, (-1.3, 1.3), (-1.3, 1.3))
    title(ax, "six people cannot stay safe")
    draw_vertices(ax, pos, r=0.065)
    note = note_below(fig, x=0.5, ha="center", fontsize=11.5)

    steps = []
    for v in others:
        color = 0 if v in reds else 1
        steps.append(("edge", centre, v, color,
                      f"one person's connections, colored one by one"))
    steps.append(("mark", None, None, None,
                  "five connections, two colors: some color appears 3 times"))
    trio = reds
    pairs = [(trio[0], trio[1]), (trio[1], trio[2]), (trio[0], trio[2])]
    for a, b in pairs:
        steps.append(("try", a, b, 0,
                      "if this pair used red, a red triangle closes"))
        steps.append(("settle", a, b, 1,
                      "so this pair must use blue"))
    steps.append(("end", None, None, None,
                  "but now the three of them form a blue triangle"))

    state = {"tried": None, "flash": []}

    def update(i):
        i = min(i, len(steps) - 1)
        kind, a, b, c, text = steps[i]
        # clear any provisional edge from the previous frame
        if state["tried"] is not None:
            state["tried"].remove()
            state["tried"] = None
        for artist in state["flash"]:
            artist.remove()
        state["flash"] = []
        if kind == "edge":
            draw_edge(ax, pos, a, b, EDGE_COLORS[c], lw=2.8)
        elif kind == "mark":
            for v in reds:
                state["flash"].append(
                    draw_edge(ax, pos, centre, v, EDGE_COLORS[0], lw=6.5,
                              zorder=6))
        elif kind == "try":
            state["tried"] = draw_edge(ax, pos, a, b, EDGE_COLORS[c], lw=2.8)
            state["flash"] = flash_triangle(ax, pos, (centre, a, b),
                                            EDGE_COLORS[0], lw=6.5)
        elif kind == "settle":
            draw_edge(ax, pos, a, b, EDGE_COLORS[c], lw=2.8)
        elif kind == "end":
            state["flash"] = flash_triangle(ax, pos, tuple(trio),
                                            EDGE_COLORS[1], lw=6.5)
            note.set_color(EDGE_COLORS[1])
        note.set_text(text)
        if kind != "end":
            note.set_color(INK2)
        return []

    frames = len(steps) * 2 + end_pad(fps, 3.0)

    def update_slow(i):
        return update(i // 2)

    save_anim(fig, update_slow, frames, OUT / "pigeonhole.gif", fps=fps)


def census_png():
    """Every one of the 32768 colorings of six people, counted by triangles.

    The bar at zero is empty: no coloring of six escapes.  The bar at two is
    where the luckiest colorings live, which is Goodman's refinement of the
    theorem, found here by brute force.
    """
    edges = list(itertools.combinations(range(6), 2))
    counts = {}
    for bits in range(2 ** len(edges)):
        coloring = empty_coloring(6)
        for e, (i, j) in enumerate(edges):
            color_edge(coloring, i, j, (bits >> e) & 1)
        t = len(monochromatic_triangles(coloring))
        counts[t] = counts.get(t, 0) + 1
    assert counts.get(0, 0) == 0 and min(counts) == 2

    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    xs = list(range(0, max(counts) + 1))
    ys = [counts.get(x, 0) for x in xs]
    bars = ax.bar(xs, ys, width=0.7, color=BLUE, alpha=0.8)
    bars[0].set_color(RED)
    ax.text(0, 900, "empty:\nno safe\ncoloring", ha="center", fontsize=9,
            color=RED)
    ax.set_xticks(xs)
    plot_axes(ax, xlabel="one-color triangles in the coloring",
              ylabel="how many of the 32768 colorings")
    title(ax, "all two-colorings of six people, checked one by one")
    save_fig(fig, OUT / "census.png")


if __name__ == "__main__":
    pigeonhole_gif()
    census_png()
    print("wrote", OUT)

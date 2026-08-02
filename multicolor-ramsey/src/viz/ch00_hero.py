"""The opening figure: the sixteen-person coloring drawn string by string."""

import matplotlib.pyplot as plt

from common import (EDGE_COLORS, GREEN, INK2, MUTED, draw_edge, draw_vertices,
                    edge_order_by_color, end_pad, note_below, out_dir,
                    ring_positions, save_anim, style_axes, title)
from ramsey_guide.core import gf16_coloring, is_triangle_free

OUT = out_dir("00-start-here")


def hero_gif(fps=20):
    """All 120 connections of the record three-color table, laid one by one.

    The order is color by color, so the reader watches three separate nets
    settle over the same sixteen people.  The point of the figure is the
    final frame: a completely connected table with no one-color triangle,
    which is exactly the object the whole article is about.
    """
    coloring = gf16_coloring()
    assert is_triangle_free(coloring)
    pos = ring_positions(16, radius=1.0)
    edges = edge_order_by_color(coloring)
    per_frame = 2                        # two strings per frame keeps it brisk
    build = (len(edges) + per_frame - 1) // per_frame

    fig, ax = plt.subplots(figsize=(6.4, 6.9))
    fig.subplots_adjust(bottom=0.10, top=0.94)
    style_axes(ax, (-1.28, 1.28), (-1.28, 1.28))
    title(ax, "sixteen people, three colors, no one-color triangle")
    draw_vertices(ax, pos)
    note = note_below(fig, x=0.5, ha="center", fontsize=12)

    drawn = []

    def update(i):
        step = min((i + 1) * per_frame, len(edges))
        while len(drawn) < step:
            a, b = edges[len(drawn)]
            c = int(coloring[a, b])
            drawn.append(draw_edge(ax, pos, a, b, EDGE_COLORS[c], lw=1.4,
                                   alpha=0.75))
        if step < len(edges):
            note.set_text(f"connections colored  {step:3d} / {len(edges)}")
            note.set_color(INK2)
        else:
            note.set_text("all 120 colored, and no triangle shares one color")
            note.set_color(GREEN)
        return []

    save_anim(fig, update, build + end_pad(fps), OUT / "hero.gif", fps=fps)


if __name__ == "__main__":
    hero_gif()
    print("wrote", OUT)

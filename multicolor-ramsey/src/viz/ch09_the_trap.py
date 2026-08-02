"""Figures for chapter 9: the two-room trap, sprung and then disarmed."""

import matplotlib.pyplot as plt

from common import (EDGE_COLORS, GREEN, INK2, MUTED, draw_edge, draw_vertices,
                    end_pad, flash_triangle, note_below, out_dir,
                    ring_positions, save_anim, save_fig, style_axes, title)
from ramsey_guide.core import (RING_LABELS, monochromatic_triangles,
                               pentagon_coloring, trap_coloring)

OUT = out_dir("09-the-trap")

TEAM_COLORS = ["#7fb0ea", "#f2c063", "#b9a6e8"]        # pale badge fills


def block_positions():
    """The pentagon room on the left, the outside vertex on the right."""
    pos = ring_positions(5, radius=0.72, centre=(-0.55, 0.0))
    pos.append((1.45, 0.0))
    return pos


def teams_png():
    """The red net inside the room, with its three teams badged.

    Team badges are the vertex fills.  Within one team there is never a red
    connection, which is what makes the teams useful: anything that lands
    entirely inside one team can never close a red triangle.
    """
    coloring = pentagon_coloring()
    pos = ring_positions(5, radius=0.85)
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    style_axes(ax, (-1.35, 1.35), (-1.3, 1.3))
    title(ax, "the red net, and its three teams")
    for i in range(5):
        for j in range(i + 1, 5):
            if coloring[i, j] == 0:
                draw_edge(ax, pos, i, j, EDGE_COLORS[0], lw=2.6)
    for i, (x, y) in enumerate(pos):
        ax.add_patch(plt.Circle((x, y), 0.11, fc=TEAM_COLORS[RING_LABELS[i]],
                                ec=INK2, lw=1.4, zorder=8))
        ax.text(x, y, str(RING_LABELS[i] + 1), ha="center", va="center",
                fontsize=10, zorder=9)
    ax.text(0, -1.22, "no red connection stays inside one team",
            ha="center", fontsize=10.5, color=INK2)
    save_fig(fig, OUT / "teams.png")


def trap_gif(fps=10):
    """Break the rule and a triangle closes; obey it and nothing can.

    First half: the outside vertex sends red connections to two people who
    are red-connected to each other, and the triangle springs shut.  Second
    half: red connections may only land on team one, no two members of which
    are red-connected, and the room absorbs them safely.  Both endings are
    verified by the tests on the exact same colorings drawn here.
    """
    pos = block_positions()
    broken = trap_coloring(obey_rule=False)
    obeyed = trap_coloring(obey_rule=True)
    tri = monochromatic_triangles(broken)[0]
    assert not monochromatic_triangles(obeyed)

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    fig.subplots_adjust(bottom=0.15, top=0.95)
    style_axes(ax, (-1.75, 2.1), (-1.25, 1.25))
    note = note_below(fig, x=0.5, ha="center", fontsize=11.5)

    def draw_scene(coloring, badge=False):
        for artist in list(ax.lines) + list(ax.patches) + list(ax.texts):
            artist.remove()
        for i in range(5):
            for j in range(i + 1, 5):
                c = int(coloring[i, j])
                draw_edge(ax, pos, i, j, EDGE_COLORS[c],
                          lw=2.4 if c == 0 else 1.2,
                          alpha=0.95 if c == 0 else 0.35)
        for u in range(5):
            c = int(coloring[5, u])
            draw_edge(ax, pos, 5, u, EDGE_COLORS[c],
                      lw=2.6 if c == 0 else 1.4,
                      alpha=0.95 if c == 0 else 0.5)
        for i, (x, y) in enumerate(pos[:5]):
            fill = TEAM_COLORS[RING_LABELS[i]] if badge else "white"
            ax.add_patch(plt.Circle((x, y), 0.09, fc=fill, ec=INK2, lw=1.3,
                                    zorder=8))
        x, y = pos[5]
        ax.add_patch(plt.Circle((x, y), 0.09, fc="white", ec=INK2, lw=1.3,
                                zorder=8))
        ax.text(x, y - 0.24, "outside", ha="center", fontsize=9, color=MUTED)

    def update(i):
        if i < 4:
            draw_scene(broken)
            note.set_text("rule ignored: red lands wherever it likes")
            note.set_color(INK2)
        elif i < 8:
            draw_scene(broken)
            flash_triangle(ax, pos, tri, EDGE_COLORS[0], lw=6.0)
            note.set_text("two red landings, red-connected to each other:\n"
                          "the triangle snaps shut")
            note.set_color(EDGE_COLORS[0])
        elif i < 12:
            draw_scene(obeyed, badge=True)
            note.set_text("rule obeyed: red may only land on team one")
            note.set_color(INK2)
        else:
            draw_scene(obeyed, badge=True)
            note.set_text("teammates are never red-connected, so no red\n"
                          "triangle can close; the yellow strings are a "
                          "color\nthis room does not use inside: harmless too")
            note.set_color(GREEN)
        return []

    save_anim(fig, update, 16 + end_pad(fps, 3.5), OUT / "trap.gif", fps=fps)


if __name__ == "__main__":
    teams_png()
    trap_gif()
    print("wrote", OUT)

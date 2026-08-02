"""Figures for chapter 8: rooms, their palettes, and the parity rule."""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

from common import (BASELINE, EDGE_COLORS, GREEN, INK2, MUTED, RED,
                    end_pad, note_below, out_dir, ring_positions, save_anim,
                    save_fig, style_axes, title)

OUT = out_dir("08-palettes")

CHIP_COLORS = EDGE_COLORS[:4]           # the four colors in play


def room(ax, centre, held, name, width=1.15, height=0.95):
    """A rounded box of people, with its color chips above.

    A filled chip is a color the room uses inside; a hollow chip is a color
    the room's palette forbids, which the room keeps missing on purpose.
    """
    cx, cy = centre
    box = FancyBboxPatch((cx - width / 2, cy - height / 2), width, height,
                         boxstyle="round,pad=0.06,rounding_size=0.12",
                         fc="white", ec=BASELINE, lw=1.6, zorder=2)
    ax.add_patch(box)
    dots = ring_positions(4, radius=0.28, centre=centre)
    for x, y in dots:
        ax.plot([x], [y], "o", ms=8, mfc="white", mec=INK2, zorder=8)
    for c, colour in enumerate(CHIP_COLORS):
        x = cx - 0.42 + 0.28 * c
        y = cy + height / 2 + 0.17
        if c in held:
            ax.add_patch(Rectangle((x - 0.09, y - 0.09), 0.18, 0.18,
                                   fc=colour, ec=colour, zorder=6))
        else:
            ax.add_patch(Rectangle((x - 0.09, y - 0.09), 0.18, 0.18,
                                   fc="white", ec=colour, lw=1.6, zorder=6))
            ax.plot([x - 0.07, x + 0.07], [y - 0.07, y + 0.07],
                    color=colour, lw=1.4, zorder=7)
    ax.text(cx, cy - height / 2 - 0.16, name, ha="center", fontsize=11,
            color=INK2)
    return dots


def rooms_gif(fps=10):
    """A connection between rooms auditions colors until the rule passes.

    Left room holds red and blue; right room holds red and yellow.  Red is
    held by both rooms, so a red connection could close triangles on either
    side; violet is held by neither, so it would be wasted; blue is held by
    exactly one, and that is the only kind the construction ever uses.
    """
    held_p, held_q = {0, 1}, {0, 2}
    fig, ax = plt.subplots(figsize=(8.0, 4.9))
    fig.subplots_adjust(bottom=0.15, top=0.96)
    style_axes(ax, (-2.35, 2.35), (-1.35, 1.35))
    dots_p = room(ax, (-1.35, -0.1), held_p, "left room")
    dots_q = room(ax, (1.35, -0.1), held_q, "right room")
    note = note_below(fig, x=0.5, ha="center", fontsize=11.5)

    a, b = dots_p[0], dots_q[3]
    state = {"line": None}

    #: the audition script: (color, verdict, caption)
    script = [
        (0, False, "red? both rooms hold red: too dangerous on both sides"),
        (3, False, "violet? neither room holds violet: it would be wasted"),
        (1, True, "blue? the left room holds it, the right room misses it"),
    ]

    def update(i):
        step = min(i // 3, len(script) - 1)
        colour, ok, caption = script[step]
        if state["line"] is not None:
            state["line"].remove()
        state["line"] = ax.plot([a[0], b[0]], [a[1], b[1]],
                                color=EDGE_COLORS[colour], lw=3.0,
                                ls="-" if ok else (0, (4, 3)),
                                zorder=4)[0]
        note.set_text(caption + ("\naccepted: every cross color is held on "
                                 "exactly one side" if ok else ""))
        note.set_color(GREEN if ok else INK2)
        return []

    frames = 3 * len(script) + end_pad(fps, 3.0)
    save_anim(fig, update, frames, OUT / "rooms.gif", fps=fps)


def parity_png():
    """All eight ways one color can relate to three rooms, each one failing.

    A one-color triangle across three rooms would need its color held on
    exactly one side of each of the three walls.  In every pattern, some
    wall has the color on both sides or on neither, and that wall is drawn
    dashed: the triangle cannot be completed through it.
    """
    fig, axes = plt.subplots(2, 4, figsize=(10.6, 5.4))
    centres = [(0, 0.62), (-0.62, -0.45), (0.62, -0.45)]
    for idx, (p, q, r) in enumerate([(a, b, c) for a in (1, 0)
                                     for b in (1, 0) for c in (1, 0)]):
        ax = axes[idx // 4][idx % 4]
        style_axes(ax, (-1.25, 1.25), (-1.15, 1.3))
        held = (p, q, r)
        for (cx, cy), h, name in zip(centres, held, "PQR"):
            ax.add_patch(plt.Circle((cx, cy), 0.30, fc="white", ec=BASELINE,
                                    lw=1.5, zorder=2))
            ax.text(cx, cy + 0.44, name, ha="center", fontsize=9, color=MUTED)
            if h:
                ax.add_patch(Rectangle((cx - 0.09, cy - 0.09), 0.18, 0.18,
                                       fc=CHIP_COLORS[2], ec=CHIP_COLORS[2],
                                       zorder=6))
            else:
                ax.add_patch(Rectangle((cx - 0.09, cy - 0.09), 0.18, 0.18,
                                       fc="white", ec=CHIP_COLORS[2], lw=1.4,
                                       zorder=6))
        for i, j in ((0, 1), (1, 2), (0, 2)):
            (x0, y0), (x1, y1) = centres[i], centres[j]
            legal = held[i] != held[j]
            ax.plot([x0, x1], [y0, y1], color=CHIP_COLORS[2],
                    lw=2.4 if legal else 1.6,
                    ls="-" if legal else (0, (3, 3)),
                    alpha=0.9 if legal else 0.55, zorder=1)
        walls = sum(held[i] != held[j] for i, j in ((0, 1), (1, 2), (0, 2)))
        ax.text(0, -1.02, f"{walls} of 3 walls usable", ha="center",
                fontsize=8.6, color=INK2)
    fig.suptitle("no pattern makes all three walls usable: three-room "
                 "triangles are impossible", fontsize=12, color=INK2)
    save_fig(fig, OUT / "parity.png")


if __name__ == "__main__":
    rooms_gif()
    parity_png()
    print("wrote", OUT)

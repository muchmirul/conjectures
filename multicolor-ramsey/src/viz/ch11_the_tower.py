"""Figures for chapter 11: stacking the floors, and the base that climbs."""

import math

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from common import (BASELINE, BLUE, GREEN, INK2, MUTED, RED, VIOLET, end_pad,
                    note_below, out_dir, plot_axes, save_anim, save_fig,
                    style_axes, title)
from ramsey_guide.examples import (GF16_BASE, PENTAGON_BASE, PRE_2026_BASE)

OUT = out_dir("11-the-tower")


def tower_gif(fps=10):
    """Floors of rooms of rooms, with each floor multiplying by more.

    The picture is a diagram, not a portrait: the real first floor already
    has more rooms than there are atoms in a person.  What the diagram keeps
    honest is the shape: every floor houses whole copies of the floor below
    in every one of its rooms, and the number of rooms per floor grows as
    the tower rises, which is exactly what a fixed product could not do.
    """
    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    fig.subplots_adjust(bottom=0.14, top=0.95)
    style_axes(ax, (-0.3, 10.3), (-0.4, 5.6))
    note = note_below(fig, x=0.5, ha="center", fontsize=11.5)

    def draw_floor(x0, y0, w, h, rooms, colour, depth):
        ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                    boxstyle="round,pad=0.03,rounding_size=0.08",
                                    fc="white", ec=colour, lw=2.0, zorder=3))
        if depth == 0:
            ax.plot([x0 + w / 2], [y0 + h / 2], "o", ms=4, mfc=colour,
                    mec=colour, zorder=6)
            return
        pad, gap = 0.12 * h, 0.06 * w
        rw = (w - 2 * gap - (rooms - 1) * gap) / rooms
        for r in range(rooms):
            draw_floor(x0 + gap + r * (rw + gap), y0 + pad, rw, h - 2 * pad,
                       max(2, rooms - 1), MUTED, depth - 1)

    captions = [
        "floor one: a few rooms, each holding one person",
        "floor two: more rooms, each holding all of floor one",
        "floor three: more rooms again, each holding all of floor two",
        "every floor spends the same few colors, but multiplies by more\n"
        "than the floor before: the rate per color climbs",
    ]
    frames_per = 4

    def update(i):
        stage = min(i // frames_per, 3)
        for artist in list(ax.patches) + list(ax.lines):
            artist.remove()
        floors = [(0.0, 0.0, 2.2, 1.5, 2, BLUE, 1),
                  (2.9, 0.0, 3.0, 2.9, 3, VIOLET, 2),
                  (6.4, 0.0, 3.7, 5.2, 4, GREEN, 3)]
        for k in range(min(stage + 1, 3)):
            x0, y0, w, h, rooms, colour, depth = floors[k]
            draw_floor(x0, y0, w, h, rooms, colour, depth)
        note.set_text(captions[stage])
        note.set_color(INK2 if stage < 3 else GREEN)
        return []

    save_anim(fig, update, 4 * frames_per + end_pad(fps, 3.5),
              OUT / "tower.gif", fps=fps)


def base_png():
    """The old flat rates, and the new one that climbs off the chart.

    The flat dashed lines are what fixed recipes achieve: the same people
    per color at every color count.  The rising curve is the shape of the
    2026 construction's rate, the cube root of the color count divided by
    its logarithm.  The curve is drawn without the paper's constant, which
    was deliberately left enormous; what the theorem asserts is the climb,
    not the altitude at any one point.
    """
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ks = [10 ** (0.1 * i) for i in range(10, 121)]
    shape = [k ** (1 / 3) / math.log(k) for k in ks]
    ax.plot(ks, shape, color=RED, lw=2.2,
            label="the 2026 shape: cube root over logarithm")
    for value, label, colour in (
            (PENTAGON_BASE, "pentagon products, 2.24", BLUE),
            (GF16_BASE, "sixteen-table products, 2.52", GREEN),
            (PRE_2026_BASE, "best fixed recipe, 3.28", VIOLET)):
        ax.axhline(value, color=colour, lw=1.4, ls="--", label=label)
    ax.set_xscale("log")
    ax.set_xlim(1e1, 1e12)
    ax.set_ylim(0, 24)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    plot_axes(ax, xlabel="colors (log scale)",
              ylabel="people per color (shape only)")
    title(ax, "fixed recipes stay flat; the new construction climbs")
    save_fig(fig, OUT / "base.png")


if __name__ == "__main__":
    tower_gif()
    base_png()
    print("wrote", OUT)

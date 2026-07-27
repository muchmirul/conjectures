"""Figures for chapter 2: the three classical rooms, and their areas."""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    YELLOW, needle_line, out_dir, place, readout, save_anim, save_fig,
                    style_axes, title)
from kakeya_guide.plotting import shade
from kakeya_guide.shapes import (DELTOID_AREA, DISC_AREA, TRIANGLE_AREA,
                                 deltoid, deltoid_tangent_chord, disc,
                                 equilateral, equilateral_turn)

OUT = out_dir("02-turning-around")


def _room(ax, poly, name, area, color):
    style_axes(ax, (-0.72, 0.72), (-0.72, 0.72))
    shade(ax, poly, color=color, alpha=0.22, zorder=2)
    xs = [p[0] for p in poly] + [poly[0][0]]
    ys = [p[1] for p in poly] + [poly[0][1]]
    ax.plot(xs, ys, color=color, lw=1.6, zorder=3)
    title(ax, f"{name}\narea {area:.4f}", size=11.5)


def rooms_gif(n=90, fps=14):
    """The needle really turns: spin, three-point turn, slide."""
    fig, axes = plt.subplots(1, 3, figsize=(10.6, 4.2))
    circle = disc(0.5, 240)
    tri = equilateral(1.0)
    delt = deltoid(n=360)
    _room(axes[0], circle, "the obvious room: a disc", DISC_AREA, BLUE)
    _room(axes[1], tri, "Pal's triangle, height 1", TRIANGLE_AREA, GREEN)
    _room(axes[2], delt, "Kakeya's guess: the deltoid", DELTOID_AREA, VIOLET)
    needles = [needle_line(ax, lw=3.0) for ax in axes]
    trails = [[ax.plot([], [], color=BLUE, lw=0.9, alpha=0.15, zorder=4)[0]
               for _ in range(n)] for ax in axes]

    def update(i):
        j = min(i, n - 1)
        u = j / (n - 1)
        a = math.pi * u
        spots = [((-0.5 * math.cos(a), -0.5 * math.sin(a)),
                  (0.5 * math.cos(a), 0.5 * math.sin(a))),
                 equilateral_turn(u),
                 deltoid_tangent_chord(2 * math.pi * u)]
        for (line, dots), trail, (p, q) in zip(needles, trails, spots):
            place(line, dots, p, q)
            trail[j].set_data([p[0], q[0]], [p[1], q[1]])
        return []

    save_anim(fig, update, n + 10, OUT / "rooms.gif", fps=fps)


def shrinking_png():
    """Each answer beat the last. Where does it stop?"""
    names = ["disc", "triangle", "deltoid", "?"]
    areas = [DISC_AREA, TRIANGLE_AREA, DELTOID_AREA, 0.0]
    colors = [BLUE, GREEN, VIOLET, RED]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.set_xlim(-0.7, 3.7)
    ax.set_ylim(0, 0.92)
    ax.set_xticks(range(4))
    ax.set_xticklabels(names, fontsize=11, color=INK2)
    ax.set_yticks([0, 0.25, 0.5, 0.75])
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("bottom", "left"):
        ax.spines[s].set_color(BASELINE)
    ax.grid(True, axis="y", color=GRIDLINE, lw=0.8, zorder=0)
    title(ax, "area of the room the needle turns in")
    bars = [ax.bar([i], [0], width=0.55, color=c, alpha=0.85, zorder=3)[0]
            for i, c in enumerate(colors)]
    labels = [ax.text(i, 0, "", ha="center", va="bottom", fontsize=10,
                      color=INK2, zorder=4) for i in range(4)]
    qmark = ax.text(3, 0.42, "?", ha="center", va="center", fontsize=34,
                    color=RED, alpha=0.0, zorder=5)

    for n, (b, lab) in enumerate(zip(bars, labels)):
        b.set_height(areas[n])
        lab.set_position((n, areas[n] + 0.015))
        lab.set_text(f"{areas[n]:.4f}" if areas[n] else "")
    qmark.set_alpha(1.0)
    save_fig(fig, OUT / "shrinking.png")


if __name__ == "__main__":
    rooms_gif()
    shrinking_png()
    print(f"wrote figures to {OUT}")

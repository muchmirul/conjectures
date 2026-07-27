"""Figures for chapter 1: a needle, and the only thing about it that matters."""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, VIOLET,
                    YELLOW, needle_line, out_dir, place, readout, save_anim,
                    style_axes, title)

OUT = out_dir("01-the-needle")


def directions_gif(n=36, fps=9):
    """Turn the needle a half circle and the dial fills: that is every direction."""
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.4, 4.2))
    style_axes(axL, (-0.95, 0.95), (-0.95, 0.95))
    style_axes(axR, (-1.15, 1.15), (-0.35, 1.15))
    title(axL, "one needle, turning")
    title(axR, "directions used so far")

    axL.plot([0], [0], "o", ms=4, color=MUTED, zorder=5)
    ghosts = [axL.plot([], [], color=BLUE, lw=1.2, alpha=0.18, zorder=3)[0]
              for _ in range(n)]
    line, dots = needle_line(axL, lw=3.4)

    axR.add_patch(plt.Circle((0, 0), 1.0, fc="none", ec=GRIDLINE, lw=1.4))
    filled = [axR.plot([], [], color=GREEN, lw=6, solid_capstyle="butt",
                       alpha=0.9, zorder=4)[0] for _ in range(n)]
    counter = readout(axR, (0.03, 0.97), "", fontsize=12)

    def update(i):
        j = min(i, n - 1)
        a = math.pi * j / (n - 1)
        p = (-0.5 * math.cos(a), -0.5 * math.sin(a))
        q = (0.5 * math.cos(a), 0.5 * math.sin(a))
        place(line, dots, p, q)
        ghosts[j].set_data([p[0], q[0]], [p[1], q[1]])
        arc = np.linspace(math.pi * (j - 0.5) / (n - 1), a, 8)
        filled[j].set_data(np.cos(arc), np.sin(arc))
        counter.set_text(f"{int(round(180 * j / (n - 1))):3d} of 180 degrees")
        return [line]

    save_anim(fig, update, n + 8, OUT / "directions.gif", fps=fps)


def position_gif(fps=10, n=28):
    """Three needles, same direction, different places: same direction."""
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    style_axes(ax, (-1.6, 1.6), (-0.85, 0.85))
    title(ax, "position is not the point: direction is")
    homes = [(-1.0, 0.35), (0.0, -0.3), (1.0, 0.3)]
    colors = [BLUE, VIOLET, GREEN]
    needles = [needle_line(ax, color=c, lw=3.2) for c in colors]
    label = readout(ax, (0.02, 0.97), "", fontsize=12)

    def update(i):
        a = math.pi * min(i, n - 1) / (n - 1)
        for (cx, cy), (line, dots) in zip(homes, needles):
            dx, dy = 0.5 * math.cos(a), 0.5 * math.sin(a)
            place(line, dots, (cx - dx, cy - dy), (cx + dx, cy + dy))
        label.set_text(f"all three needles point the same way: "
                       f"{int(round(math.degrees(a))):3d} degrees")
        return []

    save_anim(fig, update, n + 6, OUT / "position.gif", fps=fps)


if __name__ == "__main__":
    directions_gif()
    position_gif()
    print(f"wrote figures to {OUT}")

"""Figure for chapter 0: the hero turn."""

import matplotlib.pyplot as plt
import numpy as np

from common import (BLUE, GREEN, GRIDLINE, INK, INK2, MUTED, RED, VIOLET,
                    YELLOW, add_slivers, ease, needle_at, needle_line, out_dir,
                    place, readout, save_anim, save_fig, style_axes, turn_schedule)
from kakeya_guide.core import union_area
from kakeya_guide.examples import tree
from kakeya_guide.shapes import DISC_AREA, disc

OUT = out_dir("00-start-here")


def hero_gif(k=4, fps=14):
    """A needle turning through every direction inside a spiky little room."""
    figure = tree(k)
    area = float(union_area(figure))
    xs = [float(v) for s in figure for v in (s.b0, s.b1, s.ax)]
    lo, hi = min(xs) - 0.06, max(xs) + 0.06
    fig, ax = plt.subplots(figsize=(5.6, 5.6 * 1.1 / (hi - lo)))
    style_axes(ax, (lo, hi), (-0.05, 1.05))

    add_slivers(ax, figure, color=GREEN, alpha=0.45, zorder=3)
    plan = turn_schedule(figure, per_sliver=3, per_jump=2)
    trail = [ax.plot([], [], color=BLUE, lw=1.1, alpha=0.22, zorder=4)[0]
             for _ in plan]
    line, dots = needle_line(ax, color=BLUE, lw=3.4)
    readout(ax, (0.02, 0.98),
            f"needle  length 1\nroom    area {area:.3f}", color=INK2,
            fontsize=11)

    def update(i):
        idx = min(i, len(plan) - 1)
        p, q = needle_at(figure, plan[idx])
        place(line, dots, p, q)
        trail[idx].set_data([p[0], q[0]], [p[1], q[1]])
        return [line]

    save_anim(fig, update, len(plan) + 12, OUT / "hero.gif", fps=fps)



if __name__ == "__main__":
    hero_gif()
    print(f"wrote figures to {OUT}")

"""Figures for chapter 6: what certificates actually prove in small dimensions."""

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    out_dir, plot_axes, save_fig, style_axes, title)
from sphere_packing_guide.examples import (FOUND_BOUNDS, KNOWN_DENSITIES,
                                           known_density)

OUT = out_dir("06-best-so-far")


def gap_png():
    """Our own certificates against the densities that are actually reachable.

    Space is drawn as a tube being filled from the bottom.  Blue is how full
    the best known packing really makes it, red from the certificate's ceiling
    upward is proved unreachable, and the violet sliver between them is all
    that remains unknown.  The sliver is too thin to see at true scale, which
    is itself the point, so a magnifying window blows it up beside each tube.
    """
    fig, ax = plt.subplots(figsize=(10.0, 5.4))
    style_axes(ax, (-6, 62), (-14, 108), equal=False)
    groups = [(0, 2), (32, 3)]
    for x0, d in groups:
        t = known_density(d) * 100
        b = FOUND_BOUNDS[d] * 100
        # the tube: all of space, filled from the floor
        ax.add_patch(plt.Rectangle((x0, 0), 5, 100, fill=False, ec=BASELINE,
                                   lw=1.4, zorder=4))
        ax.add_patch(plt.Rectangle((x0, 0), 5, t, facecolor=BLUE, alpha=0.55,
                                   zorder=2))
        ax.add_patch(plt.Rectangle((x0, t), 5, b - t, facecolor=VIOLET,
                                   alpha=0.45, zorder=2))
        ax.add_patch(plt.Rectangle((x0, b), 5, 100 - b, facecolor=RED,
                                   alpha=0.10, hatch="///", edgecolor=RED,
                                   lw=0, zorder=2))
        for level, label in ((0, "empty"), (100, "completely full")):
            ax.plot([x0 - 0.9, x0], [level, level], color=BASELINE, lw=1.1)
            ax.text(x0 - 1.5, level, label, ha="right", va="center",
                    fontsize=8.5, color=MUTED)
        # the magnifying window on the sliver where everything unknown lives
        w0, w1 = t - 1.0, b + 1.0
        s0, s1 = 22, 96                       # where the window sits on the page
        ax.add_patch(plt.Rectangle((x0 + 11, s0), 6, s1 - s0, fill=False,
                                   ec=INK2, lw=1.3, zorder=5))
        ax.plot([x0 + 5, x0 + 11], [w0, s0], color=INK2, lw=0.9, ls=":",
                zorder=3)
        ax.plot([x0 + 5, x0 + 11], [w1, s1], color=INK2, lw=0.9, ls=":",
                zorder=3)

        def up(v):
            return s0 + (v - w0) / (w1 - w0) * (s1 - s0)

        ax.add_patch(plt.Rectangle((x0 + 11, s0), 6, up(t) - s0,
                                   facecolor=BLUE, alpha=0.55, zorder=4))
        ax.add_patch(plt.Rectangle((x0 + 11, up(t)), 6, up(b) - up(t),
                                   facecolor=VIOLET, alpha=0.45, zorder=4))
        ax.add_patch(plt.Rectangle((x0 + 11, up(b)), 6, s1 - up(b),
                                   facecolor=RED, alpha=0.10, hatch="///",
                                   edgecolor=RED, lw=0, zorder=4))
        ax.text(x0 + 17.8, up(b) + 3, f"proved impossible\nabove {b:.2f} %",
                fontsize=9, color=RED, va="center")
        ax.text(x0 + 17.8, (up(t) + up(b)) / 2, "unknown", fontsize=9,
                color=VIOLET, va="center")
        ax.text(x0 + 17.8, up(t) - 3, f"actually reached:\n{t:.2f} %",
                fontsize=9, color=BLUE, va="center")
        ax.text(x0 + 8.5, -7.5, f"{d} dimensions", ha="center", fontsize=10.5,
                color=INK2)
    title(ax, "space drawn as a tube being filled, with the unknown sliver magnified")
    save_fig(fig, OUT / "gap.png")


if __name__ == "__main__":
    gap_png()
    print("wrote", OUT)

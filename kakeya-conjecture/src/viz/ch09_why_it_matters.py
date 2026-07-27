"""Figures for chapter 9: why a needle problem holds up other mathematics."""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    YELLOW, out_dir, readout, save_fig, style_axes, title)

OUT = out_dir("09-why-it-matters")


def tubes_png(n_dirs=24):
    """Fat needles, all pointing differently: how much do they pile up?

    A wave travelling in a direction lives in a thin tube.  Add waves going
    every way and the question of how small their union can be is exactly
    Kakeya's question, one thickness at a time.
    """
    widths = [0.16, 0.08, 0.04, 0.02]
    fig, axes = plt.subplots(1, len(widths), figsize=(11.0, 3.3))
    for ax, w in zip(axes, widths):
        style_axes(ax, (-0.75, 0.75), (-0.75, 0.75))
        title(ax, f"tube thickness {w:.2f}", size=10.5)
        for j in range(n_dirs):
            a = math.pi * j / n_dirs
            dx, dy = math.cos(a), math.sin(a)
            pts = [(-0.5 * dx - w * dy / 2, -0.5 * dy + w * dx / 2),
                   (0.5 * dx - w * dy / 2, 0.5 * dy + w * dx / 2),
                   (0.5 * dx + w * dy / 2, 0.5 * dy - w * dx / 2),
                   (-0.5 * dx + w * dy / 2, -0.5 * dy - w * dx / 2)]
            ax.add_patch(plt.Polygon(pts, closed=True, facecolor=BLUE,
                                     alpha=0.14, edgecolor="none", zorder=3))
    save_fig(fig, OUT / "tubes.png")



if __name__ == "__main__":
    tubes_png()
    print(f"wrote figures to {OUT}")

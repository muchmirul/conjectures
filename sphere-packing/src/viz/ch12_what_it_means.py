"""Figures for chapter 12: what was settled, and what was not."""

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    out_dir, plot_axes, save_fig, style_axes, title)
from sphere_packing_guide.examples import ALPHA_STAR, KL_EXPONENT, MILESTONES

OUT = out_dir("12-what-it-means")


def two_radii_png():
    """The two sign problems: same limit, and never actually equal.

    The quantities really are radii, so they are drawn as radii: in each
    panel the dashed green circle is the common limit, drawn at the same size
    every time because everything is measured per square root of the
    dimension.  The two solid circles close onto it as the dimension grows
    and never reach it, and the blue one, the plus problem, is always the
    smaller of the two.  The spacing of the circles sketches the trend; only
    the limit itself is the exact 2026 number.
    """
    dims = [4, 16, 64, 256]
    fig, ax = plt.subplots(figsize=(10.4, 3.9))
    style_axes(ax, (-2.1, 12.9), (-2.45, 3.15))
    for k, d in enumerate(dims):
        cx = k * 3.6
        minus = 1 + 0.9 / np.sqrt(d)
        plus = 1 + 0.5 / np.sqrt(d)
        ax.add_patch(plt.Circle((cx, 0), minus, fill=False, ec=VIOLET,
                                lw=2.2, zorder=3))
        ax.add_patch(plt.Circle((cx, 0), plus, fill=False, ec=BLUE, lw=2.2,
                                zorder=3))
        ax.add_patch(plt.Circle((cx, 0), 1.0, fill=False, ec=GREEN, lw=1.5,
                                ls="--", zorder=3))
        ax.text(cx, -2.05, f"dimension {d}", ha="center", fontsize=9.5,
                color=INK2)
    ax.text(-2.0, 2.85, "outer, violet: the minus problem", color=VIOLET,
            fontsize=9.5, ha="left")
    ax.text(3.4, 2.85, "inner, blue: the plus problem", color=BLUE,
            fontsize=9.5, ha="left")
    ax.text(8.4, 2.85, "dashed, green: the limit they share", color=GREEN,
            fontsize=9.5, ha="left")
    title(ax, "the two radii close on the same circle and never reach it", size=11.5)
    save_fig(fig, OUT / "two_radii.png")


if __name__ == "__main__":
    two_radii_png()
    print("wrote", OUT)

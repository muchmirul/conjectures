"""Figures for chapter 7: is there a best possible certificate, and what is it?"""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    end_pad, note_below, out_dir, plot_axes, save_anim,
                    save_fig, style_axes, title)
from sphere_packing_guide.examples import ALPHA_STAR, KL_EXPONENT

OUT = out_dir("07-the-ceiling")


def exponents_png():
    """One step of each shrinking rule, drawn as squares instead of slopes.

    Every bound of this kind is a fixed shrinking factor applied once per
    dimension.  So the honest picture of a bound is a row of squares, each a
    fixed fraction of the area of the one before.  Drawn side by side, the
    1978 rule and the 2026 rule shrink so nearly alike that no eye can tell
    them apart, which is exactly what the next figure needs the reader to
    believe before it compounds the difference.
    """
    old_side = math.sqrt(2 ** -KL_EXPONENT)
    new_side = math.sqrt(2 ** -ALPHA_STAR)
    fig, ax = plt.subplots(figsize=(10.2, 4.4))
    style_axes(ax, (-9.5, 15.2), (-2.4, 8.6))
    for base_y, side_factor, label, colour in (
            (4.9, old_side, f"1978: times {2 ** -KL_EXPONENT:.4f}\n"
             "of the ceiling per step", MUTED),
            (0.0, new_side, f"2026: times {2 ** -ALPHA_STAR:.4f}\n"
             "of the ceiling per step", GREEN)):
        x, s = 0.0, 2.2
        for i in range(8):
            ax.add_patch(plt.Rectangle((x, base_y), s, s, facecolor=colour,
                                       alpha=0.55, zorder=3))
            x += s + 0.55
            s *= side_factor
        ax.text(-1.0, base_y + 1.1, label, ha="right", va="center",
                fontsize=10, color=colour)
    ax.text(2.8, -1.7, "each square is one added dimension; area is the ceiling",
            fontsize=9.5, color=MUTED, ha="left")
    title(ax, "the two shrinking rules, one step of dimension at a time")
    save_fig(fig, OUT / "exponents.png")


def advantage_gif(frames=64, fps=12):
    """The invisible difference in rate, compounded before the reader's eyes.

    The gray disc holds still: it is the 1978 ceiling, whatever it happens to
    be in the current dimension.  The green disc is the 2026 ceiling drawn to
    scale against it, area for area.  As the dimension counter climbs, the
    fourth-decimal difference in rate compounds into a disc forty times
    smaller.  The compounding is the content, so this one moves.
    """
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    style_axes(ax, (-3.4, 3.4), (-1.85, 1.95))
    ax.add_patch(plt.Circle((-1.6, 0), 1.0, facecolor=MUTED, alpha=0.5,
                            zorder=3))
    green = plt.Circle((1.6, 0), 1.0, facecolor=GREEN, alpha=0.6, zorder=3)
    ax.add_patch(green)
    ax.text(-1.6, 1.42, "the 1978 ceiling,\nheld at a fixed size", ha="center",
            fontsize=9.5, color=INK2)
    ax.text(1.6, 1.42, "the 2026 ceiling,\ndrawn to scale beside it",
            ha="center", fontsize=9.5, color=GREEN)
    fig.subplots_adjust(bottom=0.16)
    note = note_below(fig, fontsize=11.5)
    title(ax, "a difference in the fourth decimal place, compounded")

    def update(i):
        t = min(i, frames - 1) / (frames - 1)
        d = 10 * (1000 / 10) ** t               # dimension 10 up to 1000
        times = 2 ** ((ALPHA_STAR - KL_EXPONENT) * d)
        green.set_radius(math.sqrt(1 / times))
        note.set_text(f"dimension {d:6.0f}   "
                      f"the new ceiling is {times:5.1f} times smaller")
        return []

    save_anim(fig, update, frames + end_pad(fps), OUT / "advantage.gif",
              fps=fps)


if __name__ == "__main__":
    exponents_png()
    advantage_gif()
    print("wrote", OUT)

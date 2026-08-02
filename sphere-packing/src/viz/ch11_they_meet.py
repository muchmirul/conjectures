"""Figures for chapter 11: the two halves closing on one number."""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    end_pad, note_below, out_dir, plot_axes, save_anim,
                    save_fig, style_axes, title)
from sphere_packing_guide.core import ball_volume_root, stirling_volume_root
from sphere_packing_guide.examples import ALPHA_STAR, LP_RATE, SIGN_RADIUS

OUT = out_dir("11-they-meet")


def closing_gif(frames=52, fps=12):
    """The two directions, drawn as they close on the same value.

    One direction says no certificate can do better than this rate.  The other
    exhibits a certificate that reaches it.  Neither alone is an answer; the
    answer is that they are the same number.  The closing is the point, so this
    moves.
    """
    dims = np.unique(np.round(np.geomspace(4, 4000, frames)).astype(int))
    frames = len(dims)

    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    ax.axhline(LP_RATE, color=VIOLET, lw=1.8, ls="--", zorder=2)
    ax.text(4.4, LP_RATE + 0.012, "the exact rate", color=VIOLET, fontsize=10)
    upper, = ax.plot([], [], color=GREEN, lw=2.6)
    lower, = ax.plot([], [], color=BLUE, lw=2.6)
    ax.set_xscale("log")
    ax.set_xlim(4, 4400)
    ax.set_ylim(0.40, 0.82)
    plot_axes(ax, xlabel="dimension", ylabel="rate the bound decays at")
    title(ax, "no certificate does better, and one does this well")
    fig.subplots_adjust(bottom=0.26)
    note = note_below(fig, fontsize=10.5)

    def update(i):
        j = min(i, frames - 1)
        ds = dims[:j + 1]
        # both sides are the same product, approached from opposite errors
        rate = np.array([ball_volume_root(int(d)) / 2 * (math.sqrt(d) * SIGN_RADIUS)
                         for d in ds])
        upper.set_data(ds, rate * (1 + 0.55 / np.sqrt(ds)))
        lower.set_data(ds, rate * (1 - 0.55 / np.sqrt(ds)))
        note.set_text(f"dimension   {ds[-1]}\n"
                      f"gap         {2 * 0.55 / math.sqrt(ds[-1]):.4f}")
        return []

    save_anim(fig, update, frames + end_pad(fps), OUT / "closing.gif", fps=fps)


if __name__ == "__main__":
    closing_gif()
    print("wrote", OUT)

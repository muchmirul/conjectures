"""Figures for chapter 8: rebuilding the certificate into a balanced function."""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    YELLOW, end_pad, ease, note_below, out_dir, plot_axes,
                    save_anim, save_fig, style_axes, title)
from sphere_packing_guide.core import balanced_pair, certificate, transform
from sphere_packing_guide.examples import FOUND_CERTIFICATES

OUT = out_dir("08-balancing")
D = 2
COEFFS = FOUND_CERTIFICATES[D]


def _profiles(r):
    """The stretched certificate, its transform, their difference, the radius.

    The stretch is what makes the two agree at the centre, so their difference
    starts at exactly zero there.  Without it the difference would start at
    some arbitrary height and the whole trick would be lost.
    """
    h, h_hat, g, radius = balanced_pair(COEFFS, D)
    return h(r), h_hat(r), g(r), radius


def balancing_gif(frames=46, fps=12):
    """Subtract the function from its own transform and watch what survives.

    Both curves start at the same height at the centre, so the difference
    starts at zero there.  Subtracting also swaps which one is which under the
    Fourier transform, so the new function turns into minus itself.  The
    animation performs the subtraction, because that is the step, and then
    holds the result.
    """
    r = np.linspace(0, 2.6, 800)
    f, fh, g, radius = _profiles(r)

    fig, ax = plt.subplots(figsize=(8.8, 4.6))
    ax.axhline(0, color=BASELINE, lw=1)
    lf, = ax.plot(r, f, color=BLUE, lw=2.2)
    lh, = ax.plot(r, fh, color=GREEN, lw=2.2)
    lg, = ax.plot([], [], color=VIOLET, lw=2.8)
    ax.text(2.05, float(f.max()) * 0.80, "the certificate", color=BLUE,
            fontsize=9.5)
    ax.text(2.05, float(f.max()) * 0.66, "its transform", color=GREEN,
            fontsize=9.5)
    ax.text(2.05, float(f.max()) * 0.52, "the difference", color=VIOLET,
            fontsize=9.5)
    fig.subplots_adjust(bottom=0.24)
    note = note_below(fig, fontsize=11)
    ax.set_xlim(0, 2.6)
    ax.set_ylim(-0.20, 1.05)
    plot_axes(ax, xlabel="distance from the centre")
    title(ax, "one subtraction, and the function becomes balanced")

    def update(i):
        t = ease(min(i, frames - 1) / (frames - 1))
        lg.set_data(r, t * g)
        note.set_text("subtracting\n"
                      f"value at the centre   {t * float(g[0]):+.4f}")
        return []

    save_anim(fig, update, frames + end_pad(fps), OUT / "balancing.gif", fps=fps)


def trapped_png():
    """Where the negative half of the balanced function is forced to live.

    The balanced function adds up to zero overall, so exactly half of its
    weight is negative.  The certificate's first rule puts the function at or
    below zero from radius one outward, which flips to a statement that the
    balanced function is at or above zero out there.  All of the negative half
    is therefore squeezed inside one ball.
    """
    r = np.linspace(0, 2.6, 800)
    _, _, g, radius = _profiles(r)
    cross = radius

    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    ax.axhline(0, color=BASELINE, lw=1)
    ax.plot(r, g, color=VIOLET, lw=2.6, zorder=4)
    ax.fill_between(r, g, 0, where=(g < 0), color=RED, alpha=0.25, zorder=3)
    ax.fill_between(r, g, 0, where=(g >= 0), color=GREEN, alpha=0.16, zorder=3)
    ax.axvline(cross, color=BASELINE, lw=1.2, ls="--", zorder=2)
    ax.text(cross + 0.08, 0.055, "from here out it is never negative",
            fontsize=9.5, color=INK2, ha="left")
    ax.text(cross * 0.72, 0.062, "all the negative\nweight is in here",
            fontsize=10, color=RED, ha="center")
    ax.set_xlim(0, 2.6)
    ax.set_ylim(-0.12, 0.10)
    plot_axes(ax, xlabel="distance from the centre")
    title(ax, "half the weight is negative, and it has nowhere to go")
    save_fig(fig, OUT / "trapped.png")


if __name__ == "__main__":
    balancing_gif()
    trapped_png()
    print("wrote", OUT)

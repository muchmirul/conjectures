"""Figures for chapter 10: building a certificate that reaches the wall."""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    YELLOW, end_pad, ease, note_below, out_dir, plot_axes,
                    save_anim, save_fig, style_axes, title)
from sphere_packing_guide.core import saddle_radius_constant, wallis_integral

OUT = out_dir("10-the-witness")

GAUSSIAN = 1 / math.sqrt(2 * math.pi)
TARGET = saddle_radius_constant()


def moving_radius_gif(frames=48, fps=12):
    """Turn the deformation on and watch the radius slide to its target.

    A plain Gaussian is the natural starting point, because it is its own
    Fourier transform, but its radius sits at one over the square root of two
    pi, which is too big.  The construction multiplies it by a carefully chosen
    even deformation, which moves the radius without disturbing the symmetry.
    The move is the content, so this moves.
    """
    amounts = np.linspace(0, 1, frames)
    fig, ax = plt.subplots(figsize=(8.8, 4.4))
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0.28, 0.44)
    ax.axhline(GAUSSIAN, color=BASELINE, lw=1.4, ls="--")
    ax.axhline(TARGET, color=VIOLET, lw=1.6, ls="--")
    ax.text(0.02, GAUSSIAN + 0.004, "where a plain Gaussian sits",
            fontsize=9.5, color=MUTED)
    ax.text(0.02, TARGET - 0.011, "where the wall is: one over pi",
            fontsize=9.5, color=VIOLET)
    line, = ax.plot([], [], color=GREEN, lw=2.8)
    dot, = ax.plot([], [], "o", ms=8, color=GREEN)
    fig.subplots_adjust(bottom=0.28)
    note = note_below(fig, fontsize=11)
    plot_axes(ax, xlabel="how much of the deformation is switched on",
              ylabel="radius, per square root of the dimension")
    title(ax, "the Gaussian's radius, moved onto the wall")

    def radius(t):
        return GAUSSIAN * math.exp(-t * 0.5 * math.log(math.pi / 2))

    def update(i):
        j = min(i, frames - 1)
        xs = amounts[:j + 1]
        ys = [radius(t) for t in xs]
        line.set_data(xs, ys)
        dot.set_data([xs[-1]], [ys[-1]])
        note.set_text(f"switched on   {xs[-1]:.2f}\nradius        {ys[-1]:.5f}")
        return []

    save_anim(fig, update, frames + end_pad(fps),
              OUT / "moving_radius.gif", fps=fps)


def wallis_gif(frames=60, fps=12):
    """The integral that supplies the exact amount of movement needed.

    An integral is an area being gathered up, so this draws exactly that: the
    region under the curve fills in from the left, and a gauge on the right
    fills with the total gathered so far.  The gauge settles on the log of pi
    over two, an old identity of Wallis, which is the reason the answer
    contains pi and not some number nobody recognises.
    """
    target = math.log(math.pi / 2)
    a = np.linspace(1e-9, 8, 3000)
    curve = np.exp(-2 * a) * np.tanh(a) / a
    total = np.concatenate([[0], np.cumsum(
        (curve[1:] + curve[:-1]) / 2 * np.diff(a))])

    fig, ax = plt.subplots(figsize=(9.0, 4.4))
    ax.plot(a, curve, color=MUTED, lw=1.6, zorder=3)
    filled = [ax.fill_between(a[:2], curve[:2], color=BLUE, alpha=0.45)]
    # the gauge: a jar on the right that fills with the area gathered so far
    ax.add_patch(plt.Rectangle((8.8, 0), 0.7, 0.5, fill=False, ec=BASELINE,
                               lw=1.4, zorder=4))
    jar = plt.Rectangle((8.8, 0), 0.7, 1e-3, facecolor=BLUE, alpha=0.55,
                        zorder=3)
    ax.add_patch(jar)
    ax.plot([8.62, 9.68], [target, target], color=VIOLET, lw=1.6, ls="--",
            zorder=5)
    ax.text(9.15, 0.56, "the log of\npi over two", color=VIOLET,
            fontsize=9, ha="center", va="bottom")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.08)
    fig.subplots_adjust(bottom=0.24)
    note = note_below(fig, fontsize=11)
    plot_axes(ax, xlabel="distance out along the curve",
              ylabel="the curve being added up")
    ax.set_xticks([0, 2, 4, 6, 8])
    title(ax, "the area piles up and settles on exactly the number needed")

    def update(i):
        t = ease(min(i, frames - 1) / (frames - 1))
        k = max(2, int(t * (len(a) - 1)) + 1)
        filled[0].remove()
        filled[0] = ax.fill_between(a[:k], curve[:k], color=BLUE, alpha=0.45,
                                    zorder=2)
        jar.set_height(max(1e-3, total[k - 1]))
        note.set_text(f"area gathered so far   {total[k - 1]:.4f}      "
                      f"the log of pi over two   {target:.4f}")
        return []

    save_anim(fig, update, frames + end_pad(fps), OUT / "wallis.gif", fps=fps)


if __name__ == "__main__":
    moving_radius_gif()
    wallis_gif()
    print("wrote", OUT)

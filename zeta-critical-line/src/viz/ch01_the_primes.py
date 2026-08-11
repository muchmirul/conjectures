"""Figures for chapter 1: the prime staircase and its wobble."""

import math

import mpmath
import numpy as np
import matplotlib.pyplot as plt

from common import BLUE, GREEN, INK2, MUTED, RED, VIOLET, out_dir, plot_axes, \
    save_fig, title
from zeta_guide.core import primes_up_to

OUT = out_dir("01-the-primes")


def staircase_png():
    """The prime count up to 100, one step per prime."""
    ps = primes_up_to(100)
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    xs = [1] + [p for p in ps for _ in (0, 1)] + [100]
    ys = [0]
    c = 0
    for _ in ps:
        ys += [c, c + 1]
        c += 1
    ys += [c]
    ax.plot(xs, ys, color=BLUE, lw=1.8)
    for p in ps:
        ax.plot([p], [0], marker="|", ms=9, color=VIOLET, mew=1.6)
    ax.annotate("71 and 73 arrive together", xy=(72, 20.4), xytext=(48, 23.2),
                fontsize=9, color=INK2,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
    ax.annotate("a long silence after 89", xy=(93, 24.1), xytext=(70, 17.5),
                fontsize=9, color=INK2,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
    plot_axes(ax, xlabel="numbers from 1 to 100 (primes ticked below)",
              ylabel="primes seen so far")
    title(ax, "the prime staircase: up one step at every prime")
    save_fig(fig, OUT / "staircase.png")


def wobble_png():
    """The true count minus Gauss's smooth guess, up to ten thousand.

    The smooth guess is the logarithmic-integral curve Gauss arrived at;
    subtracting it leaves the wobble whose frequencies are the zeta zeros.
    """
    X = 10_000
    ps = primes_up_to(X)
    xs = np.arange(50, X + 1, 10)
    pi_x = np.searchsorted(ps, xs, side="right")
    li = np.array([float(mpmath.li(float(x))) for x in xs])
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.plot(xs, pi_x - li, color=BLUE, lw=1.2)
    ax.text(150, -1.6, "zero would mean the guess is exact", fontsize=9,
            color=MUTED, va="top")
    plot_axes(ax, xlabel="numbers up to ten thousand",
              ylabel="true count minus the smooth guess")
    title(ax, "what is left when the smooth curve is subtracted: the wobble")
    save_fig(fig, OUT / "wobble.png")


if __name__ == "__main__":
    staircase_png()
    wobble_png()
    print("wrote", OUT)

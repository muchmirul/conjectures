"""Figures for chapter 9: the whole-number trick and its matrix upgrade."""

import numpy as np
import matplotlib.pyplot as plt

from common import BLUE, GREEN, INK2, MUTED, RED, out_dir, plot_axes, \
    save_fig, title
from zeta_guide.core import rank_trace_floor, whole_number_charge, \
    whole_number_floor

OUT = out_dir("09-the-whole-number-trick")


def parabola_png():
    """m squared against 3m - 2, touching at one and two."""
    ms = np.linspace(0.5, 4.4, 200)
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(ms, ms ** 2, color=BLUE, lw=2.0, label="the square")
    ax.plot(ms, 3 * ms - 2, color=MUTED, lw=1.8, ls="--",
            label="three times, minus two")
    for m in (1, 2, 3, 4):
        ax.plot([m], [whole_number_charge(m)], "o", ms=7, color=BLUE)
        ax.plot([m], [whole_number_floor(m)], "o", ms=6, mfc="none",
                mec=GREEN, mew=1.8)
    ax.annotate("even at one and two", xy=(1.5, 2.5), xytext=(0.7, 8.5),
                fontsize=9.5, color=INK2,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
    ax.annotate("from three up, the square\ncharges strictly more",
                xy=(3, 9), xytext=(3.0, 3.0), fontsize=9.5, color=INK2,
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
    ax.legend(loc="upper left", fontsize=9.5, frameon=False)
    plot_axes(ax, xlabel="a pin's multiplicity (always a whole number)",
              ylabel="energy charged")
    title(ax, "the whole-number trick: the square never dips below the line")
    save_fig(fig, OUT / "parabola.png")


def floor_png():
    """Random bowl-and-saddle tables never violate the rank-trace floor.

    Each instance: P a random sum of r bowls (positive semidefinite, rank
    at most r), Q a random mix with at most b upward directions.  The
    inequality promises rank(P) is at least the printed floor; the scatter
    shows floor against actual rank, everything on the safe side.
    """
    rng = np.random.default_rng(7)
    pts = []
    d = 12
    for _ in range(2500):
        r = rng.integers(1, d + 1)
        b = rng.integers(0, 4)
        V = rng.normal(size=(d, r)) * rng.choice([0.3, 1.0, 2.0])
        P = V @ V.T
        W = rng.normal(size=(d, b)) if b else np.zeros((d, 1))
        U = rng.normal(size=(d, 2))
        Q = W @ W.T - U @ U.T * rng.choice([0.0, 0.5, 1.5])
        bq = int(np.sum(np.linalg.eigvalsh(Q) > 1e-9))
        floor = rank_trace_floor(P, Q, bq)
        rank = int(np.linalg.matrix_rank(P, tol=1e-9))
        pts.append((floor, rank))
    floors = np.array([p[0] for p in pts])
    ranks = np.array([p[1] for p in pts])
    assert np.all(ranks >= floors - 1e-7)

    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    keep = floors > -25
    ax.plot([-25, 13], [-25, 13], color=MUTED, lw=1.2, ls="--")
    ax.scatter(floors[keep], ranks[keep], s=10, color=BLUE, alpha=0.35)
    ax.text(-8, 11.7, "safe side: true count at or above the floor",
            fontsize=9.5, color=INK2)
    ax.text(3.5, 0.6, "violations would\nland here", fontsize=9.5, color=RED,
            ha="center")
    plot_axes(ax, xlabel="the floor the inequality guarantees",
              ylabel="the true count of bowl directions")
    title(ax, "2500 random bowl-and-saddle tables: no violation")
    save_fig(fig, OUT / "floor.png")


if __name__ == "__main__":
    parabola_png()
    floor_png()
    print("wrote", OUT)

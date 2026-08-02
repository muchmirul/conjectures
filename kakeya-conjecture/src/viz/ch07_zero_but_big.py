"""Figures for chapter 7: no area left, and still not small."""

import math
from fractions import Fraction

import matplotlib.pyplot as plt

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    out_dir, save_fig, style_axes, title)
from kakeya_guide.dimension import (box_count, box_dimension,
                                    cantor_intervals, cantor_length,
                                    similarity_dimension)

OUT = out_dir("07-zero-but-big")


def cantor_png(levels=7):
    """Throw away the middle third, again and again: the length dies."""
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    style_axes(ax, (-0.03, 1.03), (-levels - 0.6, 0.6), equal=False)
    title(ax, "cut out the middle third, forever")
    for m in range(levels + 1):
        pieces = cantor_intervals(m)
        for lo, hi in pieces:
            ax.add_patch(plt.Rectangle((float(lo), -m - 0.22), float(hi - lo),
                                       0.44, fc=GREEN, ec="none", alpha=0.85,
                                       zorder=3))
        word = "piece " if len(pieces) == 1 else "pieces"
        ax.text(1.05, -m, f"{len(pieces):3d} {word}   "
                          f"length {float(cantor_length(m)):.4f}",
                va="center", ha="left", fontsize=9.5, color=INK2,
                family="monospace")
    save_fig(fig, OUT / "cantor.png")


def boxcount_png(levels=6):
    """Count boxes as they shrink: the count grows, and the slope is the size."""
    ivals = cantor_intervals(levels)
    scales = [Fraction(1, 3) ** m for m in range(1, levels + 1)]
    counts = [box_count(ivals, e) for e in scales]
    dim = box_dimension(list(zip(scales, counts)))

    fig = plt.figure(figsize=(10.2, 4.0))
    grid = fig.add_gridspec(3, 2, width_ratios=[1.3, 1], hspace=0.7,
                            wspace=0.18)
    for row, m in enumerate((1, 2, 3)):
        ax = fig.add_subplot(grid[row, 0])
        style_axes(ax, (-0.02, 1.02), (-0.32, 0.42), equal=False)
        eps = Fraction(1, 3) ** m
        hit = set()
        for lo, hi in ivals:
            hit.update(range(math.floor(lo / eps), math.ceil(hi / eps)))
        for c in sorted(hit):
            ax.add_patch(plt.Rectangle((c * float(eps), -0.18), float(eps),
                                       0.36, fc=BLUE, ec=BLUE, lw=0.6,
                                       alpha=0.22, zorder=3))
        for lo, hi in ivals:
            ax.add_patch(plt.Rectangle((float(lo), -0.06), float(hi - lo), 0.12,
                                       fc=GREEN, ec="none", alpha=0.9,
                                       zorder=4))
        ax.text(0.0, 0.24, f"boxes of side {float(eps):.4f}: "
                           f"{box_count(ivals, eps)}",
                fontsize=10, color=INK2, family="monospace")
        if row == 0:
            title(ax, "cover it with boxes, then shrink them", size=11.5)

    axp = fig.add_subplot(grid[:, 1])
    axp.set_xscale("log")
    axp.set_yscale("log")
    axp.set_xlim(3e-4, 0.6)
    axp.set_ylim(1.5, 200)
    axp.set_xlabel("box size", color=INK2, fontsize=10)
    axp.tick_params(colors=MUTED, labelsize=9)
    for s in ("top", "right"):
        axp.spines[s].set_visible(False)
    for s in ("bottom", "left"):
        axp.spines[s].set_color(BASELINE)
    axp.grid(True, color=GRIDLINE, lw=0.8, zorder=0)
    title(axp, "boxes needed, against box size", size=11.5)
    axp.plot([float(e) for e in scales], counts, "o-", color=VIOLET, lw=2,
             ms=5, zorder=4)
    axp.text(0.05, 0.09, f"slope = {dim:.4f}\n      = log2/log3",
             transform=axp.transAxes, fontsize=11, color=INK2,
             family="monospace")
    save_fig(fig, OUT / "boxcount.png")


def zoo_png():
    """Length and dimension are different questions with different answers."""
    rows = [
        ("a single dot", "0", 0.0, RED),
        ("Cantor set, thirds", "0", similarity_dimension(2, Fraction(1, 3)),
         VIOLET),
        ("Cantor set, quarters", "0", 0.5, VIOLET),
        ("Cantor set x a line", "0", 1 + similarity_dimension(2, Fraction(1, 3)),
         BLUE),
        ("a Besicovitch set", "0", 2.0, GREEN),
        ("a solid square", "1", 2.0, GRIDLINE),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    ax.set_xlim(0, 3.0)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=10, color=INK2)
    ax.set_xlabel("dimension", color=INK2, fontsize=10)
    ax.set_xticks([0, 0.5, 1, 1.5, 2])
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    ax.grid(True, axis="x", color=GRIDLINE, lw=0.8, zorder=0)
    title(ax, "size measured two ways: area (or length) and dimension")
    for n, (name, size, dim, color) in enumerate(rows):
        ax.barh([n], [dim], height=0.5, color=color, alpha=0.85, zorder=3)
        ax.text(dim + 0.06, n, f"dimension {dim:.2f},  area {size}",
                va="center", ha="left", fontsize=9, color=INK2, zorder=5)
    save_fig(fig, OUT / "zoo.png")


if __name__ == "__main__":
    cantor_png()
    boxcount_png()
    zoo_png()
    print(f"wrote figures to {OUT}")

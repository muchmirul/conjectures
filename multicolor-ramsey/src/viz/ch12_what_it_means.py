"""Figures for chapter 12: what was answered, what remains, and the channel payoff."""

import math

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from common import (BASELINE, BLUE, EDGE_COLORS, GREEN, INK2, MUTED, RED,
                    draw_edge, out_dir, plot_axes, ring_positions, save_fig,
                    style_axes, title)
from ramsey_guide.core import C5_CODEBOOK, pentagon_confusable

OUT = out_dir("12-what-it-means")


def sandwich_png():
    """What is now known, and the gap that is still open.

    Both edges of the band grow like the color count raised to a multiple of
    the color count; only the multiple differs, a third below and one above.
    Before 2026 the band's lower edge was exponential, a different kind of
    growth altogether; now the two edges have the same kind of shape and
    only the multiple is unsettled.
    """
    ks = [10 ** (0.05 * i) for i in range(28, 101)]
    # the sizes themselves overflow anything, so the chart shows how many
    # digits they have, which is the honest scale for numbers this large
    lower = [(k / 3) * math.log10(max(k / math.log(k) ** 3, 1.0)) for k in ks]
    upper = [k * math.log10(k) for k in ks]
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ax.plot(ks, upper, color=BLUE, lw=2.0,
            label="ceiling: about the color count, per color")
    ax.plot(ks, lower, color=RED, lw=2.0,
            label="new floor: about its cube root, per color")
    ax.fill_between(ks, lower, upper, color=MUTED, alpha=0.12)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(1, 3e5)
    ax.text(2.4e3, 6e1, "still open:\nwhich power wins", ha="center",
            fontsize=10, color=INK2)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    plot_axes(ax, xlabel="colors (log scale)",
              ylabel="digits in the safe table size (log scale)")
    title(ax, "after 2026: both edges of the gap now grow the same way")
    save_fig(fig, OUT / "sandwich.png")


def channel_png():
    """Shannon's five-symbol channel, and the trick of speaking in pairs.

    Left: five symbols; a gray band joins two symbols the noise can turn
    into each other, so any three symbols include a confusable pair.  Right:
    the five two-letter words of the classic code, every pair of which
    differs safely in some position.  The tests re-check both halves.
    """
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.6),
                             gridspec_kw={"width_ratios": [1, 1.15]})
    ax = axes[0]
    pos = ring_positions(5, radius=0.85)
    style_axes(ax, (-1.35, 1.35), (-1.35, 1.35))
    for i in range(5):
        for j in range(i + 1, 5):
            if pentagon_confusable(i, j):
                draw_edge(ax, pos, i, j, MUTED, lw=5.5, alpha=0.45)
    for i, (x, y) in enumerate(pos):
        ax.add_patch(plt.Circle((x, y), 0.13, fc="white", ec=INK2, lw=1.5,
                                zorder=8))
        ax.text(x, y, "abcde"[i], ha="center", va="center", fontsize=11,
                zorder=9)
    title(ax, "noise confuses neighbours", size=11)

    ax = axes[1]
    style_axes(ax, (-1.7, 3.2), (-0.7, 5.4))
    ax.text(0.75, 5.05, "five safe two-letter words", ha="center",
            fontsize=11, color=INK2)
    for row, word in enumerate(C5_CODEBOOK):
        yy = 4.15 - row * 0.95
        for col, sym in enumerate(word):
            ax.add_patch(Rectangle((col * 0.95, yy), 0.8, 0.7, fc="white",
                                   ec=BASELINE, lw=1.4, zorder=2))
            ax.text(col * 0.95 + 0.4, yy + 0.35, "abcde"[sym], ha="center",
                    va="center", fontsize=12, zorder=3)
    ax.text(0.75, -0.45, "any two rows differ safely somewhere",
            ha="center", fontsize=9.5, color=MUTED)
    save_fig(fig, OUT / "channel.png")


if __name__ == "__main__":
    sandwich_png()
    channel_png()
    print("wrote", OUT)

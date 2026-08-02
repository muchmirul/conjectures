"""Figures for chapter 4: the growth question the whole article is about."""

import matplotlib.pyplot as plt

from common import (BLUE, GREEN, INK2, MUTED, RED, VIOLET, out_dir, plot_axes,
                    save_fig, title)
from ramsey_guide.examples import GF16_BASE, PENTAGON_BASE, PRE_2026_BASE

OUT = out_dir("04-the-question")


def rate_png():
    """The one number the question is about: safe people per color.

    Each bar takes a known safe table and asks how many people it supports
    for each color it spends, measured so that spending the same rate twice
    multiplies the table.  The bars creep upward.  The question is whether
    the creep ever stops.
    """
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    labels = ["the pentagon\n(2 colors, 5 people)",
              "the sixteen table\n(3 colors, 16 people)",
              "the best known\nfixed recipe (2021)",
              "more colors,\nmore colors, ..."]
    values = [PENTAGON_BASE, GF16_BASE, PRE_2026_BASE]
    bars = ax.bar(range(3), values, width=0.55,
                  color=[BLUE, BLUE, VIOLET], alpha=0.85)
    for i, v in enumerate(values):
        ax.text(i, v + 0.08, f"{v:.2f}", ha="center", fontsize=11, color=INK2)
    # the fourth position is the question itself
    ax.bar([3], [PRE_2026_BASE], width=0.55, color=MUTED, alpha=0.15)
    ax.text(3, PRE_2026_BASE + 0.08, "?", ha="center", fontsize=17,
            color=RED)
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, fontsize=8.6)
    ax.set_ylim(0, 4.4)
    plot_axes(ax, ylabel="people supported, per color spent")
    title(ax, "does this number climb forever, or level off?")
    save_fig(fig, OUT / "rate.png")


if __name__ == "__main__":
    rate_png()
    print("wrote", OUT)

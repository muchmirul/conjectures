"""Figures for chapter 3: why you cannot settle this by checking arrangements."""

import math
import random

import matplotlib.pyplot as plt

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    arrow, card, disc, hex_centres, out_dir, save_fig,
                    style_axes, title)

OUT = out_dir("03-cannot-check")


def many_packings_png():
    """Six arrangements out of infinitely many, none of which settles anything."""
    rng = random.Random(4)
    fig, axes = plt.subplots(2, 3, figsize=(9.8, 6.4))
    for n, ax in enumerate(axes.ravel()):
        style_axes(ax, (-0.2, 5.2), (-0.2, 5.2))
        placed = []
        tries = 0
        while len(placed) < 26 and tries < 4000:
            tries += 1
            p = (rng.uniform(0.5, 4.7), rng.uniform(0.5, 4.7))
            if all(math.dist(p, q) >= 1.0 for q in placed):
                placed.append(p)
        for p in placed:
            disc(ax, p, 0.5, color=BLUE, alpha=0.5)
        ax.text(0.5, -0.02, f"{len(placed)} circles", transform=ax.transAxes,
                ha="center", va="top", fontsize=9, color=MUTED)
    fig.suptitle("six arrangements, and there is no end to them",
                 color=INK2, fontsize=12.5)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    save_fig(fig, OUT / "many_packings.png")


if __name__ == "__main__":
    many_packings_png()
    print("wrote", OUT)

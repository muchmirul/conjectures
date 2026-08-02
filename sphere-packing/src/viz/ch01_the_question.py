"""Figures for chapter 1: what packing density is, and who wins in the plane."""

import math

import matplotlib.pyplot as plt

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    disc, end_pad, ease, hex_centres, lerp_centres,
                    note_below, out_dir, plot_axes, save_anim, save_fig,
                    square_centres, style_axes, title)
from sphere_packing_guide.examples import KNOWN_DENSITIES, known_density

OUT = out_dir("01-the-question")

SQUARE_DENSITY = math.pi / 4                 # one circle per unit square
HEX_DENSITY = math.pi / math.sqrt(12)


def rearrange_gif(n=7, frames=44, fps=14):
    """Slide the square arrangement into the hexagonal one.

    The circles never change size and none of them is removed.  All that
    happens is that every other row slides sideways and the rows move closer,
    and the wasted space between them shrinks.  The motion is the argument, so
    this one is an animation rather than two still pictures.
    """
    start = square_centres(n)
    target = hex_centres(n)
    fig, (ax, axb) = plt.subplots(1, 2, figsize=(9.9, 4.6),
                                  gridspec_kw={"width_ratios": [1.35, 1]})
    style_axes(ax, (-0.75, n + 0.30), (-0.75, n - 0.25))
    title(ax, "the same circles, moved")
    circles = [disc(ax, p, 0.5, color=BLUE, alpha=0.5) for p in start]
    fig.subplots_adjust(bottom=0.20)
    note = note_below(fig, fontsize=11.5)

    axb.set_xlim(0, 1)
    axb.set_ylim(0.70, 0.95)
    plot_axes(axb, ylabel="fraction of the plane covered")
    axb.set_xticks([])
    axb.axhline(SQUARE_DENSITY, color=BASELINE, lw=1, ls="--")
    axb.axhline(HEX_DENSITY, color=GREEN, lw=1, ls="--")
    axb.text(0.02, SQUARE_DENSITY + 0.005, "square rows", color=MUTED, fontsize=9)
    axb.text(0.02, HEX_DENSITY + 0.005, "staggered rows", color=GREEN, fontsize=9)
    bar = axb.bar([0.72], [SQUARE_DENSITY], width=0.30, color=BLUE, alpha=0.75)[0]
    title(axb, "how much is covered", size=11.5)

    def update(i):
        t = ease(min(i, frames - 1) / (frames - 1))
        for c, p in zip(circles, lerp_centres(start, target, t)):
            c.center = p
        density = (1 - t) * SQUARE_DENSITY + t * HEX_DENSITY
        bar.set_height(density)
        note.set_text(f"covered   {density * 100:5.2f} %")
        return []

    save_anim(fig, update, frames + end_pad(fps), OUT / "rearrange.gif", fps=fps)


def known_png():
    """The five settled dimensions, each drawn as a hundred equal pieces of space.

    A bar chart asks the reader to translate a height back into an amount.
    Cutting space into a hundred equal pieces and colouring the filled ones
    lets the amount be counted instead: dimension eight keeps twenty five
    pieces, and dimension twenty four keeps less than a fifth of one piece.
    """
    dims = [1, 2, 3, 8, 24]
    values = [known_density(d) for d in dims]
    names = [KNOWN_DENSITIES[d][0] for d in dims]
    panel, gap = 10.0, 4.0
    fig, ax = plt.subplots(figsize=(11.2, 3.6))
    style_axes(ax, (-1, 5 * panel + 4 * gap + 1), (-3.4, 13.2))
    for k, (d, v, nm) in enumerate(zip(dims, values, names)):
        x0 = k * (panel + gap)
        colour = MUTED if d == 1 else BLUE
        # the grid of one hundred pieces
        for g in range(11):
            ax.plot([x0, x0 + panel], [g, g], color=GRIDLINE, lw=0.7, zorder=1)
            ax.plot([x0 + g, x0 + g], [0, panel], color=GRIDLINE, lw=0.7,
                    zorder=1)
        # the filled pieces, counted from the bottom left
        pieces = v * 100
        full = int(pieces)
        for i in range(full):
            ax.add_patch(plt.Rectangle((x0 + i % 10, i // 10), 1, 1,
                                       facecolor=colour, alpha=0.75, zorder=2))
        frac = pieces - full
        if frac > 1e-6:
            ax.add_patch(plt.Rectangle((x0 + full % 10, full // 10), 1, frac,
                                       facecolor=colour, alpha=0.75, zorder=2))
        ax.text(x0 + panel / 2, 12.0, f"{v * 100:.2f} %", ha="center",
                fontsize=10.5, color=INK2)
        ax.text(x0 + panel / 2, 10.6, nm, ha="center", fontsize=8.5,
                color=MUTED)
        ax.text(x0 + panel / 2, -1.9,
                f"{d} dimension" if d == 1 else f"{d} dimensions",
                ha="center", fontsize=9.5, color=INK2)
    title(ax, "each best known packing, drawn as one hundred equal pieces of space")
    save_fig(fig, OUT / "known.png")


def waste_png():
    """Where the wasted space actually sits, in the plane."""
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.7))
    for ax, centres, label, colour in (
            (axes[0], square_centres(5), "square rows", BLUE),
            (axes[1], hex_centres(5), "staggered rows", GREEN)):
        style_axes(ax, (-0.6, 4.1), (-0.6, 4.1))
        ax.add_patch(plt.Rectangle((-0.5, -0.5), 4.5, 4.5, facecolor=RED,
                                   alpha=0.13, zorder=0))
        for p in centres:
            disc(ax, p, 0.5, color=colour, alpha=0.62, zorder=3)
        title(ax, label)
    fig.text(0.5, 0.02, "red is the gap the circles never reach",
             ha="center", color=MUTED, fontsize=10)
    save_fig(fig, OUT / "waste.png")


if __name__ == "__main__":
    rearrange_gif()
    known_png()
    waste_png()
    print("wrote", OUT)

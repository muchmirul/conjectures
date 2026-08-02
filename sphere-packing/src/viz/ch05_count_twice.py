"""Figures for chapter 5: the same total, counted in two places."""

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    YELLOW, end_pad, note_below, out_dir, plot_axes,
                    save_anim, save_fig, style_axes, title)

OUT = out_dir("05-count-twice")


def two_counts_gif(frames=52, fps=12):
    """Run over every pair of centres, then over every frequency instead.

    The left panel adds one number for each pair of ball centres.  Every pair
    that is not a centre with itself sits at distance one or more, where the
    first rule forces the number to be at or below zero, so the running total
    can only be pulled down by them.  The right panel adds one number for each
    frequency, where the second rule forces every number to be at or above
    zero, so that total can only be pushed up.  One quantity, squeezed from
    both sides.  The sweep is the argument, so this moves.
    """
    n = 5
    centres = [(i, j) for i in range(n) for j in range(n)]
    pairs = [(a, b) for a in range(len(centres)) for b in range(len(centres))]
    freqs = [(i, j) for i in range(-2, 3) for j in range(-2, 3)]

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.9, 5.0))
    style_axes(axL, (-0.8, n - 0.2), (-0.8, n - 0.2))
    title(axL, "counted over pairs of centres")
    axL.plot([p[0] for p in centres], [p[1] for p in centres], "o", ms=9,
             color=GRIDLINE, zorder=2)
    link, = axL.plot([], [], color=VIOLET, lw=1.6, zorder=4)
    hi, = axL.plot([], [], "o", ms=10, color=VIOLET, zorder=5)
    fig.subplots_adjust(bottom=0.26)
    noteL = note_below(fig, x=0.012, fontsize=10.5)

    style_axes(axR, (-2.8, 2.8), (-2.8, 2.8))
    title(axR, "counted over frequencies")
    axR.plot([p[0] for p in freqs], [p[1] for p in freqs], "o", ms=9,
             color=GRIDLINE, zorder=2)
    lit = axR.plot([], [], "o", ms=10, color=GREEN, zorder=5)[0]
    noteR = note_below(fig, x=0.52, fontsize=10.5)

    per = max(1, len(pairs) // (frames // 2))

    def update(i):
        i = min(i, frames - 1)
        if i < frames // 2:
            k = min(len(pairs) - 1, (i + 1) * per)
            a, b = pairs[k]
            pa, pb = centres[a], centres[b]
            link.set_data([pa[0], pb[0]], [pa[1], pb[1]])
            hi.set_data([pa[0], pb[0]], [pa[1], pb[1]])
            same = a == b
            noteL.set_text(f"pairs used   {k + 1}\n"
                           + ("this pair is a centre with itself"
                              if same else "distance at least one:\nthis pair "
                                           "can only pull the total down"))
            noteL.set_color(VIOLET if same else RED)
            lit.set_data([], [])
            noteR.set_text("")
        else:
            j = min(len(freqs), (i - frames // 2 + 1) * 3)
            noteL.set_text("every pair beyond the first\ncan only pull it down")
            noteL.set_color(RED)
            lit.set_data([p[0] for p in freqs[:j]], [p[1] for p in freqs[:j]])
            noteR.set_text(f"frequencies used   {j}\n"
                           "each one is at or above zero:\n"
                           "they can only push the total up")
            noteR.set_color(GREEN)
        return []

    save_anim(fig, update, frames + end_pad(fps), OUT / "two_counts.gif", fps=fps)


if __name__ == "__main__":
    two_counts_gif()
    print("wrote", OUT)

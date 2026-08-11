"""Figures for chapter 10: the budget, the dial, and the window race."""

import math

import numpy as np
import matplotlib.pyplot as plt

from common import BASELINE, BLUE, GREEN, INK2, MUTED, RED, TEAL, VIOLET, \
    out_dir, plot_axes, save_fig, title
from zeta_guide.core import CROSSOVER_DIAL, montgomery_taylor_closed_form, \
    ramp, shape_f, shape_h, shape_hd
from zeta_guide.examples import MT_DISTINCT, MT_ON_LINE

OUT = out_dir("10-two-thirds")


def budget_png():
    """The waterfall: four, minus two, minus four thirds, leaves two thirds."""
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    steps = [
        ("the table's count,\nread twice through\nthe pairing", 4.0, BLUE),
        ("the see-saw law's\nprice for allowing\nsaddles", -2.0, RED),
        ("the energy the\nprimes measured", -4 / 3, VIOLET),
        ("clean pins on the\nline, at least", 2 / 3, GREEN),
    ]
    x = 0
    level = 0.0
    for name, v, color in steps[:-1]:
        base = level if v > 0 else level + v
        ax.bar([x], [abs(v)], bottom=[base], width=0.6, color=color,
               alpha=0.85)
        lab = f"+{v:.0f}" if v > 0 else ("−2" if v == -2.0
                                         else "−4/3")
        ax.text(x, level + (0.12 if v > 0 else 0.12), lab, ha="center",
                fontsize=12, color=INK2)
        ax.text(x, -0.62, name, ha="center", fontsize=8.6, color=INK2,
                va="top")
        level += v
        if x < 3:
            ax.plot([x + 0.3, x + 1 - 0.3], [level, level], color=BASELINE,
                    lw=1.0, ls=":")
        x += 1
    name, v, color = steps[-1]
    ax.bar([x], [v], width=0.6, color=color, alpha=0.9)
    ax.text(x, v + 0.12, "2/3", ha="center", fontsize=13, color=GREEN)
    ax.text(x, -0.62, name, ha="center", fontsize=8.6, color=INK2, va="top")
    ax.axhline(0, color=MUTED, lw=0.9)
    ax.set_xlim(-0.6, 3.6)
    ax.set_ylim(-0.5, 4.45)
    ax.set_xticks([])
    plot_axes(ax, ylabel="in units of the full zero count")
    title(ax, "the whole final step: four, minus two, minus four thirds")
    fig.subplots_adjust(bottom=0.24)
    save_fig(fig, OUT / "budget.png")


def dial_png():
    """The three certified shapes as the dial turns."""
    lams = np.linspace(0.3, 1.0, 300)
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.plot(lams, [max(0, shape_h(l)) for l in lams], color=BLUE, lw=2.0,
            label="on the line, and clean")
    ax.plot(lams, [max(shape_hd(l), shape_f(l)) for l in lams], color=GREEN,
            lw=2.0, label="distinct (best of the two certificates)")
    ax.plot(lams, [shape_f(l) for l in lams], color=MUTED, lw=1.6, ls="--",
            label="the weaker certificate alone")
    ax.plot([1.0], [shape_h(1.0)], "o", ms=7, color=BLUE)
    ax.plot([1.0], [shape_hd(1.0)], "o", ms=7, color=GREEN)
    ax.text(1.005, shape_h(1.0), "2/3", fontsize=11, color=BLUE, va="center")
    ax.text(1.005, shape_hd(1.0), "5/6", fontsize=11, color=GREEN,
            va="center")
    ax.axvline(CROSSOVER_DIAL, color=BASELINE, lw=1.0)
    ax.text(CROSSOVER_DIAL + 0.008, 0.06,
            "below here, only the weaker\ncertificate says anything",
            fontsize=8.5, color=INK2)
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    ax.set_xlim(0.3, 1.1)
    ax.set_ylim(0, 1.0)
    plot_axes(ax, xlabel="the dial (the paper's bandwidth; one is the "
                         "natural setting and its proven limit)",
              ylabel="proportion certified")
    title(ax, "every constant, as a function of the dial")
    save_fig(fig, OUT / "dial.png")


def window_race_png():
    """Flat window against the optimised cosine window."""
    s = np.linspace(-0.5, 0.5, 400)
    flat = ramp((0.5 - np.abs(s)) / 0.06)
    cosw = np.cos(math.sqrt(2) * s)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 3.8),
                                   gridspec_kw={"width_ratios": [1.3, 1]})
    ax1.plot(s, flat, color=BLUE, lw=2.0, label="flat window")
    ax1.plot(s, cosw, color=TEAL, lw=2.0, label="optimised window "
                                                "(Montgomery-Taylor)")
    ax1.set_ylim(0, 1.15)
    ax1.legend(loc="lower center", fontsize=9, frameon=False)
    plot_axes(ax1, xlabel="the window profiles compared")
    ax1.set_yticks([0, 1])

    ax2.axis("off")
    rows = [
        ("", "flat", "optimised"),
        ("on the line, clean", "0.6667", f"{MT_ON_LINE:.4f}"),
        ("distinct", "0.8333", f"{MT_DISTINCT:.5f}"),
    ]
    for i, row in enumerate(rows):
        weight = "bold" if i == 0 else "normal"
        ax2.text(0.02, 0.85 - i * 0.28, row[0], fontsize=10.5, color=INK2,
                 fontweight=weight)
        ax2.text(0.62, 0.85 - i * 0.28, row[1], fontsize=10.5, color=INK2,
                 ha="center", family="monospace", fontweight=weight)
        ax2.text(0.94, 0.85 - i * 0.28, row[2], fontsize=10.5, color=INK2,
                 ha="center", family="monospace", fontweight=weight)
    ax2.set_title("what each window certifies", color=INK2, fontsize=10)
    fig.suptitle("a gently curved window buys the last half percent",
                 color=INK2, fontsize=12)
    save_fig(fig, OUT / "window_race.png")


if __name__ == "__main__":
    budget_png()
    dial_png()
    window_race_png()
    print("wrote", OUT)

"""Figure for chapter 12: the proportion line, before and after."""

import matplotlib.pyplot as plt

from common import BASELINE, BLUE, GREEN, INK2, MUTED, RED, VIOLET, out_dir, \
    plot_axes, save_fig, title
from zeta_guide.examples import METHOD_CEILING, MT_ON_LINE, NEW_PROPORTION, \
    OLD_RECORD

OUT = out_dir("12-what-it-means")


def map_png():
    fig, ax = plt.subplots(figsize=(9.2, 4.2))
    ax.barh([0], [NEW_PROPORTION], height=0.34, color=GREEN, alpha=0.75)
    ax.barh([0], [1 - NEW_PROPORTION], left=[NEW_PROPORTION], height=0.34,
            color="#eceae2")
    # the three landmarks near two thirds crowd within 0.015 of each other,
    # so every label is pushed to its own clear spot and points back in
    marks = [
        (OLD_RECORD, "the record until 2026:\n5/12, by Levinson's method",
         BLUE, OLD_RECORD, -0.55, "center"),
        (NEW_PROPORTION, "2026, flat window: 2/3,\nclean and on the line",
         GREEN, 0.485, 0.55, "center"),
        (MT_ON_LINE, "best window:\n0.6725", GREEN, 0.655, -0.55, "center"),
        (METHOD_CEILING, "the method's proven\nceiling: 0.68185", RED, 0.80,
         0.55, "center"),
        (1.0, "all of them:\nthe hypothesis,\nstill open", INK2, 1.0, -0.55,
         "center"),
    ]
    for x, lab, color, lx, ly, ha in marks:
        ax.plot([x, x], [-0.17, 0.17], color=color, lw=2.0, zorder=6)
        ax.annotate(lab, xy=(x, 0.17 if ly > 0 else -0.17), xytext=(lx, ly),
                    fontsize=8.8, color=color, ha=ha,
                    va="bottom" if ly > 0 else "top",
                    arrowprops=dict(arrowstyle="-", color=color, lw=0.9,
                                    shrinkA=2, shrinkB=1, alpha=0.7))
    ax.set_xlim(0.32, 1.09)
    ax.set_ylim(-1.05, 1.05)
    ax.set_yticks([])
    ax.set_xticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plot_axes(ax, xlabel="proportion of the zeros")
    title(ax, "where the certified proportion now stands", size=11.5)
    save_fig(fig, OUT / "map.png")


if __name__ == "__main__":
    map_png()
    print("wrote", OUT)

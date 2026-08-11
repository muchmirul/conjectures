"""Figure for chapter 4: the record race for the proportion on the line."""

import matplotlib.pyplot as plt

from common import BLUE, GREEN, INK2, MUTED, RED, out_dir, plot_axes, \
    save_fig, title
from zeta_guide.examples import RECORD_RACE

OUT = out_dir("04-the-question")


def race_png():
    """One bar per record, in year order; the quality-only results at zero."""
    entries = [(y, v, s) for y, v, s in RECORD_RACE]
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    xs = range(len(entries))
    for x, (year, val, who) in zip(xs, entries):
        color = GREEN if year == 2026 else BLUE
        if val == 0:
            ax.plot([x], [0.008], marker="v", ms=8, color=MUTED)
        else:
            ax.bar([x], [val], width=0.62, color=color, alpha=0.85)
            ax.text(x, val + 0.012, f"{val:.4f}".rstrip("0").rstrip("."),
                    ha="center", fontsize=9, color=INK2)
    ax.axhline(1.0, color=MUTED, lw=0.9, ls="--")
    ax.text(0.05, 1.02, "all of them (the Riemann hypothesis)", fontsize=9,
            color=MUTED)
    short = ["Hardy", "Selberg", "Levinson", "Conrey", "Bui, Conrey,\nYoung",
             "Feng", "Pratt, Robles,\nZaharescu,\nZeindler", "this paper"]
    ax.set_xticks(list(xs))
    ax.set_xticklabels([f"{y}\n{s}" for (y, _, _), s in zip(entries, short)],
                       fontsize=8)
    ax.set_ylim(0, 1.1)
    plot_axes(ax, ylabel="proportion of zeros proved on the line")
    title(ax, "the record race (markers: proved infinite or positive, "
              "but no explicit proportion)")
    save_fig(fig, OUT / "race.png")


if __name__ == "__main__":
    race_png()
    print("wrote", OUT)

"""Figure for chapter 5: one stretch of the strip, four ways to count it.

The stretch drawn is synthetic on purpose: it contains a doubled pin and a
mirror pair, neither of which has ever been observed, so the four counters
can be seen disagreeing.  The caption and the article say it is synthetic.
"""

import matplotlib.pyplot as plt

from common import BASELINE, BLUE, GREEN, INK2, MUTED, RED, VIOLET, out_dir, \
    plot_axes, save_fig, title

OUT = out_dir("05-four-counts")

# (height, kind): kind in {clean, double, pair}
PINS = [(13, "clean"), (21, "clean"), (30, "double"), (38, "clean"),
        (47, "pair"), (56, "clean"), (64, "clean")]


def pins_png():
    fig, ax = plt.subplots(figsize=(8.8, 5.4))
    ax.axvspan(0, 1, color="#f1efe9", zorder=0)
    ax.axvline(0.5, color=BLUE, lw=2.0, zorder=2)
    ax.axvline(0, color=BASELINE, lw=1.0)
    ax.axvline(1, color=BASELINE, lw=1.0)

    full = dist = online = clean = 0
    for h, kind in PINS:
        if kind == "clean":
            ax.plot([0.5], [h], "o", ms=7, color=BLUE, zorder=5)
            full += 1
            dist += 1
            online += 1
            clean += 1
        elif kind == "double":
            ax.plot([0.5], [h], "o", ms=11, mfc="none", mec=VIOLET, mew=2.2,
                    zorder=5)
            ax.plot([0.5], [h], "o", ms=4.5, color=VIOLET, zorder=6)
            ax.annotate("a doubled pin: counts twice in\nthe full count "
                        "(synthetic: none has ever been found)",
                        xy=(0.5, h), xytext=(1.25, h), fontsize=8.5,
                        color=INK2, va="center",
                        arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
            full += 2
            dist += 1
            online += 1
        else:
            ax.plot([0.28, 0.72], [h, h], "o", ms=7, color=RED, zorder=5)
            ax.plot([0.28, 0.72], [h, h], color=RED, lw=0.8, ls=":", zorder=4)
            ax.annotate("a mirror pair: two distinct pins,\nneither on the "
                        "line (synthetic)",
                        xy=(0.72, h), xytext=(1.25, h), fontsize=8.5,
                        color=INK2, va="center",
                        arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
            full += 2
            dist += 2

    tally = (f"the full count      {full}\n"
             f"the distinct count  {dist}\n"
             f"the on-line count   {online}\n"
             f"the clean-line count {clean}")
    ax.text(-1.75, 40, tally, fontsize=10.5, family="monospace", color=INK,
            va="center",
            bbox=dict(boxstyle="round,pad=0.6", fc="white", ec=BASELINE))

    ax.set_xlim(-1.9, 3.1)
    ax.set_ylim(5, 72)
    ax.set_xticks([0, 0.5, 1])
    ax.set_xticklabels(["0", "the line", "1"], fontsize=9)
    plot_axes(ax, ylabel="height")
    title(ax, "one synthetic stretch, tallied four ways", size=11.5)
    save_fig(fig, OUT / "pins.png")


from common import INK  # noqa: E402  (used in the tally box)

if __name__ == "__main__":
    pins_png()
    print("wrote", OUT)

"""Figures for chapter 8: the prime-built density, and the two totals."""

import math

import numpy as np
import matplotlib.pyplot as plt

from common import BLUE, GREEN, INK2, MUTED, RED, VIOLET, end_pad, note_below, \
    out_dir, plot_axes, save_anim, save_fig, title
from zeta_guide.core import ToyFamily, prime_density, von_mangoldt_terms, \
    zero_heights

OUT = out_dir("08-the-prime-side")


def density_gif(fps=10):
    """Prime waves standing up into spikes at the true zero heights."""
    taus = np.linspace(100.0, 140.0, 1200)
    terms = von_mangoldt_terms(16)          # the toy family's whole reach
    zs = [g for g in zero_heights() if 100 <= g <= 140]

    smooth = np.log(taus / (2 * math.pi)) / (2 * math.pi)
    partials = [smooth.copy()]
    for n, w in terms:
        partials.append(partials[-1]
                        - (w / (math.pi * math.sqrt(n)))
                        * np.cos(taus * np.log(n)))

    fig, ax = plt.subplots(figsize=(9.0, 4.6))
    fig.subplots_adjust(bottom=0.16)
    for g in zs:
        ax.axvline(g, color=RED, lw=0.9, alpha=0.6)
    ax.text(zs[0], 1.58, "true zero heights", color=RED, fontsize=9,
            ha="left")
    line, = ax.plot([], [], color=VIOLET, lw=1.6)
    ax.set_xlim(taus[0], taus[-1])
    ax.set_ylim(-1.1, 1.75)
    plot_axes(ax, xlabel="height", ylabel="prime-built density")
    title(ax, "waves from the primes point back at the zeros")
    note = note_below(fig, x=0.5, ha="center", fontsize=11.5)

    hold = 4
    labels = ["the smooth average alone"] + \
        [f"+ the wave of {n}" for n, _ in terms]

    def update(i):
        j = min(i // hold, len(partials) - 1)
        line.set_data(taus, partials[j])
        note.set_text(labels[j] + f"   (prime powers added: {j})")
        note.set_color(GREEN if j == len(partials) - 1 else INK2)
        return []

    frames = len(partials) * hold + end_pad(fps)
    save_anim(fig, update, frames, OUT / "density.gif", fps=fps)


def totals_png():
    """The toy table with its diagonal highlighted, and the two totals.

    Shown in the paper's own units (the table divided by the window constant
    times the window length, its equation 4.4), in which the diagonal total
    should read the zero count and the energy per zero should approach four
    thirds.  At this small size the energy still runs about ten percent hot,
    which the caption and the article both say.
    """
    fam = ToyFamily(T=100.0, dial=1.0)
    G = fam.table_from_zeros(fam.real_zero_config(40, 400))
    us = np.linspace(-fam.L / 2, fam.L / 2, 4001)
    a = float(np.trapezoid(fam.window(us) ** 2, us)) / fam.L
    Ghat = G / (a * fam.L)
    count_total = float(np.trace(Ghat))
    energy_total = float(np.sum(Ghat * Ghat))
    n_window = sum(1 for g in zero_heights() if 100 <= g <= 200)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.4, 4.4),
                                   gridspec_kw={"width_ratios": [1.15, 1]})
    im = ax1.imshow(Ghat, cmap="cividis", origin="lower")
    d = fam.d
    ax1.plot([0, d - 1], [0, d - 1], color=GREEN, lw=1.6, alpha=0.9)
    plot_axes(ax1, xlabel="microphone", ylabel="microphone")
    ax1.set_title("the diagonal, where the count lives", color=INK2,
                  fontsize=10)

    ax2.axis("off")
    lines = [
        ("the count (diagonal total)", f"{count_total:.1f}"),
        ("zeros really in the stretch", f"{n_window}"),
        ("", ""),
        ("the energy (all entries squared)", f"{energy_total:.1f}"),
        ("energy per zero counted, here", f"{energy_total / n_window:.2f}"),
        ("its limit at the natural dial", "4/3 = 1.33"),
        ("", ""),
        ("(the approach is slow, like one", ""),
        ("over the window length)", ""),
    ]
    y = 0.92
    for name, val in lines:
        if name:
            ax2.text(0.02, y, name, fontsize=10.5, color=INK2, va="top")
            ax2.text(0.98, y, val, fontsize=10.5, color=INK, va="top",
                     ha="right", family="monospace")
        y -= 0.105
    ax2.set_title("two totals the primes reveal", color=INK2, fontsize=10)
    save_fig(fig, OUT / "totals.png")


from common import INK  # noqa: E402

if __name__ == "__main__":
    density_gif()
    totals_png()
    print("wrote", OUT)

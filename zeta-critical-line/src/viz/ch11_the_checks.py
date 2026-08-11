"""Figures for chapter 11: the agreement scatter and the synthetic attacks."""

import numpy as np
import matplotlib.pyplot as plt

from common import BLUE, GREEN, INK2, MUTED, RED, VIOLET, out_dir, plot_axes, \
    save_fig, title
from zeta_guide.core import ToyFamily, cs_certificate, positive_directions, \
    zero_heights

OUT = out_dir("11-the-checks")

FAM = ToyFamily(T=100.0, dial=1.0)


def agree_png():
    """Every table entry: computed from zeros against computed from primes."""
    Gz = FAM.table_from_zeros(FAM.real_zero_config(40, 400))
    Gp = FAM.table_from_primes()
    disc = np.max(np.abs(Gz - Gp)) / np.max(np.abs(Gz))

    fig, ax = plt.subplots(figsize=(6.2, 5.6))
    ax.plot([Gz.min(), Gz.max()], [Gz.min(), Gz.max()], color=MUTED, lw=1.0,
            ls="--")
    ax.scatter(Gz.ravel(), Gp.ravel(), s=8, color=BLUE, alpha=0.35)
    ax.text(0.03, 0.97,
            f"{FAM.d * FAM.d} entries\nlargest relative disagreement:\n"
            f"{disc:.1e}",
            transform=ax.transAxes, fontsize=10, color=INK2, va="top",
            family="monospace")
    plot_axes(ax, xlabel="entry, computed from the zeros",
              ylabel="same entry, computed from the primes")
    title(ax, "two computations that share no input agree")
    save_fig(fig, OUT / "agree.png")


def synthetic_png():
    """Hostile synthetic configurations: the certificate stays honest.

    Each configuration keeps the true zero ordinates of the toy stretch but
    changes their nature; the certificate (from the table's two totals) must
    never exceed the true number of clean on-line pins.  The mirror-pair
    depths are synthetic; none has ever been found in the real zeta.
    """
    base = [g for g in zero_heights() if 40 <= g <= 400]
    n_stretch = sum(1 for g in base if 100 <= g <= 200)

    def full_count(zeros):
        """The configuration's own full count in the stretch: multiplicity
        counts, and a mirror pair is two pins."""
        total = 0
        for gamma, m in zeros:
            if 100 <= complex(gamma).real <= 200:
                total += m * (2 if abs(complex(gamma).imag) > 1e-12 else 1)
        return total

    def cert(zeros):
        G = FAM.table_from_zeros(zeros)
        return cs_certificate(G) - full_count(zeros)

    configs = [
        ("the real zeros\n(all clean, on line)",
         [(complex(g), 1) for g in base], n_stretch),
        ("half the heights\nturned into\nmirror pairs",
         [(complex(g), 1) if i % 2 else (g + 0.25j, 1)
          for i, g in enumerate(base)],
         sum(1 for i, g in enumerate(base) if i % 2 and 100 <= g <= 200)),
        ("every pin\ndoubled",
         [(complex(g), 2) for g in base], 0),
        ("every height a\nmirror pair",
         [(g + 0.25j, 1) for g in base], 0),
    ]

    names = [c[0] for c in configs]
    certs = [cert(c[1]) for c in configs]
    truths = [c[2] for c in configs]
    for c, t in zip(certs, truths):
        assert c <= t + 1e-6, (c, t)

    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    xs = np.arange(len(configs))
    ax.bar(xs - 0.19, truths, width=0.36, color=BLUE, alpha=0.85,
           label="true clean on-line pins in the stretch")
    ax.bar(xs + 0.19, certs, width=0.36, color=GREEN, alpha=0.85,
           label="what the certificate claims")
    ax.axhline(0, color=MUTED, lw=0.9)
    ax.set_xticks(xs)
    ax.set_xticklabels(names, fontsize=8.6)
    ax.legend(fontsize=9, frameon=False)
    plot_axes(ax, ylabel="pins")
    title(ax, "attacking the certificate with synthetic configurations: "
              "it never overclaims", size=11)
    save_fig(fig, OUT / "synthetic.png")


if __name__ == "__main__":
    agree_png()
    synthetic_png()
    print("wrote", OUT)

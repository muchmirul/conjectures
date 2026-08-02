"""Figures for chapter 4: the two sign rules, and what they cost."""

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    YELLOW, end_pad, note_below, out_dir, plot_axes,
                    save_anim, save_fig, style_axes, title)
from sphere_packing_guide.core import (certificate, density_bound,
                                       is_admissible, seed_certificate,
                                       transform)
from sphere_packing_guide.examples import FOUND_CERTIFICATES

OUT = out_dir("04-the-certificate")
D = 2


def _panels(fig, coeffs, d=D, rmax=2.4):
    """Draw the function and its transform side by side, with the rules shown."""
    r = np.linspace(0, rmax, 900)
    f = certificate(coeffs, d)(r)
    fh = transform(coeffs, d)(r)
    axL, axR = fig.subplots(1, 2)

    axL.axhline(0, color=BASELINE, lw=1)
    axL.axvspan(1.0, rmax, color=RED, alpha=0.08)
    axL.text(1.72, max(f) * 0.82, "from here out\nit must stay\nat or below zero",
             ha="center", fontsize=9, color=RED)
    lineL, = axL.plot(r, f, color=BLUE, lw=2.4)
    axL.set_xlim(0, rmax)
    plot_axes(axL, xlabel="distance from the centre")
    title(axL, "the function")

    axR.axhline(0, color=BASELINE, lw=1)
    lineR, = axR.plot(r, fh, color=GREEN, lw=2.4)
    axR.set_xlim(0, rmax)
    plot_axes(axR, xlabel="frequency")
    title(axR, "its Fourier transform")
    return axL, axR, lineL, lineR, r


def rules_png():
    """One certificate that passes, with both rules drawn on top of it."""
    fig = plt.figure(figsize=(9.8, 4.3))
    coeffs = FOUND_CERTIFICATES[D]
    axL, axR, _, _, r = _panels(fig, coeffs)
    fh = transform(coeffs, D)(r)
    axR.axhspan(min(-0.05, float(fh.min()) - 0.05), 0, color=RED, alpha=0.08)
    axR.text(1.5, float(fh.max()) * 0.55, "it must never\ndip below zero",
             ha="center", fontsize=9, color=RED)
    fig.suptitle("a certificate is one function obeying both rules at once",
                 color=INK2, fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    save_fig(fig, OUT / "rules.png")


def tuning_gif(frames=48, fps=12):
    """Turn one dial and watch a rule break.

    The dial mixes the working certificate with a small extra amount of one
    building block.  Past a point the transform dips below zero, the second
    rule fails, and the certificate stops proving anything.  Where exactly it
    breaks is mathematics, not decoration, so this one moves.
    """
    base = list(FOUND_CERTIFICATES[D])
    amounts = np.linspace(0.0, 0.30, frames)

    fig = plt.figure(figsize=(9.8, 4.6))
    axL, axR, lineL, lineR, r = _panels(fig, base)
    axR.set_ylim(-0.35, 1.15)
    axL.set_ylim(-0.45, 1.15)
    axR.axhspan(-0.35, 0, color=RED, alpha=0.08)
    fig.subplots_adjust(bottom=0.28)
    note = note_below(fig, fontsize=11)

    def update(i):
        a = amounts[min(i, frames - 1)]
        coeffs = list(base)
        coeffs[1] = base[1] - a
        lineL.set_ydata(certificate(coeffs, D)(r))
        lineR.set_ydata(transform(coeffs, D)(r))
        ok = is_admissible(coeffs, D, samples=8000)
        verdict = "both rules hold" if ok else "the second rule is broken"
        bound = density_bound(coeffs, D)
        shown = f"{bound:.4f}" if ok else "nothing proved"
        note.set_text(f"dial    {a:.3f}\n{verdict}\nbound   {shown}")
        note.set_color(GREEN if ok else RED)
        lineR.set_color(GREEN if ok else RED)
        return []

    save_anim(fig, update, frames + end_pad(fps), OUT / "tuning.gif", fps=fps)


def simple_png():
    """The simplest certificate anyone would write down, in the plane."""
    fig = plt.figure(figsize=(9.8, 4.3))
    coeffs = seed_certificate(D, rho=1.0)
    _panels(fig, coeffs)
    fig.suptitle("the simplest one: it obeys both rules and proves very little",
                 color=INK2, fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    save_fig(fig, OUT / "simple.png")


if __name__ == "__main__":
    rules_png()
    simple_png()
    tuning_gif()
    print("wrote", OUT)

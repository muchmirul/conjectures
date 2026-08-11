"""Figures for chapter 3: zeros are waves, and their sum is the staircase."""

import math

import numpy as np
import matplotlib.pyplot as plt

from common import BLUE, GREEN, INK2, MUTED, RED, VIOLET, end_pad, note_below, \
    out_dir, plot_axes, save_anim, save_fig, title
from zeta_guide.core import psi_from_waves, psi_staircase, zero_heights

OUT = out_dir("03-the-music")

XS = np.linspace(2.0, 50.0, 900)


def one_wave_png():
    """The first zero's wave alone: frequency from its height 14.13."""
    g = zero_heights()[0]
    rho = 0.5 + 1j * g
    wave = -2 * np.sqrt(XS) / abs(rho) * np.cos(g * np.log(XS)
                                                - np.angle(rho))
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.plot(XS, wave, color=BLUE, lw=1.6)
    plot_axes(ax, xlabel="position along the numbers",
              ylabel="this wave's contribution")
    title(ax, "the wave of the first zero (height 14.13): one pure tone")
    save_fig(fig, OUT / "one_wave.png")


def waves_gif(fps=10):
    """Adding zero-waves until the staircase appears.

    The target staircase is the weighted prime tally (each prime power steps
    up by the logarithm of its prime); the rebuild is the explicit formula
    truncated to the first K zeros, with K climbing.
    """
    target = psi_staircase(XS)
    ks = [0, 1, 2, 3, 5, 8, 12, 20, 35, 60, 100]
    curves = [psi_from_waves(XS, k) for k in ks]

    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    fig.subplots_adjust(bottom=0.16)
    ax.plot(XS, target, color=MUTED, lw=1.6, label="the true staircase")
    line, = ax.plot([], [], color=BLUE, lw=1.7,
                    label="smooth ramp + zero-waves")
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    plot_axes(ax, xlabel="position along the numbers",
              ylabel="weighted prime tally")
    title(ax, "waves from the zeros rebuild the prime staircase")
    note = note_below(fig, x=0.5, ha="center", fontsize=12)

    hold = 2  # frames per step

    def update(i):
        j = min(i // hold, len(ks) - 1)
        line.set_data(XS, curves[j])
        note.set_text(f"zero-waves added: {ks[j]:3d}")
        note.set_color(GREEN if j == len(ks) - 1 else INK2)
        return []

    frames = len(ks) * hold + end_pad(fps)
    save_anim(fig, update, frames, OUT / "waves.gif", fps=fps)


if __name__ == "__main__":
    one_wave_png()
    waves_gif()
    print("wrote", OUT)

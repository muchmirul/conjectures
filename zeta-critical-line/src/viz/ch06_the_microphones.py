"""Figures for chapter 6: the window, the microphones, and the real table.

The toy family here is the same one the tests use: the stretch of heights
100 to 200, 44 microphones, window at the natural dial setting.
"""

import numpy as np
import matplotlib.pyplot as plt

from common import BLUE, GREEN, INK2, MUTED, RED, TEAL, VIOLET, YELLOW, \
    end_pad, note_below, out_dir, plot_axes, save_anim, save_fig, title
from zeta_guide.core import ToyFamily

OUT = out_dir("06-the-microphones")

FAM = ToyFamily(T=100.0, dial=1.0)


def window_png():
    """Left: the window shape.  Right: the row of sensitivity bumps."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.4),
                                   gridspec_kw={"width_ratios": [1, 2.1]})
    us = np.linspace(-FAM.L / 2 * 1.25, FAM.L / 2 * 1.25, 400)
    ax1.plot(us, FAM.window(us), color=BLUE, lw=2.0)
    ax1.set_ylim(-0.05, 1.15)
    plot_axes(ax1, xlabel="the window: flat top, gentle ramps")
    ax1.set_yticks([0, 1])

    rs = np.linspace(-6, 6, 500)
    bump = FAM.response(rs)
    bump = bump / bump.max()
    for k in range(7):
        tk = k * FAM.h
        color = BLUE if k % 2 else TEAL
        ax2.plot(rs + tk, bump, color=color, lw=1.5, alpha=0.85)
    ax2.set_xlim(-4, 6 * FAM.h + 4)
    ax2.set_yticks([])
    plot_axes(ax2, xlabel="height axis: one sensitivity bump per microphone, "
                          "evenly spaced")
    fig.suptitle("the window, and the microphones it shapes", color=INK2,
                 fontsize=12)
    save_fig(fig, OUT / "window.png")


def listen_gif(fps=12):
    """A zero sliding between two microphones; the joint entry updates."""
    t1, t2 = 0.0, FAM.h
    rs = np.linspace(-5, t2 + 5, 400)
    b1 = FAM.response(rs - t1)
    b2 = FAM.response(rs - t2)
    peak = float(FAM.response(np.array([0.0]))[0])

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    fig.subplots_adjust(bottom=0.16)
    ax.plot(rs, b1 / peak, color=TEAL, lw=1.8)
    ax.plot(rs, b2 / peak, color=BLUE, lw=1.8)
    ax.text(t1, 1.06, "microphone A", ha="center", fontsize=9, color=TEAL)
    ax.text(t2, 1.06, "microphone B", ha="center", fontsize=9, color=BLUE)
    ax.axhline(0, color=MUTED, lw=0.8)
    zline = ax.axvline(0, color=RED, lw=2.0)
    dotA, = ax.plot([], [], "o", ms=8, color=TEAL, zorder=6)
    dotB, = ax.plot([], [], "o", ms=8, color=BLUE, zorder=6)
    ax.set_ylim(-0.4, 1.18)
    ax.set_yticks([])
    plot_axes(ax, xlabel="height axis (the red line is a zero)")
    title(ax, "one zero rings both microphones")
    note = note_below(fig, x=0.5, ha="center", fontsize=11.5)

    path = np.concatenate([np.linspace(-3.5, t2 + 3.5, 84)])

    def update(i):
        g = path[min(i, len(path) - 1)]
        zline.set_xdata([g, g])
        a = float(FAM.response(np.array([g - t1]))[0]) / peak
        b = float(FAM.response(np.array([g - t2]))[0]) / peak
        dotA.set_data([g], [a])
        dotB.set_data([g], [b])
        note.set_text(f"A hears {a:+.2f}   B hears {b:+.2f}   "
                      f"their table entry gets {a * b:+.2f}")
        return []

    frames = len(path) + end_pad(fps)
    save_anim(fig, update, frames, OUT / "listen.gif", fps=fps)


def table_png():
    """The real 44-by-44 table from the zeros near the toy stretch."""
    zeros = FAM.real_zero_config(40, 400)
    G = FAM.table_from_zeros(zeros)
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    im = ax.imshow(G, cmap="cividis", origin="lower")
    fig.colorbar(im, ax=ax, shrink=0.8, label="entry value")
    plot_axes(ax, xlabel="microphone", ylabel="microphone")
    title(ax, f"the table for heights 100 to 200: {FAM.d} microphones, "
              f"built from {len(zeros)} real zeros", size=10.5)
    save_fig(fig, OUT / "table.png")


if __name__ == "__main__":
    window_png()
    listen_gif()
    table_png()
    print("wrote", OUT)

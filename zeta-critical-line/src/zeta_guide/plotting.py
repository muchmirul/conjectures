"""Matplotlib helpers shared by every figure and animation in the guide.

Visual language (kept consistent across all chapters):

* blue    = the critical line and anything sitting on it
* red     = anything off the line (always synthetic: none has been found)
* green   = a verdict, a certificate, anything proved
* violet  = the primes and everything computed from them
* thin warm-gray = scaffolding: axes, the strip, guide lines

Colors come from the repository's shared palette; figures render on a
near-white surface so they read on both light and dark GitHub themes.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# --- palette ---------------------------------------------------------------

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

BLUE = "#2a78d6"
GREEN = "#008300"    # a verdict, anything proved
RED = "#d03b3b"      # off the line, always synthetic
VIOLET = "#4a3aa7"   # the primes' color
YELLOW = "#eda100"
TEAL = "#00787a"
BROWN = "#8a5a2c"

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.family": "sans-serif",
    "font.size": 11,
    "text.color": INK,
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK2,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.grid": False,
    "figure.dpi": 110,
})


# --- axes ------------------------------------------------------------------

def style_axes(ax, xlim=None, ylim=None, equal=True):
    """Recessive chart chrome: no box, no ticks, just the drawing."""
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    if equal:
        ax.set_aspect("equal")
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)


def plot_axes(ax, xlabel=None, ylabel=None):
    """A chart that keeps its numbers: ticks stay, the box goes."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(BASELINE)
    if xlabel:
        ax.set_xlabel(xlabel, color=INK2, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, color=INK2, fontsize=10)
    ax.tick_params(labelsize=9)


def style_3d(ax):
    """Recessive chrome for the rotating surface shots."""
    ax.set_facecolor(SURFACE)
    for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane.set_pane_color((1, 1, 1, 0))
        pane.line.set_color(BASELINE)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(False)


def title(ax, text, size=12):
    ax.set_title(text, color=INK2, fontsize=size)


def readout(ax, xy, text, color=INK2, fontsize=13, mono=True, ha="left"):
    """A live number in the corner of an animation."""
    return ax.text(*xy, text, transform=ax.transAxes, ha=ha, va="top",
                   fontsize=fontsize, color=color,
                   family="monospace" if mono else "sans-serif", zorder=10)


def card(ax, xy, wh, text, color=BLUE, fontsize=13, alpha=1.0, zorder=6):
    """A rounded box with a line of text, for the statement cards."""
    box = FancyBboxPatch(xy, *wh, boxstyle="round,pad=0.12,rounding_size=0.18",
                         fc="white", ec=color, lw=2.0, zorder=zorder,
                         alpha=alpha)
    ax.add_patch(box)
    t = ax.text(xy[0] + wh[0] / 2, xy[1] + wh[1] / 2, text, ha="center",
                va="center", fontsize=fontsize, color=INK, zorder=zorder + 1,
                alpha=alpha)
    return box, t


def arrow(ax, p, q, color=INK2, lw=2, style="-|>", curve=0.0, zorder=5):
    a = FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=15, color=color,
                        lw=lw, connectionstyle=f"arc3,rad={curve}", zorder=zorder)
    ax.add_patch(a)
    return a


# --- animation -------------------------------------------------------------

def ease(t):
    return 3 * t ** 2 - 2 * t ** 3


def _snap_to_even_pixels(fig):
    """Round the canvas to an even number of pixels each way.

    An odd pixel width comes out of the GIF writer sheared, every row slipping
    one pixel sideways, so every animation is nudged onto even dimensions
    before it is written.
    """
    dpi = fig.get_dpi()

    def even_inches(v):
        px = max(2, int(round(v * dpi / 2)) * 2)
        return (px + 0.25) / dpi      # the slack survives the writer's floor

    w, h = fig.get_size_inches()
    fig.set_size_inches(even_inches(w), even_inches(h))


def save_anim(fig, update, frames, out_path, fps=20):
    _snap_to_even_pixels(fig)
    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / fps)
    anim.save(out_path, writer=PillowWriter(fps=fps))
    plt.close(fig)
    return out_path


def save_fig(fig, path, dpi=150):
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    return path

"""Matplotlib helpers shared by every figure and animation in the guide.

Visual language (kept consistent across all chapters):

* the edge colors of a coloring are always drawn from EDGE_COLORS, in order,
  so color 0 is red in every chapter, color 1 is blue, and so on
* green   = a verdict of safe, and anything proved
* a red flash / thick outline = a one-color triangle being exhibited
* thin warm-gray = scaffolding: circles vertices sit on, boxes, guide lines

Colors come from a validated colorblind-safe-leaning palette; figures render
on a near-white surface so they read on both light and dark GitHub themes.
"""

from __future__ import annotations

import math

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

# --- palette ---------------------------------------------------------------

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

BLUE = "#2a78d6"
GREEN = "#008300"    # a verdict of safe, anything proved
RED = "#d03b3b"
VIOLET = "#4a3aa7"
YELLOW = "#eda100"
TEAL = "#00787a"
BROWN = "#8a5a2c"

#: the colors of a coloring, in the order the chapters use them: color 0 is
#: always this red, color 1 always this blue, and so on, in every figure
EDGE_COLORS = [RED, BLUE, YELLOW, VIOLET, TEAL, GREEN, BROWN]

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


# --- drawing colorings ------------------------------------------------------

def ring_positions(n: int, radius: float = 1.0,
                   centre=(0.0, 0.0), phase: float = math.pi / 2) -> list:
    """Vertices spread evenly on a circle, starting from the top."""
    return [(centre[0] + radius * math.cos(phase + 2 * math.pi * i / n),
             centre[1] + radius * math.sin(phase + 2 * math.pi * i / n))
            for i in range(n)]


def draw_vertices(ax, pos, r=0.055, color=INK, zorder=8, labels=None,
                  label_offset=1.16, fontsize=10):
    """The dots people sit at, drawn above the strings between them."""
    for i, (x, y) in enumerate(pos):
        ax.add_patch(Circle((x, y), r, facecolor="white", edgecolor=color,
                            lw=1.6, zorder=zorder))
    if labels:
        for i, (x, y) in enumerate(pos):
            ax.text(x * label_offset, y * label_offset, str(labels[i]),
                    ha="center", va="center", fontsize=fontsize, color=MUTED,
                    zorder=zorder)


def draw_edge(ax, pos, i, j, color, lw=1.8, alpha=0.85, zorder=3):
    (x0, y0), (x1, y1) = pos[i], pos[j]
    return ax.plot([x0, x1], [y0, y1], color=color, lw=lw, alpha=alpha,
                   zorder=zorder, solid_capstyle="round")[0]


def draw_coloring(ax, coloring, pos, lw=1.8, alpha=0.85, zorder=3,
                  only_color=None):
    """Every colored edge of a coloring, in the shared edge palette."""
    n = len(coloring)
    artists = []
    for i in range(n):
        for j in range(i + 1, n):
            c = int(coloring[i, j])
            if c < 0 or (only_color is not None and c != only_color):
                continue
            artists.append(draw_edge(ax, pos, i, j, EDGE_COLORS[c], lw=lw,
                                     alpha=alpha, zorder=zorder))
    return artists


def flash_triangle(ax, pos, tri, color, lw=5.0, zorder=6):
    """Thicken the three sides of the triangle being exhibited."""
    i, j, k = tri
    return [draw_edge(ax, pos, a, b, color, lw=lw, alpha=0.95, zorder=zorder)
            for a, b in ((i, j), (j, k), (i, k))]


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

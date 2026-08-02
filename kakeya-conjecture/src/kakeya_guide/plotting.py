"""Matplotlib helpers shared by every figure and animation in the guide.

Visual language (kept consistent across all chapters):

* blue   = the needle, and the directions it has to hit
* green  = a region that is doing its job (a set the needle turns inside)
* red    = wasted area, the thing every construction is fighting
* yellow = the patch of area being measured right now
* thin warm-gray = scaffolding: the original triangle, grid lines, guides

Colors come from a validated colorblind-safe palette; figures render on a
near-white surface so they read on both light and dark GitHub themes.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

# --- palette ---------------------------------------------------------------

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

BLUE = "#2a78d6"     # the needle
GREEN = "#008300"    # a region that works
RED = "#d03b3b"      # wasted area
VIOLET = "#4a3aa7"   # highlighted direction
YELLOW = "#eda100"   # area under the spotlight

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

def style_axes(ax, xlim=None, ylim=None, equal=True, baseline=False):
    """Recessive chart chrome: no box, no ticks, optional ground line."""
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
    if baseline:
        ax.axhline(0, color=BASELINE, lw=1, zorder=1)


def title(ax, text, size=12):
    ax.set_title(text, color=INK2, fontsize=size)


# --- slivers and figures ---------------------------------------------------

def sliver_patch(s, color=GREEN, alpha=0.32, lw=0.0, zorder=3, edge=None):
    """One triangle of a Perron tree as a matplotlib patch."""
    pts = [(float(x), float(y)) for x, y in s.polygon()]
    return Polygon(pts, closed=True, facecolor=color, alpha=alpha,
                   edgecolor=edge or color, lw=lw, zorder=zorder)


def outline(ax, pts, color=INK2, lw=1.4, zorder=5, ls="-"):
    xs = [p[0] for p in pts] + [pts[0][0]]
    ys = [p[1] for p in pts] + [pts[0][1]]
    ax.plot(xs, ys, color=color, lw=lw, zorder=zorder, ls=ls)


def shade(ax, pts, color=GREEN, alpha=0.25, zorder=2, edge_lw=0.0):
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, alpha=alpha,
                         edgecolor=color, lw=edge_lw, zorder=zorder))


# --- labels and cards ------------------------------------------------------

def card(ax, xy, wh, text, color=BLUE, fontsize=13, alpha=1.0, zorder=6):
    """A rounded box with a line of text: used for the statement cards."""
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


def readout(ax, xy, text, color=INK2, fontsize=13, mono=True, ha="left"):
    """A live number in the corner of an animation (area so far, and so on)."""
    return ax.text(*xy, text, transform=ax.transAxes, ha=ha, va="top",
                   fontsize=fontsize, color=color,
                   family="monospace" if mono else "sans-serif", zorder=10)


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


# --- three dimensions, seen from all sides ---------------------------------

def axes_3d(fig, position=111, box=1.15, elev=18):
    """A bare 3D axes: no panes, no ticks, just the shape and its axes."""
    ax = fig.add_subplot(position, projection="3d")
    ax.set_xlim(-box, box)
    ax.set_ylim(-box, box)
    ax.set_zlim(-box, box)
    ax.set_box_aspect((1, 1, 1))
    ax.set_axis_off()
    ax.view_init(elev=elev, azim=0)
    return ax


def compass_3d(ax, length=1.0, labels=("x", "y", "z")):
    """Three arrows out of the origin, so the reader can see which way is which."""
    dirs = [(length, 0, 0), (0, length, 0), (0, 0, length)]
    for (dx, dy, dz), name in zip(dirs, labels):
        ax.plot([0, dx], [0, dy], [0, dz], color=BASELINE, lw=1.2, zorder=1)
        ax.text(dx * 1.09, dy * 1.09, dz * 1.09, name, color=MUTED,
                fontsize=9, zorder=1)


def spin_gif(fig, axes, out_path, frames=48, fps=14, elev=18, turn=360):
    """Rotate the camera right round a 3D scene and write it as a GIF.

    A still picture of three dimensional space is a lie by omission: the depth
    is exactly what the reader cannot see.  Spinning the point of view is the
    cheapest honest fix.
    """
    axes = axes if isinstance(axes, (list, tuple)) else [axes]

    def update(i):
        for ax in axes:
            ax.view_init(elev=elev, azim=turn * i / frames)
        return []

    return save_anim(fig, update, frames, out_path, fps=fps)


def save_fig(fig, path, dpi=150):
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    return path


# --- small plots -----------------------------------------------------------

def area_curve(ax, xs, ys, color=RED, label=None, marker="o"):
    ax.plot(xs, ys, marker=marker, color=color, lw=2, ms=5, label=label,
            zorder=4)
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("bottom", "left"):
        ax.spines[s].set_color(BASELINE)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.grid(True, color=GRIDLINE, lw=0.8, zorder=0)

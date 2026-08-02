"""Matplotlib helpers shared by every figure and animation in the guide.

Visual language (kept consistent across all chapters):

* blue   = balls, and the packing itself
* green  = a certificate doing its job, and anything proved
* red    = wasted space, and any rule being broken
* yellow = the quantity being measured right now
* thin warm-gray = scaffolding: boxes, grids, guide lines

Colors come from a validated colorblind-safe palette; figures render on a
near-white surface so they read on both light and dark GitHub themes.
"""

from __future__ import annotations

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

BLUE = "#2a78d6"     # the balls, the packing
GREEN = "#008300"    # a certificate that works, anything proved
RED = "#d03b3b"      # wasted space, a rule broken
GOOD = "#0ca30c"
VIOLET = "#4a3aa7"   # the quantity under discussion
YELLOW = "#eda100"   # what is being measured right now

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


def disc(ax, centre, radius, color=BLUE, alpha=0.55, lw=0.0, zorder=3,
         edge=None):
    """One ball, seen flat."""
    c = Circle(centre, radius, facecolor=color, alpha=alpha, lw=lw,
               edgecolor=edge or color, zorder=zorder)
    ax.add_patch(c)
    return c


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


def ball_3d(ax, centre, radius, color=BLUE, alpha=0.32, n=26, zorder=3):
    """One ball drawn as a surface, so it reads as solid rather than as a disc."""
    u = np.linspace(0, 2 * np.pi, n)
    v = np.linspace(0, np.pi, n)
    x = centre[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = centre[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = centre[2] + radius * np.outer(np.ones_like(u), np.cos(v))
    return ax.plot_surface(x, y, z, color=color, alpha=alpha, linewidth=0,
                           shade=True, zorder=zorder)


def wire_cube(ax, half=1.0, color=BASELINE, lw=1.0):
    """The box a ball is being compared against."""
    pts = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
           (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]
    for i, j in edges:
        a, b = pts[i], pts[j]
        ax.plot([half * a[0], half * b[0]], [half * a[1], half * b[1]],
                [half * a[2], half * b[2]], color=color, lw=lw, zorder=1)


def spin_gif(fig, axes, out_path, frames=48, fps=14, elev=18, turn=360):
    """Rotate the camera right round a 3D scene and write it as a GIF.

    A still picture of three dimensional space is a lie by omission: the depth
    is exactly what the reader cannot see.  Spinning the point of view is the
    cheapest honest fix.  These loop seamlessly and deliberately carry no end
    pause, because the motion is the whole content.
    """
    axes = axes if isinstance(axes, (list, tuple)) else [axes]

    def update(i):
        for ax in axes:
            ax.view_init(elev=elev, azim=turn * i / frames)
        return []

    return save_anim(fig, update, frames, out_path, fps=fps)


def rotate_4d(points, angle, planes=((0, 3),)):
    """Turn a set of four dimensional points in the chosen coordinate planes.

    Four dimensions cannot be drawn, but they can be turned and then shadowed
    down into three, and the way the shadow moves is what a reader can actually
    learn from.  Each plane is a pair of axes that the rotation mixes.
    """
    pts = np.array(points, dtype=float)
    for i, j in planes:
        c, s = np.cos(angle), np.sin(angle)
        a, b = pts[:, i].copy(), pts[:, j].copy()
        pts[:, i] = c * a - s * b
        pts[:, j] = s * a + c * b
    return pts


def project_to_3d(points, distance=3.0):
    """Cast four dimensional points into three, the way a lamp casts shadows."""
    pts = np.asarray(points, dtype=float)
    scale = distance / (distance - pts[:, 3])
    return pts[:, :3] * scale[:, None]

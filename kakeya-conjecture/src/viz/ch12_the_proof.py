"""Figures for chapter 12: February 2025, and what is still open.

The theorem is about three dimensional space, so both figures here are actually
three dimensional and the camera goes right round them: a still picture of 3D
hides the one thing the reader needs to see.  The timeline and the status table
are typed into the chapter instead of drawn, and tests/test_guide.py checks them
against the data in kakeya_guide.examples.
"""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    YELLOW, out_dir, readout, save_fig, style_axes, title)
from kakeya_guide.core import extrusion_holds_direction, union_area
from kakeya_guide.examples import tree
from kakeya_guide.plotting import axes_3d, compass_3d, spin_gif

OUT = out_dir("12-the-proof")




def volume_gif(n_tubes=90, frames=32, fps=12):
    """Tubes pointing every way in space, with the camera going round them.

    What Wang and Zahl proved is a statement about exactly this picture: put
    thin tubes in space pointing in every direction and their union cannot be
    squeezed thin.  Directions are spread over the sphere with the golden angle
    so no accidental pattern creeps in.
    """
    fig = plt.figure(figsize=(5.4, 5.4))
    ax = axes_3d(fig, box=0.72, elev=16)
    compass_3d(ax, 0.66)
    golden = math.pi * (3 - math.sqrt(5))
    rng = np.random.default_rng(2025)
    for j in range(n_tubes):
        z = 1 - (j + 0.5) * 2 / n_tubes          # uniform over the sphere
        r = math.sqrt(max(0.0, 1 - z * z))
        phi = golden * j
        d = np.array([r * math.cos(phi), r * math.sin(phi), z])
        mid = rng.normal(0, 0.11, 3)             # tubes need not share a point
        p, q = mid - 0.5 * d, mid + 0.5 * d
        ax.plot(*zip(p, q), color=BLUE if j % 3 else VIOLET, lw=2.6,
                alpha=0.32, solid_capstyle="round", zorder=3)
    ax.text2D(0.02, 0.97, f"{n_tubes} directions in space\ndimension 3",
              transform=ax.transAxes, va="top", fontsize=11, color=INK2,
              family="monospace")
    spin_gif(fig, ax, OUT / "volume.gif", frames=frames, fps=fps, elev=16)


def kakeya3d_gif(k=4, half=0.5, frames=32, fps=12):
    """A Kakeya set of space you can turn around in your hand.

    Take the flat Perron tree of chapter 5 and push it sideways into a slab.
    A unit segment of space pointing along (a, b, c) casts a shadow on the
    plane that is *shorter* than a unit, so it fits inside the segment the flat
    tree already holds, while the height it needs is covered by the slab.  So
    the extruded tree holds every direction of space whose shadow lies in the
    tree's fan, and four rotated copies hold the rest.  Checked in
    tests/test_core.py, not asserted here.
    """
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    figure = tree(k)
    area = float(union_area(figure))
    xs = [float(v) for s in figure for v in (s.b0, s.b1, s.ax)]
    cx, cy = (min(xs) + max(xs)) / 2, 0.5          # centre it on the origin

    fig = plt.figure(figsize=(5.6, 5.6))
    ax = axes_3d(fig, box=0.72, elev=16)

    faces = []
    for s in figure:
        b0, b1, apex, h = (float(s.b0) - cx, float(s.b1) - cx,
                           float(s.ax) - cx, float(s.h))
        corners = [(b0, -cy), (b1, -cy), (apex, h - cy)]
        for z in (-half, half):                    # the two flat copies
            faces.append([(x, y, z) for x, y in corners])
        for (x0, y0), (x1, y1) in zip(corners, corners[1:] + corners[:1]):
            faces.append([(x0, y0, -half), (x1, y1, -half),
                          (x1, y1, half), (x0, y0, half)])
    solid = Poly3DCollection(faces, facecolor=GREEN, edgecolor="none",
                             alpha=0.09, zorder=3)
    ax.add_collection3d(solid)

    # a needle that genuinely lies inside the slab, and leans out of the plane
    widest = max(figure, key=lambda s: s.ax)
    lo, hi = (float(v) for v in widest.direction_interval())
    run = (lo + hi) / 2
    rise = 0.5                                     # how much of it points along z
    flat = math.sqrt(1 - rise ** 2) / math.hypot(run, 1.0)
    start = np.array([float(widest.ax) - cx, 1.0 - cy, -rise / 2])
    d = np.array([run * flat, -flat, rise])
    ax.plot(*zip(start, start + d), color=BLUE, lw=4.5, solid_capstyle="round",
            zorder=9)
    ax.text2D(0.02, 0.97,
              f"the flat tree, {2 ** k} slivers of area {area:.3f},\n"
              f"pushed sideways into a slab of space",
              transform=ax.transAxes, va="top", fontsize=10.5, color=INK2,
              family="monospace")
    ax.text2D(0.02, 0.06,
              "the blue needle points out of the flat plane\n"
              "and still lies inside the solid",
              transform=ax.transAxes, va="bottom", fontsize=10, color=BLUE)
    spin_gif(fig, ax, OUT / "kakeya3d.gif", frames=frames, fps=fps, elev=16)


if __name__ == "__main__":
    volume_gif()
    kakeya3d_gif()
    print(f"wrote figures to {OUT}")

"""Figures for chapter 10: Kakeya on a finite grid, and Dvir's proof."""

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    YELLOW, out_dir, readout, save_fig, style_axes, title)
from kakeya_guide.finite import (directions, dvir_bound, greedy_kakeya_set,
                                 grid, kakeya_table, line, min_kakeya_size,
                                 tangent_line_kakeya)
from kakeya_guide.plotting import axes_3d, spin_gif

OUT = out_dir("10-on-a-grid")


def grid_png(q=7):
    """The smallest Kakeya set of the grid, and the line it holds per direction."""
    size, K = min_kakeya_size(q, 2, return_set=True)
    dirs = directions(q, 2)
    chosen = []
    for b in dirs:                       # recover which lines the answer used
        for a in sorted(K):
            L = line(a, b, q)
            if L <= K:
                chosen.append((b, sorted(L)))
                break

    fig, (ax, axd) = plt.subplots(1, 2, figsize=(10.2, 5.2),
                                  gridspec_kw={"width_ratios": [1, 1]})
    style_axes(ax, (-0.75, q - 0.25), (-0.75, q - 0.25))
    title(ax, f"the smallest Kakeya set in the grid F_{q} x F_{q}\n"
              f"{size} of {q * q} points, holding {len(dirs)} directions",
          size=11.5)
    for x in range(q):
        for y in range(q):
            ax.add_patch(plt.Rectangle((x - 0.42, y - 0.42), 0.84, 0.84,
                                       fc=GRIDLINE, ec="none", alpha=0.5,
                                       zorder=2))
    for x, y in K:
        ax.add_patch(plt.Rectangle((x - 0.42, y - 0.42), 0.84, 0.84, fc=GREEN,
                                   ec="none", alpha=0.85, zorder=3))

    # one panel per direction: which line of that direction the set contains
    style_axes(axd, (-0.75, q - 0.25), (-0.75, q - 0.25))
    title(axd, "the line it holds in each direction", size=11.5)
    for x in range(q):
        for y in range(q):
            axd.add_patch(plt.Rectangle((x - 0.42, y - 0.42), 0.84, 0.84,
                                        fc=GRIDLINE, ec="none", alpha=0.35,
                                        zorder=2))
    palette = [BLUE, VIOLET, GREEN, RED, YELLOW, "#0f8a8a", "#a2377f", "#6b6b1f"]
    for n, (b, L) in enumerate(chosen):
        color = palette[n % len(palette)]
        for x, y in L:
            axd.add_patch(plt.Circle((x, y), 0.17 + 0.035 * (n % 3), fc=color,
                                     ec="none", alpha=0.75, zorder=3 + n))
    axd.text(0.5, -0.06, "one colour per direction, wrapping around the edges",
             transform=axd.transAxes, ha="center", fontsize=9.5, color=MUTED)
    save_fig(fig, OUT / "grid.png")


def grid3d_gif(q=3, frames=32, fps=11):
    """The same question one dimension up, and actually shown in 3D.

    The grid F_3^3 is 27 points with 13 directions through it.  A greedy sweep
    finds a Kakeya set of 15 of those points, above Dvir's floor of 10.  The
    camera goes round because the whole point of this figure is that the third
    axis is real.
    """
    K = greedy_kakeya_set(q, 3)
    dirs = directions(q, 3)
    fig = plt.figure(figsize=(6.0, 6.0))
    ax = axes_3d(fig, box=q - 0.35, elev=18)
    ax.set_xlim(-0.6, q - 0.4)
    ax.set_ylim(-0.6, q - 0.4)
    ax.set_zlim(-0.6, q - 0.4)

    pts = np.array([p for p in grid(q, 3)])
    inside = np.array([p in K for p in map(tuple, pts)])
    ax.scatter(*pts[~inside].T, s=26, color=GRIDLINE, alpha=0.9,
               depthshade=False, zorder=2)
    ax.scatter(*pts[inside].T, s=95, color=GREEN, alpha=0.85,
               depthshade=False, zorder=4)

    # one held line per direction, drawn where it does not wrap around
    for b in dirs:
        for a in sorted(K):
            L = line(a, b, q)
            if L <= K:
                run = np.array([[(a[i] + t * b[i]) for i in range(3)]
                                for t in range(q)], float)
                if run.max() < q:                 # skip the wrapped ones
                    ax.plot(*run.T, color=VIOLET, lw=1.6, alpha=0.5, zorder=3)
                break
    ax.text2D(0.02, 0.98,
              f"F_{q} x F_{q} x F_{q}: {q ** 3} points, {len(dirs)} directions\n"
              f"a Kakeya set of {len(K)}, floor {dvir_bound(q, 3)}\n"
              f"(lines that wrap round the edges are left undrawn)",
              transform=ax.transAxes, va="top", fontsize=10.5, color=INK2,
              family="monospace")
    spin_gif(fig, ax, OUT / "grid3d.gif", frames=frames, fps=fps, elev=18)


def counts_png():
    """The whole grid, Dvir's floor, and the true smallest set."""
    rows = kakeya_table((2, 3, 5, 7))
    fig, ax = plt.subplots(figsize=(7.8, 4.0))
    xs = np.arange(len(rows))
    ax.set_xticks(xs)
    ax.set_xticklabels([f"q = {r['q']}" for r in rows], fontsize=11,
                       color=INK2)
    ax.set_ylim(0, max(r["grid"] for r in rows) * 1.15)
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("bottom", "left"):
        ax.spines[s].set_color(BASELINE)
    ax.grid(True, axis="y", color=GRIDLINE, lw=0.8, zorder=0)
    title(ax, "points in the grid, in Dvir's floor, and in the smallest set")
    series = [("whole grid", "grid", GRIDLINE),
              ("smallest Kakeya set", "minimum", GREEN),
              ("Dvir's floor", "dvir_bound", VIOLET)]
    for n, (label, key, color) in enumerate(series):
        offs = xs + (n - 1) * 0.27
        vals = [r[key] for r in rows]
        ax.bar(offs, vals, width=0.25, color=color, alpha=0.9, label=label,
               zorder=3)
        for x, v in zip(offs, vals):
            ax.text(x, v + 0.7, str(v), ha="center", va="bottom",
                    fontsize=8.5, color=INK2)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    save_fig(fig, OUT / "counts.png")



if __name__ == "__main__":
    grid_png()
    grid3d_gif()
    counts_png()
    print(f"wrote figures to {OUT}")

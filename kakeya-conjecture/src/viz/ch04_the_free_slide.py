"""Figures for chapter 4: sliding costs nothing, and Pal's trick uses that."""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GRIDLINE, INK2, MUTED, RED, end_pad,
                    needle_line, out_dir, place, readout, save_anim, save_fig,
                    style_axes, title)
from kakeya_guide.shapes import pal_join_area, pal_join_travel, sector_area

OUT = out_dir("04-the-free-slide")


def free_slide_gif(n=34, fps=12):
    """Along its own line: nothing swept.  Sideways: area, immediately."""
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.9))
    for ax, name in ((axL, "slide along the needle's own line"),
                     (axR, "slide sideways")):
        style_axes(ax, (-1.35, 1.35), (-0.62, 0.62))
        title(ax, name, size=11.5)
        ax.plot([-1.3, 1.3], [0, 0], color=GRIDLINE, lw=1.0, zorder=1)
    swept_free = axL.fill_between([-0.5, 0.5], -0.004, 0.004, color=RED,
                                  alpha=0.0, zorder=2)
    swept_side = [None]
    lineL, dotsL = needle_line(axL, lw=3.2)
    lineR, dotsR = needle_line(axR, lw=3.2)
    noteL = readout(axL, (0.03, 0.97), "", fontsize=11.5)
    noteR = readout(axR, (0.03, 0.97), "", fontsize=11.5)

    def update(i):
        u = min(i, n - 1) / (n - 1)
        s = -0.7 + 1.4 * u
        place(lineL, dotsL, (s - 0.5, 0.0), (s + 0.5, 0.0))
        noteL.set_text(f"moved  {abs(s + 0.7):.2f}\nswept  0.00")
        place(lineR, dotsR, (-0.5, 0.55 * (2 * u - 1)), (0.5, 0.55 * (2 * u - 1)))
        if swept_side[0] is not None:
            swept_side[0].remove()
        swept_side[0] = axR.fill_between([-0.5, 0.5], -0.55,
                                         0.55 * (2 * u - 1), color=RED,
                                         alpha=0.25, zorder=2)
        noteR.set_text(f"moved  {1.1 * u:.2f}\nswept  {1.1 * u:.2f}")
        return []

    save_anim(fig, update, n + end_pad(fps), OUT / "free_slide.gif", fps=fps)


def pal_join_gif(theta=0.32, fps=11):
    """Pal's join: change lines for as little area as you like, if you go far."""
    gap = 0.55
    reach = pal_join_travel(gap, theta)
    fig, ax = plt.subplots(figsize=(9.2, 3.6))
    style_axes(ax, (-0.6, reach + 1.5), (-0.55, gap + 0.75), equal=False)
    title(ax, "Pal's join: get onto the other line, sweeping almost nothing")
    ax.plot([-0.6, reach + 1.4], [0, 0], color=GRIDLINE, lw=1.2, zorder=1)
    ax.plot([-0.6, reach + 1.4], [gap, gap], color=GRIDLINE, lw=1.2, zorder=1)
    ax.text(-0.55, 0.06, "line A", color=MUTED, fontsize=10)
    ax.text(-0.55, gap + 0.06, "line B", color=MUTED, fontsize=10)
    wedge = [None, None]
    line, dots = needle_line(ax, lw=3.2)
    note = readout(ax, (0.02, 0.97), "", fontsize=11.5)

    stages = [("slide out", 14), ("pivot", 10), ("cross", 14), ("pivot back", 10)]
    frames = sum(f for _, f in stages)

    def pivot_patch(cx, cy, a0, a1):
        arc = np.linspace(a0, a1, 24)
        pts = [(cx, cy)] + [(cx + math.cos(a), cy + math.sin(a)) for a in arc]
        return plt.Polygon(pts, closed=True, facecolor=RED, alpha=0.3,
                           edgecolor="none", zorder=2)

    def update(i):
        i = min(i, frames - 1)
        stage, local = 0, i
        for n_, (_, f) in enumerate(stages):
            if local < f:
                stage = n_
                break
            local -= f
        u = local / max(stages[stage][1] - 1, 1)
        swept = 0.0
        if stage == 0:
            x = reach * u
            place(line, dots, (x, 0), (x + 1, 0))
            note.set_text(f"slide along line A   swept {swept:.3f}")
        elif stage == 1:
            a = theta * u
            place(line, dots, (reach, 0),
                  (reach + math.cos(a), math.sin(a)))
            swept = sector_area(a)
            if wedge[0] is not None:
                wedge[0].remove()
            wedge[0] = pivot_patch(reach, 0, 0, a)
            ax.add_patch(wedge[0])
            note.set_text(f"pivot {math.degrees(a):4.1f} degrees   "
                          f"swept {swept:.3f}")
        elif stage == 2:
            back = reach * (1 - u)
            x, y = back, (reach - back) * math.tan(theta)
            place(line, dots, (x, y),
                  (x + math.cos(theta), y + math.sin(theta)))
            note.set_text(f"slide along the slanted line   "
                          f"swept {sector_area(theta):.3f}")
        else:
            a = theta * (1 - u)
            place(line, dots, (0, gap), (math.cos(a), gap + math.sin(a) - 0.0))
            if wedge[1] is not None:
                wedge[1].remove()
            wedge[1] = pivot_patch(0, gap, a, theta)
            ax.add_patch(wedge[1])
            note.set_text(f"pivot back   swept {pal_join_area(theta):.3f} in all")
        return []

    save_anim(fig, update, frames + end_pad(fps), OUT / "pal_join.gif", fps=fps)


def cost_png():
    """Make the pivots smaller and the cost dies; the trip gets longer."""
    thetas = [0.4, 0.2, 0.1, 0.05, 0.025, 0.0125]
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(2e-2, 1.0)
    ax.set_ylim(1e-2, 1e3)
    ax.set_xlabel("pivot angle (radians)", color=INK2, fontsize=10)
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("bottom", "left"):
        ax.spines[s].set_color(BASELINE)
    ax.grid(True, color=GRIDLINE, lw=0.8, zorder=0)
    title(ax, "the join's area falls; the distance travelled explodes")
    a_line, = ax.plot([], [], "o-", color=RED, lw=2, ms=5, label="area swept",
                      zorder=4)
    t_line, = ax.plot([], [], "o-", color=BLUE, lw=2, ms=5,
                      label="distance travelled", zorder=4)
    ax.legend(frameon=False, fontsize=9, loc="upper right")

    a_line.set_data(thetas, [pal_join_area(t) for t in thetas])
    t_line.set_data(thetas, [pal_join_travel(1.0, t) for t in thetas])
    save_fig(fig, OUT / "cost.png")


if __name__ == "__main__":
    free_slide_gif()
    pal_join_gif()
    cost_png()
    print(f"wrote figures to {OUT}")

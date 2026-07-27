"""Figures for chapter 5: Perron's tree, stage by stage, with exact areas."""

from fractions import Fraction

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    YELLOW, add_slivers, ease, morph_slivers, out_dir, readout,
                    save_anim, save_fig, style_axes, title)
from kakeya_guide.core import (perron_stages, perron_tree, ramped_alphas,
                               union_area)
from kakeya_guide.examples import steady_area, tree
from kakeya_guide.plotting import area_curve

OUT = out_dir("05-the-perron-tree")


def tree_gif(k=5, per_stage=10, fps=11):
    """Cut the triangle into 2^k slivers, then slide them together."""
    alphas = ramped_alphas(k)
    stages = perron_stages(k, alphas)
    areas = [float(union_area(s)) for s in stages]
    xs = [float(v) for s in stages[-1] for v in (s.b0, s.b1, s.ax)]
    lo, hi = min(xs) - 0.05, 1.05

    fig, ax = plt.subplots(figsize=(6.2, 4.3))
    style_axes(ax, (lo, hi), (-0.06, 1.12))
    add_slivers(ax, stages[0], color=GRIDLINE, alpha=1.0, zorder=1)
    patches = add_slivers(ax, stages[0], color=GREEN, alpha=0.42, zorder=3)
    note = readout(ax, (0.02, 0.99), "", fontsize=11.5)

    frames = per_stage * k + 16

    def update(i):
        i = min(i, per_stage * k)
        stage = min(i // per_stage, k - 1)
        t = ease((i - stage * per_stage) / per_stage) if k else 1.0
        if i >= per_stage * k:
            stage, t = k - 1, 1.0
        morph_slivers(patches, stages[stage], stages[stage + 1], t)
        area = areas[stage] + (areas[stage + 1] - areas[stage]) * t
        note.set_text(f"slivers {2 ** k}\nsqueeze {stage + 1} of {k}\n"
                      f"area    {area:.4f}")
        return []

    save_anim(fig, update, frames, OUT / "tree.gif", fps=fps)


def areas_png(k_max=7):
    """The steady squeeze stalls at 1/6.  Varying the squeeze walks past it."""
    steady = [float(steady_area(k)) for k in range(k_max + 1)]
    ramped = [float(union_area(tree(k))) for k in range(k_max + 1)]

    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    ax.set_xlim(-0.3, k_max + 0.3)
    ax.set_ylim(0, 0.55)
    ax.set_xticks(range(k_max + 1))
    ax.set_xlabel("times the triangle was halved", color=INK2, fontsize=10)
    area_curve(ax, [], [], color=RED)
    ax.axhline(1 / 6, color=BASELINE, lw=1.2, ls="--", zorder=2)
    ax.text(k_max - 0.1, 0.175, "one sixth", color=MUTED, fontsize=9, ha="right")
    title(ax, "area of the tree, exactly")
    s_line, = ax.plot([], [], "o-", color=VIOLET, lw=2.2, ms=5, zorder=4,
                      label="same squeeze every time")
    r_line, = ax.plot([], [], "o-", color=RED, lw=2.2, ms=5, zorder=5,
                      label="squeeze that varies")
    ax.legend(frameon=False, fontsize=9.5, loc="upper right")

    s_line.set_data(range(k_max + 1), steady)
    r_line.set_data(range(k_max + 1), ramped)
    # the curves cross, so each label goes on the side away from the other one
    for k in (2, 4, k_max):
        steady_on_top = steady[k] > ramped[k]
        ax.annotate(f"{steady[k]:.4f}", (k, steady[k]),
                    textcoords="offset points",
                    xytext=(0, 10 if steady_on_top else -17),
                    ha="center", fontsize=8.5, color=VIOLET)
        ax.annotate(f"{ramped[k]:.4f}", (k, ramped[k]),
                    textcoords="offset points",
                    xytext=(0, -17 if steady_on_top else 10),
                    ha="center", fontsize=8.5, color=RED)
    ax.text(0.5, 0.06, f"{2 ** k_max} slivers by the right hand end",
            transform=ax.transAxes, ha="center", fontsize=9.5, color=MUTED)
    save_fig(fig, OUT / "areas.png")


def stall_png(k=8):
    """Side by side: the same cut, squeezed two ways."""
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.2))
    figs = [perron_tree(k, Fraction(2, 3)), tree(k)]
    names = ["one squeeze for every stage", "a squeeze that varies with scale"]
    for ax, figure, name in zip(axes, figs, names):
        xs = [float(v) for s in figure for v in (s.b0, s.b1, s.ax)]
        style_axes(ax, (min(xs) - 0.05, max(xs) + 0.05), (-0.06, 1.1))
        add_slivers(ax, figure, color=GREEN, alpha=0.45, zorder=3)
        title(ax, f"{name}\narea {float(union_area(figure)):.4f}", size=11)
    fig.tight_layout()
    save_fig(fig, OUT / "stall.png")


if __name__ == "__main__":
    tree_gif()
    areas_png()
    stall_png()
    print(f"wrote figures to {OUT}")

"""Every figure of part three: rings that know how to integrate.

    cd src/viz && python part3_figures.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, BROWN, GREEN, INK, INK2, MUTED, RED,
                    SURFACE, TEAL, VIOLET, YELLOW, end_pad, note_below,
                    out_dir, plot_axes, save_anim, save_fig, spin, style_3d,
                    style_axes)
from condensed_guide import core as C

SLUG = "condensed-math03"
FPS = 20


# --- 0 · hero: the unit ball as the exponent turns --------------------------

def hero():
    d = out_dir(SLUG, "00-start-here")
    fig, (ax, axr) = plt.subplots(1, 2, figsize=(8.4, 4.2),
                                  width_ratios=[1, 1.15])
    fig.subplots_adjust(left=0.02, right=0.96, top=0.9, bottom=0.17,
                        wspace=0.22)
    tag = note_below(fig)
    lo, hi = 0.35, 2.4
    sweep = 46
    frames = 2 * sweep + end_pad(FPS)

    def exponent(f):
        # down from the top to the bottom, then hold at the allowed end
        t = min(1.0, f / (2 * sweep))
        return hi + (lo - hi) * t

    def update(f):
        ax.clear()
        axr.clear()
        p = exponent(f)
        style_axes(ax, (-1.45, 1.45), (-1.45, 1.55))
        ax.set_title("unit region for the measure size", color=INK2,
                     fontsize=11.5)
        th = np.linspace(0, 2 * np.pi, 720)
        pts = C.lp_ball(p, 720)
        allowed = p <= 1 + 1e-9
        ax.plot([-1.35, 1.35], [0, 0], color=BASELINE, lw=1)
        ax.plot([0, 0], [-1.35, 1.35], color=BASELINE, lw=1)
        ax.fill(pts[:, 0], pts[:, 1], color=GREEN if allowed else RED,
                alpha=0.13, lw=0)
        ax.plot(pts[:, 0], pts[:, 1], color=VIOLET, lw=2.4)
        # the chord that tests convexity
        a = C.lp_ball(p, 720)[int(720 * 0.09)]
        b = C.lp_ball(p, 720)[int(720 * 0.41)]
        mid = (a + b) / 2
        convex = C.lp_size(mid, p) <= 1 + 1e-9
        ax.plot([a[0], b[0]], [a[1], b[1]], color=GREEN if convex else RED,
                lw=1.8)
        ax.scatter([mid[0]], [mid[1]], s=44, color=GREEN if convex else RED,
                   zorder=4, edgecolors="none")
        ax.text(0, 1.44, "convex" if convex else "not convex", ha="center",
                color=GREEN if convex else RED, fontsize=10.5)

        plot_axes(axr, "the exponent", "size after merging, over before")
        axr.set_title("size ratio after four equal boxes are merged", color=INK2, fontsize=11.5)
        xs = np.linspace(lo, hi, 240)
        axr.plot(xs, [C.worst_merge_ratio(4, x) for x in xs], color=TEAL,
                 lw=2.2)
        axr.axhline(1, color=BASELINE, ls="--", lw=1)
        axr.axvline(1, color=GREEN, ls="--", lw=1)
        axr.scatter([p], [C.worst_merge_ratio(4, p)], s=52, color=INK,
                    zorder=5)
        axr.set_ylim(0, 3.4)
        axr.text(1.03, 3.15, "boundary p = 1", color=GREEN, fontsize=9.5)
        tag.set_text(f"exponent {p:.2f}     "
                     f"merging changes the size by "
                     f"{C.worst_merge_ratio(4, p):.2f}     "
                     + ("merge-compatible" if allowed else "merge increases size"))
        return ()

    save_anim(fig, update, frames, d / "hero.gif", fps=FPS)


# --- 1 · a ring with a rule -------------------------------------------------

def measures():
    d = out_dir(SLUG, "01-a-ring-with-a-rule")
    fig, ax = plt.subplots(figsize=(7.8, 3.9))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.08)
    style_axes(ax, (0, 1), (0, 1), equal=False)
    ax.set_title("a ring together with its modules of measures",
                 color=INK2, fontsize=12)
    ax.add_patch(plt.Rectangle((0.04, 0.62), 0.24, 0.24, fc="#efeafa",
                               ec=VIOLET, lw=1.8))
    ax.text(0.16, 0.74, "the ring", ha="center", va="center", color=VIOLET,
            fontsize=11.5)
    S = C.cantor(3)
    for lvl in range(4):
        n = 2 ** lvl
        for k in range(n):
            x = 0.06 + (k + 0.5) / n * 0.2
            y = 0.46 - lvl * 0.06
            ax.scatter([x], [y], s=16, color=BLUE, zorder=3,
                       edgecolors="none")
            if lvl:
                px = 0.06 + (k // 2 + 0.5) / (n // 2) * 0.2
                ax.plot([x, px], [y, y + 0.06], color=BASELINE, lw=0.8,
                        zorder=1)
    ax.text(0.16, 0.16, "a probe", ha="center", color=BLUE, fontsize=11)
    ax.annotate("", (0.5, 0.5), (0.32, 0.5),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2))
    ax.text(0.41, 0.56, "assign a measure module", ha="center", color=GREEN, fontsize=10.5)
    ax.add_patch(plt.Rectangle((0.53, 0.24), 0.43, 0.56, fc="#e6f2f1",
                               ec=TEAL, lw=1.8))
    ax.text(0.745, 0.73, "module of allowed measures", ha="center",
            color=TEAL, fontsize=11)
    rng = np.random.default_rng(3)
    for k in range(9):
        h = 0.08 + 0.22 * abs(np.sin(1.7 * k))
        ax.add_patch(plt.Rectangle((0.57 + k * 0.042, 0.31), 0.03, h,
                                   color=TEAL, lw=0))
    ax.text(0.745, 0.16, "each point enters as its Dirac measure",
            ha="center", color=INK2, fontsize=10)
    save_fig(fig, d / "measures.png")


# --- 2 · two rules that work ------------------------------------------------

def two_rules():
    d = out_dir(SLUG, "02-two-that-work")
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.8))
    fig.subplots_adjust(left=0.04, right=0.97, top=0.84, bottom=0.16,
                        wspace=0.18)
    fig.suptitle("two analytic measure rules and their infinite sums",
                 color=INK2, fontsize=12, y=0.965)

    ax = axes[0]
    style_axes(ax, (0, 1), (0, 1), equal=False)
    ax.set_title("the base-p rule", color=TEAL, fontsize=11)
    x0, w = 0.05, 0.9
    for k in range(6):
        ax.add_patch(plt.Rectangle((x0, 0.42), w, 0.3, fc=TEAL, ec=TEAL,
                                   lw=1.3, alpha=0.06 + 0.05 * k))
        nw = w / 2
        x0 += (w - nw) if k % 2 else 0
        w = nw
    ax.scatter([x0 + w / 2], [0.57], s=60, color=GREEN, zorder=4,
               edgecolors="none")
    ax.text(0.5, 0.26, "a series whose terms shrink p-adically\nat each step",
            ha="center", color=INK2, fontsize=10, linespacing=1.5)
    ax.text(0.5, 0.08, "converges to one p-adic value", ha="center", color=GREEN,
            fontsize=10.5)

    ax = axes[1]
    style_axes(ax, (0, 1), (0, 1), equal=False)
    ax.set_title("solid measures over a discrete ring", color=VIOLET,
                 fontsize=11)
    for k in range(14):
        x = 0.05 + k * 0.066
        ax.add_patch(plt.Circle((x, 0.62), 0.017, fc=VIOLET, ec=VIOLET,
                                lw=1.3))
    ax.text(0.985, 0.62, "…", va="center", ha="right", color=MUTED,
            fontsize=9.5)
    ax.text(0.5, 0.4, "a measure may use every product coordinate",
            ha="center", color=INK2, fontsize=10)
    ax.text(0.5, 0.26, "the coefficient ring remains discrete",
            ha="center", color=INK2, fontsize=10)
    ax.text(0.5, 0.08, "integration is still uniquely defined", ha="center",
            color=GREEN, fontsize=10.5)
    save_fig(fig, d / "two_rules.png")


# --- 3 · the exponent -------------------------------------------------------

def merge():
    d = out_dir(SLUG, "03-the-real-lines-own-rule")
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.86, bottom=0.17)
    plot_axes(ax, "the exponent", "size after merging, over before")
    ax.set_title("refinement requires merging not to increase size", color=INK2,
                 fontsize=12)
    xs = np.linspace(0.35, 2.5, 400)
    for boxes, colour in [(2, TEAL), (4, VIOLET), (9, BROWN)]:
        ax.plot(xs, [C.worst_merge_ratio(boxes, x) for x in xs], color=colour,
                lw=2.1, label=f"merge {boxes} equal boxes")
    ax.axhline(1, color=BASELINE, ls="--", lw=1.2)
    ax.axvline(1, color=GREEN, ls="--", lw=1.4)
    ax.set_ylim(0, 3.6)
    ax.axvspan(0.35, 1.0, color=GREEN, alpha=0.08, lw=0)
    ax.text(0.66, 3.3, "compatible with merging", ha="center", color=GREEN, fontsize=11)
    ax.text(1.75, 3.3, "size can increase", ha="center", color=RED, fontsize=11)
    ax.legend(frameon=False, fontsize=9, loc="center right")
    fig.text(0.5, 0.025, "every curve meets the no-growth threshold at exponent one",
             ha="center", color=INK2, fontsize=10)
    save_fig(fig, d / "merge.png")


def lp_balls():
    d = out_dir(SLUG, "03-the-real-lines-own-rule")
    ps = [0.5, 0.75, 1.0, 1.5, 2.0]
    fig, axes = plt.subplots(1, len(ps), figsize=(9.6, 2.9))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.78, bottom=0.2,
                        wspace=0.12)
    fig.suptitle("unit regions for several exponents", color=INK2,
                 fontsize=12, y=0.965)
    for ax, p in zip(axes, ps):
        style_axes(ax, (-1.3, 1.3), (-1.3, 1.3))
        pts = C.lp_ball(p, 720)
        convex = C.is_convex(p)
        ax.fill(pts[:, 0], pts[:, 1], color=GREEN if p <= 1 else RED,
                alpha=0.13, lw=0)
        ax.plot(pts[:, 0], pts[:, 1], color=VIOLET, lw=2.0)
        a, b = pts[int(720 * 0.09)], pts[int(720 * 0.41)]
        mid = (a + b) / 2
        ax.plot([a[0], b[0]], [a[1], b[1]],
                color=GREEN if convex else RED, lw=1.5)
        ax.scatter([mid[0]], [mid[1]], s=26,
                   color=GREEN if convex else RED, zorder=4,
                   edgecolors="none")
        ax.set_title(f"exponent {p:g}", color=INK, fontsize=10.5)
        ax.text(0, -1.22, "convex" if convex else "not convex", ha="center",
                color=GREEN if convex else RED, fontsize=9.5)
    fig.text(0.5, 0.045, "merging is compatible at p no greater than one; convexity fails below one",
             ha="center", color=INK2, fontsize=10)
    save_fig(fig, d / "lp_balls.png")


# --- 4 · functions near the edge --------------------------------------------

def tail():
    d = out_dir(SLUG, "04-functions-near-the-edge")
    fig, (ax, axb) = plt.subplots(2, 1, figsize=(7.8, 4.6),
                                  height_ratios=[1, 1.5])
    fig.subplots_adjust(left=0.06, right=0.97, top=0.92, bottom=0.15,
                        hspace=0.42)
    tag = note_below(fig)
    steps_n = 44
    frames = steps_n + end_pad(FPS)
    powers = list(range(2, -5, -1))

    def update(f):
        ax.clear()
        axb.clear()
        t = min(1.0, f / (steps_n * 0.9))
        T = 1 + t * 26
        style_axes(ax, (0, 1), (0, 1), equal=False)
        ax.set_title("moving toward the formal boundary at infinity", color=INK2, fontsize=12)
        ax.annotate("", (0.97, 0.5), (0.03, 0.5),
                    arrowprops=dict(arrowstyle="-|>", color=BASELINE, lw=2))
        ax.scatter([0.03 + t * 0.88], [0.5], s=80, color=BLUE, zorder=4,
                   edgecolors="none")
        ax.text(0.97, 0.72, "boundary at infinity", ha="right", color=BROWN, fontsize=10.5)
        ax.text(0.03 + t * 0.88, 0.22, f"coordinate T = {T:.1f}", ha="center",
                color=INK2, fontsize=10)

        plot_axes(axb, None, "how much each power matters out there")
        sizes = [T ** e for e in powers]
        colours = [RED if e >= 0 else TEAL for e in powers]
        axb.bar(range(len(powers)), np.log10(np.array(sizes)) , color=colours,
                lw=0)
        axb.set_xticks(range(len(powers)))
        axb.set_xticklabels([f"x^{e}" if e >= 0 else f"1/x^{-e}"
                             for e in powers], fontsize=9)
        axb.set_ylim(-7, 4)
        axb.axhline(0, color=BASELINE, lw=1)
        tag.set_text("red: global terms removed     teal: boundary tail retained")
        return ()

    save_anim(fig, update, frames, d / "tail.gif", fps=FPS)


def cross():
    d = out_dir(SLUG, "04-functions-near-the-edge")
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    fig.subplots_adjust(left=0.04, right=0.96, top=0.9, bottom=0.1)
    style_axes(ax, (-1.25, 1.25), (-1.25, 1.35))
    ax.set_title("coordinate cross with one shared origin",
                 color=INK2, fontsize=12)
    ax.plot([-1.1, 1.1], [0, 0], color=BASELINE, lw=3)
    ax.plot([0, 0], [-1.1, 1.1], color=BASELINE, lw=3)
    for x, y in [(1.1, 0), (-1.1, 0), (0, 1.1), (0, -1.1)]:
        ax.scatter([x], [y], s=90, color=BROWN, zorder=4, edgecolors="none")
    ax.scatter([0], [0], s=120, color=BLUE, zorder=5, edgecolors="none")
    ax.text(0.12, 0.13, "the crossing point", color=BLUE, fontsize=10.5)
    ax.text(0, 1.28, "four directions toward the boundary", ha="center", color=BROWN,
            fontsize=10.5)
    ax.text(0, -1.22, "the two branch functions must agree at the shared origin",
            ha="center", va="top", color=INK2, fontsize=10.5, linespacing=1.5)
    save_fig(fig, d / "cross.png")


# --- 5 · compact support ----------------------------------------------------

def compact_support():
    d = out_dir(SLUG, "05-compact-support")
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    fig.subplots_adjust(left=0.04, right=0.97, top=0.9, bottom=0.15)
    tag = note_below(fig)
    steps_n = 36
    frames = steps_n + end_pad(FPS)
    top, tails = 3, 5
    near = top + tails + 1
    everywhere = top + 1

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (0, 1), equal=False)
        ax.set_title("boundary functions modulo global functions", color=INK2,
                     fontsize=12)
        t = min(1.0, f / (steps_n * 0.8))
        cell = 0.072
        for k in range(near):
            ax.add_patch(plt.Rectangle((0.05 + k * cell, 0.72), cell - 0.008,
                                       0.12, color=VIOLET, lw=0))
        ax.text(0.05, 0.88, f"truncated boundary ring: {near} coordinates",
                color=VIOLET, fontsize=10.5)
        shown = int(round(t * everywhere))
        for k in range(shown):
            ax.add_patch(plt.Rectangle((0.05 + k * cell, 0.46), cell - 0.008,
                                       0.12, color=BASELINE, lw=0))
        ax.text(0.05, 0.62, f"global polynomial ring: {everywhere} coordinates",
                color=INK2, fontsize=10.5)
        if t > 0.55:
            a = (t - 0.55) / 0.45
            left = near - everywhere
            for k in range(left):
                ax.add_patch(plt.Rectangle((0.05 + k * cell, 0.16),
                                           cell - 0.008, 0.12, color=TEAL,
                                           lw=0, alpha=a))
            ax.text(0.05, 0.32, f"quotient: {left} retained tail coordinates",
                    color=TEAL, fontsize=10.5, alpha=a)
        tag.set_text("global polynomial coordinates cancel in the boundary quotient")
        return ()

    save_anim(fig, update, frames, d / "compact_support.gif", fps=FPS)


def dualizing():
    d = out_dir(SLUG, "05-compact-support")
    tails = list(range(1, 8))
    line = [C.line_edge_quotient_rank(3, m) for m in tails]
    crossr = [C.cross_edge_quotient_rank(3, m) for m in tails]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.86, bottom=0.17)
    plot_axes(ax, "tails kept", "pieces left over")
    ax.set_title("truncated boundary quotients for the line and cross",
                 color=INK2, fontsize=12)
    ax.plot(tails, line, "o-", color=TEAL, lw=2.1, ms=6,
            label="line: one set of tail coordinates")
    ax.plot(tails, crossr, "o-", color=BROWN, lw=2.1, ms=6,
            label="cross: two branch tails and one extra coordinate")
    ax.annotate("cross count equals twice the line count plus one",
                (tails[-2], crossr[-2]), xytext=(1.6, 12.5), color=BROWN,
                fontsize=9.5,
                arrowprops=dict(arrowstyle="-", color=BROWN, lw=0.9))
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    fig.text(0.5, 0.025, "the additional coordinate comes from the relation at the shared origin",
             ha="center", color=INK2, fontsize=10)
    save_fig(fig, d / "dualizing.png")


# --- 6 · gluing -------------------------------------------------------------

def spa():
    d = out_dir(SLUG, "06-gluing-the-pictures")
    fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.4))
    fig.subplots_adjust(left=0.03, right=0.98, top=0.78, bottom=0.14,
                        wspace=0.12)
    fig.suptitle("boundedness conditions determine a valuation region",
                 color=INK2, fontsize=12, y=0.965)
    rng = np.random.default_rng(7)
    pts = rng.random((260, 2))
    cases = [([], "no added boundedness condition"),
             ([("x", 0.62)], "one function required to be bounded"),
             ([("x", 0.62), ("y", 0.55)], "two functions required to be bounded")]
    for ax, (cuts, label) in zip(axes, cases):
        style_axes(ax, (-0.04, 1.04), (-0.16, 1.06), equal=False)
        keep = np.ones(len(pts), bool)
        for axis, bound in cuts:
            keep &= (pts[:, 0] < bound) if axis == "x" else (pts[:, 1] < bound)
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, fc="none", ec=BASELINE,
                                   lw=1.2))
        hi_x = min([b for a, b in cuts if a == "x"], default=1.0)
        hi_y = min([b for a, b in cuts if a == "y"], default=1.0)
        ax.add_patch(plt.Rectangle((0, 0), hi_x, hi_y, fc=GREEN, alpha=0.15,
                                   ec=GREEN, lw=1.8))
        ax.scatter(pts[~keep, 0], pts[~keep, 1], s=6, color=BASELINE)
        ax.scatter(pts[keep, 0], pts[keep, 1], s=7, color=GREEN)
        ax.set_title(label, color=INK, fontsize=10)
        ax.text(0.5, -0.11, f"{int(keep.sum())} / {len(pts)} samples retained",
                ha="center", color=INK2, fontsize=9.5)
    fig.text(0.5, 0.03, "schematic only: the axes are independent valuation parameters, not ring coordinates",
             ha="center", color=MUTED, fontsize=9.5)
    save_fig(fig, d / "spa.png")


def gluing():
    d = out_dir(SLUG, "06-gluing-the-pictures")
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    fig.subplots_adjust(left=0.04, right=0.97, top=0.9, bottom=0.15)
    tag = note_below(fig)
    steps_n = 34
    frames = steps_n + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (0, 1), equal=False)
        ax.set_title("compatible module data glue across an overlap",
                     color=INK2, fontsize=12)
        t = min(1.0, f / (steps_n * 0.75))
        ax.add_patch(plt.Rectangle((0.05, 0.6), 0.52, 0.2, color=BLUE,
                                   alpha=0.22, lw=0))
        ax.add_patch(plt.Rectangle((0.43, 0.6), 0.52, 0.2, color=TEAL,
                                   alpha=0.22, lw=0))
        ax.add_patch(plt.Rectangle((0.43, 0.6), 0.14, 0.2, fc="none", ec=INK,
                                   ls="--", lw=1.2))
        ax.text(0.2, 0.84, "one patch", color=BLUE, fontsize=10.5)
        ax.text(0.78, 0.84, "the other", color=TEAL, fontsize=10.5)
        ax.text(0.5, 0.54, "common restriction", ha="center", color=INK2,
                fontsize=9.5)
        for k in range(6):
            a = np.clip(t * 3 - k * 0.15, 0, 1)
            ax.add_patch(plt.Rectangle((0.08 + k * 0.075, 0.32), 0.05, 0.1,
                                       color=BLUE, lw=0, alpha=0.6 * a))
            ax.add_patch(plt.Rectangle((0.53 + k * 0.075, 0.32), 0.05, 0.1,
                                       color=TEAL, lw=0, alpha=0.6 * a))
        ax.text(0.5, 0.26, "module data on each patch", ha="center",
                color=INK2, fontsize=10)
        if t > 0.6:
            a = (t - 0.6) / 0.4
            ax.add_patch(plt.Rectangle((0.05, 0.06), 0.9, 0.12, color=GREEN,
                                       alpha=0.2 + 0.4 * a, lw=0))
            ax.text(0.5, 0.12, "one global object on the union", ha="center",
                    va="center", color=GREEN, fontsize=11, alpha=a)
        tag.set_text("Theorem 9.8 is descent for the derived module categories")
        return ()

    save_anim(fig, update, frames, d / "gluing.gif", fps=FPS)


# --- 7 · the six operations -------------------------------------------------

def six():
    d = out_dir(SLUG, "07-six-operations")
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.06)
    style_axes(ax, (0, 1), (0, 1), equal=False)
    ax.set_title("the six operations as three adjoint pairs", color=INK2, fontsize=12)
    pairs = [("tensor product", "derived internal Hom",
              TEAL, 0.76, "standard pair"),
             ("pullback", "ordinary pushforward",
              BLUE, 0.47, "standard pair"),
             ("compactly supported pushforward",
              "its right adjoint", VIOLET, 0.18, "boundary pair")]
    for left, right, colour, y, tag in pairs:
        ax.add_patch(plt.Rectangle((0.04, y), 0.4, 0.19, fc="white",
                                   ec=colour, lw=1.8))
        ax.text(0.24, y + 0.095, left, ha="center", va="center", color=INK,
                fontsize=10.5, wrap=True)
        ax.add_patch(plt.Rectangle((0.56, y), 0.4, 0.19, fc="white",
                                   ec=colour, lw=1.8))
        ax.text(0.76, y + 0.095, right, ha="center", va="center", color=INK,
                fontsize=10.5)
        ax.annotate("", (0.55, y + 0.12), (0.45, y + 0.12),
                    arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.6))
        ax.annotate("", (0.45, y + 0.07), (0.55, y + 0.07),
                    arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.6))
        ax.text(0.5, y - 0.05, tag, ha="center",
                color=VIOLET if tag == "boundary pair" else MUTED, fontsize=9.5)
    save_fig(fig, d / "six.png")


# --- 8 · duality ------------------------------------------------------------

def duality():
    d = out_dir(SLUG, "08-duality-watched")
    fig = plt.figure(figsize=(8.2, 4.4))
    ax = fig.add_subplot(121, projection="3d")
    axb = fig.add_subplot(122)
    fig.subplots_adjust(left=0.0, right=0.96, top=0.92, bottom=0.06,
                        wspace=0.02)
    frames = 48
    u = np.linspace(0, 2 * np.pi, 48)
    v = np.linspace(0, 2 * np.pi, 24)
    U, V = np.meshgrid(u, v)
    R, r = 1.5, 0.55
    X = (R + r * np.cos(V)) * np.cos(U)
    Y = (R + r * np.cos(V)) * np.sin(U)
    Z = r * np.sin(V)
    holes = 2

    def update(f):
        ax.clear()
        axb.clear()
        ax.plot_surface(X, Y, Z, color=BASELINE, alpha=0.3, linewidth=0,
                        rstride=1, cstride=1, shade=True)
        tt = np.linspace(0, 2 * np.pi, 200)
        ax.plot((R + r) * np.cos(tt), (R + r) * np.sin(tt),
                np.zeros_like(tt), color=VIOLET, lw=3.0)
        ax.plot(R + r * np.cos(tt), np.zeros_like(tt), r * np.sin(tt),
                color=TEAL, lw=3.0)
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        ax.set_zlim(-1.7, 1.7)
        ax.set_box_aspect((1, 1, 0.75))
        style_3d(ax)
        ax.set_axis_off()
        ax.view_init(elev=25, azim=spin(f, frames))
        ax.set_title("complementary classes on a smooth surface", color=INK2, fontsize=11.5)

        style_axes(axb, (0, 1), (0, 1), equal=False)
        axb.set_title("pairing followed by the trace", color=INK2,
                      fontsize=11.5)
        for k in range(holes):
            y = 0.76 - k * 0.16
            axb.add_patch(plt.Rectangle((0.06, y), 0.28, 0.11, color=VIOLET,
                                        lw=0))
            axb.add_patch(plt.Rectangle((0.62, y), 0.28, 0.11, color=TEAL,
                                        lw=0))
            axb.plot([0.36, 0.6], [y + 0.055, y + 0.055], color=GREEN, lw=1.4)
        axb.text(0.2, 0.92, "classes in one degree", ha="center", color=VIOLET,
                 fontsize=10.5)
        axb.text(0.76, 0.92, "complementary degree", ha="center", color=TEAL,
                 fontsize=10.5)
        axb.annotate("", (0.48, 0.3), (0.2, 0.48),
                     arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6))
        axb.annotate("", (0.48, 0.3), (0.76, 0.48),
                     arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6))
        axb.add_patch(plt.Rectangle((0.3, 0.1), 0.36, 0.15, fc="none",
                                    ec=GREEN, lw=2))
        axb.text(0.48, 0.175, "scalar on the base", ha="center", va="center",
                 color=GREEN, fontsize=11)
        return ()

    save_anim(fig, update, frames, d / "duality.gif", fps=FPS)


def pairing():
    d = out_dir(SLUG, "08-duality-watched")
    genera = [1, 2, 3, 4, 5]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    fig.subplots_adjust(left=0.11, right=0.97, top=0.86, bottom=0.17)
    plot_axes(ax, "genus of the surface", "dimension of each side")
    ax.set_title("dimensions in a finite model of a perfect pairing", color=INK2,
                 fontsize=12)
    x = np.arange(len(genera))
    ax.bar(x - 0.19, genera, width=0.36, color=VIOLET, label="first vector space")
    ax.bar(x + 0.19, genera, width=0.36, color=TEAL, label="dual vector space")
    ax.set_xticks(x)
    ax.set_xticklabels([str(g) for g in genera])
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    fig.text(0.5, 0.025, "equal dimensions are necessary for perfection; Theorem 11.1 proves the pairing itself",
             ha="center", color=INK2, fontsize=10)
    save_fig(fig, d / "pairing.png")


def main():
    hero()
    measures()
    two_rules()
    merge()
    lp_balls()
    tail()
    cross()
    compact_support()
    dualizing()
    spa()
    gluing()
    six()
    duality()
    pairing()
    print("part three: 14 figures")


if __name__ == "__main__":
    main()

"""Every figure of part one: shapes you can only see by probing them.

    cd src/viz && python part1_figures.py

Static pictures are png, and only things whose motion is the mathematics are
gif: a probe refining, a matching being made, a landing being torn, a
staircase assembling, a camera going round a surface.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

from common import (BASELINE, BLUE, BROWN, GREEN, INK, INK2, MUTED, RED,
                    SURFACE, TEAL, VIOLET, YELLOW, end_pad, note_below,
                    out_dir, save_anim, save_fig, spin, style_3d, style_axes,
                    plot_axes, title)
from condensed_guide import core as C

SLUG = "condensed-math01"
FPS = 20


# --- 0 · hero: a probe refining, and the dust it cuts out -------------------

def hero():
    d = out_dir(SLUG, "00-start-here")
    depth = 6
    fig, (ax, axd) = plt.subplots(
        2, 1, figsize=(7.6, 4.6), height_ratios=[2.5, 1])
    fig.subplots_adjust(left=0.04, right=0.98, top=0.94, bottom=0.13,
                        hspace=0.24)
    style_axes(ax, (-0.03, 1.03), (-depth - 0.5, 0.6), equal=False)
    style_axes(axd, (-0.03, 1.03), (-0.6, 0.6), equal=False)
    ax.set_title("finite stages of a binary probe", color=INK2, fontsize=12)
    axd.set_title("intervals selected by the visible stage", color=INK2, fontsize=11)
    tag = note_below(fig)

    per_level = 14
    frames = depth * per_level + end_pad(FPS)

    def update(f):
        ax.clear()
        axd.clear()
        style_axes(ax, (-0.03, 1.03), (-depth - 0.5, 0.6), equal=False)
        style_axes(axd, (-0.03, 1.03), (-0.6, 0.6), equal=False)
        ax.set_title("finite stages of a binary probe", color=INK2,
                     fontsize=12)
        axd.set_title("intervals selected by the visible stage", color=INK2,
                      fontsize=11)

        shown = min(depth, f // per_level)
        part = min(1.0, (f % per_level) / (per_level * 0.7)) if f < depth * per_level else 1.0
        S = C.cantor(depth)

        for lvl in range(shown + 1):
            n = 2 ** lvl
            xs = np.array([(k + 0.5) / n for k in range(n)])
            ax.scatter(xs, np.full(n, -lvl), s=max(4, 46 - 6 * lvl),
                       color=BLUE, zorder=3, edgecolors="none")
            if lvl:
                pn = 2 ** (lvl - 1)
                pxs = np.array([(k + 0.5) / pn for k in range(pn)])
                for k in range(n):
                    ax.plot([xs[k], pxs[k // 2]], [-lvl, -lvl + 1],
                            color=BASELINE, lw=0.9, zorder=1)

        # the level being born, sliding out of its parent
        if shown < depth:
            n = 2 ** (shown + 1)
            pn = 2 ** shown
            pxs = np.array([(k + 0.5) / pn for k in range(pn)])
            txs = np.array([(k + 0.5) / n for k in range(n)])
            xs = np.array([pxs[k // 2] + (txs[k] - pxs[k // 2]) * part
                           for k in range(n)])
            ys = np.full(n, -shown - part)
            for k in range(n):
                ax.plot([xs[k], pxs[k // 2]], [ys[k], -shown],
                        color=BASELINE, lw=0.9, zorder=1, alpha=part)
            ax.scatter(xs, ys, s=max(4, 46 - 6 * (shown + 1)), color=TEAL,
                       zorder=3, edgecolors="none", alpha=0.35 + 0.65 * part)

        # the dust: the boxes the finest visible level cuts the line into
        level = min(depth, shown + (1 if part > 0.5 else 0))
        n = 2 ** level
        width = 1.0 / n * 0.62
        for k in range(n):
            axd.add_patch(plt.Rectangle(((k + 0.5) / n - width / 2, -0.22),
                                        max(0.0016, width), 0.44,
                                        color=VIOLET, lw=0))
        tag.set_text(f"splits {level}     boxes {n}     "
                     f"each displayed stage is finite")
        return ()

    save_anim(fig, update, frames, d / "hero.gif", fps=FPS)


# --- 1 · the two real lines -------------------------------------------------

def bijection():
    d = out_dir(SLUG, "01-two-real-lines")
    fig, ax = plt.subplots(figsize=(7.6, 3.5))
    fig.subplots_adjust(left=0.04, right=0.98, top=0.9, bottom=0.16)
    tag = note_below(fig)
    n = 22
    xs = np.linspace(0.06, 0.94, n)
    frames = n + 6 + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (-0.55, 0.95), equal=False)
        ax.set_title("the identity map between two topologies", color=INK2, fontsize=12)
        ax.text(0.5, 0.86, "discrete real line: every point isolated", ha="center",
                color=BROWN, fontsize=11)
        ax.text(0.5, -0.5, "usual real line: nearby values remain nearby", ha="center",
                color=VIOLET, fontsize=11)
        ax.scatter(xs, np.full(n, 0.62), s=54, color=BROWN, zorder=3,
                   edgecolors="none")
        ax.plot([0.03, 0.97], [-0.28, -0.28], color=VIOLET, lw=4, zorder=2)

        done = min(n, f)
        for k in range(done):
            ax.plot([xs[k], xs[k]], [0.56, -0.24], color=GREEN, lw=1.4,
                    alpha=0.75, zorder=1)
            ax.scatter([xs[k]], [-0.28], s=34, color=GREEN, zorder=4,
                       edgecolors="none")
        tag.set_text(f"matched {done}/{n}     kernel 0     cokernel 0"
                     + ("     topologies differ" if done == n else ""))
        return ()

    save_anim(fig, update, frames, d / "bijection.gif", fps=FPS)


# --- 2 · the three probes ---------------------------------------------------

def tree_order(S, level):
    """The order to draw a level's boxes in so no two branches cross.

    A box's place in the row has to be decided by its whole ancestry, coarsest
    first, or a parent will not sit above its own children.  The p-adic system
    labels its boxes by residues, which is the right mathematics and the wrong
    drawing order, so the labels are sorted by the path that reaches them.
    """
    return sorted(S.levels[level],
                  key=lambda lab: tuple(str(S.project(lab, level, i))
                                        for i in range(level + 1)))


def draw_probe(ax, S, depth, node=26):
    pos = {}
    for lvl in range(depth + 1):
        ordered = tree_order(S, lvl)
        n = len(ordered)
        for k, label in enumerate(ordered):
            pos[(lvl, label)] = ((k + 0.5) / n, -lvl)
    for lvl in range(depth):
        for label in S.levels[lvl + 1]:
            a = pos[(lvl + 1, label)]
            b = pos[(lvl, S.parents[lvl][label])]
            ax.plot([a[0], b[0]], [a[1], b[1]], color=BASELINE, lw=0.85,
                    zorder=1)
    for (lvl, label), (x, y) in pos.items():
        ax.scatter([x], [y], s=node, color=BLUE, zorder=3, edgecolors="none")
    return pos


def probes():
    d = out_dir(SLUG, "02-branching-probes")
    fig, axes = plt.subplots(1, 3, figsize=(9.4, 3.9))
    fig.subplots_adjust(left=0.03, right=0.98, top=0.82, bottom=0.16,
                        wspace=0.14)
    # each probe is drawn to the depth where its own pattern is clearest, and
    # the depth is written under it so the counts can be read honestly
    specs = [(C.cantor(4), 4, "halving probe",
              "each box has two children"),
             (C.convergent_sequence(5), 5, "approaching-sequence probe",
              "one more point is separated at each stage"),
             (C.p_adic(3, 3), 3, "base-p probe",
              "each box has p children, with p equal to three")]
    deepest = max(depth for _, depth, _, _ in specs)
    for ax, (S, depth, name, sub) in zip(axes, specs):
        style_axes(ax, (-0.06, 1.06), (-deepest - 0.8, 0.55), equal=False)
        draw_probe(ax, S, depth, node=26)
        ax.set_title(name, color=INK, fontsize=11.5, pad=16)
        ax.text(0.5, 0.42, sub, ha="center", color=MUTED, fontsize=9.5)
        counts = " ".join(str(c) for c in S.sizes())
        ax.text(0.5, -deepest - 0.45, f"number of boxes at each stage\n{counts}",
                ha="center", va="top", color=INK2, fontsize=9.5,
                family="monospace")
    save_fig(fig, d / "probes.png")


# --- 3 · landing a probe ----------------------------------------------------

def landing():
    d = out_dir(SLUG, "03-what-a-shape-says")
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    fig.subplots_adjust(left=0.04, right=0.98, top=0.9, bottom=0.17)
    tag = note_below(fig)
    n = 9
    hold = 26
    frames = 2 * hold + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (-0.1, 1.05), equal=False)
        torn = f >= hold
        step = min(1.0, (f % hold) / (hold * 0.55)) if not torn else \
            min(1.0, (f - hold) / (hold * 0.55))
        ax.set_title("testing continuity with an approaching sequence", color=INK2,
                     fontsize=12)
        # the probe: marching points and their limit
        pys = np.array([0.92 - 0.075 * k for k in range(n)])
        ax.scatter(np.full(n, 0.1), pys, s=42, color=BLUE, zorder=3,
                   edgecolors="none")
        ax.scatter([0.1], [0.12], s=90, color=VIOLET, zorder=3,
                   edgecolors="none")
        ax.text(0.1, 0.03, "the limit point", ha="center", color=VIOLET,
                fontsize=10)
        # the target
        ts = np.linspace(0, 1, 300)
        curve = 0.5 + 0.28 * np.sin(2.6 * np.pi * ts)
        ax.plot(0.52 + 0.34 * np.cos(2 * np.pi * ts) * 0, ts, color=BASELINE,
                lw=0)
        ax.plot(np.full_like(ts, 0.86), ts, color=BASELINE, lw=2)
        ax.text(0.86, 1.0, "target space", ha="center", color=MUTED,
                fontsize=10)
        # where the marching points land
        landings = 0.5 + 0.36 / (np.arange(n) + 1.4)
        limit_land = 0.5 if not torn else 0.15
        shown = int(round(step * n))
        for k in range(shown):
            ax.plot([0.13, 0.83], [pys[k], landings[k]], color=BLUE, lw=1.0,
                    alpha=0.5, zorder=1)
            ax.scatter([0.86], [landings[k]], s=26, color=BLUE, zorder=4,
                       edgecolors="none")
        if step > 0.85:
            colour = RED if torn else GREEN
            ax.plot([0.13, 0.83], [0.12, limit_land], color=colour, lw=2.0,
                    zorder=2)
            ax.scatter([0.86], [limit_land], s=70, color=colour, zorder=4,
                       edgecolors="none")
            if torn:
                ax.plot([0.9, 0.9], [0.5, limit_land], color=RED, lw=3,
                        zorder=4)
                ax.text(0.93, (0.5 + limit_land) / 2, "different limits",
                        color=RED, fontsize=10, va="center", rotation=90)
            else:
                ax.text(0.93, 0.5, "continuous", color=GREEN, fontsize=10,
                        va="center", rotation=90)
        tag.set_text("the sequence images approach 0.50     "
                     + (f"the limit image is {limit_land:.2f}     discontinuous"
                        if torn else
                        "the limit image is 0.50     continuous"))
        return ()

    save_anim(fig, update, frames, d / "landing.gif", fps=FPS)


def sequence_test():
    d = out_dir(SLUG, "03-what-a-shape-says")
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    fig.subplots_adjust(left=0.04, right=0.96, top=0.88, bottom=0.08)
    style_axes(ax, (-1.35, 1.35), (-1.15, 1.35))
    ax.set_title("a convergent sequence detects a missing boundary point", color=INK2, fontsize=12)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.fill(1.0 * np.cos(th), 1.0 * np.sin(th), color=VIOLET, alpha=0.13,
            zorder=1)
    ax.plot(np.cos(th), np.sin(th), color=VIOLET, lw=1.6, ls="--", zorder=2)
    ax.text(0, -1.08, "the dashed boundary is not included", ha="center",
            color=VIOLET, fontsize=10.5)
    ks = np.arange(1, 11)
    r = 1 - 0.55 / ks
    ang = np.full_like(r, np.pi / 4)
    ax.scatter(r * np.cos(ang), r * np.sin(ang), s=40, color=BLUE, zorder=4,
               edgecolors="none")
    ax.plot(r * np.cos(ang), r * np.sin(ang), color=BLUE, lw=1.1, zorder=3)
    ax.scatter([np.cos(np.pi / 4)], [np.sin(np.pi / 4)], s=110, color=RED,
               zorder=5, edgecolors="none")
    ax.annotate("all sequence terms lie in the set", (r[3] * np.cos(ang[0]),
                                           r[3] * np.sin(ang[0])),
                xytext=(-1.25, 0.25), color=BLUE, fontsize=10.5,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=1))
    ax.annotate("the limit point is outside", (np.cos(np.pi / 4), np.sin(np.pi / 4)),
                xytext=(0.25, 1.18), color=RED, fontsize=10.5,
                arrowprops=dict(arrowstyle="-", color=RED, lw=1))
    ax.text(0, -1.32, "therefore the set is not closed",
            ha="center", color=INK2, fontsize=10.5)
    save_fig(fig, d / "sequence_test.png")


# --- 4 · cut and glue -------------------------------------------------------

def cut():
    d = out_dir(SLUG, "04-cut-and-glue")
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.06)
    style_axes(ax, (0, 1), (0, 1), equal=False)
    ax.set_title("answers on disjoint pieces are independent",
                 color=INK2, fontsize=12)
    for x0, x1, colour, name in [(0.05, 0.42, BLUE, "left piece"),
                                 (0.58, 0.95, TEAL, "right piece")]:
        ax.add_patch(plt.Rectangle((x0, 0.62), x1 - x0, 0.22, color=colour,
                                   alpha=0.22, lw=0))
        S = C.cantor(3)
        n = 8
        xs = np.linspace(x0 + 0.03, x1 - 0.03, n)
        ax.scatter(xs, np.full(n, 0.73), s=26, color=colour, zorder=3,
                   edgecolors="none")
        ax.text((x0 + x1) / 2, 0.88, name, ha="center", color=colour,
                fontsize=10.5)
    ax.annotate("", (0.5, 0.5), (0.24, 0.6),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4))
    ax.annotate("", (0.5, 0.5), (0.76, 0.6),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.4))
    ax.add_patch(plt.Rectangle((0.28, 0.18), 0.44, 0.26, fc="white",
                               ec=GREEN, lw=2))
    ax.text(0.5, 0.31, "answer on the whole probe:\none value from each piece",
            ha="center", va="center", color=INK, fontsize=11)
    ax.text(0.5, 0.06, "every pair is valid because the pieces are disjoint",
            ha="center", color=GREEN, fontsize=10.5)
    save_fig(fig, d / "cut.png")


def glue():
    d = out_dir(SLUG, "04-cut-and-glue")
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.15)
    tag = note_below(fig)
    steps = 30
    frames = steps + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (0, 1), equal=False)
        ax.set_title("compatible answers on a cover descend uniquely",
                     color=INK2, fontsize=12)
        t = min(1.0, f / (steps * 0.7))
        ax.add_patch(plt.Rectangle((0.06, 0.66), 0.5, 0.2, color=BLUE,
                                   alpha=0.24, lw=0))
        ax.add_patch(plt.Rectangle((0.44, 0.42), 0.5, 0.2, color=TEAL,
                                   alpha=0.24, lw=0))
        ax.add_patch(plt.Rectangle((0.44, 0.42), 0.12, 0.44, fc="none",
                                   ec=INK, ls="--", lw=1.3))
        ax.text(0.5, 0.34, "the overlap", ha="center", color=INK2,
                fontsize=10)
        ax.text(0.31, 0.89, "first covering piece", ha="center", color=BLUE,
                fontsize=10.5)
        ax.text(0.69, 0.65, "second covering piece", ha="center", color=TEAL,
                fontsize=10.5)
        if t > 0.35:
            a = (t - 0.35) / 0.65
            ax.add_patch(plt.Rectangle((0.06, 0.1), 0.88, 0.16, color=GREEN,
                                       alpha=0.2 + 0.5 * a, lw=0))
            ax.text(0.5, 0.18, "one resulting answer on the base", ha="center",
                    va="center", color=GREEN, fontsize=11.5, alpha=a)
        tag.set_text("the two restrictions agree on the overlap"
                     + ("     one answer descends to the base"
                        if t > 0.95 else ""))
        return ()

    save_anim(fig, update, frames, d / "glue.gif", fps=FPS)


# --- 5 · the ghost ----------------------------------------------------------

def ghost():
    d = out_dir(SLUG, "05-the-ghost")
    depth = 7
    fig, (ax, axp) = plt.subplots(2, 1, figsize=(7.6, 4.4),
                                  height_ratios=[3, 1])
    fig.subplots_adjust(left=0.05, right=0.97, top=0.92, bottom=0.15,
                        hspace=0.35)
    tag = note_below(fig)
    per = 15
    frames = depth * per + end_pad(FPS)

    def update(f):
        ax.clear()
        axp.clear()
        style_axes(ax, (0, 1), (-0.03, 1.03), equal=False)
        style_axes(axp, (0, 1), (-1, 1), equal=False)
        ax.set_title("continuous maps modulo locally constant maps",
                     color=INK2, fontsize=12)
        lvl = min(depth, f // per)
        n = 2 ** lvl
        vals = np.zeros(n)
        for k in range(n):
            v, step = 0.5, 0.5
            for i in range(lvl):
                bit = (k >> (lvl - 1 - i)) & 1
                step /= 2
                v += step if bit else -step
            vals[k] = v
        xs = np.arange(n) / n
        ax.bar(xs, vals, width=1 / n, align="edge", color=VIOLET, lw=0)
        spread = 0.0
        if n >= 2:
            spread = float(np.max(np.abs(vals[0::2] - vals[1::2])))
        axp.plot([0.02, 0.98], [0, 0], color=BASELINE, lw=2)
        axp.text(0.5, -0.62, "value on the one-point probe: zero",
                 ha="center", color=MUTED, fontsize=10.5)
        tag.set_text(f"level {lvl}     boxes {n}     variation {spread:.4f}     Q(*) = 0")
        return ()

    save_anim(fig, update, frames, d / "ghost.gif", fps=FPS)


# --- 6 · unfoldable probes --------------------------------------------------

def folding():
    d = out_dir(SLUG, "06-unfoldable-probes")
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.16)
    tag = note_below(fig)
    n = 11
    frames = n + 12 + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (0, 1), equal=False)
        ax.set_title("testing whether a cover has a continuous section", color=INK2,
                     fontsize=12)
        xs = np.linspace(0.06, 0.78, n)
        for x in xs:
            ax.scatter([x], [0.78], s=30, color=BASELINE, zorder=2,
                       edgecolors="none")
            ax.scatter([x], [0.52], s=30, color=BASELINE, zorder=2,
                       edgecolors="none")
            ax.scatter([x], [0.2], s=34, color=VIOLET, zorder=3,
                       edgecolors="none")
        ax.scatter([0.9], [0.2], s=80, color=VIOLET, zorder=3,
                   edgecolors="none")
        ax.text(0.9, 0.1, "the limit", ha="center", color=VIOLET, fontsize=10)
        ax.text(0.03, 0.94, "two possible lifts above each point", color=INK2,
                fontsize=10.5)
        ax.text(0.03, 0.06, "base probe", color=INK2, fontsize=10.5)
        done = min(n, f)
        for k in range(done):
            y = 0.78 if k % 2 == 0 else 0.52
            ax.scatter([xs[k]], [y], s=70, color=BLUE, zorder=4,
                       edgecolors="none")
            ax.plot([xs[k], xs[k]], [y - 0.03, 0.24], color=BLUE, lw=1.1,
                    alpha=0.55, zorder=1)
        if f >= n + 6:
            for y in (0.78, 0.52):
                ax.scatter([0.9], [y], s=110, facecolors="none",
                           edgecolors=RED, linewidths=2.2, zorder=4)
            ax.text(0.9, 0.36, "no continuous\nchoice", ha="center", color=RED,
                    fontsize=10.5)
        tag.set_text("selected lifts alternate"
                     + ("     no continuous section at the limit"
                        if f >= n + 6 else ""))
        return ()

    save_anim(fig, update, frames, d / "folding.gif", fps=FPS)


def no_convergence():
    d = out_dir(SLUG, "06-unfoldable-probes")
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    fig.subplots_adjust(left=0.04, right=0.96, top=0.86, bottom=0.14)
    style_axes(ax, (0, 1), (0, 1), equal=False)
    ax.set_title("a nonconstant sequence cannot converge here",
                 color=INK2, fontsize=12)
    n = 14
    xs = np.linspace(0.07, 0.72, n)
    ax.add_patch(plt.Rectangle((0.03, 0.52), 0.94, 0.3, color=GREEN,
                               alpha=0.12, lw=0))
    ax.add_patch(plt.Rectangle((0.03, 0.16), 0.94, 0.3, color=BROWN,
                               alpha=0.12, lw=0))
    ax.text(0.79, 0.67, "region A", ha="left", color=GREEN,
            fontsize=10.5, va="center")
    ax.text(0.79, 0.31, "region B, its complement", ha="left", color=BROWN,
            fontsize=10.5, va="center")
    for k, x in enumerate(xs):
        y = 0.67 if k % 2 == 0 else 0.31
        ax.scatter([x], [y], s=52, color=GREEN if k % 2 == 0 else BROWN,
                   zorder=3, edgecolors="none")
        ax.text(x, y + 0.09 if k % 2 == 0 else y - 0.12, str(k + 1),
                ha="center", color=MUTED, fontsize=8.5)
    ax.text(0.5, 0.03, "infinitely many terms remain in both separated regions",
            ha="center", color=INK2, fontsize=10.5)
    save_fig(fig, d / "no_convergence.png")


# --- 7 · nothing was lost ---------------------------------------------------

def nesting():
    d = out_dir(SLUG, "07-nothing-was-lost")
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.93, bottom=0.05)
    style_axes(ax, (0, 1), (0, 1), equal=False)
    ax.set_title("ordinary spaces inside condensed sets", color=INK2, fontsize=12)
    # nested frames rather than nested ovals: a band of an oval is narrowest
    # exactly where a label wants to sit, and every label here is a phrase
    bands = [(0.02, 0.98, 0.94, "#e8e6f7", VIOLET, "condensed sets"),
             (0.09, 0.91, 0.80, "#dfeaf8", BLUE, "condensed sets represented by spaces"),
             (0.16, 0.84, 0.66, "#dff0ea", TEAL,
              "metric spaces and CW complexes"),
             (0.23, 0.77, 0.52, "#e3f0dd", GREEN, "compact Hausdorff spaces")]
    floor = 0.13
    for x0, x1, top, fill, edge, label in bands:
        ax.add_patch(plt.Rectangle((x0, floor), x1 - x0, top - floor,
                                   fc=fill, ec=edge, lw=1.8, zorder=1))
    for i, (x0, x1, top, fill, edge, label) in enumerate(bands):
        ax.text((x0 + x1) / 2, top - 0.052, label, ha="center", va="center",
                color=edge, fontsize=10.5, zorder=3)
    # the ghost: inside condensed sets, outside everything that came from a
    # space, so it is drawn in the outermost band and nowhere else
    ax.scatter([0.055], [0.45], s=64, color=RED, zorder=4, edgecolors="none")
    ax.text(0.055, 0.38, "point-invisible\nquotient", ha="center", va="top", color=RED,
            fontsize=10, zorder=4, linespacing=1.3)
    ax.text(0.5, 0.05, "the quotient from section 5 does not come from an ordinary space",
            ha="center", color=INK2, fontsize=10)
    save_fig(fig, d / "nesting.png")


def roundtrip():
    d = out_dir(SLUG, "07-nothing-was-lost")
    fig, ax = plt.subplots(figsize=(7.6, 3.2))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.16)
    tag = note_below(fig)
    steps = 34
    frames = steps + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (0, 1), equal=False)
        ax.set_title("translate by probes, then recover the topology", color=INK2,
                     fontsize=12)
        t = min(1.0, f / (steps * 0.85))
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(0.11 + 0.07 * np.cos(th), 0.55 + 0.19 * np.sin(th),
                color=VIOLET, lw=3)
        ax.text(0.11, 0.24, "the space", ha="center", color=INK2,
                fontsize=10.5)
        for i in range(5):
            alpha = np.clip((t - 0.1 * i) * 4, 0, 1)
            ax.add_patch(plt.Rectangle((0.4, 0.42 + 0.09 * i), 0.2, 0.065,
                                       fc="none", ec=BLUE, lw=1.5,
                                       alpha=alpha))
        ax.text(0.5, 0.24, "all probe values", ha="center", color=INK2,
                fontsize=10.5)
        if t > 0.55:
            a = (t - 0.55) / 0.45
            ax.plot(0.89 + 0.07 * np.cos(th), 0.55 + 0.19 * np.sin(th),
                    color=GREEN, lw=3, alpha=a)
            ax.text(0.89, 0.24, "the space again", ha="center", color=INK2,
                    fontsize=10.5, alpha=a)
        ax.annotate("", (0.37, 0.6), (0.21, 0.6),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.6))
        ax.text(0.29, 0.68, "record probe maps", ha="center", color=BLUE,
                fontsize=9.5)
        if t > 0.55:
            ax.annotate("", (0.79, 0.6), (0.63, 0.6),
                        arrowprops=dict(arrowstyle="-|>", color=GREEN,
                                        lw=1.6))
            ax.text(0.71, 0.68, "recover the topology", ha="center", color=GREEN,
                    fontsize=9.5)
        tag.set_text("the recovered space has the original topology and maps"
                     if t > 0.95 else "recording the space's continuous probe maps")
        return ()

    save_anim(fig, update, frames, d / "roundtrip.gif", fps=FPS)


# --- 8 · counting holes -----------------------------------------------------

def winding():
    d = out_dir(SLUG, "08-counting-holes")
    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.93, bottom=0.14)
    tag = note_below(fig)
    turns = 3
    steps = 78
    frames = steps + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (-1.7, 1.7), (-1.7, 1.7))
        ax.set_title("winding number of a closed path", color=INK2, fontsize=12)
        th = np.linspace(0, 2 * np.pi, 300)
        ax.plot(np.cos(th), np.sin(th), color=BASELINE, lw=18, zorder=1,
                solid_capstyle="round")
        t = min(1.0, f / steps)
        ts = np.linspace(0, t * 2 * np.pi, max(2, int(600 * t) + 2))
        ang = turns * ts
        rad = 1 + 0.12 * np.sin(5 * ts)
        ax.plot(rad * np.cos(ang), rad * np.sin(ang), color=BLUE, lw=2.4,
                zorder=3)
        if len(ts):
            ax.scatter([rad[-1] * np.cos(ang[-1])], [rad[-1] * np.sin(ang[-1])],
                       s=64, color=BLUE, zorder=4, edgecolors="none")
        done = int(np.floor(t * turns + 1e-9))
        tag.set_text(f"winding {done}/{turns}"
                     + ("     unchanged by deformation" if t >= 1 else ""))
        return ()

    save_anim(fig, update, frames, d / "winding.gif", fps=FPS)


def torus():
    d = out_dir(SLUG, "08-counting-holes")
    fig = plt.figure(figsize=(6.0, 5.0))
    ax = fig.add_subplot(111, projection="3d")
    fig.subplots_adjust(left=0.0, right=1.0, top=0.95, bottom=0.02)
    frames = 48                       # a whole turn: loops with no pause
    u = np.linspace(0, 2 * np.pi, 48)
    v = np.linspace(0, 2 * np.pi, 24)
    U, V = np.meshgrid(u, v)
    R, r = 1.5, 0.55
    X = (R + r * np.cos(V)) * np.cos(U)
    Y = (R + r * np.cos(V)) * np.sin(U)
    Z = r * np.sin(V)
    tt = np.linspace(0, 2 * np.pi, 200)
    lx, ly, lz = (R + r) * np.cos(tt), (R + r) * np.sin(tt), np.zeros_like(tt)
    mx = (R + r * np.cos(tt))
    m1x, m1y, m1z = mx, np.zeros_like(tt), r * np.sin(tt)

    def update(f):
        ax.clear()
        ax.plot_surface(X, Y, Z, color=BASELINE, alpha=0.28, linewidth=0,
                        antialiased=True, shade=True, rstride=1, cstride=1)
        ax.plot(lx, ly, lz, color=BLUE, lw=3.4)
        ax.plot(m1x, m1y, m1z, color=GREEN, lw=3.4)
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        ax.set_zlim(-1.6, 1.6)
        ax.set_box_aspect((1, 1, 0.72))
        style_3d(ax)
        ax.set_axis_off()             # the surface is the picture, not the box
        ax.view_init(elev=26, azim=spin(f, frames))
        ax.set_title("two independent loop directions on the torus",
                     color=INK2, fontsize=11)
        return ()

    save_anim(fig, update, frames, d / "torus.gif", fps=FPS)


def ranks():
    d = out_dir(SLUG, "08-counting-holes")
    top = 6
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.78, bottom=0.19)
    plot_axes(ax, "degree", "how many independent holes")
    width = 0.13
    for n in range(1, top + 1):
        rs = C.exterior_ranks(n)
        xs = np.arange(len(rs)) + (n - top / 2 - 0.5) * width
        ax.bar(xs, rs, width=width * 0.9, color=plt.cm.viridis(0.15 + 0.13 * n),
               label=f"{n} circle" + ("s" if n > 1 else ""))
    ax.set_xticks(range(top + 1))
    ax.set_ylim(0, max(C.exterior_ranks(top)) * 1.08)
    # the legend sits above the drawing, where no bar can ever reach it
    ax.legend(frameon=False, fontsize=9, ncol=6, loc="lower center",
              bbox_to_anchor=(0.5, 1.02), columnspacing=1.1, handlelength=1.1)
    fig.suptitle("cohomology ranks of products of circles", color=INK2,
                 fontsize=12, y=0.975)
    fig.text(0.5, 0.025, "each row agrees with the corresponding row of Pascal's triangle",
             ha="center", color=INK2, fontsize=10)
    save_fig(fig, d / "ranks.png")


def main():
    hero()
    bijection()
    probes()
    landing()
    sequence_test()
    cut()
    glue()
    ghost()
    folding()
    no_convergence()
    nesting()
    roundtrip()
    winding()
    torus()
    ranks()
    print("part one: 15 figures")


if __name__ == "__main__":
    main()

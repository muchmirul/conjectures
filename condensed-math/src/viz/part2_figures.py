"""Every figure of part two: infinite sums that finally land.

    cd src/viz && python part2_figures.py
"""

from __future__ import annotations

from fractions import Fraction

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, BROWN, GREEN, INK, INK2, MUTED, RED,
                    SURFACE, TEAL, VIOLET, YELLOW, end_pad, note_below,
                    out_dir, plot_axes, save_anim, save_fig, spin, style_3d,
                    style_axes)
from condensed_guide import core as C
from condensed_guide.examples import TENSOR_CLAIMS

SLUG = "condensed-math02"
FPS = 20


def _tree_positions(S, depth):
    """Where to draw each box, coarsest ancestry first so nothing crosses."""
    pos = {}
    for lvl in range(depth + 1):
        ordered = sorted(S.levels[lvl],
                         key=lambda lab, l=lvl: tuple(
                             str(S.project(lab, l, i)) for i in range(l + 1)))
        n = len(ordered)
        for k, label in enumerate(ordered):
            pos[(lvl, label)] = ((k + 0.5) / n, -lvl)
    return pos


# --- 0 · hero: weights handed down ------------------------------------------

def hero():
    d = out_dir(SLUG, "00-start-here")
    depth = 4
    S = C.cantor(depth)
    pos = _tree_positions(S, depth)
    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    fig.subplots_adjust(left=0.04, right=0.83, top=0.92, bottom=0.15)
    tag = note_below(fig)
    per = 16
    frames = depth * per + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (-0.03, 1.03), (-depth - 0.55, 0.6), equal=False)
        ax.set_title("compatible weights through successive refinements",
                     color=INK2, fontsize=12)
        stage = min(depth, f // per)
        part = min(1.0, (f % per) / (per * 0.7)) if f < depth * per else 1.0
        # the bias slides back and forth so the split is visibly a choice,
        # then freezes once the tree is fully grown, so the last frame really
        # is a repeat and the pause at the end is a pause
        settled = min(f, depth * per - 1)
        bias = 0.5 + 0.28 * np.sin(settled / 9.0)
        weights = [{"": 64.0}]
        for lvl in range(depth):
            nxt = {}
            for lab in S.levels[lvl]:
                v = weights[lvl][lab]
                nxt[lab + "0"] = v * (1 - bias)
                nxt[lab + "1"] = v * bias
            weights.append(nxt)

        for lvl in range(stage + 1):
            grow = part if lvl == stage and stage < depth else 1.0
            for lab in S.levels[lvl]:
                x, y = pos[(lvl, lab)]
                if lvl:
                    px, py = pos[(lvl - 1, S.parents[lvl - 1][lab])]
                    ax.plot([x, px], [y, py], color=BASELINE, lw=0.9, zorder=1)
                r = max(9.0, weights[lvl][lab] * 5.2)
                ax.scatter([x], [y], s=r, color=TEAL, zorder=3,
                           edgecolors="none")
            total = sum(weights[lvl].values())
            ax.text(1.02, -lvl, f"L{lvl}: {total:.0f}",
                    transform=ax.get_yaxis_transform(), color=GREEN,
                    fontsize=8.5, va="center", family="monospace",
                    clip_on=False)
        tag.set_text(f"right-child share {bias:.2f}     "
                     f"total at every stage 64")
        return ()

    save_anim(fig, update, frames, d / "hero.gif", fps=FPS)


# --- 1 · the doubling sum, read two ways ------------------------------------

def padic_walk():
    d = out_dir(SLUG, "01-sums-with-nowhere-to-land")
    p, terms = 2, 9
    sums = [int(s) for s in C.geometric_partial_sums(p, terms)]
    fig, (ax, axn) = plt.subplots(2, 1, figsize=(7.8, 5.0),
                                  height_ratios=[1, 1])
    fig.subplots_adjust(left=0.06, right=0.97, top=0.92, bottom=0.15,
                        hspace=0.42)
    tag = note_below(fig)
    frames = terms * 5 + end_pad(FPS)

    def update(f):
        ax.clear()
        axn.clear()
        k = min(terms - 1, f // 5)
        style_axes(ax, (0, 1), (0, 1), equal=False)
        ax.set_title("ordinary distance: partial sums grow", color=RED,
                     fontsize=11.5)
        top = sums[terms - 1]
        for j in range(k + 1):
            w = np.log(sums[j] + 1) / np.log(top + 1)
            ax.add_patch(plt.Rectangle((0.02, 0.86 - j * 0.098), w * 0.78,
                                       0.062, color=RED, alpha=0.75, lw=0))
            ax.text(0.02 + w * 0.78 + 0.012, 0.89 - j * 0.098, str(sums[j]),
                    color=INK2, fontsize=9, va="center", family="monospace")

        style_axes(axn, (0, 1), (0, 1), equal=False)
        axn.set_title("2-adic distance: partial sums converge", color=TEAL,
                      fontsize=11.5)
        x0, w = 0.03, 0.94
        for j in range(k + 1):
            axn.add_patch(plt.Rectangle((x0, 0.16), w, 0.66, fc=TEAL,
                                        ec=TEAL, lw=1.4,
                                        alpha=0.06 + 0.04 * j))
            nw = w / p
            x0 = x0 + (w - nw if j % 2 else 0)
            w = nw
        axn.scatter([x0 + w / 2], [0.49], s=70, color=GREEN, zorder=5,
                    edgecolors="none")
        axn.text(0.5, 0.03, "2-adic limit: minus one",
                 ha="center", color=GREEN, fontsize=10.5)
        tag.set_text(f"n {k + 1}     sum {sums[k]}     ordinary error {abs(sums[k] + 1)}     "
                     f"2-adic error {2.0 ** -(k + 1):.5f}")
        return ()

    save_anim(fig, update, frames, d / "padic_walk.gif", fps=FPS)


def distance():
    d = out_dir(SLUG, "01-sums-with-nowhere-to-land")
    p, terms = 2, 12
    sums = C.geometric_partial_sums(p, terms)
    lim = C.geometric_limit(p)
    ordinary = [float(abs(s - lim)) for s in sums]
    padic = [C.p_adic_abs(s - lim, p) for s in sums]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    fig.subplots_adjust(left=0.13, right=0.97, top=0.86, bottom=0.16)
    plot_axes(ax, "terms added", "distance to the value the sum reaches")
    ax.set_yscale("log")
    ax.set_title("error measured by ordinary and 2-adic distance", color=INK2,
                 fontsize=12)
    ks = np.arange(1, terms + 1)
    ax.plot(ks, ordinary, "o-", color=RED, lw=2, ms=5,
            label="ordinary error doubles at each step")
    ax.plot(ks, padic, "o-", color=TEAL, lw=2, ms=5,
            label="2-adic error halves at each step")
    ax.legend(frameon=False, fontsize=9.5, loc="center left")
    ax.set_xticks(ks[::2])
    fig.text(0.5, 0.025, "exact calculation; both errors are measured from minus one",
             ha="center", color=INK2, fontsize=10)
    save_fig(fig, d / "distance.png")


# --- 2 · reading a measurement at two levels --------------------------------

def integral():
    d = out_dir(SLUG, "02-weights-that-agree")
    depth, read = 5, 2
    S = C.cantor(depth)
    w = C.counting_measure(S)
    f = {lab: 1 + 3 * (k % 4) for k, lab in enumerate(S.levels[read])}
    fine = C.refine(S, f, read, depth)
    a = w.integrate(f, read)
    b = w.integrate(fine, depth)
    fig, axes = plt.subplots(2, 1, figsize=(7.4, 4.4))
    fig.subplots_adjust(left=0.06, right=0.97, top=0.87, bottom=0.14,
                        hspace=0.42)
    fig.suptitle("one function integrated at coarse and fine stages",
                 color=INK2, fontsize=12, y=0.975)
    for ax, (level, values, colour) in zip(
            axes, [(read, f, TEAL), (depth, fine, VIOLET)]):
        n = S.size(level)
        ordered = sorted(S.levels[level])
        vals = [values[lab] for lab in ordered]
        ax.bar(np.arange(n) / n, vals, width=1 / n, align="edge", color=colour,
               lw=0)
        style_axes(ax, (0, 1), (0, max(vals) * 1.25), equal=False)
        ax.set_title(f"read on {n} boxes", color=colour, fontsize=10.5)
    total = a
    fig.text(0.5, 0.035, f"weighted integral at both stages:  {total}    "
                         f"(weight one on each of the {S.size(depth)} "
                         f"finest boxes)",
             ha="center", color=GREEN, fontsize=11, family="monospace")
    assert a == b
    save_fig(fig, d / "integral.png")


# --- 3 · a measurement taken apart into steps -------------------------------

def steps():
    d = out_dir(SLUG, "03-stacks-of-steps")
    depth = 4
    n = 2 ** depth
    rng = np.random.default_rng(4)
    target = rng.integers(1, 7, n)
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    fig.subplots_adjust(left=0.05, right=0.97, top=0.9, bottom=0.17)
    tag = note_below(fig)
    frames = n + 2 + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (0, int(target.max()) + 1.4), equal=False)
        ax.set_title("reconstructing a function from box indicators", color=INK2,
                     fontsize=12)
        k = min(n, f)
        xs = np.arange(n) / n
        ax.bar(xs, target, width=1 / n, align="edge", fc="none",
               edgecolor=VIOLET, lw=1.6, zorder=3)
        built = np.where(np.arange(n) < k, target, 0)
        ax.bar(xs, built, width=1 / n, align="edge", color=TEAL, lw=0,
               zorder=2)
        for j in range(k):
            ax.text(xs[j] + 0.5 / n, target[j] + 0.28, str(target[j]),
                    ha="center", color=GREEN, fontsize=8.5,
                    family="monospace")
        tag.set_text(f"basis functions used {k} of {n}     "
                     f"integer coefficients"
                     + ("     exact reconstruction" if k == n else ""))
        return ()

    save_anim(fig, update, frames, d / "steps.gif", fps=FPS)


def basis_size():
    d = out_dir(SLUG, "03-stacks-of-steps")
    depths = [1, 2, 3, 4]
    boxes = [2 ** k for k in depths]
    found = [len(C.nobeling_basis(C.cantor_points(k))) for k in depths]
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.86, bottom=0.18)
    plot_axes(ax, "splits", "how many")
    ax.set_title("finite-stage indicator basis and box count",
                 color=INK2, fontsize=12)
    x = np.arange(len(depths))
    ax.bar(x - 0.19, boxes, width=0.36, color=BASELINE,
           label="boxes in the finite stage")
    ax.bar(x + 0.19, found, width=0.36, color=TEAL,
           label="indicator basis elements")
    for i, (b, g) in enumerate(zip(boxes, found)):
        ax.text(i + 0.19, g + 0.4, str(g), ha="center", color=TEAL,
                fontsize=9.5)
    ax.set_xticks(x)
    ax.set_xticklabels([str(k) for k in depths])
    ax.legend(frameon=False, fontsize=9.5, loc="upper left")
    fig.text(0.5, 0.03, "this finite calculation illustrates, but does not prove, Nöbeling's theorem",
             ha="center", color=INK2, fontsize=10)
    save_fig(fig, d / "basis_size.png")


# --- 4 · products and sums --------------------------------------------------

def product_sum():
    d = out_dir(SLUG, "04-products-in-sums-out")
    n = 16
    fig, axes = plt.subplots(2, 1, figsize=(7.6, 3.8))
    fig.subplots_adjust(left=0.04, right=0.97, top=0.88, bottom=0.13,
                        hspace=0.62)
    rng = np.random.default_rng(1)
    settings = rng.integers(1, 6, n)
    for ax, (title_, mask, colour) in zip(
            axes,
            [("product: unrestricted integer coordinates",
              np.ones(n, bool), VIOLET),
             ("direct sum: finitely many nonzero coordinates",
              np.arange(n) < 4, TEAL)]):
        style_axes(ax, (0, 1), (-0.55, 1.0), equal=False)
        ax.set_title(title_, color=colour, fontsize=11)
        for k in range(n):
            x = (k + 0.5) / (n + 1.4)
            ax.add_patch(plt.Circle((x, 0.42), 0.021, fc="none", ec=colour,
                                    lw=1.5))
            if mask[k]:
                ang = settings[k] / 6 * 2 * np.pi
                ax.plot([x, x + 0.016 * np.sin(ang)],
                        [0.42, 0.42 + 0.016 * np.cos(ang) * 3],
                        color=colour, lw=2)
            else:
                ax.text(x, 0.42, "0", ha="center", va="center", color=MUTED,
                        fontsize=8)
        ax.text((n + 0.9) / (n + 1.4), 0.42, "continues", va="center",
                color=MUTED, fontsize=9.5)
    save_fig(fig, d / "product_sum.png")


def finite_reach():
    d = out_dir(SLUG, "04-products-in-sums-out")
    n = 16
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    fig.subplots_adjust(left=0.04, right=0.97, top=0.9, bottom=0.17)
    tag = note_below(fig)
    reach = 7
    frames = n + 4 + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (0, 1), equal=False)
        ax.set_title("an integer homomorphism reads finitely many coordinates", color=INK2,
                     fontsize=12)
        at = min(n, f)
        for k in range(n):
            x = (k + 0.5) / (n + 1.2)
            seen = k < min(at, reach)
            ax.add_patch(plt.Circle((x, 0.68), 0.019,
                                    fc=BLUE if seen else "none",
                                    ec=BLUE if k < reach else BASELINE,
                                    lw=1.5))
        ax.text((n + 0.7) / (n + 1.2), 0.68, "…", va="center", ha="right",
                color=MUTED, fontsize=9.5)
        head = min(at, n) / (n + 1.2)
        stalled = at > reach
        ax.annotate("", (min(head, (reach + 0.1) / (n + 1.2)), 0.5),
                    (0.02, 0.5),
                    arrowprops=dict(arrowstyle="-|>",
                                    color=RED if stalled else BLUE, lw=2))
        if stalled:
            ax.text((reach + 0.4) / (n + 1.2), 0.42,
                    "last coordinate used", color=RED, fontsize=10.5)
            ax.text(0.5, 0.2, "the tail can be arranged to be divisible by every power of two;",
                    ha="center", color=INK2, fontsize=10.5)
            ax.text(0.5, 0.11, "an integer with that divisibility must be zero",
                    ha="center", color=RED, fontsize=10.5)
        tag.set_text(f"coordinates read {min(at, reach)}"
                     + ("     finite support" if stalled else ""))
        return ()

    save_anim(fig, update, frames, d / "finite_reach.gif", fps=FPS)


# --- 5 · the solid rule -----------------------------------------------------

def extension():
    d = out_dir(SLUG, "05-the-solid-rule")
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.16)
    tag = note_below(fig)
    steps_n = 34
    frames = steps_n + end_pad(FPS)
    S = C.cantor(3)
    pos = _tree_positions(S, 3)

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (0, 1), equal=False)
        ax.set_title("unique extension from point weights to all measures",
                     color=INK2, fontsize=12)
        t = min(1.0, f / (steps_n * 0.8))
        for (lvl, lab), (x, y) in pos.items():
            ax.scatter([0.06 + x * 0.24], [0.82 + y * 0.16], s=18, color=BLUE,
                       zorder=3, edgecolors="none")
        for lvl in range(3):
            for lab in S.levels[lvl + 1]:
                a = pos[(lvl + 1, lab)]
                b = pos[(lvl, S.parents[lvl][lab])]
                ax.plot([0.06 + a[0] * 0.24, 0.06 + b[0] * 0.24],
                        [0.82 + a[1] * 0.16, 0.82 + b[1] * 0.16],
                        color=BASELINE, lw=0.8, zorder=1)
        ax.text(0.18, 0.94, "a probe", ha="center", color=BLUE, fontsize=10.5)
        # the points landing in the group
        m = 8
        for k in range(m):
            a = np.clip(t * 3 - k * 0.12, 0, 1)
            ax.scatter([0.52 + 0.045 * k], [0.66], s=34, color=VIOLET,
                       zorder=3, alpha=a, edgecolors="none")
        ax.text(0.68, 0.76, "map from the probe's points", ha="center",
                color=VIOLET, fontsize=10.5)
        if t > 0.45:
            a = (t - 0.45) / 0.55
            ax.add_patch(plt.Rectangle((0.5, 0.16), 0.44, 0.34, fc="none",
                                       ec=GREEN, lw=2, alpha=a))
            ax.text(0.72, 0.4, "unique extension", ha="center", color=GREEN,
                    fontsize=11, alpha=a)
            ax.text(0.72, 0.29, "every compatible weighting receives a value",
                    ha="center", color=INK2, fontsize=10, alpha=a)
            ax.annotate("", (0.72, 0.52), (0.72, 0.62),
                        arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8,
                                        alpha=a))
        ax.annotate("", (0.48, 0.66), (0.34, 0.7),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.5))
        tag.set_text("existence defines integration     "
                     "uniqueness makes its value unambiguous"
                     if t > 0.95 else "mapping the probe's points")
        return ()

    save_anim(fig, update, frames, d / "extension.gif", fps=FPS)


def solid_or_not():
    """Each candidate group drawn as the thing it is, with its verdict.

    A picture of six names and six ticks would be a table pretending to be a
    figure, so each cell draws the group's own shape instead: a lattice, a
    row of dials, a nesting, a decaying series, a row that runs out, and an
    unbroken line.
    """
    d = out_dir(SLUG, "05-the-solid-rule")

    def lattice(ax):
        ax.plot([0.06, 0.94], [0.5, 0.5], color=BASELINE, lw=1.2)
        for k in range(9):
            ax.scatter([0.1 + k * 0.1], [0.5], s=42, color=TEAL, zorder=3,
                       edgecolors="none")

    def dials(ax, filled=8):
        # eight dials, not nine, so the "and on" has room and never lands on
        # the last one
        for k in range(8):
            x = 0.085 + k * 0.093
            ax.add_patch(plt.Circle((x, 0.5), 0.029, fc=TEAL if k < filled
                                    else "none", ec=TEAL, lw=1.4))
        ax.text(0.99, 0.5, "…", va="center", ha="right", color=MUTED,
                fontsize=8.5)

    def nesting(ax):
        # boxes inside boxes, each half the last and sharing a left edge, so
        # the shrinking reads cleanly instead of clustering
        x0, w = 0.06, 0.88
        for k in range(6):
            inset = k * 0.035
            ax.add_patch(plt.Rectangle((x0, 0.24 + inset), w,
                                       0.52 - 2 * inset, fc="none", ec=TEAL,
                                       lw=1.4))
            w /= 2

    def series(ax):
        for k in range(9):
            h = 0.62 / (1 + 0.9 * k)
            ax.add_patch(plt.Rectangle((0.07 + k * 0.098, 0.22), 0.06, h,
                                       color=TEAL, lw=0))

    def ruler(ax):
        ax.plot([0.06, 0.94], [0.5, 0.5], color=RED, lw=5,
                solid_capstyle="round")

    cells = [("integers", True, lattice,
              "integer integration"),
             ("product of integer groups", True, dials,
              "coordinatewise integration"),
             ("p-adic integers", True, nesting,
              "p-adic completion"),
             ("formal power series", True, series,
              "coefficientwise integration"),
             ("direct sum of integers", False,
              lambda ax: dials(ax, filled=3),
              "a measure may have infinite support"),
             ("additive real line", False, ruler,
              "divisibility forces vanishing")]

    fig, axes = plt.subplots(2, 3, figsize=(9.4, 4.4))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.83, bottom=0.05,
                        wspace=0.1, hspace=0.62)
    fig.suptitle("examples that satisfy or fail the solid extension rule",
                 color=INK2, fontsize=12, y=0.965)
    for ax, (name, ok, draw, why) in zip(axes.ravel(), cells):
        style_axes(ax, (0, 1), (0, 1), equal=False)
        colour = GREEN if ok else RED
        draw(ax)
        ax.add_patch(plt.Rectangle((0.005, 0.005), 0.99, 0.99, fc="none",
                                   ec=colour, lw=1.6))
        ax.set_title(name, color=INK, fontsize=10.5, pad=7)
        ax.text(0.5, -0.16, ("solid: " if ok else "not solid: ") + why,
                ha="center", va="top", color=colour, fontsize=9.5)
    save_fig(fig, d / "solid_or_not.png")


# --- 6 · where the real line goes -------------------------------------------

def divisible():
    d = out_dir(SLUG, "06-where-the-real-line-goes")
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    fig.subplots_adjust(left=0.05, right=0.97, top=0.9, bottom=0.16)
    tag = note_below(fig)
    n = 9
    frames = n * 4 + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (0, 1), equal=False)
        ax.set_title("repeated division in the reals and integers", color=INK2, fontsize=12)
        k = min(n, f // 4)
        r, z = 720.0, 720.0
        ax.text(0.06, 0.94, "real numbers", color=VIOLET, fontsize=11)
        ax.text(0.56, 0.94, "integers", color=BROWN, fontsize=11)
        left = True
        for j in range(k + 1):
            div = j + 2
            y = 0.80 - j * 0.075
            ax.add_patch(plt.Rectangle((0.06, y - 0.026),
                                       max(0.004, r / 720 * 0.36), 0.05,
                                       color=VIOLET, lw=0))
            ax.text(0.43, y, f"÷{div}", color=MUTED, fontsize=9,
                    ha="right", va="center", family="monospace")
            inside = float(z).is_integer()
            ax.add_patch(plt.Rectangle((0.56, y - 0.026),
                                       max(0.004, abs(z) / 720 * 0.36), 0.05,
                                       color=BROWN if inside else RED, lw=0,
                                       alpha=1.0 if inside else 0.4))
            if not inside and left:
                ax.text(0.94, y, "not an integer", color=RED, fontsize=9.5,
                        ha="right", va="center")
                left = False
            r /= div
            z /= div
        ax.text(0.5, 0.035, "every homomorphism from the reals to the integers is zero",
                ha="center", color=RED, fontsize=10.0)
        tag.set_text(f"divisions {k}     real result exists     integer result eventually fails")
        return ()

    save_anim(fig, update, frames, d / "divisible.gif", fps=FPS)


def no_map():
    d = out_dir(SLUG, "06-where-the-real-line-goes")
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.1)
    style_axes(ax, (0, 1), (0, 1), equal=False)
    ax.set_title("a divisible group maps trivially to the integers", color=INK2, fontsize=12)
    ax.add_patch(plt.Rectangle((0.04, 0.52), 0.3, 0.3, fc="#efeafa",
                               ec=VIOLET, lw=1.8))
    ax.text(0.19, 0.67, "additive reals\ndivisible group", ha="center",
            va="center", color=VIOLET, fontsize=11, linespacing=1.5)
    ax.add_patch(plt.Rectangle((0.64, 0.52), 0.3, 0.3, fc="#eef4fb",
                               ec=BLUE, lw=1.8))
    ax.text(0.79, 0.67, "one coordinate\ninteger values", ha="center",
            va="center", color=BLUE, fontsize=11, linespacing=1.5)
    ax.annotate("", (0.62, 0.67), (0.36, 0.67),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
    ax.text(0.49, 0.73, "any homomorphism", ha="center", color=RED, fontsize=10)
    ax.text(0.49, 0.59, "is the zero map", ha="center", color=RED,
            fontsize=10)
    ax.text(0.5, 0.36, "the image must be divisible by every positive integer",
            ha="center", color=INK2, fontsize=11)
    ax.text(0.5, 0.27, "zero is the only integer with this property",
            ha="center", color=INK2, fontsize=11)
    ax.text(0.5, 0.11, "there is no nonzero map to any integer coordinate",
            ha="center", color=RED, fontsize=11.5)
    save_fig(fig, d / "no_map.png")


# --- 7 · the multiplication table -------------------------------------------

def tensor_table():
    d = out_dir(SLUG, "07-the-multiplication-table")
    names = ["Z_p", "Z_l", "Z[[T]]", "Z[[U]]", "R"]
    pretty = ["p-adic", "l-adic", "T-series", "U-series", "reals"]

    def show(key):
        if key == "0":
            return "zero"
        base, _, rest = key.partition("[[")
        head = {"Z_p": "p-adic", "Z_l": "l-adic", "Z": "integers"}[base]
        if not rest:
            return head
        return head + "\n" + rest.rstrip("]").replace(",", " and ") + "-series"

    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    fig.subplots_adjust(left=0.16, right=0.98, top=0.79, bottom=0.13)
    style_axes(ax, (-0.02, 1.02), (-0.02, 1.02), equal=False)
    ax.set_title("completed tensor products of sample solid groups", color=INK2, fontsize=12,
                 pad=26)
    n = len(names)
    for j, p in enumerate(pretty):
        ax.text((j + 0.5) / n, 1.045, p, ha="center", color=INK2, fontsize=10)
    for i, p in enumerate(pretty):
        ax.text(-0.015, 1 - (i + 0.5) / n, p, ha="right", va="center",
                color=INK2, fontsize=10)
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            res = C.solid_tensor(a, b)
            zero = res == "0"
            colour = RED if zero else TEAL
            ax.add_patch(plt.Rectangle((j / n + 0.004, 1 - (i + 1) / n + 0.004),
                                       1 / n - 0.008, 1 / n - 0.008,
                                       color=colour, alpha=0.14, lw=0))
            ax.text((j + 0.5) / n, 1 - (i + 0.5) / n, show(res), ha="center",
                    va="center", color=colour, fontsize=9.5, linespacing=1.35)
            if C.quoted_tensor(a, b):
                ax.scatter([(j + 0.94) / n], [1 - (i + 0.1) / n], s=16,
                           color=VIOLET, zorder=4, edgecolors="none")
    ax.scatter([0.02], [-0.075], s=16, color=VIOLET, clip_on=False,
               edgecolors="none")
    ax.text(0.045, -0.075, "five entries are stated in Example 6.4; the other cells "
                           "apply the same rule with renamed variables",
            va="center", color=INK2, fontsize=9.5)
    ax.text(0.02, -0.14, "distinct prime completions and the real factor give zero here",
            va="center", color=INK2, fontsize=9.5)
    save_fig(fig, d / "tensor_table.png")


def rulers():
    d = out_dir(SLUG, "07-the-multiplication-table")
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    fig.subplots_adjust(left=0.04, right=0.97, top=0.88, bottom=0.16)
    tag = note_below(fig)
    frames = 46 + end_pad(FPS)

    def update(f):
        ax.clear()
        style_axes(ax, (0, 1), (0, 1), equal=False)
        ax.set_title("incompatible p-adic and l-adic completion directions", color=INK2,
                     fontsize=12)
        # the sliding is the point, and it stops at the end so the closing
        # message is held rather than swept away
        settled = min(f, 30)
        slide = 0.06 * np.sin(settled / 7.0)
        for y, factor, colour, label in [(0.66, 2, VIOLET,
                                          "boxes shrinking by two"),
                                         (0.3, 3, BROWN,
                                          "boxes shrinking by three")]:
            ax.text(0.03, y + 0.17, label, color=colour, fontsize=10.5)
            x0, w = 0.03 + (slide if colour == BROWN else 0), 0.92
            for k in range(6):
                ax.add_patch(plt.Rectangle((x0, y - 0.06), w, 0.12, fc="none",
                                           ec=colour, lw=1.5))
                x0 += w * (1 - 1 / factor) / 2
                w /= factor
        if settled >= 24:
            ax.text(0.5, 0.06, "the completed tensor product is zero",
                    ha="center", color=RED, fontsize=11.5)
        tag.set_text("each prime is invertible in the other completion")
        return ()

    save_anim(fig, update, frames, d / "rulers.gif", fps=FPS)


# --- 8 · solidify a shape ---------------------------------------------------

def solidify():
    d = out_dir(SLUG, "08-solidify-a-shape")
    fig = plt.figure(figsize=(8.0, 4.4))
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
    H = C.torus().homology()

    def update(f):
        ax.clear()
        axb.clear()
        ax.plot_surface(X, Y, Z, color=TEAL, alpha=0.32, linewidth=0,
                        rstride=1, cstride=1, shade=True)
        ax.set_xlim(-2.2, 2.2)
        ax.set_ylim(-2.2, 2.2)
        ax.set_zlim(-1.7, 1.7)
        ax.set_box_aspect((1, 1, 0.75))
        style_3d(ax)
        ax.set_axis_off()
        ax.view_init(elev=25, azim=spin(f, frames))
        ax.set_title("derived solidification of a torus", color=INK2, fontsize=11.5)
        style_axes(axb, (0, 1), (0, 1), equal=False)
        axb.set_title("integral homology by degree", color=INK2, fontsize=11.5)
        for k, (free, tors) in enumerate(H):
            y = 0.78 - k * 0.26
            axb.text(0.04, y + 0.09, f"degree {k}", color=INK2, fontsize=10)
            for i in range(free):
                axb.add_patch(plt.Rectangle((0.04 + i * 0.12, y - 0.03), 0.1,
                                            0.1, color=TEAL, lw=0))
            if not free and not tors:
                axb.text(0.04, y + 0.02, "none", color=MUTED, fontsize=10)
        return ()

    save_anim(fig, update, frames, d / "solidify.gif", fps=FPS)


def homology_bars():
    d = out_dir(SLUG, "08-solidify-a-shape")
    order = ["circle", "figure eight", "sphere", "torus", "klein bottle"]
    fig, axes = plt.subplots(1, len(order), figsize=(9.6, 3.2))
    fig.subplots_adjust(left=0.02, right=0.99, top=0.8, bottom=0.24,
                        wspace=0.12)
    fig.suptitle("integral homology of five cell complexes",
                 color=INK2, fontsize=12, y=0.97)
    tallest = max(free + len(t) for name in order
                  for free, t in C.SHAPES[name]().homology())
    for ax, name in zip(axes, order):
        H = C.SHAPES[name]().homology()
        style_axes(ax, (-0.62, 2.62), (-0.62, tallest + 0.25), equal=False)
        ax.set_title(name, color=INK, fontsize=10.5, pad=8)
        for k, (free, tors) in enumerate(H):
            for i in range(free):
                ax.add_patch(plt.Rectangle((k - 0.34, i * 1.02), 0.68, 0.86,
                                           color=TEAL, lw=0))
            for i, t in enumerate(tors):
                ax.add_patch(plt.Rectangle((k - 0.34, (free + i) * 1.02), 0.68,
                                           0.86, color=BROWN, lw=0))
                ax.text(k, (free + i) * 1.02 + 0.43, str(t), ha="center",
                        va="center", color="white", fontsize=11)
            if not free and not tors:
                ax.plot([k - 0.34, k + 0.34], [0.03, 0.03], color=BASELINE,
                        lw=2)
            ax.text(k, -0.34, str(k), ha="center", va="center", color=MUTED,
                    fontsize=9.5)
        ax.text(1.0, -0.58, "degree", ha="center", va="center", color=MUTED,
                fontsize=9)
    fig.text(0.5, 0.055, "teal: free integer class.     brown: finite-order torsion class.",
             ha="center", color=INK2, fontsize=9.5)
    save_fig(fig, d / "homology_bars.png")


def main():
    hero()
    padic_walk()
    distance()
    integral()
    steps()
    basis_size()
    product_sum()
    finite_reach()
    extension()
    solid_or_not()
    divisible()
    no_map()
    tensor_table()
    rulers()
    solidify()
    homology_bars()
    print("part two: 16 figures")


if __name__ == "__main__":
    main()

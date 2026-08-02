"""Figures for chapter 9: the radius that cannot be pushed any lower."""

import math

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    YELLOW, end_pad, note_below, out_dir, plot_axes,
                    save_anim, save_fig, style_axes, title)
from sphere_packing_guide.core import (harmonic_measure, logistic_density,
                                       sign_radius_constant)

OUT = out_dir("09-the-wall")


def wall_gif(frames=54, fps=12):
    """Squeeze the radius and watch the demand become impossible.

    Half of the balanced function's weight has to be negative, and all of it
    has to fit inside the ball of the given radius.  The proof shows that once
    the radius drops below one over pi times the square root of the dimension,
    the weight that can fit inside is exponentially small.  Half is not
    exponentially small, so the squeeze cannot be completed.  The shrinking is
    the argument, so this moves.
    """
    d = 400
    limit = sign_radius_constant() * math.sqrt(d)
    radii = np.linspace(limit * 1.9, limit * 0.55, frames)

    fig, (ax, axb) = plt.subplots(1, 2, figsize=(9.9, 4.6),
                                  gridspec_kw={"width_ratios": [1, 1.1]})
    style_axes(ax, (-limit * 2.1, limit * 2.1), (-limit * 2.1, limit * 2.1))
    title(ax, "the ball the negative weight must fit into")
    circle = plt.Circle((0, 0), radii[0], facecolor=RED, alpha=0.18,
                        edgecolor=RED, lw=2.0)
    ax.add_patch(circle)
    ax.add_patch(plt.Circle((0, 0), limit, facecolor="none", edgecolor=VIOLET,
                            lw=1.8, ls="--"))
    ax.text(0, limit * 1.12, "the wall", color=VIOLET, fontsize=10,
            ha="center")

    axb.set_xlim(radii[-1] * 0.95, radii[0] * 1.02)
    axb.set_ylim(0, 0.62)
    axb.axhline(0.5, color=BLUE, lw=1.6, ls="--")
    axb.text(limit * 1.12, 0.535, "half: what the function demands",
             color=BLUE, fontsize=9.5)
    axb.axvline(limit, color=VIOLET, lw=1.6, ls="--")
    curve, = axb.plot([], [], color=RED, lw=2.6)
    dot, = axb.plot([], [], "o", ms=7, color=RED)
    plot_axes(axb, xlabel="radius of the ball",
              ylabel="weight that can fit inside")
    title(axb, "what the proof allows to fit")
    fig.subplots_adjust(bottom=0.24)
    note = note_below(fig, x=0.52, fontsize=10.5)

    def allowed(radius):
        """A readable stand-in for the exponential mass bound of the proof.

        The theorem gives an exponentially small allowance once the radius is
        under the wall.  This curve is drawn to show that behaviour, not to
        reproduce the constant, which the article says plainly.
        """
        if radius >= limit:
            return 0.5
        gap = (limit - radius) / limit
        return 0.5 * math.exp(-14 * gap)

    def update(i):
        i = min(i, frames - 1)
        r = radii[i]
        circle.set_radius(r)
        xs = radii[:i + 1]
        ys = [allowed(x) for x in xs]
        curve.set_data(xs, ys)
        dot.set_data([r], [ys[-1]])
        if r >= limit:
            note.set_text("still room")
            note.set_color(INK2)
        else:
            note.set_text("past the wall:\nnowhere near half fits")
            note.set_color(RED)
        return []

    save_anim(fig, update, frames + end_pad(fps), OUT / "wall.gif", fps=fps)


def ingredients_png():
    """The two weightings the proof leans on, drawn side by side."""
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.6, 3.9))
    T = np.linspace(-6, 6, 800)
    for sigma, colour, label in ((0.0, GRIDLINE, "half way"),
                                 (0.6, BLUE, "closer to the edge"),
                                 (0.9, VIOLET, "almost at the edge")):
        axL.plot(T, harmonic_measure(sigma, T), color=colour, lw=2.2,
                 label=label)
    axL.legend(frameon=False, fontsize=9)
    plot_axes(axL, xlabel="frequency")
    title(axL, "how much each frequency counts", size=11)

    u = np.linspace(-6, 6, 800)
    axR.plot(u, logistic_density(u), color=GREEN, lw=2.6)
    axR.fill_between(u, logistic_density(u), color=GREEN, alpha=0.14)
    plot_axes(axR, xlabel="frequency")
    title(axR, "what it becomes at the edge", size=11)
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    fig.text(0.5, 0.03, "this shape is where the number one over pi comes from",
             ha="center", fontsize=10, color=INK2)
    save_fig(fig, OUT / "ingredients.png")


if __name__ == "__main__":
    wall_gif()
    ingredients_png()
    print("wrote", OUT)

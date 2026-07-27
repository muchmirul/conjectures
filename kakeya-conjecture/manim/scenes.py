"""Flagship animations of the guide, as Manim Community Edition scenes.

These are OPTIONAL, fancier renders of the same stories told by the committed
matplotlib GIFs (see manim/README.md for install notes; every committed image
in guide/ was produced WITHOUT manim, so nothing in the guide depends on this
file).

Render examples:

    manim -qm --format=gif scenes.py PerronTree
    manim -qh scenes.py NeedleTurn

Scenes use Text (Pango) only, no LaTeX installation required.
"""

from fractions import Fraction

import numpy as np
from manim import (BLUE, DOWN, GREEN, GREY, LEFT, ORANGE, RED, RIGHT, UP,
                   WHITE, Create, FadeIn, FadeOut, Line, Polygon, Rotate,
                   Scene, Text, VGroup, Write)

from kakeya_guide.core import perron_stages, ramped_alphas, union_area
from kakeya_guide.examples import tree


def _poly(sliver, color=GREEN, opacity=0.45):
    (x0, y0), (x1, y1), (x2, y2) = [(float(a), float(b))
                                    for a, b in sliver.polygon()]
    p = Polygon(np.array([x0, y0, 0.0]), np.array([x1, y1, 0.0]),
                np.array([x2, y2, 0.0]), color=color, stroke_width=0)
    p.set_fill(color, opacity=opacity)
    return p


class PerronTree(Scene):
    """Chapter 5: cut a triangle into slivers and slide them together."""

    def construct(self):
        k = 4
        stages = perron_stages(k, ramped_alphas(k))
        scale, shift = 5.0, np.array([-2.2, -2.4, 0.0])

        def group(slivers):
            g = VGroup(*[_poly(s) for s in slivers])
            g.scale(scale, about_point=np.array([0.0, 0.0, 0.0])).shift(shift)
            return g

        label = Text(f"{2 ** k} slivers, area "
                     f"{float(union_area(stages[0])):.3f}", font_size=26)
        label.to_edge(UP)
        current = group(stages[0])
        self.play(Create(current), Write(label))
        for stage in range(k):
            nxt = group(stages[stage + 1])
            new_label = Text(f"{2 ** k} slivers, area "
                             f"{float(union_area(stages[stage + 1])):.3f}",
                             font_size=26).to_edge(UP)
            self.play(current.animate.become(nxt),
                      label.animate.become(new_label), run_time=1.4)
        self.wait()


class NeedleTurn(Scene):
    """Chapter 6: the needle pivots inside each sliver, then hops to the next."""

    def construct(self):
        figure = tree(3)
        scale, shift = 5.0, np.array([-2.2, -2.4, 0.0])
        shapes = VGroup(*[_poly(s, opacity=0.4) for s in figure])
        shapes.scale(scale, about_point=np.array([0.0, 0.0, 0.0])).shift(shift)
        self.play(Create(shapes))

        def place(sliver, run):
            ax, h = float(sliver.ax), float(sliver.h)
            norm = np.hypot(run, 1.0)
            p = np.array([ax, h, 0.0]) * scale + shift
            q = (np.array([ax + run / norm, h - 1.0 / norm, 0.0]) * scale
                 + shift)
            return Line(p, q, color=BLUE, stroke_width=7)

        order = sorted(figure, key=lambda s: s.direction_interval())
        needle = place(order[0], float(order[0].direction_interval()[0]))
        self.play(Create(needle))
        for s in order:
            lo, hi = (float(v) for v in s.direction_interval())
            for run in np.linspace(lo, hi, 6):
                self.play(needle.animate.become(place(s, run)), run_time=0.12)
        self.wait()


class OverlapIsFree(Scene):
    """Chapter 3: two halves slide together and the ink on the page drops."""

    def construct(self):
        left = Polygon([-2, -1.5, 0], [0, -1.5, 0], [0, 1.5, 0], color=GREEN,
                       stroke_width=0).set_fill(GREEN, 0.5)
        right = Polygon([0, -1.5, 0], [2, -1.5, 0], [0, 1.5, 0], color=GREEN,
                        stroke_width=0).set_fill(GREEN, 0.5)
        caption = Text("nothing shrinks, nothing turns, and the area falls",
                       font_size=26).to_edge(UP)
        self.play(Create(left), Create(right), Write(caption))
        self.play(right.animate.shift(LEFT * 1.33), run_time=2)
        self.play(FadeIn(Text("area x 2/3", font_size=30, color=ORANGE)
                         .to_edge(DOWN)))
        self.wait()


class PalJoin(Scene):
    """Chapter 4: change lines for almost no area, by going far away."""

    def construct(self):
        a = Line([-6, -1, 0], [6, -1, 0], color=GREY)
        b = Line([-6, 1, 0], [6, 1, 0], color=GREY)
        self.play(Create(a), Create(b))
        needle = Line([-5, -1, 0], [-3.5, -1, 0], color=BLUE, stroke_width=7)
        self.play(Create(needle))
        self.play(needle.animate.shift(RIGHT * 8), run_time=1.6)   # free
        self.play(Rotate(needle, angle=0.26, about_point=np.array([3.0, -1, 0])),
                  run_time=1.0)
        self.play(needle.animate.shift(np.array([-7.6, 2.0, 0.0])), run_time=1.8)
        self.play(Rotate(needle, angle=-0.26,
                         about_point=needle.get_start()), run_time=1.0)
        self.play(FadeIn(Text("swept: as little as you like", font_size=28,
                              color=ORANGE).to_edge(DOWN)))
        self.wait()

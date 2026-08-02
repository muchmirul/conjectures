"""Figures for chapter 2: what happens to a ball when dimensions are added."""

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK2, MUTED, RED, VIOLET,
                    YELLOW, axes_3d, ball_3d, compass_3d, end_pad, note_below,
                    out_dir, plot_axes, project_to_3d, rotate_4d, save_anim,
                    save_fig, spin_gif, style_axes, title, wire_cube)
from sphere_packing_guide.core import ball_fraction_of_cube, ball_volume

OUT = out_dir("02-room-runs-out")


def ball_in_box_gif(frames=54, fps=15):
    """One ball inside the box that just holds it, turned all the way round.

    Flat on the page a ball inside a square looks like it nearly fills it.
    Turning the box shows the four corners in three dimensions, and there are
    eight of them, not four.  That is the whole point of the chapter, and only
    a rotation makes it visible.  Seamless loop, no end pause.
    """
    fig = plt.figure(figsize=(5.6, 5.6))
    ax = axes_3d(fig, box=1.35, elev=17)
    wire_cube(ax, half=1.0, color=BASELINE, lw=1.3)
    ball_3d(ax, (0, 0, 0), 1.0, color=BLUE, alpha=0.36, n=40)
    spin_gif(fig, ax, OUT / "ball_in_box.gif", frames=frames, fps=fps, elev=17)


def _border_points(n):
    """n points spread evenly round the box border, starting at a corner.

    The box on the page is a square, so it only has four true corners; the
    extra points stand for the corners the higher dimensional box has and the
    page cannot show.  Starting at a corner keeps the four real ones in the
    set, and by dimension ten the border is one solid ring of them.
    """
    perimeter = 8.0
    xs, ys = [], []
    for k in range(n):
        s = perimeter * k / n
        side = min(3, int(s // 2))
        along = s - 2 * side             # each edge is two units long
        if side == 0:
            x, y = 1, 1 - along          # right edge, going down
        elif side == 1:
            x, y = 1 - along, -1         # bottom edge, going left
        elif side == 2:
            x, y = -1, -1 + along        # left edge, going up
        else:
            x, y = -1 + along, 1         # top edge, going right
        xs.append(x)
        ys.append(y)
    return xs, ys


def corners_gif(fps=12, step_frames=12):
    """The corners double, and the ball's share of the box collapses.

    Instead of a bar chart of the fractions, this keeps the picture from the
    spinning figure above: one box, one ball.  The blue disc is drawn with
    exactly the ball's share of the box's area, so in dimension two it is the
    inscribed circle itself, and each added dimension doubles the red corner
    marks and visibly eats the disc.  The collapse is the motion, so it moves.
    """
    dims = list(range(2, 11))
    radii = [np.sqrt(4 * ball_fraction_of_cube(d) / np.pi) for d in dims]

    fig, ax = plt.subplots(figsize=(6.0, 6.6))
    style_axes(ax, (-1.45, 1.45), (-1.45, 1.45))
    ax.add_patch(plt.Rectangle((-1, -1), 2, 2, fill=False, ec=BASELINE,
                               lw=1.6, zorder=2))
    ball = plt.Circle((0, 0), radii[0], facecolor=BLUE, alpha=0.5, zorder=3)
    ax.add_patch(ball)
    dots, = ax.plot([], [], "o", color=RED, ms=6, ls="", zorder=4)
    title(ax, "the same box, one dimension at a time")
    fig.subplots_adjust(bottom=0.17)
    note = note_below(fig, fontsize=11.5)

    intro = step_frames + 4       # hold dimension two a moment longer

    def state(i):
        if i < intro:
            return 0, 1.0
        step, t = divmod(i - intro, step_frames)
        step = min(step + 1, len(dims) - 1)
        return step, min(1.0, t / (step_frames * 0.55))

    def update(i):
        step, t = state(min(i, intro + (len(dims) - 1) * step_frames - 1))
        d = dims[step]
        r0 = radii[step - 1] if step else radii[0]
        r = r0 + (radii[step] - r0) * (3 * t * t - 2 * t ** 3)
        ball.set_radius(r)
        xs, ys = _border_points(2 ** d)
        dots.set_data(xs, ys)
        dots.set_markersize(max(2.2, 7 - 0.5 * d))
        share = ball_fraction_of_cube(d) * 100
        note.set_text(f"dimension {d:2d}      corners {2 ** d:5d}\n"
                      f"the ball's share of the box {share:6.2f} %")
        return []

    frames = intro + (len(dims) - 1) * step_frames
    save_anim(fig, update, frames + end_pad(fps), OUT / "corners.gif", fps=fps)


def volume_peak_png():
    """The unit ball itself, drawn at its true relative size, dimension by dimension.

    The same fact as a line chart, but with nothing to decode: each disc's
    area is proportional to the ball's volume in that dimension, so the eye
    sees the swelling to dimension five and the collapse afterwards directly.
    """
    dims = list(range(1, 26))
    vols = [ball_volume(d) for d in dims]
    radii = [0.2 * np.sqrt(v) for v in vols]
    fig, ax = plt.subplots(figsize=(10.6, 2.9))
    style_axes(ax, (0, 26), (-0.85, 1.75))
    ax.axhline(0, color=BASELINE, lw=1.1, zorder=1)
    for d, r in zip(dims, radii):
        ax.add_patch(plt.Circle((d, r), r, facecolor=VIOLET, alpha=0.7,
                                zorder=3))
    for d in (1, 5, 10, 15, 20, 25):
        ax.text(d, -0.32, str(d), ha="center", fontsize=9, color=MUTED)
    ax.text(13, -0.68, "dimension", ha="center", fontsize=10, color=INK2)
    peak = int(np.argmax(vols)) + 1
    ax.annotate(f"biggest in dimension {peak}", xy=(peak, 2 * radii[peak - 1]),
                xytext=(peak + 4.5, 1.45), color=INK2, fontsize=10,
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3))
    ax.text(21, 0.62, "by dimension 25 almost\nnothing is left", color=MUTED,
            fontsize=9.5, ha="center")
    title(ax, "the ball of radius one, drawn at its true relative size")
    save_fig(fig, OUT / "volume_peak.png")


def four_d_gif(frames=64, fps=15):
    """A four dimensional cube, turned in four dimensions, shadowed into three.

    Four dimensions cannot be drawn honestly, so this draws the shadow and then
    turns the object in a plane that involves the fourth axis.  The shadow
    breathes: corners swing from the middle to the outside and back.  That
    swelling is the fourth direction making itself felt, and it is the reason
    the corners keep getting further from the centre as dimensions are added.
    Seamless loop, no end pause.
    """
    corners = np.array([[a, b, c, e] for a in (-1, 1) for b in (-1, 1)
                        for c in (-1, 1) for e in (-1, 1)], dtype=float)
    edges = [(i, j) for i in range(16) for j in range(i + 1, 16)
             if np.sum(np.abs(corners[i] - corners[j])) == 2]

    fig = plt.figure(figsize=(5.6, 5.6))
    ax = axes_3d(fig, box=2.15, elev=16)
    lines = [ax.plot([], [], [], color=BLUE, lw=1.3, alpha=0.75)[0]
             for _ in edges]
    dots, = ax.plot([], [], [], "o", ms=4.2, color=VIOLET)

    def update(i):
        angle = 2 * np.pi * i / frames
        turned = rotate_4d(corners, angle, planes=((0, 3),))
        shown = project_to_3d(turned, distance=3.0)
        for line, (a, b) in zip(lines, edges):
            line.set_data([shown[a, 0], shown[b, 0]], [shown[a, 1], shown[b, 1]])
            line.set_3d_properties([shown[a, 2], shown[b, 2]])
        dots.set_data(shown[:, 0], shown[:, 1])
        dots.set_3d_properties(shown[:, 2])
        ax.view_init(elev=16, azim=360 * i / frames)
        return []

    save_anim(fig, update, frames, OUT / "four_d.gif", fps=fps)


if __name__ == "__main__":
    ball_in_box_gif()
    corners_gif()
    volume_peak_png()
    four_d_gif()
    print("wrote", OUT)

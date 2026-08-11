"""Figures for chapter 7: bowls, saddles, and the see-saw law.

The bowl and the saddle are genuine surfaces, so they are drawn in three
dimensions and the camera makes a seamless orbit: the rotation is what
shows their shapes.  The eigenvalue chart uses the same toy table as
chapter 6 and a synthetic mirror pair.
"""

import numpy as np
import matplotlib.pyplot as plt

from common import BASELINE, BLUE, GREEN, INK2, MUTED, RED, out_dir, \
    plot_axes, save_anim, save_fig, style_3d, title
from zeta_guide.core import ToyFamily, positive_directions

OUT = out_dir("07-bowls-and-saddles")


def bowl_saddle_gif(fps=20):
    xs = np.linspace(-1, 1, 61)
    X, Y = np.meshgrid(xs, xs)
    bowl = (0.8 * X + 0.6 * Y) ** 2          # a rank-one bowl: up one way, flat one way
    saddle = 2 * X * Y                        # up one way, down the other

    fig = plt.figure(figsize=(8.8, 4.4))
    ax1 = fig.add_subplot(121, projection="3d")
    ax2 = fig.add_subplot(122, projection="3d")
    for ax, Z, name, color in ((ax1, bowl, "a bowl: never below zero", BLUE),
                               (ax2, saddle, "a saddle: up one way,\n"
                                             "down the other", RED)):
        style_3d(ax)
        ax.plot_surface(X, Y, Z, rcount=60, ccount=60, cmap="cividis",
                        linewidth=0, antialiased=True, alpha=0.95)
        ax.set_title(name, color=color, fontsize=10)
        ax.set_zlim(-2, 2)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([-2, 0, 2])

    n_frames = 90

    def update(i):
        az = -55 + 360.0 * i / n_frames
        ax1.view_init(elev=22, azim=az)
        ax2.view_init(elev=22, azim=az)
        return []

    # a full orbit that loops seamlessly: no end pad on rotating shots
    save_anim(fig, update, n_frames, OUT / "bowl_saddle.gif", fps=fps)


def seesaw_png():
    """Eigenvalues of the real toy table, next to a mirror pair's own block.

    The pair is added as its own contribution, not mixed into the table:
    mixed in, its downward direction can be swamped by the table's positive
    mass, which is exactly why the paper counts upward directions rather
    than hunting for downward ones.
    """
    fam = ToyFamily(T=100.0, dial=1.0)
    zeros = fam.real_zero_config(40, 400)
    G = fam.table_from_zeros(zeros)
    # one synthetic mirror pair at depth 0.3, mid-stretch, on its own
    pair = fam.table_from_zeros([(150.0 + 0.3j, 1)])

    ev = np.sort(np.linalg.eigvalsh(G))
    evp = np.sort(np.linalg.eigvalsh(pair))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 3.9))
    for ax, e, name in ((ax1, ev, "the real table: every direction\n"
                                  "curves up or is flat"),
                        (ax2, evp, "one synthetic mirror pair, alone:\n"
                                   "one up, one down, the rest flat")):
        colors = [RED if v < -1e-9 else BLUE for v in e]
        ax.bar(range(len(e)), e, color=colors, width=0.8)
        ax.axhline(0, color=MUTED, lw=0.9)
        plot_axes(ax, xlabel="direction (sorted)")
        ax.set_title(name, color=INK2, fontsize=10)
    ax1.set_ylabel("curvature of the table's surface", color=INK2, fontsize=10)
    assert int(np.sum(ev < -1e-9)) == 0
    assert int(np.sum(evp < -1e-9)) == 1
    assert int(np.sum(evp > 1e-9)) == 1
    save_fig(fig, OUT / "seesaw.png")


if __name__ == "__main__":
    bowl_saddle_gif()
    seesaw_png()
    print("wrote", OUT)

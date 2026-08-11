"""Figures for chapter 2: the zeta landscape, the strip, the line.

The landscape is genuinely three-dimensional (two input coordinates and a
height), so it is drawn as a surface and the camera makes a full seamless
orbit around it: the rotation is what shows the third dimension.
"""

import math

import numpy as np
import matplotlib.pyplot as plt

from common import BASELINE, BLUE, GREEN, INK2, MUTED, RED, VIOLET, out_dir, \
    plot_axes, save_anim, save_fig, style_3d, title
from zeta_guide.core import zeta_em, zero_heights

OUT = out_dir("02-riemanns-map")


def landscape_gif(fps=20):
    """A camera orbit of the zeta landscape over the strip.

    Height is the size of zeta, gently compressed (log of 1 + size) so the
    pole near the bottom does not flatten everything else.  The floor line
    sigma = 1/2 is drawn, and the surface touches the floor exactly along
    it, at the zeros.
    """
    sigmas = np.linspace(-0.1, 1.1, 61)
    ts = np.linspace(5.0, 42.0, 185)
    S, T = np.meshgrid(sigmas, ts)
    Z = np.empty_like(S)
    for i in range(T.shape[0]):
        for j in range(S.shape[1]):
            Z[i, j] = abs(zeta_em(S[i, j] + 1j * T[i, j]))
    H = np.minimum(Z, 3.2)          # cap, so the dips to zero stay readable

    fig = plt.figure(figsize=(7.0, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    style_3d(ax)
    ax.plot_surface(S, T, H, rcount=150, ccount=56, cmap="cividis",
                    linewidth=0, antialiased=True, alpha=0.9)
    zs = [g for g in zero_heights() if ts[0] < g < ts[-1]]
    ax.scatter([0.5] * len(zs), zs, [0.03] * len(zs), color=RED, s=22,
               depthshade=False, zorder=8)
    ax.plot([0.5, 0.5], [ts[0], ts[-1]], [0, 0], color=BLUE, lw=2.2,
            zorder=7)
    ax.set_xlabel("first coordinate (the strip runs 0 to 1)", fontsize=8,
                  color=INK2, labelpad=6)
    ax.set_ylabel("height", fontsize=8, color=INK2, labelpad=6)
    ax.set_zlabel("size of zeta (capped)", fontsize=8, color=INK2,
                  labelpad=2)
    ax.set_title("the zeta landscape touches the floor only on the line",
                 color=INK2, fontsize=11)

    n_frames = 100

    def update(i):
        ax.view_init(elev=28, azim=-60 + 360.0 * i / n_frames)
        return []

    # a full orbit that loops seamlessly: no end pad on rotating shots
    save_anim(fig, update, n_frames, OUT / "landscape.gif", fps=fps)


def strip_png():
    """The flat map: the strip, the line, the first zeros, the symmetry."""
    zs = [g for g in zero_heights() if g <= 102][:30]
    fig, ax = plt.subplots(figsize=(6.4, 7.2))
    ax.axvspan(0, 1, color="#f1efe9", zorder=0)
    ax.axvline(0.5, color=BLUE, lw=2.0, zorder=3)
    ax.axvline(0, color=BASELINE, lw=1.0)
    ax.axvline(1, color=BASELINE, lw=1.0)
    ax.plot([0.5] * len(zs), zs, "o", ms=5, color=RED, zorder=5)
    for g, lab in [(zs[0], "height 14.13"), (zs[1], "height 21.02")]:
        ax.annotate(lab, xy=(0.55, g), xytext=(1.5, g), fontsize=9,
                    color=INK2, va="center",
                    arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
    ax.annotate("mirror rule: a zero\noff the line would\ncome with its twin,\n"
                "reflected across\nthe line", xy=(-3.4, 66), xytext=(-3.4, 52),
                fontsize=9, color=INK2, annotation_clip=False)
    ax.annotate("", xy=(0.85, 47), xytext=(0.15, 47),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.2))
    ax.text(0.5, 107, "the strip", ha="center", fontsize=10, color=INK2)
    ax.text(1.15, 3.5, "the line", ha="left", fontsize=10, color=BLUE)
    ax.set_xlim(-3.6, 3.4)
    ax.set_ylim(0, 112)
    ax.set_xticks([0, 0.5, 1])
    ax.set_xticklabels(["0", "one\nhalf", "1"], fontsize=8)
    plot_axes(ax, xlabel="first coordinate", ylabel="height")
    title(ax, "the first thirty zeros, all on the line", size=11)
    save_fig(fig, OUT / "strip.png")


if __name__ == "__main__":
    landscape_gif()
    strip_png()
    print("wrote", OUT)

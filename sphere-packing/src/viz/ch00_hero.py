"""Figures for chapter 0: the opening picture and the map of the guide."""

import matplotlib.pyplot as plt
import numpy as np

from common import (BASELINE, BLUE, GREEN, GRIDLINE, INK, INK2, MUTED, VIOLET,
                    axes_3d, ball_3d, fcc_centres, out_dir, save_fig, spin_gif,
                    style_axes)

OUT = out_dir("00-start-here")


def hero_gif(frames=60, fps=15):
    """The greengrocer's stack, turning, so the reader sees it is solid.

    A still photograph of packed balls is ambiguous: flat discs would look the
    same.  Turning the camera all the way round is what tells the eye these are
    spheres sitting in depth.  The loop is seamless and carries no end pause,
    because here the motion is the content.
    """
    centres = fcc_centres(1)
    keep = [p for p in centres if np.linalg.norm(p) <= 2.05]

    fig = plt.figure(figsize=(6.6, 6.6))
    ax = axes_3d(fig, box=1.9, elev=16)
    for p in keep:
        near = np.linalg.norm(p) < 0.01
        ball_3d(ax, p / 2, np.sqrt(2) / 4, color=VIOLET if near else BLUE,
                alpha=0.5 if near else 0.30, n=30)
    spin_gif(fig, ax, OUT / "hero.gif", frames=frames, fps=fps, elev=16)


if __name__ == "__main__":
    hero_gif()
    print("wrote", OUT)

"""The hero: the zeta path along the critical line, striking the centre.

The value of zeta at height t on the line is a point in the plane; as t
climbs the point traces a curve that swings around and repeatedly passes
through the origin.  Every exact strike is a zero.  The motion IS the
mathematics here: the curve passing through the centre is what "a zero on
the critical line" means.
"""

import numpy as np

from common import BLUE, GREEN, INK2, MUTED, RED, end_pad, note_below, out_dir, \
    save_anim, style_axes, title
import matplotlib.pyplot as plt

from zeta_guide.core import zeta_on_line, zero_heights

OUT = out_dir("00-start-here")


def hero_gif(fps=20):
    t_max = 50.0
    ts = np.linspace(1.0, t_max, 1400)
    vals = np.array([zeta_on_line(t) for t in ts])
    zeros = [g for g in zero_heights() if g <= t_max]

    fig, ax = plt.subplots(figsize=(6.4, 6.8))
    fig.subplots_adjust(bottom=0.11, top=0.93)
    style_axes(ax, (-2.2, 4.6), (-3.0, 3.4))
    title(ax, "the zeta function along the critical line")
    ax.axhline(0, color=MUTED, lw=0.7)
    ax.axvline(0, color=MUTED, lw=0.7)
    ax.plot(0, 0, "o", ms=10, mfc="none", mec=GREEN, mew=2.0, zorder=9)

    trail, = ax.plot([], [], color=BLUE, lw=1.4, alpha=0.75, zorder=4)
    head, = ax.plot([], [], "o", ms=7, color=BLUE, zorder=8)
    note = note_below(fig, x=0.5, ha="center", fontsize=12)
    hits = []

    seg = max(2, len(ts) // 220)

    def update(i):
        n = min((i + 1) * seg, len(ts))
        trail.set_data(vals.real[:n], vals.imag[:n])
        head.set_data([vals.real[n - 1]], [vals.imag[n - 1]])
        t_now = ts[n - 1]
        while len(hits) < len(zeros) and zeros[len(hits)] <= t_now:
            hits.append(ax.plot(0, 0, "o", ms=4.5, color=GREEN, zorder=10)[0])
        note.set_text(f"height {t_now:5.1f}   zeros struck so far: {len(hits)}")
        note.set_color(GREEN if hits and abs(t_now - zeros[len(hits) - 1]) < 0.6
                       else INK2)
        return []

    frames = int(np.ceil(len(ts) / seg)) + end_pad(fps)
    save_anim(fig, update, frames, OUT / "hero.gif", fps=fps)


if __name__ == "__main__":
    hero_gif()
    print("wrote", OUT)

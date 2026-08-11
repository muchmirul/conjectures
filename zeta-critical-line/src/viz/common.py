"""Shared drawing helpers for the chapter figure scripts.

Run any chapter script from this folder and it writes straight into the
matching guide/ chapter:

    cd src/viz && python ch03_the_music.py
"""

from __future__ import annotations

from pathlib import Path

from zeta_guide.plotting import (BASELINE, BLUE, BROWN, GREEN, GRIDLINE, INK,
                                 INK2, MUTED, RED, SURFACE, TEAL, VIOLET,
                                 YELLOW, arrow, card, ease, plot_axes, readout,
                                 save_anim, save_fig, style_3d, style_axes,
                                 title)

GUIDE = Path(__file__).resolve().parents[2] / "guide"


def out_dir(chapter_folder: str) -> Path:
    d = GUIDE / chapter_folder
    d.mkdir(parents=True, exist_ok=True)
    return d


def end_pad(fps: int, seconds: float = 2.5) -> int:
    """How many extra frames to ask for so the last one stays up to be read.

    Every non-looping animation here ends on the frame that carries the
    point.  The update functions clamp their index, so any frames past the
    end simply repeat that last one.  Without a pause of a couple of seconds
    the loop wipes the answer away mid-sentence.  The two camera orbits do
    not use this: they loop seamlessly instead.
    """
    return max(1, round(fps * seconds))


def note_below(fig, x=0.012, y=0.022, fontsize=11, color=INK2, ha="left"):
    """A live readout placed under the drawing, never on top of it.

    A number that changes has to sit somewhere, and inside the axes it will
    eventually land on a curve, because the picture moves and the text does
    not.  Putting it in reserved space below the axes makes an overlap
    impossible rather than unlikely.  Call `fig.subplots_adjust(bottom=...)`
    first so the space is really there.
    """
    return fig.text(x, y, "", ha=ha, va="bottom", fontsize=fontsize,
                    color=color, family="monospace", zorder=20)

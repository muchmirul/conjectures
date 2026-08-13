"""Shared drawing helpers for the figure scripts.

Run any part's script from this folder and it writes straight into that
part's guide chapters:

    cd src/viz && python part1_figures.py

Each part keeps its figures in one script rather than one script per
chapter, because the parts share layout helpers heavily inside themselves
and almost nothing across.  The Makefile still offers a target per part.
"""

from __future__ import annotations

from pathlib import Path

from condensed_guide.parts import PARTS_DIR
from condensed_guide.plotting import (BASELINE, BLUE, BROWN, GREEN, GRIDLINE,
                                      INK, INK2, MUTED, RED, SURFACE, TEAL,
                                      VIOLET, YELLOW, arrow, card, draw_tree,
                                      ease, plot_axes, readout, save_anim,
                                      save_fig, style_3d, style_axes, title,
                                      tree_layout)


def out_dir(part_slug: str, chapter_folder: str) -> Path:
    d = PARTS_DIR / part_slug / "guide" / chapter_folder
    d.mkdir(parents=True, exist_ok=True)
    return d


def end_pad(fps: int, seconds: float = 2.5) -> int:
    """How many extra frames to ask for so the last one stays up to be read.

    Every animation here that builds towards a point ends on the frame that
    carries it.  The update functions clamp their index, so any frames past
    the end simply repeat that last one.  Without a pause of a couple of
    seconds the loop wipes the answer away mid-sentence.  The rotating camera
    shots do not use this: they loop seamlessly instead.
    """
    return max(1, round(fps * seconds))


def note_below(fig, x=0.012, y=0.02, fontsize=11, color=INK2, ha="left"):
    """A live readout placed under the drawing, never on top of it.

    A number that changes has to sit somewhere, and inside the axes it will
    eventually land on a drawing, because the picture moves and the text does
    not.  Putting it in reserved space below the axes makes an overlap
    impossible rather than unlikely.  Call `fig.subplots_adjust(bottom=...)`
    first so the space is really there.
    """
    return fig.text(x, y, "", ha=ha, va="bottom", fontsize=fontsize,
                    color=color, family="monospace", zorder=20)


def spin(frame: int, frames: int, start: float = 20.0) -> float:
    """A camera angle that returns exactly to where it began.

    Rotating shots are the one kind of animation here that must not pause on
    its last frame, so the angle is a whole turn spread over the frame count
    and the final frame is the first one again.
    """
    return start + 360.0 * frame / frames

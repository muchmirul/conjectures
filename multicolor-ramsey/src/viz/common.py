"""Shared drawing helpers for the chapter figure scripts.

Run any chapter script from this folder and it writes straight into the
matching guide/ chapter:

    cd src/viz && python ch02_six_is_forced.py
"""

from __future__ import annotations

from pathlib import Path

from ramsey_guide.plotting import (BASELINE, BLUE, BROWN, EDGE_COLORS, GREEN,
                                   GRIDLINE, INK, INK2, MUTED, RED, SURFACE,
                                   TEAL, VIOLET, YELLOW, arrow, card,
                                   draw_coloring, draw_edge, draw_vertices,
                                   ease, flash_triangle, plot_axes, readout,
                                   ring_positions, save_anim, save_fig,
                                   style_axes, title)

GUIDE = Path(__file__).resolve().parents[2] / "guide"


def out_dir(chapter_folder: str) -> Path:
    d = GUIDE / chapter_folder
    d.mkdir(parents=True, exist_ok=True)
    return d


def end_pad(fps: int, seconds: float = 2.5) -> int:
    """How many extra frames to ask for so the last one stays up to be read.

    Every animation here ends on the frame that carries the point, usually a
    verdict or a finished coloring.  The update functions clamp their index,
    so any frames past the end simply repeat that last one.  Without a pause
    of a couple of seconds the loop wipes the answer away mid-sentence, which
    is the single most irritating thing an explanatory GIF can do.
    """
    return max(1, round(fps * seconds))


def note_below(fig, x=0.012, y=0.022, fontsize=11, color=INK2, ha="left"):
    """A live readout placed under the drawing, never on top of it.

    A number that changes has to sit somewhere, and inside the axes it will
    eventually land on an edge or a vertex, because the picture moves and the
    text does not.  Putting it in reserved space below the axes makes an
    overlap impossible rather than unlikely.  Call
    `fig.subplots_adjust(bottom=...)` first so the space is really there.
    """
    return fig.text(x, y, "", ha=ha, va="bottom", fontsize=fontsize,
                    color=color, family="monospace", zorder=20)


def edge_order_by_color(coloring) -> list[tuple[int, int]]:
    """Edges listed color by color, the order the build-up animations use."""
    n = len(coloring)
    colors = sorted({int(coloring[i, j]) for i in range(n)
                     for j in range(i + 1, n) if coloring[i, j] >= 0})
    out = []
    for c in colors:
        for i in range(n):
            for j in range(i + 1, n):
                if coloring[i, j] == c:
                    out.append((i, j))
    return out

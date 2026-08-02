"""Figures for chapter 10: the referee's card and the meeting guarantee."""

import itertools

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from common import (BASELINE, EDGE_COLORS, GREEN, INK2, MUTED, end_pad,
                    note_below, out_dir, save_anim, save_fig, style_axes,
                    title)
from ramsey_guide.core import (answer_maps, cover_holds_everywhere,
                               exceptional_columns, find_saturated_matrix)

OUT = out_dir("10-the-referee")

CELL = [EDGE_COLORS[0], EDGE_COLORS[1]]        # the two-symbol alphabet


def _draw_matrix(ax, matrix, x0=0.0, y0=0.0, size=0.5):
    s, n = matrix.shape
    for r in range(s):
        for z in range(n):
            ax.add_patch(Rectangle((x0 + z * size, y0 + (s - 1 - r) * size),
                                   size * 0.92, size * 0.92,
                                   fc=CELL[int(matrix[r, z])], ec="none",
                                   alpha=0.75, zorder=2))
    return size


def referee_gif(fps=10):
    """Pick any four columns of the found table: some row shows both colors.

    The table is the actual thirteen-row table this repository found and
    then verified against all seventy ways of choosing four of its eight
    columns.  The animation replays a handful of those checks: the chosen
    columns light up, the scan walks down the rows, and it always finds a
    row carrying both colors inside the chosen columns.
    """
    matrix = find_saturated_matrix(2, seed=0)
    s, n = matrix.shape
    size = 0.5
    picks = [(0, 1, 2, 3), (0, 2, 4, 6), (1, 3, 5, 7), (4, 5, 6, 7),
             (0, 3, 4, 7)]

    def winning_row(cols):
        return next(r for r in range(s)
                    if len({int(matrix[r, z]) for z in cols}) == 2)

    fig, ax = plt.subplots(figsize=(6.2, 7.6))
    fig.subplots_adjust(bottom=0.11, top=0.95)
    style_axes(ax, (-0.6, n * size + 0.6), (-0.6, s * size + 0.6))
    title(ax, "the referee's card: 13 rows, 8 columns, 2 symbols")
    _draw_matrix(ax, matrix, size=size)
    note = note_below(fig, x=0.5, ha="center", fontsize=11.5)

    marks = []

    def update(i):
        pick, phase = divmod(i, 6)
        pick = min(pick, len(picks) - 1)
        cols = picks[pick]
        win = winning_row(cols)
        for m in marks:
            m.remove()
        marks.clear()
        for z in cols:
            marks.append(ax.add_patch(Rectangle(
                (z * size - 0.03, -0.03), size * 0.92 + 0.06,
                s * size + 0.03, fc="none", ec=INK2, lw=1.6, zorder=5)))
        if phase < 4:
            row = min(int(phase / 3 * win + 0.999), win) if win else 0
            row = min(win, max(0, int(win * phase / 3)))
            y = (s - 1 - row) * size
            marks.append(ax.add_patch(Rectangle(
                (-0.06, y - 0.03), n * size + 0.06, size * 0.92 + 0.06,
                fc="none", ec=MUTED, lw=1.6, zorder=5)))
            note.set_text(f"columns {tuple(c + 1 for c in cols)}: "
                          "scanning for a row with both symbols")
            note.set_color(INK2)
        else:
            y = (s - 1 - win) * size
            marks.append(ax.add_patch(Rectangle(
                (-0.06, y - 0.03), n * size + 0.06, size * 0.92 + 0.06,
                fc="none", ec=GREEN, lw=2.6, zorder=6)))
            note.set_text(f"columns {tuple(c + 1 for c in cols)}: row "
                          f"{win + 1} shows both symbols\n(all 70 column "
                          "choices pass; the tests check every one)")
            note.set_color(GREEN)
        return []

    frames = 6 * len(picks) + end_pad(fps, 3.0)
    save_anim(fig, update, frames, OUT / "referee.gif", fps=fps)


def meeting_gif(fps=10):
    """Two words meet: some position agrees with one of the fixed answers.

    The top strip is your word, the bottom strip mine.  Between them sit the
    two answer strips, written once and for all before any words are chosen:
    the referee's answer to mine, and the referee's answer to yours.  The
    scan walks the positions until one of the two agreements appears, and
    the guarantee, verified exhaustively by the tests, is that it always
    does.
    """
    matrix = find_saturated_matrix(2, seed=0)
    s = matrix.shape[0]
    f, g = answer_maps(matrix, 2, 3)

    x = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
    y = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0]
    fy, gx = f(y), g(x)
    hits = [d for d in range(s) if x[d] == fy[d] or y[d] == gx[d]]
    first = hits[0]

    rows = [("your word", x, None),
            ("answer to mine", fy, "x"),
            ("answer to yours", gx, "y"),
            ("my word", y, None)]
    size = 0.5

    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    fig.subplots_adjust(bottom=0.17, top=0.95)
    style_axes(ax, (-3.6, s * size + 0.4), (-0.9, 4 * size + 0.75))
    for k, (label, word, _) in enumerate(rows):
        yy = (3 - k) * size * 1.28
        ax.text(-0.25, yy + size * 0.45, label, ha="right", fontsize=10,
                color=INK2)
        for d in range(s):
            ax.add_patch(Rectangle((d * size, yy), size * 0.9, size * 0.9,
                                   fc=CELL[word[d]], ec="none", alpha=0.8,
                                   zorder=2))
    note = note_below(fig, x=0.5, ha="center", fontsize=11.5)
    marks = []

    def update(i):
        d = min(i // 2, first)
        for m in marks:
            m.remove()
        marks.clear()
        marks.append(ax.add_patch(Rectangle(
            (d * size - 0.04, -0.12), size * 0.98, 4 * size * 1.28 + 0.14,
            fc="none", ec=INK2 if d < first else GREEN,
            lw=1.8 if d < first else 2.8, zorder=6)))
        if d < first:
            note.set_text(f"position {d + 1}: no agreement yet")
            note.set_color(INK2)
        else:
            which = ("your word matches the answer to mine"
                     if x[d] == fy[d] else
                     "my word matches the answer to yours")
            note.set_text(f"position {d + 1}: {which}\n"
                          "the tests check every pair of words: none escapes")
            note.set_color(GREEN)
        return []

    frames = 2 * (first + 1) + end_pad(fps, 3.0)
    save_anim(fig, update, frames, OUT / "meeting.gif", fps=fps)


if __name__ == "__main__":
    referee_gif()
    meeting_gif()
    print("wrote", OUT)

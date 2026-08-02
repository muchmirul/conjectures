"""The named numbers the guide keeps coming back to.

Anything marked "computed" is derived by `core.py` and re-checked in `tests/`.
Anything marked "quoted" is somebody else's theorem, written down here so the
guide and the tests refer to one copy of it.  `notes/research-content.md`
carries the sources.
"""

from __future__ import annotations

import math

from .core import (explicit_new_base, saturated_params, stage_colors,
                   upper_staircase)

# --- the small answers that are known exactly --------------------------------

#: quoted: the forcing sizes that are settled, and the one that is boxed in.
#: "forcing size" is the smallest table at which a one-color triangle becomes
#: unavoidable; the largest safe table is one less.
KNOWN_FORCING = {
    1: (3, "count to three"),
    2: (6, "Greenwood and Gleason 1955"),
    3: (17, "Greenwood and Gleason 1955"),
}

#: quoted: four colors is only known to lie in this range (lower end Chung
#: 1973, upper end Fettes, Kramer and Radziszowski 2004, both as reported in
#: Radziszowski's dynamic survey of small Ramsey numbers)
FOUR_COLOR_RANGE = (51, 62)

#: computed: the largest safe tables this repository builds and verifies
SAFE_TABLES = {2: 5, 3: 16}

# --- the growth rates the story turns on --------------------------------------

#: computed from the pentagon: multiplying it forever gives this many
#: vertices per color, the square root of five
PENTAGON_BASE = 5 ** 0.5

#: computed from the sixteen-vertex coloring: the cube root of sixteen
GF16_BASE = 16 ** (1 / 3)

#: quoted: the best fixed base known before the 2026 work, from five-color
#: constructions built out of Schur-type partitions
PRE_2026_BASE = 380 ** (1 / 5)

#: quoted: the record upper bound multiplies k factorial by this
FACTORIAL_RECORD_FACTOR = math.e - 1 / 6

# --- the 2026 construction's own parameters -----------------------------------

#: computed: the matrix sizes at alphabet size two, small enough that this
#: repository finds the matrix and verifies every promise exhaustively
H2_PARAMS = saturated_params(2)          # (3, 13)

#: computed: the parameters the paper prints for its smallest real stage
H3_PARAMS = saturated_params(3)          # (7, 57)

#: computed: the color count of the smallest real stage, 342; below it the
#: explicit bound says nothing and the trivial bound covers the gap
FIRST_STAGE_COLORS = stage_colors(3)

#: the exponent in the final answer: the base grows like the cube root of
#: the color count, divided by its logarithm
GROWTH_EXPONENT = 1 / 3


def upper_bound(k: int) -> int:
    """The simple staircase's forcing size at k colors."""
    return upper_staircase(k)[-1]


def old_lower_bound(k: int) -> float:
    """The pre-2026 record: a fixed base raised to the color count."""
    return PRE_2026_BASE ** k


def new_lower_bound(k: int) -> float:
    """The 2026 bound with its explicit constant, as printed in the paper."""
    return explicit_new_base(k) ** k


# --- history, in the order the guide tells it ----------------------------------

#: quoted: the milestones the article names, with the year each landed
MILESTONES = (
    (1955, "Greenwood and Gleason settle two colors at six and three colors "
           "at seventeen, using the sixteen-vertex coloring this guide draws"),
    (1971, "Erdős, McEliece and Taylor tie the growth question to Shannon's "
           "channel capacity"),
    (1973, "Chung shows four colors need at least fifty one people"),
    (1983, "Chung and Grinstead's survey records Erdős's cash prizes for the "
           "growth question"),
    (1995, "Alon and Orlitsky make the channel connection explicit"),
    (2021, "Schur-type constructions push the fixed base to its best value, "
           "about 3.28 vertices per color"),
    (2026, "the growth question is answered: the base grows without bound, "
           "like the cube root of the color count"),
)

__all__ = [
    "FACTORIAL_RECORD_FACTOR", "FIRST_STAGE_COLORS", "FOUR_COLOR_RANGE",
    "GF16_BASE", "GROWTH_EXPONENT", "H2_PARAMS", "H3_PARAMS", "KNOWN_FORCING",
    "MILESTONES", "PENTAGON_BASE", "PRE_2026_BASE", "SAFE_TABLES",
    "new_lower_bound", "old_lower_bound", "upper_bound",
]

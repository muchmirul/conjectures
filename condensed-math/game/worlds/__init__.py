"""The eight worlds, in the order they are played.

The route is fixed and each world is readable given the ones before it and
nothing else.  Worlds 1 to 3 are not condensed mathematics at all: they build
the four ordinary ideas the subject leans on and then break them, because a
reader who has not watched the break has no reason to accept the repair.
Worlds 4 to 6 are Lectures I to III, world 7 is Lectures IV to VI, and world 8
is Lectures VII to XI at the level of intuition this format can carry
honestly.

`tests/test_game.py` checks the route: every world reachable, every brick
supplying its own preliminary, its guess, its name and its mathematics.
"""

from __future__ import annotations

from ..model import World
from .w01_what_you_already_do import WORLD as W1
from .w02_nearness import WORLD as W2
from .w03_the_broken_test import WORLD as W3
from .w04_probes import WORLD as W4
from .w05_the_answer_sheet import WORLD as W5
from .w06_the_repair import WORLD as W6
from .w07_sums_that_land import WORLD as W7
from .w08_rings_and_geometry import WORLD as W8

WORLDS: list[World] = [W1, W2, W3, W4, W5, W6, W7, W8]

BY_SLUG = {w.slug: w for w in WORLDS}


def world_of(slug: str) -> World:
    return BY_SLUG[slug]

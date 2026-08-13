"""The shape of the topic: three parts, and the chapters inside each one.

Condensed mathematics is one subject but a wide one, so this topic is split
into three articles that are read in order.  Every build script reads this
file, so the folder names, the chapter titles and the reading order are
written down once and cannot drift between the guide, the web pages and the
playable pages.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTS_DIR = ROOT / "parts"
DOCS = ROOT.parent / "docs" / "condensed-math"

TOPIC = "condensed-math"
RAW = ("https://raw.githubusercontent.com/muchmirul/conjectures/main/"
       f"{TOPIC}/parts/")
SITE = f"https://muchmirul.github.io/conjectures/{TOPIC}/"


@dataclass(frozen=True)
class Part:
    slug: str
    number: int
    title: str
    blurb: str
    lectures: str
    chapters: dict[int, tuple[str, str]]

    @property
    def dir(self) -> Path:
        return PARTS_DIR / self.slug

    @property
    def article(self) -> Path:
        return self.dir / "ARTICLE.md"

    @property
    def guide(self) -> Path:
        return self.dir / "guide"

    @property
    def raw(self) -> str:
        return f"{RAW}{self.slug}/"

    @property
    def play_url(self) -> str:
        return f"{SITE}{self.slug}/play/"


PART_ONE = Part(
    slug="condensed-math01",
    number=1,
    title="Shapes You Can Only See By Probing Them",
    blurb=("Why a set with a topology is two structures badly glued, what a "
           "probe is, and how replacing a space by everything it says to "
           "probes makes subtraction work again."),
    lectures="Lectures I to III",
    chapters={
        0: ("00-start-here", "Start here"),
        1: ("01-two-real-lines", "Two real lines"),
        2: ("02-branching-probes", "Probes that branch"),
        3: ("03-what-a-shape-says", "What a shape says to a probe"),
        4: ("04-cut-and-glue", "Cut, and glue"),
        5: ("05-the-ghost", "The quotient with no points"),
        6: ("06-unfoldable-probes", "Probes that never need folding"),
        7: ("07-nothing-was-lost", "Nothing was lost"),
        8: ("08-counting-holes", "Counting holes"),
    },
)

PART_TWO = Part(
    slug="condensed-math02",
    number=2,
    title="Infinite Sums That Finally Land",
    blurb=("Endless sums are the reason topology was dragged into algebra in "
           "the first place. Solid groups are the ones where every such sum "
           "has exactly one answer, and their building blocks turn out to be "
           "products of copies of the whole numbers."),
    lectures="Lectures IV to VI",
    chapters={
        0: ("00-start-here", "Start here"),
        1: ("01-sums-with-nowhere-to-land", "Sums with nowhere to land"),
        2: ("02-weights-that-agree", "Weights that agree"),
        3: ("03-stacks-of-steps", "Every function is a stack of steps"),
        4: ("04-products-in-sums-out", "Products in, sums out"),
        5: ("05-the-solid-rule", "The solid rule"),
        6: ("06-where-the-real-line-goes", "Where the real line goes"),
        7: ("07-the-multiplication-table", "The multiplication table"),
        8: ("08-solidify-a-shape", "Solidify a shape, get its holes"),
    },
)

PART_THREE = Part(
    slug="condensed-math03",
    number=3,
    title="Rings That Know How To Integrate",
    blurb=("Carry the solid rule from whole numbers to rings, and geometry "
           "follows: functions near the edge of a space, cohomology with "
           "compact support, and a duality that was previously assembled by "
           "hand falls out of one adjoint."),
    lectures="Lectures VII to XI",
    chapters={
        0: ("00-start-here", "Start here"),
        1: ("01-a-ring-with-a-rule", "A ring with a rule for sums"),
        2: ("02-two-that-work", "Two rules that work"),
        3: ("03-the-real-lines-own-rule", "The real line's own rule"),
        4: ("04-functions-near-the-edge", "Functions near the edge"),
        5: ("05-compact-support", "Cohomology with compact support"),
        6: ("06-gluing-the-pictures", "Gluing the local pictures"),
        7: ("07-six-operations", "The six operations"),
        8: ("08-duality-watched", "Duality, watched"),
    },
)

PARTS = [PART_ONE, PART_TWO, PART_THREE]
BY_SLUG = {p.slug: p for p in PARTS}


def part_of(slug: str) -> Part:
    return BY_SLUG[slug]

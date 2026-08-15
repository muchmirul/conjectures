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
    title="Understanding Spaces Through Probes",
    blurb=("Learn how finite branching probes record closeness, why points "
           "alone miss important information, and how condensed sets repair "
           "kernels and cokernels without losing familiar spaces."),
    lectures="Lectures I to III",
    chapters={
        0: ("00-start-here", "Start here"),
        1: ("01-two-real-lines", "The same numbers, but different ideas of closeness"),
        2: ("02-branching-probes", "Building a probe from finite stages"),
        3: ("03-what-a-shape-says", "Mapping a probe into a space"),
        4: ("04-cut-and-glue", "The cut and glue rules"),
        5: ("05-the-ghost", "A quotient that points cannot detect"),
        6: ("06-unfoldable-probes", "Probes on which every cover splits"),
        7: ("07-nothing-was-lost", "Recovering familiar spaces"),
        8: ("08-counting-holes", "Keeping track of holes"),
    },
)

PART_TWO = Part(
    slug="condensed-math02",
    number=2,
    title="Giving Infinite Sums a Meaning",
    blurb=("Use compatible weights on finite probe stages to define solid "
           "groups. Then see how these groups handle infinite sums and why "
           "derived solidification recovers ordinary homology."),
    lectures="Lectures IV to VI",
    chapters={
        0: ("00-start-here", "Start here"),
        1: ("01-sums-with-nowhere-to-land", "One series, two ideas of distance"),
        2: ("02-weights-that-agree", "Compatible weights on a probe"),
        3: ("03-stacks-of-steps", "A basis for integer-valued functions"),
        4: ("04-products-in-sums-out", "Products and direct sums"),
        5: ("05-the-solid-rule", "The unique-extension rule"),
        6: ("06-where-the-real-line-goes", "Why the usual real line disappears"),
        7: ("07-the-multiplication-table", "Completed tensor products"),
        8: ("08-solidify-a-shape", "Solidification recovers homology"),
    },
)

PART_THREE = Part(
    slug="condensed-math03",
    number=3,
    title="Measure Rules for Rings and Geometry",
    blurb=("Give each ring a measure rule suited to its own notion of "
           "convergence. This leads from real and p-adic measures to boundary "
           "functions, compact support, the six operations, and duality."),
    lectures="Lectures VII to XI",
    chapters={
        0: ("00-start-here", "Start here"),
        1: ("01-a-ring-with-a-rule", "A ring and its legal measures"),
        2: ("02-two-that-work", "Two analytic examples"),
        3: ("03-the-real-lines-own-rule", "A measure rule for the real numbers"),
        4: ("04-functions-near-the-edge", "Global functions and boundary tails"),
        5: ("05-compact-support", "Compactly supported cohomology"),
        6: ("06-gluing-the-pictures", "Gluing affine patches"),
        7: ("07-six-operations", "The six operations"),
        8: ("08-duality-watched", "Coherent duality"),
    },
)

PARTS = [PART_ONE, PART_TWO, PART_THREE]
BY_SLUG = {p.slug: p for p in PARTS}


def part_of(slug: str) -> Part:
    return BY_SLUG[slug]

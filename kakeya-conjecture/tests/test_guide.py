"""The guide's typed tables, checked against the data they came from.

Some things the guide used to draw as pictures are now typed straight into the
chapters: a picture of a list is a list nobody can select, search or read
aloud.  The cost of typing them is that they can drift, so these tests read the
markdown back and compare it with `kakeya_guide.examples`.
"""

import re
from pathlib import Path

import pytest

from kakeya_guide.examples import STATUS, TIMELINE, blokhuis_mazzocca
from kakeya_guide.finite import dvir_bound, min_kakeya_size

GUIDE = Path(__file__).resolve().parents[1] / "guide"


def rows_of(markdown: str) -> list[list[str]]:
    """Every table row in a chapter, as lists of stripped cells."""
    out = []
    for line in markdown.splitlines():
        if line.startswith("|") and not set(line) <= set("|-: "):
            out.append([c.strip() for c in line.strip("|").split("|")])
    return out


def plain(cell: str) -> str:
    return cell.replace("**", "").strip()


# --- chapter 12: the timeline and the status table -------------------------

def test_the_timeline_in_the_chapter_matches_the_data():
    rows = rows_of((GUIDE / "12-the-proof" / "README.md").read_text())
    typed = {(int(plain(r[0])), plain(r[1])) for r in rows
             if plain(r[0]).isdigit() and len(r) == 3}
    for year, who, _ in TIMELINE:
        assert (year, who.replace("-", ", ")) in typed or (year, who) in typed, \
            f"{year} {who} is in the data but not in the chapter"


def test_every_dimension_of_the_status_table_is_in_the_chapter():
    text = (GUIDE / "12-the-proof" / "README.md").read_text()
    rows = rows_of(text)
    typed = {plain(r[0]): plain(r[1]) for r in rows if len(r) == 2}
    assert typed["1"].startswith("trivial")
    assert "Davies" in typed["2"] and "1971" in typed["2"]
    assert "Wang and Zahl" in typed["3"] and "2025" in typed["3"]
    assert typed["4"] == "open"
    assert set(STATUS) == {1, 2, 3, 4, 5}
    assert "open" in STATUS[5] and "5 and up" in typed


# --- chapter 10: the grid numbers ------------------------------------------

def test_the_grid_table_matches_what_the_search_finds():
    rows = rows_of((GUIDE / "10-on-a-grid" / "README.md").read_text())
    checked = 0
    for r in rows:
        m = re.fullmatch(r"\$q=(\d+)\$|q = ?(\d+)|\$q ?= ?(\d+)\$", plain(r[0]))
        if not m:
            continue
        q = int(next(g for g in m.groups() if g))
        grid, dirs, smallest, floor = (int(plain(c)) for c in r[1:5])
        assert grid == q * q
        assert dirs == q + 1
        assert smallest == min_kakeya_size(q, 2) == blokhuis_mazzocca(q)
        assert floor == dvir_bound(q, 2)
        checked += 1
    assert checked == 4, "the chapter should quote four grid sizes"


# --- every chapter: the figures it points at exist -------------------------

#: Cards for link previews, not part of any chapter, so no README points at
#: them.  They are git-ignored and rebuilt locally by their chapter script.
LOCAL_ONLY = {"thumbnail.png"}


@pytest.mark.parametrize("chapter", sorted(p.name for p in GUIDE.iterdir()
                                           if p.is_dir()))
def test_chapter_figures_exist_and_are_used(chapter):
    folder = GUIDE / chapter
    text = (folder / "README.md").read_text()
    referenced = set(re.findall(r'src="([^"]+\.(?:gif|png))"', text))
    on_disk = {p.name for p in folder.iterdir()
               if p.suffix in (".gif", ".png") and p.name not in LOCAL_ONLY}
    assert referenced <= on_disk, f"{chapter} points at a missing figure"
    assert on_disk <= referenced, f"{chapter} has a figure nothing points at"


def test_no_figure_is_only_words():
    """Text-only pictures belong in the markdown, not in a PNG.

    A crude guard: the figures that were text cards are gone, and the ones that
    remain are named after things that are drawn.
    """
    gone = {"statement_card.png", "dvir.png", "grid_lies.png", "status.png",
            "timeline.png", "roadmap.png", "web.png"}
    present = {p.name for p in GUIDE.glob("*/*.png")} | \
              {p.name for p in GUIDE.glob("*/*.gif")}
    assert not (gone & present)

"""The article and the repository have to agree with each other.

These tests do not check mathematics.  They check the things that quietly rot:
a figure that was renamed, a chapter that lost its picture, a number written
into the prose that no longer matches the number the code produces.
"""

import re
from pathlib import Path

import pytest

from ramsey_guide.core import upper_staircase
from ramsey_guide.examples import (FIRST_STAGE_COLORS, FOUR_COLOR_RANGE,
                                   GF16_BASE, PENTAGON_BASE, PRE_2026_BASE)

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = ROOT / "ARTICLE.md"
GUIDE = ROOT / "guide"

IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def test_every_figure_the_article_asks_for_exists():
    missing = [src for _, src in IMAGE.findall(ARTICLE.read_text())
               if not (ROOT / src).exists()]
    assert missing == []


def test_every_rendered_figure_is_actually_used():
    """A figure nobody looks at is a figure nobody maintains."""
    used = {src for _, src in IMAGE.findall(ARTICLE.read_text())}
    have = {str(p.relative_to(ROOT)) for p in GUIDE.rglob("*")
            if p.suffix in {".gif", ".png"}}
    assert sorted(have - used) == []


def test_every_figure_has_alt_text():
    empty = [src for alt, src in IMAGE.findall(ARTICLE.read_text())
             if len(alt.strip()) < 12]
    assert empty == []


def test_every_chapter_folder_has_a_readme():
    chapters = sorted(p for p in GUIDE.iterdir() if p.is_dir())
    assert len(chapters) == 13
    assert all((c / "README.md").exists() for c in chapters)


def test_the_chapter_readmes_match_the_article():
    """The chapter files are generated, so a stale one means someone forgot.

    Regenerating is `make guide`.  This test fails if ARTICLE.md moved on and
    the chapter copies did not, which is the exact drift this repository has
    already suffered once in another topic.
    """
    import build_guide

    sections = build_guide.split_sections(ARTICLE.read_text())
    for number, (folder, _) in build_guide.CHAPTERS.items():
        body = build_guide.localise(sections[number][1], folder)
        readme = (GUIDE / folder / "README.md").read_text()
        for paragraph in [p for p in body.split("\n\n") if p.strip()][:3]:
            assert paragraph.strip() in readme, f"{folder} is stale"


def test_the_numbers_in_the_prose_match_the_code():
    text = ARTICLE.read_text()
    assert f"{PENTAGON_BASE:.2f}" in text                    # 2.24
    assert f"{GF16_BASE:.2f}" in text                        # 2.52
    assert f"{PRE_2026_BASE:.2f}" in text                    # 3.28
    assert ", ".join(str(v) for v in upper_staircase(5)) in text
    assert str(2 ** 15) in text                              # 32768
    lo, hi = FOUR_COLOR_RANGE
    assert f"between {lo} and {hi}" in text
    assert str(FIRST_STAGE_COLORS) in text                   # 342
    assert "ten to the sixtieth" in text
    assert "57 rows" in text and "114 colors" in text


def test_the_article_does_not_promise_more_than_it_delivers():
    """Claims this repository is not allowed to make."""
    text = ARTICLE.read_text().lower()
    assert "we prove the theorem" not in text
    assert "every idea is shown as an animation" not in text
    # it must say plainly that the full construction is not implemented
    assert "described, not implemented" in text
    # and it must not pretend the new bound wins at drawable sizes
    assert "older constructions give bigger tables" in text


def test_the_glossary_names_every_invented_word():
    text = ARTICLE.read_text()
    glossary = text.split("The plain words, and the real ones")[1]
    for invented in ("a safe table", "the forcing size", "people per color",
                     "a room", "a palette", "a team", "the referee's card",
                     "the two answer lists"):
        assert invented in glossary


def test_the_article_never_uses_an_em_dash():
    assert "—" not in ARTICLE.read_text()

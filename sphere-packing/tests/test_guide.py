"""The article and the repository have to agree with each other.

These tests do not check mathematics.  They check the things that quietly rot:
a figure that was renamed, a chapter that lost its picture, a number written
into the prose that no longer matches the number the code produces.
"""

import re
from pathlib import Path

import pytest

from sphere_packing_guide.examples import (ALPHA_STAR, FOUND_BOUNDS,
                                           KL_EXPONENT, LP_RATE, known_density)

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
    assert f"{ALPHA_STAR:.16f}" in text
    assert "0.59905576" in text
    assert f"{known_density(2) * 100:.2f} percent" in text
    assert f"{FOUND_BOUNDS[2] * 100:.2f} percent" in text
    assert "40.6 times smaller" in text


def test_the_article_does_not_promise_more_than_it_delivers():
    """Two claims this repository is not allowed to make."""
    text = ARTICLE.read_text().lower()
    assert "we prove the theorem" not in text
    assert "every idea is shown as an animation" not in text
    # and it must say plainly that the main argument is not implemented
    assert "described, not implemented" in text


def test_the_glossary_names_every_invented_word():
    text = ARTICLE.read_text()
    glossary = text.split("The plain words, and the real ones")[1]
    for invented in ("certificate", "the two sign rules", "the balanced function",
                     "the wall", "halvings per dimension"):
        assert invented in glossary

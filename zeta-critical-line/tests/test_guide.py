"""The article and the repository have to agree with each other.

These tests do not check mathematics.  They check the things that quietly rot:
a figure that was renamed, a chapter that lost its picture, a number written
into the prose that no longer matches the number the code produces.
"""

import re
from pathlib import Path

import pytest

from zeta_guide.core import CROSSOVER_DIAL, shape_h, shape_hd
from zeta_guide.examples import (FIRST_ZERO, METHOD_CEILING, MT_DISTINCT,
                                 MT_ON_LINE, OLD_RECORD, RECORD_RACE,
                                 XI_PRIME_FLAT)

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
    assert f"{FIRST_ZERO:.2f}" in text                       # 14.13
    assert "two thirds" in text and "five sixths" in text
    assert "five twelfths" in text and "0.4166" in text
    assert f"{MT_ON_LINE:.4f}" in text                       # 0.6725
    assert f"{MT_DISTINCT:.5f}" in text                      # 0.83625
    assert str(METHOD_CEILING) in text                       # 0.68185
    assert "0.016" in text
    assert "1.04" in text and "1.26" in text and "1.70" in text
    assert f"{XI_PRIME_FLAT[0]}" in text                     # 0.85838
    assert f"{XI_PRIME_FLAT[1]}" in text                     # 0.92919
    assert "44 microphones" in text
    assert "ten trillion" in text
    # the years of the record race the prose tells
    for year in (1914, 1942, 1974, 1989, 2020, 2026):
        assert str(year) in text


def test_the_article_does_not_promise_more_than_it_delivers():
    """Claims this repository is not allowed to make."""
    text = ARTICLE.read_text().lower()
    assert "we prove the theorem" not in text
    assert "every idea is shown as an animation" not in text
    # it must say plainly that the full construction is not implemented
    assert "described, not implemented" in text
    # it must not claim any bearing on the hypothesis itself
    assert "no bearing on the riemann hypothesis" in text
    # and it must carry the effectivity caveat
    assert "at any height a computer can" in text


def test_the_article_credits_the_ancestry():
    """Montgomery had 2/3 under RH in 1973; the paper removed the RH.  The
    guide must never present the number itself as new."""
    text = ARTICLE.read_text()
    assert "Montgomery" in text
    assert "Baluyot" in text and "Goldston" in text
    assert "Suriajaya" in text and "Turnage-Butterbaugh" in text
    assert "1973" in text


def test_the_glossary_names_every_invented_word():
    text = ARTICLE.read_text()
    glossary = text.split("The plain words, and the real ones")[1]
    for invented in ("the line", "the strip", "a clean pin", "a mirror pair",
                     "a microphone", "the window", "the dial", "the table",
                     "a bowl", "a saddle", "the see-saw law", "the count",
                     "the energy", "the whole-number trick",
                     "the certificate"):
        assert invented in glossary, invented


def test_the_article_never_uses_an_em_dash():
    assert "—" not in ARTICLE.read_text()


def test_the_paper_is_in_the_repository():
    pdf = ROOT.parent / "docs" / "zeta-critical-line" / "paper" \
        / "more-than-two-thirds.pdf"
    assert pdf.exists() and pdf.stat().st_size > 100_000
    assert "more-than-two-thirds.pdf" in ARTICLE.read_text()

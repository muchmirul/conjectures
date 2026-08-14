"""The three articles, the chapter files and the built pages must line up.

Prose that lives in two places drifts, so this topic generates the chapter
READMEs and the web pages from one ARTICLE.md per part.  These tests check
the generation really happened, that every picture an article asks for is on
disk, and that the house rules the repository writes by are kept.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

import build_docs
import build_guide
import build_interactive
from condensed_guide.parts import DOCS, PARTS


# --- the articles themselves ------------------------------------------------

@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_each_part_has_its_article(part):
    assert part.article.exists()
    text = part.article.read_text()
    assert text.startswith("# ")
    assert len(text) > 4000


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_the_article_has_every_numbered_section(part):
    sections = build_guide.split_sections(part.article.read_text())
    assert sorted(sections) == sorted(part.chapters)


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_every_picture_the_article_asks_for_is_on_disk(part):
    text = part.article.read_text()
    refs = re.findall(r"!\[[^\]]*\]\((guide/[^)]+)\)", text)
    assert refs, "an article with no pictures is not this repository's style"
    missing = [r for r in refs if not (part.dir / r).exists()]
    assert not missing, f"{part.slug} is missing {missing}"


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_every_picture_carries_alt_text(part):
    for alt, src in re.findall(r"!\[([^\]]*)\]\((guide/[^)]+)\)",
                               part.article.read_text()):
        assert len(alt) > 20, f"{src} has thin alt text"


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_animations_are_only_used_where_something_moves(part):
    """A figure that merely redraws itself should have been a png.

    The rule the repository writes by is that motion is reserved for
    mathematics, so the gifs are listed here by name and any new one has to
    be justified by being added to this list.
    """
    moving = {
        "condensed-math01": {"hero.gif", "bijection.gif", "landing.gif",
                             "glue.gif", "ghost.gif", "folding.gif",
                             "roundtrip.gif", "winding.gif", "torus.gif"},
        "condensed-math02": {"hero.gif", "padic_walk.gif", "steps.gif",
                             "finite_reach.gif", "extension.gif",
                             "divisible.gif", "rulers.gif", "solidify.gif"},
        "condensed-math03": {"hero.gif", "tail.gif", "compact_support.gif",
                             "gluing.gif", "duality.gif"},
    }
    found = {p.name for p in part.guide.rglob("*.gif")}
    assert found == moving[part.slug]


#: the rotating camera shots, which must loop seamlessly instead of pausing
ROTATING = {"torus.gif", "solidify.gif", "duality.gif"}


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_animations_hold_their_last_frame_long_enough_to_read(part):
    """A loop that wipes the answer away mid-sentence is unreadable.

    Every animation that builds towards a point ends on the frame carrying
    it, and that frame must stay up for about two and a half seconds.  The
    rotating camera shots are the exception: they go round once and start
    again, so a pause would show as a stutter.
    """
    from PIL import Image

    for gif in sorted(part.guide.rglob("*.gif")):
        with Image.open(gif) as im:
            im.seek(im.n_frames - 1)
            hold = im.info.get("duration", 0) / 1000
        if gif.name in ROTATING:
            assert hold < 0.2, f"{gif.name} rotates, so it must not pause"
        else:
            assert hold >= 2.4, \
                f"{gif.name} holds its last frame only {hold:.2f}s"


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_the_article_carries_a_glossary(part):
    text = part.article.read_text()
    assert "## Glossary" in text
    body = text.split("## Glossary", 1)[1]
    rows = [l for l in body.splitlines() if l.startswith("|")]
    assert len(rows) > 12, "every invented phrase needs its standard name"


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_the_article_says_what_it_checks(part):
    text = part.article.read_text()
    assert "## Checking it yourself" in text
    assert "make test" in text


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_the_article_points_at_the_lectures(part):
    text = part.article.read_text()
    assert "arxiv.org/abs/2605.03658" in text
    assert "How this part lines up with the lectures" in text or \
           "How this guide lines up" in text
    # every cited page must be a page the lectures actually have
    for page in re.findall(r"2605\.03658v1#page=(\d+)", text):
        assert 5 <= int(page) <= 78


def chapter_bodies(part):
    """Each numbered chapter's text, keyed by its number."""
    out, current, buf = {}, None, []
    for line in part.article.read_text().splitlines():
        m = re.match(r"^## (\d+) · ", line)
        if m:
            if current is not None:
                out[current] = "\n".join(buf)
            current, buf = int(m.group(1)), []
        elif re.match(r"^## ", line):
            if current is not None:
                out[current] = "\n".join(buf)
            current, buf = None, []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf)
    return out


def chapters_with_maths(part):
    """Which numbered chapters currently state their mathematics."""
    bodies = chapter_bodies(part)
    return {n: bodies[n] for n in sorted(bodies)
            if n > 0 and "### The mathematics" in bodies[n]}


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_every_statement_is_paired_with_words_and_a_simulation(part):
    """The rule for this topic: the mathematics is never shown on its own.

    Each formal statement is paired with a reading of every symbol in ordinary
    words and with the simulation that lets the reader move it. This checks
    the pairing in every numbered chapter. Coverage is checked separately
    below, so a missing statement cannot disappear from this loop unnoticed.
    """
    for n, body in chapters_with_maths(part).items():
        block = body.split("### The mathematics", 1)[1]
        assert "```math" in block or "$" in block, \
            f"{part.slug} chapter {n}: the heading carries no statement"
        assert "arxiv.org/pdf/2605.03658v1#page=" in block, \
            f"{part.slug} chapter {n}: the statement does not cite the lectures"
        assert "**Reading the symbols.**" in block, \
            f"{part.slug} chapter {n}: no plain reading of the symbols"
        assert "**Why it matters.**" in block, \
            f"{part.slug} chapter {n}: no explanation of the statement's role"
        assert "**In the simulation.**" in block, \
            f"{part.slug} chapter {n}: the statement is not tied to its activity"
        assert f"play/{n:02d}.html" in block, \
            f"{part.slug} chapter {n}: the pairing does not reach the activity"


def test_every_chapter_writes_out_its_mathematics():
    """Every numbered chapter states the cited mathematics explicitly."""
    done = {p.slug: sorted(chapters_with_maths(p)) for p in PARTS}
    wanted = {p.slug: sorted(c for c in p.chapters if c > 0) for p in PARTS}
    assert done == wanted


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_the_maths_renders_on_the_built_page(part):
    """A formula that does not render is worse than no formula."""
    html = (DOCS / part.slug / "index.html").read_text()
    assert "tex-chtml.js" in html, "MathJax is not loaded"
    opened = html.count('<section class="mathpair">')
    assert opened == len(chapters_with_maths(part)), \
        f"{part.slug}: {opened} paired blocks rendered from the article's blocks"
    assert opened == html.count("</section>"), "a paired block was left open"
    if opened:
        assert '<div class="eq">' in html, "no display maths was rendered"


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_no_em_dashes(part):
    assert "—" not in part.article.read_text()


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_every_numbered_section_offers_something_to_play_with(part):
    text = part.article.read_text()
    for n in part.chapters:
        assert f"play/{n:02d}.html" in text, f"chapter {n} has no simulation"


# --- the generated chapter files -------------------------------------------

@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_every_chapter_readme_was_generated(part):
    for n, (folder, title) in part.chapters.items():
        readme = part.guide / folder / "README.md"
        assert readme.exists()
        text = readme.read_text()
        assert text.startswith("# ")
        assert "all of part" in text          # the navigation footer


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_chapter_readmes_point_at_pictures_beside_them(part):
    for n, (folder, title) in part.chapters.items():
        text = (part.guide / folder / "README.md").read_text()
        for src in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
            assert not src.startswith("guide/"), "path was not localised"
            assert (part.guide / folder / src).resolve().exists(), src


def test_the_chapter_files_are_generated_not_hand_written():
    """Regenerating must not change anything, or a copy has been edited."""
    before = {p: p.read_text() for part in PARTS
              for p in part.guide.rglob("README.md")}
    build_guide.main()
    after = {p: p.read_text() for p in before}
    changed = [str(p) for p in before if before[p] != after[p]]
    assert not changed, f"hand edits would be lost in {changed}"


# --- the built web pages ----------------------------------------------------

@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_the_web_page_was_built(part):
    page = DOCS / part.slug / "index.html"
    assert page.exists()
    html = page.read_text()
    assert part.title in html
    assert "<h2" in html


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_the_web_page_embeds_every_simulation(part):
    html = (DOCS / part.slug / "index.html").read_text()
    for n in part.chapters:
        assert f'<iframe src="play/{n:02d}.html?embed"' in html
        assert f'<a href="play/{n:02d}.html">' in html
    assert html.count("<iframe") == len(part.chapters)


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_the_web_page_offers_a_fallback_for_every_picture(part):
    """A gif that has not loaded looks like a broken one, so try twice."""
    html = (DOCS / part.slug / "index.html").read_text()
    imgs = re.findall(r'<img src="([^"]+)" alt="[^"]*" data-fallbacks="([^"]+)"',
                      html)
    assert imgs
    for src, fallbacks in imgs:
        assert src in fallbacks.replace("&amp;", "&")
        assert len(fallbacks.split(";")) == 2


@pytest.mark.parametrize("page", [DOCS / "index.html"] +
                         [DOCS / p.slug / "index.html" for p in PARTS],
                         ids=lambda p: p.parent.name)
def test_the_built_pages_are_well_formed(page):
    """Every tag opened is closed, in order.

    A bold paragraph opens and closes with an asterisk exactly as an italic
    one does, and the closing line of two of the parts is entirely bold, so
    the hero header was once closed there by mistake.  This catches that and
    anything like it.
    """
    from html.parser import HTMLParser

    void = {"img", "br", "meta", "link", "hr", "input", "source"}

    class Check(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack, self.bad = [], []

        def handle_starttag(self, tag, attrs):
            if tag not in void:
                self.stack.append(tag)

        def handle_endtag(self, tag):
            if tag in void:
                return
            if not self.stack or self.stack[-1] != tag:
                self.bad.append((tag, self.getpos()[0], self.stack[-3:]))
            else:
                self.stack.pop()

    c = Check()
    c.feed(page.read_text())
    assert not c.bad, f"{page.name}: mismatched closings {c.bad}"
    assert not c.stack, f"{page.name}: never closed {c.stack}"


@pytest.mark.parametrize("part", PARTS, ids=lambda p: p.slug)
def test_the_hero_subtitle_is_the_opening_line_only(part):
    html = (DOCS / part.slug / "index.html").read_text()
    assert html.count("<header") == 1
    assert html.count("</header>") == 1
    assert html.count('class="subtitle"') == 1


def test_the_landing_page_lists_all_three_parts():
    html = (DOCS / "index.html").read_text()
    for part in PARTS:
        assert f'href="{part.slug}/"' in html
        assert part.title in html


def test_the_parts_link_to_each_other():
    for part in PARTS:
        html = (DOCS / part.slug / "index.html").read_text()
        for other in PARTS:
            if other.slug == part.slug:
                continue
            assert f'href="../{other.slug}/index.html"' in html
        # the source articles link by file; the built pages must not
        assert "ARTICLE.md" not in html


def test_the_paper_is_kept_with_the_topic():
    pdf = DOCS / "paper" / "lectures-on-condensed-mathematics.pdf"
    assert pdf.exists()
    assert pdf.stat().st_size > 100_000


# --- the notes --------------------------------------------------------------

def test_the_research_notes_mark_every_claim():
    notes = Path(build_guide.__file__).parent / "notes" / "research-content.md"
    text = notes.read_text()
    for word in ("computed", "quoted", "finite shadow"):
        assert word in text
    assert text.count("|") > 100, "the claim tables look truncated"


def test_the_curriculum_notes_exist():
    notes = Path(build_guide.__file__).parent / "notes" / "curriculum.md"
    assert notes.exists()
    assert "The split" in notes.read_text()

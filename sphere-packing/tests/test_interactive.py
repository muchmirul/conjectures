"""The playable pages must compute the same numbers as the library.

The pages re-implement ball volumes, the Laguerre building blocks and the
density bound in JavaScript, because they run in a browser with no network.
Two implementations of the same formula drift.  These tests run the page's
JavaScript and compare it with `sphere_packing_guide`, so a change to one side
that is not made on the other fails here rather than in front of a reader.

If node is not installed the comparison is skipped, but the structural checks
still run.
"""

import json
import math
import shutil
import subprocess
from pathlib import Path

import pytest

import build_interactive
from sphere_packing_guide.core import (ball_fraction_of_cube, ball_volume,
                                       density_bound, is_admissible,
                                       polynomial_part)
from sphere_packing_guide.examples import ALPHA_STAR, FOUND_CERTIFICATES, LP_RATE

PLAY = Path(build_interactive.OUT)
NODE = shutil.which("node") or shutil.which("nodejs")

CERT = FOUND_CERTIFICATES[2][:4]


def run_js(snippet: str):
    out = subprocess.run([NODE, "-e", build_interactive.MATHS + snippet],
                         capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


# --- structure -------------------------------------------------------------

def test_every_chapter_has_a_playable_page():
    """One page per part of the progression, except the three removed by
    request: chapters 7, 10 and 12 have no simulation page."""
    assert len(build_interactive.CHAPTERS) == 10
    assert {n for n, *_ in build_interactive.CHAPTERS} == \
        {0, 1, 2, 3, 4, 5, 6, 8, 9, 11}
    for num, *_ in build_interactive.CHAPTERS:
        assert (PLAY / f"{num:02d}.html").exists()
    for gone in (7, 10, 12):
        assert not (PLAY / f"{gone:02d}.html").exists()
    assert (PLAY / "index.html").exists()


def test_the_pages_are_self_contained():
    """No library, no network: they must work offline and from a file."""
    for page in PLAY.glob("*.html"):
        text = page.read_text()
        assert "http://" not in text
        assert "https://" not in text
        assert "<script src" not in text


def test_every_page_has_a_canvas_and_a_readout_except_the_index():
    for num, *_ in build_interactive.CHAPTERS:
        text = (PLAY / f"{num:02d}.html").read_text()
        assert '<canvas id="c"' in text
        assert 'id="out"' in text
        assert "Try this." in text


def test_the_built_page_embeds_every_simulation():
    """The rule is that the simulations are in the article, not beside it."""
    page = (Path(build_interactive.OUT).parent / "index.html").read_text()
    for num, *_ in build_interactive.CHAPTERS:
        assert f'<iframe src="play/{num:02d}.html?embed"' in page
        assert f'<a href="play/{num:02d}.html">' in page
    assert page.count("<iframe") == 10


def test_the_embedded_pages_hide_their_own_chrome():
    """Embedded, a play page must not repeat the heading the article gives it."""
    text = (Path(build_interactive.OUT) / "04.html").read_text()
    assert "body.embed" in text
    assert "classList.add('embed')" in text


def test_the_article_links_every_playable_page():
    article = (Path(build_interactive.ROOT) / "ARTICLE.md").read_text()
    for num, *_ in build_interactive.CHAPTERS:
        assert f"play/{num:02d}.html" in article


# --- the two implementations must agree ------------------------------------

@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_ball_volume_matches_the_library():
    got = run_js("console.log(JSON.stringify("
                 "[1,2,3,5,8,24,100].map(ballVolume)))")
    for d, v in zip([1, 2, 3, 5, 8, 24, 100], got):
        assert v == pytest.approx(ball_volume(d), rel=1e-10)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_ball_fraction_matches_the_library():
    got = run_js("console.log(JSON.stringify("
                 "[1,2,3,10,20,30].map(ballFractionOfCube)))")
    for d, v in zip([1, 2, 3, 10, 20, 30], got):
        assert v == pytest.approx(ball_fraction_of_cube(d), rel=1e-9)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_sign_carrying_polynomial_matches_the_library():
    coeffs = json.dumps(CERT)
    got = run_js(f"const c={coeffs};console.log(JSON.stringify("
                 "[0,0.4,0.9,1.0,1.6,2.4].map(r=>polyPart(c,2,r))))")
    for r, v in zip([0, 0.4, 0.9, 1.0, 1.6, 2.4], got):
        assert v == pytest.approx(float(polynomial_part(CERT, 2, r)), rel=1e-9,
                                  abs=1e-12)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_density_bound_matches_the_library():
    coeffs = json.dumps(CERT)
    got = run_js(f"console.log(JSON.stringify([densityBound({coeffs},2),"
                 f"admissible({coeffs},2)]))")
    assert got[0] == pytest.approx(density_bound(CERT, 2), rel=1e-9)
    assert got[1] is is_admissible(CERT, 2)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_constants_match_the_library():
    got = run_js("console.log(JSON.stringify("
                 "[ALPHA_STAR,LP_RATE,SIGN_RADIUS,KL_EXPONENT]))")
    assert got[0] == pytest.approx(ALPHA_STAR, rel=1e-14)
    assert got[1] == pytest.approx(LP_RATE, rel=1e-14)
    assert got[2] == pytest.approx(1 / math.pi, rel=1e-14)
    assert got[3] == pytest.approx(0.59905576)

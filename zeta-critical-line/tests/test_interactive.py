"""The playable pages must compute the same numbers as the library.

The pages re-implement zeta, the zero-waves, the prime density and the
paper's shape functions in JavaScript, because they run in a browser with no
network.  Two implementations of the same mathematics drift.  These tests run
the pages' JavaScript and compare it with `zeta_guide`, so a change to one
side that is not made on the other fails here rather than in front of a
reader.

If node is not installed the comparison is skipped, but the structural checks
still run.
"""

import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest

import build_interactive
from zeta_guide import core as C
from zeta_guide.examples import MT_DISTINCT, MT_ON_LINE

PLAY = Path(build_interactive.OUT)
NODE = shutil.which("node") or shutil.which("nodejs")


def run_js(snippet: str):
    out = subprocess.run([NODE, "-e", build_interactive.MATHS + snippet],
                         capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


# --- structure -------------------------------------------------------------

def test_every_chapter_has_a_playable_page():
    """One page per part of the progression, except the two that are pure
    reading: chapters 4 and 11 have no simulation page."""
    assert len(build_interactive.CHAPTERS) == 11
    assert {n for n, *_ in build_interactive.CHAPTERS} == \
        {0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 12}
    for num, *_ in build_interactive.CHAPTERS:
        assert (PLAY / f"{num:02d}.html").exists()
    for gone in (4, 11):
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
    assert page.count("<iframe") == 11


def test_the_embedded_pages_hide_their_own_chrome():
    """Embedded, a play page must not repeat the heading the article gives it."""
    text = (Path(build_interactive.OUT) / "03.html").read_text()
    assert "body.embed" in text
    assert "classList.add('embed')" in text


def test_the_article_links_every_playable_page():
    article = (Path(build_interactive.ROOT) / "ARTICLE.md").read_text()
    for num, *_ in build_interactive.CHAPTERS:
        assert f"play/{num:02d}.html" in article


def test_the_pages_css_is_not_broken_by_doubled_braces():
    """A formatting accident once left '{{' in a page's stylesheet."""
    for page in PLAY.glob("*.html"):
        assert "{{" not in page.read_text()


# --- the two implementations must agree ------------------------------------

@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_embedded_zeros_are_the_shipped_table():
    got = run_js("console.log(JSON.stringify(ZEROS))")
    assert np.allclose(got, C.zero_heights()[:50], atol=1e-8)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_zeta_matches_the_library():
    got = run_js("console.log(JSON.stringify(["
                 "zetaEM(0.5,14.134725),zetaEM(0.5,33.3),"
                 "zetaEM(0.9,21.0),zetaEM(2.0,0.0)]))")
    for js, s in zip(got, (0.5 + 14.134725j, 0.5 + 33.3j, 0.9 + 21.0j,
                           2.0 + 0j)):
        ours = C.zeta_em(s)
        assert js[0] == pytest.approx(ours.real, abs=1e-9)
        assert js[1] == pytest.approx(ours.imag, abs=1e-9)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_staircase_rebuild_matches_the_library():
    got = run_js("console.log(JSON.stringify("
                 "[psiWaves(10.5,0),psiWaves(10.5,20),psiWaves(37.2,50)]))")
    for js, (x, k) in zip(got, ((10.5, 0), (10.5, 20), (37.2, 50))):
        ours = float(C.psi_from_waves(np.array([x]), k)[0])
        # the pages embed the zero heights at twelve decimals
        assert js == pytest.approx(ours, abs=1e-7)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_prime_density_matches_the_library():
    got = run_js("console.log(JSON.stringify("
                 "[primeDensity(120.0,16),primeDensity(133.7,16)]))")
    for js, tau in zip(got, (120.0, 133.7)):
        ours = float(C.prime_density(np.array([tau]), 16)[0])
        assert js == pytest.approx(ours, abs=1e-12)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_shape_functions_match_the_library():
    got = run_js("console.log(JSON.stringify("
                 "[shapeH(1),shapeHd(1),shapeF(1),shapeH(0.6),shapeF(0.42),"
                 "energyPerCount(1),mtConstant()]))")
    expect = [C.shape_h(1), C.shape_hd(1), C.shape_f(1), C.shape_h(0.6),
              C.shape_f(0.42), C.energy_per_count(1),
              C.montgomery_taylor_closed_form()]
    assert got == pytest.approx(expect, rel=1e-12)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_constants_match_the_examples():
    got = run_js("const c=mtConstant();"
                 "console.log(JSON.stringify([2-1/c,(3-1/c)/2]))")
    assert got[0] == pytest.approx(MT_ON_LINE, rel=1e-12)
    assert got[1] == pytest.approx(MT_DISTINCT, rel=1e-12)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_whole_number_trick_matches_the_library():
    got = run_js("console.log(JSON.stringify("
                 "[...Array(6)].map((_,i)=>[charge(i+1),floor3(i+1)])))")
    for m, (c, f) in enumerate(got, start=1):
        assert c == C.whole_number_charge(m)
        assert f == C.whole_number_floor(m)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_prime_terms_match_the_library():
    got = run_js("console.log(JSON.stringify(vmTerms(16)))")
    ours = C.von_mangoldt_terms(16)
    assert [n for n, _ in got] == [n for n, _ in ours]
    for (_, wj), (_, wp) in zip(got, ours):
        assert wj == pytest.approx(wp, rel=1e-12)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_microphone_response_matches_the_library():
    fam = C.ToyFamily(T=100.0, dial=1.0)
    got = run_js("console.log(JSON.stringify("
                 "[toyResponse(0),toyResponse(1.1),toyResponse(2.3),"
                 "toyResponse(4.0),TOY_AL2]))")
    for js, r in zip(got[:4], (0.0, 1.1, 2.3, 4.0)):
        ours = float(fam.response(np.array([r]))[0])
        assert js == pytest.approx(ours, abs=1e-5)
    us = np.linspace(-fam.L / 2, fam.L / 2, 4001)
    aL2 = float(np.trapezoid(fam.window(us) ** 2, us)) * fam.L
    assert got[4] == pytest.approx(aL2, rel=1e-5)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_array_total_is_constant():
    """The sampling identity, as the page computes it."""
    got = run_js(
        "const out=[];"
        "for(const f of [0.1,0.5,0.9]){"
        "let t=0;for(let k=-40;k<=46;k++){"
        "const v=toyResponse((2+f)*TOY_H-k*TOY_H);t+=v*v;}"
        "out.push(t/TOY_AL2);}console.log(JSON.stringify(out))")
    for total in got:
        assert total == pytest.approx(1.0, rel=1e-4)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_two_by_two_eigenvalues_are_right():
    got = run_js("console.log(JSON.stringify([eig2(1,0,0),eig2(0,1,0),"
                 "eig2(1,0.8,0)]))")
    for js, (a, b, c) in zip(got, ((1, 0, 0), (0, 1, 0), (1, 0.8, 0))):
        ours = sorted(np.linalg.eigvalsh(np.array([[a, b], [b, c]])))
        assert js == pytest.approx(ours, abs=1e-12)

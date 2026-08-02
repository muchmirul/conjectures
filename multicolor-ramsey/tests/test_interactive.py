"""The playable pages must compute the same numbers as the library.

The pages re-implement the colorings, the triangle check and the growth
formulas in JavaScript, because they run in a browser with no network.  Two
implementations of the same mathematics drift.  These tests run the pages'
JavaScript and compare it with `ramsey_guide`, so a change to one side that
is not made on the other fails here rather than in front of a reader.

If node is not installed the comparison is skipped, but the structural checks
still run.
"""

import itertools
import json
import shutil
import subprocess
from pathlib import Path

import pytest

import build_interactive
from ramsey_guide import core as C
from ramsey_guide.examples import GF16_BASE, PENTAGON_BASE, PRE_2026_BASE

PLAY = Path(build_interactive.OUT)
NODE = shutil.which("node") or shutil.which("nodejs")


def run_js(snippet: str):
    out = subprocess.run([NODE, "-e", build_interactive.MATHS + snippet],
                         capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


# --- structure -------------------------------------------------------------

def test_every_chapter_has_a_playable_page():
    """The rule is one page per part of the progression, so all thirteen."""
    assert len(build_interactive.CHAPTERS) == 13
    for num, *_ in build_interactive.CHAPTERS:
        assert (PLAY / f"{num:02d}.html").exists()
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
    assert page.count("<iframe") == 13


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
def test_the_pentagon_matches_the_library():
    got = run_js("console.log(JSON.stringify(pentagonColoring()))")
    assert got == C.pentagon_coloring().tolist()


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_sixteen_table_matches_the_library():
    got = run_js("console.log(JSON.stringify(gf16Coloring(16)))")
    assert got == C.gf16_coloring().tolist()


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_triangle_check_matches_the_library():
    got = run_js("console.log(JSON.stringify(["
                 "monoTriangles(pentagonColoring()).length,"
                 "monoTriangles(gf16Coloring(16)).length]))")
    assert got == [0, 0]


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_product_matches_the_library():
    got = run_js("const P=productColoring(pentagonColoring(),"
                 "pentagonColoring(),2);"
                 "console.log(JSON.stringify([P.length,"
                 "monoTriangles(P).length]))")
    p = C.pentagon_coloring()
    product = C.product_coloring(p, p, 2)
    assert got == [len(product), len(C.monochromatic_triangles(product))]


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_staircase_matches_the_library():
    got = run_js("console.log(JSON.stringify(upperStaircase(8)))")
    assert got == C.upper_staircase(8)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_constants_match_the_library():
    got = run_js("console.log(JSON.stringify("
                 "[PENTAGON_BASE,GF16_BASE,PRE_2026_BASE,"
                 "explicitNewBase(342),explicitNewBase(1e70)]))")
    assert got[0] == pytest.approx(PENTAGON_BASE, rel=1e-12)
    assert got[1] == pytest.approx(GF16_BASE, rel=1e-12)
    assert got[2] == pytest.approx(PRE_2026_BASE, rel=1e-12)
    assert got[3] == pytest.approx(C.explicit_new_base(342), rel=1e-9)
    assert got[4] == pytest.approx(C.explicit_new_base(1e70), rel=1e-9)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_block_product_floor_matches_the_library():
    got = run_js("console.log(JSON.stringify("
                 "[...Array(14)].map((_,i)=>productLower(i+1))))")
    assert got == [C.best_product_lower(k) for k in range(1, 15)]


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_embedded_referee_table_is_the_found_one():
    got = run_js("console.log(JSON.stringify(REFEREE))")
    assert got == C.find_saturated_matrix(2, seed=0).tolist()


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_page_finds_a_saturated_row_for_every_column_choice():
    got = run_js(
        "let worst=1e9,count=0;"
        "for(let a=0;a<8;a++)for(let b=a+1;b<8;b++)"
        "for(let c=b+1;c<8;c++)for(let d=c+1;d<8;d++)"
        "{const r=saturatedRow([a,b,c,d]);count++;if(r<0)worst=-1;}"
        "console.log(JSON.stringify([count,worst>=-0.5]))")
    assert got == [70, True]


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_channel_code_matches_the_library():
    got = run_js("console.log(JSON.stringify(CODEBOOK.map((u,i)=>"
                 "CODEBOOK.map((v,j)=>i===j?-2:distinguishable(u,v)))))")
    for i, u in enumerate(C.C5_CODEBOOK):
        for j, v in enumerate(C.C5_CODEBOOK):
            if i != j:
                assert got[i][j] >= 0
                d = got[i][j]
                assert not C.pentagon_confusable(u[d], v[d])

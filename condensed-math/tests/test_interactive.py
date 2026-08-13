"""The playable pages must compute the same numbers as the library.

The pages re-implement probes, weightings, the completed tensor rule, Smith
normal form and the measure sizes in JavaScript, because they run in a
browser with no network.  Two implementations of the same mathematics drift.
These tests run the pages' JavaScript and compare it with `condensed_guide`,
so a change to one side that is not made on the other fails here rather than
in front of a reader.

They also run each page against a small DOM stub, which catches the errors a
syntax check cannot: a misspelt variable, a control read before it exists, an
arithmetic slip that throws when a slider reaches its end.

If node is not installed the JavaScript checks are skipped and the structural
ones still run.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest

import build_interactive
from condensed_guide import core as C
from condensed_guide.parts import DOCS, PARTS

NODE = shutil.which("node") or shutil.which("nodejs")
STUB = Path(__file__).resolve().parent / "domstub.js"


def run_js(snippet: str):
    out = subprocess.run([NODE, "-e", build_interactive.MATHS + snippet],
                         capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def play_dir(part):
    return DOCS / part.slug / "play"


# --- structure --------------------------------------------------------------

def test_every_chapter_of_every_part_has_a_playable_page():
    assert set(build_interactive.CHAPTERS) == {p.slug for p in PARTS}
    for part in PARTS:
        chapters = build_interactive.CHAPTERS[part.slug]
        assert {n for n, *_ in chapters} == set(part.chapters)
        for n, *_ in chapters:
            assert (play_dir(part) / f"{n:02d}.html").exists()
        assert (play_dir(part) / "index.html").exists()


def test_the_pages_are_self_contained():
    """No library, no network: they must work offline and from a file."""
    for part in PARTS:
        for page in play_dir(part).glob("*.html"):
            text = page.read_text()
            assert "http://" not in text
            assert "https://" not in text
            assert "<script src" not in text


def test_every_page_has_a_canvas_a_readout_and_a_prompt():
    for part in PARTS:
        for n, *_ in build_interactive.CHAPTERS[part.slug]:
            text = (play_dir(part) / f"{n:02d}.html").read_text()
            assert '<canvas id="c"' in text
            assert 'id="out"' in text
            assert "Try this." in text


def test_every_page_has_at_least_one_control():
    for part in PARTS:
        for n, heading, lede, try_, controls, widget, note in \
                build_interactive.CHAPTERS[part.slug]:
            assert 'type="range"' in controls or 'class="pick"' in controls, \
                f"{part.slug} chapter {n} has nothing to move"


def test_every_page_says_what_is_computed_and_what_is_quoted():
    for part in PARTS:
        for n, heading, lede, try_, controls, widget, note in \
                build_interactive.CHAPTERS[part.slug]:
            assert len(note) > 60, f"{part.slug} chapter {n} has a thin note"


def test_the_embedded_pages_hide_their_own_chrome():
    text = (play_dir(PARTS[0]) / "03.html").read_text()
    assert "body.embed" in text
    assert "classList.add('embed')" in text


def test_the_pages_css_is_not_broken_by_doubled_braces():
    """A formatting accident once left '{{' in a page's stylesheet."""
    for part in PARTS:
        for page in play_dir(part).glob("*.html"):
            head = page.read_text().split("</style>")[0]
            assert "{{" not in head


# --- every page really runs -------------------------------------------------

@pytest.mark.skipif(NODE is None, reason="node is not installed")
@pytest.mark.parametrize("slug", [p.slug for p in PARTS])
def test_every_page_runs_through_every_control_position(slug):
    part = next(p for p in PARTS if p.slug == slug)
    for n, *_ in build_interactive.CHAPTERS[slug]:
        page = play_dir(part) / f"{n:02d}.html"
        out = subprocess.run([NODE, str(STUB), str(page)],
                             capture_output=True, text=True, timeout=180)
        assert out.returncode == 0, \
            f"{slug} chapter {n} threw:\n{out.stderr[:900]}"
        result = json.loads(out.stdout)
        assert result["drawCalls"] > 20, f"{slug} chapter {n} drew nothing"
        assert result["readoutLength"] > 20, \
            f"{slug} chapter {n} printed no readout"


# --- the two implementations must agree -------------------------------------

@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_probes_match_the_library():
    got = run_js("console.log(JSON.stringify({"
                 "cantor:probeSizes(cantorProbe(5)),"
                 "seq:probeSizes(sequenceProbe(6)),"
                 "p3:probeSizes(pAdicProbe(3,4)),"
                 "p5:probeSizes(pAdicProbe(5,3))}))")
    assert got["cantor"] == C.cantor(5).sizes()
    assert got["seq"] == C.convergent_sequence(6).sizes()
    assert got["p3"] == C.p_adic(3, 4).sizes()
    assert got["p5"] == C.p_adic(5, 3).sizes()


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_fibres_match_the_library():
    got = run_js("const S=cantorProbe(4);"
                 "console.log(JSON.stringify("
                 "S.levels[2].map(l=>fibre(S,l,4,2).length)))")
    S = C.cantor(4)
    assert got == [len(S.fibre(l, at=4, over=2)) for l in S.levels[2]]


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_weightings_obey_the_agreement_rule():
    got = run_js(
        "const S=cantorProbe(4),leaves={};"
        "S.levels[4].forEach((l,i)=>leaves[l]=((i*7)%5)-2);"
        "const w=measureFromLeaves(S,leaves);"
        "console.log(JSON.stringify({ok:measureOk(S,w),"
        "top:w[0][''],levels:w.map(x=>Object.values(x)"
        ".reduce((a,b)=>a+b,0))}))")
    S = C.cantor(4)
    leaves = {l: ((i * 7) % 5) - 2 for i, l in enumerate(S.levels[4])}
    m = C.measure_from_leaves(S, leaves)
    m.check()
    assert got["ok"] is True
    assert got["top"] == m.total()
    assert got["levels"] == [m.total()] * 5


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_integral_does_not_depend_on_the_level():
    got = run_js(
        "const S=cantorProbe(5),leaves={};"
        "S.levels[5].forEach(l=>leaves[l]=1);"
        "const w=measureFromLeaves(S,leaves),f={};"
        "S.levels[2].forEach((l,k)=>f[l]=1+3*(k%4));"
        "const out=[];"
        "for(let j=2;j<=5;j++)out.push(integrate(S,w,refineFn(S,f,2,j),j));"
        "console.log(JSON.stringify(out))")
    S = C.cantor(5)
    w = C.counting_measure(S)
    f = {l: 1 + 3 * (k % 4) for k, l in enumerate(S.levels[2])}
    expect = [w.integrate(C.refine(S, f, 2, j), j) for j in range(2, 6)]
    assert got == expect
    assert len(set(got)) == 1


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_geometric_sum_matches_the_library():
    got = run_js("console.log(JSON.stringify({"
                 "s2:geomPartialSums(2,7),s3:geomPartialSums(3,5),"
                 "lim2:geomLimitTimes(2),lim3:geomLimitTimes(3)}))")
    assert got["s2"] == [int(s) for s in C.geometric_partial_sums(2, 7)]
    assert got["s3"] == [int(s) for s in C.geometric_partial_sums(3, 5)]
    assert got["lim2"] == float(C.geometric_limit(2))
    assert got["lim3"] == pytest.approx(float(C.geometric_limit(3)))


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_p_adic_size_matches_the_library():
    got = run_js("console.log(JSON.stringify("
                 "[1,2,4,8,12,27,0].map(n=>pAdicAbsInt(n,2))))")
    from fractions import Fraction
    expect = [C.p_adic_abs(Fraction(n), 2) for n in (1, 2, 4, 8, 12, 27, 0)]
    assert got == pytest.approx(expect)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_tensor_rule_matches_the_library():
    names = ["Z", "Z_p", "Z_l", "Z[[T]]", "Z[[U]]", "R"]
    got = run_js("const n=%s;const o={};"
                 "for(const a of n)for(const b of n)o[a+'|'+b]=solidTensor(a,b);"
                 "console.log(JSON.stringify(o))" % json.dumps(names))
    for a in names:
        for b in names:
            assert got[f"{a}|{b}"] == C.solid_tensor(a, b)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_agree_on_which_entries_are_quoted():
    names = ["Z_p", "Z_l", "Z[[T]]", "Z[[U]]", "R"]
    got = run_js("const n=%s;const o={};"
                 "for(const a of n)for(const b of n)o[a+'|'+b]=quotedTensor(a,b);"
                 "console.log(JSON.stringify(o))" % json.dumps(names))
    for a in names:
        for b in names:
            assert got[f"{a}|{b}"] == C.quoted_tensor(a, b)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_smith_normal_form_matches_the_library():
    cases = [[[2]], [[2, 0], [0, 3]], [[1, 2], [3, 4]], [[0], [2]],
             [[6, 0], [0, 4]], [[0, 0], [0, 0]]]
    got = run_js("console.log(JSON.stringify(%s.map(smith)))"
                 % json.dumps(cases))
    for js, m in zip(got, cases):
        assert js == C.smith_normal_form(m)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_holes_match_the_library():
    got = run_js("console.log(JSON.stringify("
                 "Object.keys(SHAPES).map(k=>[k,homology(k)])))")
    for name, H in got:
        ours = C.SHAPES[name]().homology()
        assert [(h["free"], h["torsion"]) for h in H] == ours


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_exterior_ranks_match_the_library():
    got = run_js("console.log(JSON.stringify("
                 "[1,2,3,4,5,6].map(exteriorRanks)))")
    for js, n in zip(got, range(1, 7)):
        assert js == C.exterior_ranks(n)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_measure_sizes_match_the_library():
    vals = [1.0, 0.4, 2.5, 0.1]
    got = run_js("const v=%s;console.log(JSON.stringify("
                 "[0.4,0.7,1.0,1.6,2.0].map(p=>[lpSize(v,p),"
                 "mergeRatio(v,[[0,1],[2,3]],p),worstMergeRatio(4,p)])))"
                 % json.dumps(vals))
    for js, p in zip(got, (0.4, 0.7, 1.0, 1.6, 2.0)):
        assert js[0] == pytest.approx(C.lp_size(vals, p))
        assert js[1] == pytest.approx(C.merge_ratio(vals, [[0, 1], [2, 3]], p))
        assert js[2] == pytest.approx(C.worst_merge_ratio(4, p))


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_unit_ball_matches_the_library():
    got = run_js("const o=[];"
                 "for(const p of [0.5,1.0,2.0])"
                 "for(let i=0;i<8;i++)o.push(lpBallPoint(i*Math.PI/4,p));"
                 "console.log(JSON.stringify(o))")
    k = 0
    for p in (0.5, 1.0, 2.0):
        for i in range(8):
            theta = i * np.pi / 4
            c, s = np.cos(theta), np.sin(theta)
            scale = (abs(c) ** p + abs(s) ** p) ** (1 / p)
            assert got[k] == pytest.approx([c / scale, s / scale], abs=1e-12)
            k += 1


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_pages_edge_counts_match_the_library():
    got = run_js("const o=[];"
                 "for(let top=1;top<=6;top++)for(let m=1;m<=6;m++)"
                 "o.push([lineEdgeRank(top,m),crossEdgeRank(top,m)]);"
                 "console.log(JSON.stringify(o))")
    k = 0
    for top in range(1, 7):
        for m in range(1, 7):
            assert got[k] == [C.line_edge_quotient_rank(top, m),
                              C.cross_edge_quotient_rank(top, m)]
            k += 1

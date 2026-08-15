"""The game must keep its own promises.

Three kinds of check live here.

*Shape.*  Every brick has to run concept, then intuition, then experiment, and
each stage has to contain what that stage is for: a plain statement of the
idea, a guess made before the answer exists, something the reader runs, the
name the literature uses, and the mathematics.  A brick that quietly drops its
preliminary, its guess or its symbols fails here.

*It runs.*  Each world is played from the first press to the last by
`gamestub.js`, which supplies a DOM, clicks whatever the page offers and then
moves every control every widget created.  A page that throws anywhere in that
walk fails here rather than in front of a reader.

*The numbers are the library's numbers.*  The widgets reuse
`build_interactive.MATHS`, which the play pages' tests already compare against
`condensed_guide` point by point.  What is checked here is the arithmetic the
game adds on top of it, and the fact that the reused block really is present.

If node is not installed the JavaScript checks are skipped and the structural
ones still run.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path

import pytest

from condensed_guide import core as C
from condensed_guide.parts import DOCS
from game import widgets
from game.model import STAGES, Ask, Math, Name, Play, Say, Try
from game.worlds import WORLDS

NODE = shutil.which("node") or shutil.which("nodejs")
STUB = Path(__file__).resolve().parent / "gamestub.js"
OUT = DOCS / "game"

ALL_BRICKS = [(w, b) for w in WORLDS for b in w.bricks]


def page_of(world):
    return OUT / world.page


# --- the route --------------------------------------------------------------

def test_there_are_eight_worlds_numbered_in_order():
    assert [w.number for w in WORLDS] == list(range(1, len(WORLDS) + 1))
    assert len({w.slug for w in WORLDS}) == len(WORLDS)


def test_every_world_says_what_it_promises():
    for w in WORLDS:
        assert len(w.promise) > 80, f"world {w.number} promises too little"
        assert w.title


def test_brick_slugs_are_unique_inside_a_world():
    for w in WORLDS:
        slugs = [b.slug for b in w.bricks]
        assert len(set(slugs)) == len(slugs)


# --- the pedagogy: concept, then intuition, then experiment -----------------

@pytest.mark.parametrize("world,brick", ALL_BRICKS,
                         ids=[f"{w.number}-{b.slug}" for w, b in ALL_BRICKS])
def test_every_brick_runs_the_three_stages_in_order(world, brick):
    assert [key for key, *_ in brick.stages] == [k for k, _, _ in STAGES]
    for key, label, _blurb, beats in brick.stages:
        assert beats, f"world {world.number} {brick.slug}: {key} is empty"


@pytest.mark.parametrize("world,brick", ALL_BRICKS,
                         ids=[f"{w.number}-{b.slug}" for w, b in ALL_BRICKS])
def test_every_brick_states_its_idea_and_its_preliminary(world, brick):
    """Assume the reader knows nothing: say what is needed, in plain words."""
    where = f"world {world.number} {brick.slug}"
    assert len(brick.idea) > 40, f"{where}: the concept is not stated"
    assert brick.need, f"{where}: no preliminary"
    for need in brick.need:
        assert len(need) > 25, f"{where}: thin preliminary {need!r}"
    assert len(brick.hold) > 40, f"{where}: nothing carried out of the brick"


@pytest.mark.parametrize("world,brick", ALL_BRICKS,
                         ids=[f"{w.number}-{b.slug}" for w, b in ALL_BRICKS])
def test_the_concept_stage_only_states_the_idea(world, brick):
    for beat in brick.concept:
        assert isinstance(beat, Say), \
            f"world {world.number} {brick.slug}: concept holds a {beat.kind}"


@pytest.mark.parametrize("world,brick", ALL_BRICKS,
                         ids=[f"{w.number}-{b.slug}" for w, b in ALL_BRICKS])
def test_the_intuition_stage_ends_in_a_guess(world, brick):
    kinds = [b.kind for b in brick.intuition]
    where = f"world {world.number} {brick.slug}"
    assert kinds.count("ask") == 1, f"{where}: intuition needs exactly one guess"
    assert kinds[-1] == "ask", f"{where}: the guess must come last"
    ask = brick.intuition[-1]
    assert len(ask.options) >= 2, f"{where}: a guess with one option is not one"
    for label, reply in ask.options:
        assert label and len(reply) > 60, \
            f"{where}: option {label!r} is answered too thinly"


@pytest.mark.parametrize("world,brick", ALL_BRICKS,
                         ids=[f"{w.number}-{b.slug}" for w, b in ALL_BRICKS])
def test_the_experiment_stage_runs_something_then_names_it(world, brick):
    kinds = [b.kind for b in brick.experiment]
    where = f"world {world.number} {brick.slug}"
    assert kinds.count("play") + kinds.count("try") >= 1, \
        f"{where}: nothing to run"
    assert kinds.count("name") == 1, f"{where}: the idea is never named"
    assert kinds.count("math") == 1, f"{where}: no mathematics"
    assert kinds.index("name") < kinds.index("math"), \
        f"{where}: the symbols arrive before the name"
    assert min(i for i, k in enumerate(kinds) if k in ("play", "try")) \
        < kinds.index("name"), f"{where}: named before it was run"


@pytest.mark.parametrize("world,brick", ALL_BRICKS,
                         ids=[f"{w.number}-{b.slug}" for w, b in ALL_BRICKS])
def test_every_name_and_every_formula_is_explained(world, brick):
    where = f"world {world.number} {brick.slug}"
    for beat in brick.experiment:
        if isinstance(beat, Name):
            assert beat.plain and beat.standard and beat.notation
            assert len(beat.why) > 40, f"{where}: {beat.standard} unexplained"
        if isinstance(beat, Math):
            assert beat.statement
            assert len(beat.reading) > 120, \
                f"{where}: the symbols are not read out"
            if beat.cite:
                assert beat.url.startswith("https://arxiv.org/")


@pytest.mark.parametrize("world,brick", ALL_BRICKS,
                         ids=[f"{w.number}-{b.slug}" for w, b in ALL_BRICKS])
def test_hands_on_experiments_withhold_their_answer(world, brick):
    for beat in brick.experiment:
        if isinstance(beat, Try):
            assert len(beat.steps) >= 2, f"{brick.slug}: too few steps to do"
            assert len(beat.found) > 120, f"{brick.slug}: thin finding"
        if isinstance(beat, Play):
            assert beat.widget in widgets.NAMES, \
                f"{brick.slug}: unknown widget {beat.widget}"
            assert len(beat.notice) > 100, \
                f"{brick.slug}: the widget is not told what to watch for"


def test_every_widget_that_exists_is_used_somewhere():
    used = {beat.widget for _w, b in ALL_BRICKS for beat in b.experiment
            if isinstance(beat, Play)}
    assert used <= set(widgets.NAMES)
    assert set(widgets.NAMES) - used == set(), \
        f"unused widgets: {set(widgets.NAMES) - used}"


def test_every_world_has_something_to_move():
    for w in WORLDS:
        plays = [beat for b in w.bricks for beat in b.experiment
                 if isinstance(beat, Play)]
        assert plays, f"world {w.number} has no simulation"


def test_the_route_never_assumes_what_it_has_not_built():
    """A later idea may lean on an earlier one; never the other way round."""
    seen: list[str] = []
    for w in WORLDS:
        for b in w.bricks:
            seen.append(b.slug)
    # the specification written in world 3 is answered in world 6
    assert seen.index("what-we-must-build") < seen.index("the-ghost")
    # probes exist before anything is asked of them
    assert seen.index("splitting-forever") < seen.index("what-a-shape-says")
    # gluing before the object it defines
    assert seen.index("gluing") < seen.index("a-condensed-set")
    # sums land before rings that must respect them
    assert seen.index("the-solid-rule") < seen.index("multiplying-too")


# --- the pages --------------------------------------------------------------

def test_every_world_has_a_page_and_the_index_lists_it():
    index = (OUT / "index.html").read_text()
    for w in WORLDS:
        assert page_of(w).exists(), f"world {w.number} was not built"
        assert f'href="{w.page}"' in index
        assert w.title in index


def test_the_pages_carry_no_library_and_fetch_nothing():
    for w in WORLDS:
        text = page_of(w).read_text()
        assert "<script src" not in text
        assert "<link rel=\"stylesheet\"" not in text
        assert "url(http" not in text
        # the only outbound links are citations a reader follows on purpose
        for url in re.findall(r'href="(https?://[^"]+)"', text):
            assert url.startswith(("https://arxiv.org/",
                                   "https://github.com/")), url


def test_each_page_carries_its_whole_world():
    for w in WORLDS:
        text = page_of(w).read_text()
        for b in w.bricks:
            assert b.title in text
            assert b.hold in text


def test_the_pages_reuse_the_libraries_javascript_rather_than_copying_it():
    """The widgets must not reimplement probes or measures on their own."""
    import build_interactive

    text = page_of(WORLDS[3]).read_text()
    for fn in ("function cantorProbe(", "function measureFromLeaves(",
               "function worstMergeRatio(", "function smith("):
        assert fn in build_interactive.MATHS
        assert fn in text
        assert fn not in widgets.WIDGET_JS, \
            f"{fn} is duplicated in the game's own JavaScript"


def test_the_stage_labels_reach_the_reader():
    text = page_of(WORLDS[0]).read_text()
    for _key, label, blurb in STAGES:
        assert label in text and blurb in text


def test_the_front_page_explains_the_three_stages():
    index = (OUT / "index.html").read_text()
    for _key, label, _blurb in STAGES:
        assert f"<b>{label}</b>" in index


# --- every world really plays ----------------------------------------------

def run_page(path: Path) -> dict:
    out = subprocess.run([NODE, str(STUB), str(path)],
                         capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, f"{path.name} threw:\n{out.stderr[:1200]}"
    return json.loads(out.stdout)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
@pytest.mark.parametrize("world", WORLDS, ids=[w.slug for w in WORLDS])
def test_every_world_plays_from_the_first_press_to_the_last(world):
    result = run_page(page_of(world))
    assert result["finished"], \
        f"world {world.number} did not reach its ending"
    # one press per step, plus one per guess and one per hands-on reveal
    steps = sum(2 + len(b.stages) + len(b.beats) for b in world.bricks)
    assert result["clicks"] >= steps * 0.6
    assert result["textLength"] > 8000
    assert result["drawCalls"] > 100, \
        f"world {world.number} drew almost nothing"


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_front_page_is_static_and_has_no_script():
    assert "<script>" not in (OUT / "index.html").read_text()


# --- the arithmetic the game adds on top of the library ---------------------

def run_js(snippet: str):
    import build_interactive
    source = build_interactive.MATHS + widgets.HELPERS + snippet
    out = subprocess.run([NODE, "-e", source],
                         capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


def fractions_in_window(centre: Fraction, half: Fraction, Q: int) -> int:
    """The count the zoom widget prints, in exact arithmetic."""
    seen = set()
    for q in range(1, Q + 1):
        lo = -((-(centre - half) * q).__floor__())   # ceil((centre-half)*q)
        hi = ((centre + half) * q).__floor__()
        for k in range(lo, hi + 1):
            seen.add(Fraction(k, q))
    return len(seen)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_crowding_count_is_exact():
    got = run_js("console.log(JSON.stringify(["
                 "fractionsInWindow(1,0.5,6),fractionsInWindow(1,0.25,12),"
                 "fractionsInWindow(1,0.125,20)]))")
    expect = [fractions_in_window(Fraction(1), Fraction(1, 2), 6),
              fractions_in_window(Fraction(1), Fraction(1, 4), 12),
              fractions_in_window(Fraction(1), Fraction(1, 8), 20)]
    assert got == expect
    assert expect[0] < expect[1] < expect[2] or expect[2] > 0
    # looking more finely never empties a window
    assert all(n > 0 for n in expect)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_ghosts_witness_never_settles_down():
    """The value function is constant on no box, at any stage."""
    got = run_js("const out=[];for(let n=1;n<=10;n++)out.push(wobbleInBox(n));"
                 "console.log(JSON.stringify({wob:out,"
                 "v0:valueOf('000'),v1:valueOf('100'),v2:valueOf('111')}))")
    assert got["wob"] == [2.0 ** -n for n in range(1, 11)]
    assert all(w > 0 for w in got["wob"])
    assert got["v0"] == 0.0
    assert got["v1"] == 0.5
    assert got["v2"] == pytest.approx(0.875)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_merge_widget_agrees_with_the_library_on_the_ceiling():
    got = run_js(
        "const vals=[1,1,1,1],g=[[0,1,2,3]],out=[];"
        "for(const p of [0.5,0.75,1,1.5,2])"
        "out.push([mergeRatio(vals,g,p),worstMergeRatio(4,p)]);"
        "console.log(JSON.stringify(out))")
    for (measured, closed), p in zip(got, [0.5, 0.75, 1, 1.5, 2]):
        assert measured == pytest.approx(closed)
        assert closed == pytest.approx(C.worst_merge_ratio(4, p))
        assert (closed <= 1 + 1e-12) == (p <= 1)


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_holes_widget_agrees_with_the_library():
    got = run_js("console.log(JSON.stringify("
                 "['circle','figure eight','sphere','torus','klein bottle']"
                 ".map(homology)))")
    for name, rows in zip(["circle", "figure eight", "sphere", "torus",
                           "klein bottle"], got):
        expect = C.SHAPES[name]().homology()
        assert [(r["free"], r["torsion"]) for r in rows] == \
            [(free, tors) for free, tors in expect]
    # the Klein bottle's two-torsion is the entry a careless move would lose
    assert got[4][1]["torsion"] == [2]


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_the_series_widget_lands_on_minus_one_only_in_the_base_two_rule():
    got = run_js("const s=geomPartialSums(2,8);console.log(JSON.stringify({"
                 "sums:s,ord:s.map(x=>Math.abs(x+1)),"
                 "padic:s.map(x=>pAdicAbsInt(x+1,2))}))")
    assert got["sums"] == [int(s) for s in C.geometric_partial_sums(2, 8)]
    assert got["ord"] == [2.0 ** (n + 1) for n in range(8)]
    assert got["padic"] == [2.0 ** -(n + 1) for n in range(8)]
    assert got["ord"][-1] > got["ord"][0]
    assert got["padic"][-1] < got["padic"][0]

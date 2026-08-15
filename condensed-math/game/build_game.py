"""Build the game: one page per world, plus a front page.

    cd condensed-math && make game

Writes ../docs/condensed-math/game/NN.html, one per world, and an index.
Each page is self contained: no libraries and no network requests, so a page
works offline and straight from a file.  The only outbound links are the
citations into the lectures, which a reader follows on purpose.

The reading interface is deliberately plain.  One column, one button, one
thing on screen at a time.  A reader presses Continue, reads a paragraph,
makes a guess, runs something, and is then told what it is called.  There is
no scoring, no branching and nothing to lose: a guess that misses gets a reply
explaining which instinct misled, and the route carries on.

Each brick renders in the same three stages, in the same order, always:

    Concept      what the idea is, stated before any story
    Intuition    what it feels like, ending in a guess
    Experiment   something the reader runs, then the name and the mathematics

The mathematics in the widgets is not written here.  `build_interactive.MATHS`
already carries probes, measures, the p-adic size, the merge ratio and Smith
normal form in JavaScript, and the play pages' tests already check that block
against the Python library.  This page includes the same block, so a widget
and a chapter simulation cannot quietly disagree about a number.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:                    # so build_interactive
    sys.path.insert(0, str(HERE.parent))                # imports when run
if str(HERE.parent.parent) not in sys.path:             # directly
    sys.path.insert(0, str(HERE.parent.parent))

from build_interactive import MATHS                     # noqa: E402
from condensed_guide.parts import DOCS                  # noqa: E402
from game.model import STAGES                           # noqa: E402
from game.widgets import WIDGET_JS                      # noqa: E402
from game.worlds import WORLDS                          # noqa: E402

OUT = DOCS / "game"

LECTURES = "https://arxiv.org/abs/2605.03658"
GUIDE = "../index.html"


# --- the content, as data the page can read -------------------------------


def beat_dict(beat) -> dict:
    d = asdict(beat) if is_dataclass(beat) else dict(beat)
    if d["kind"] == "ask":
        d["options"] = [list(o) for o in d["options"]]
    if d["kind"] == "try":
        d["steps"] = list(d["steps"])
    return d


def brick_dict(brick) -> dict:
    return {
        "slug": brick.slug,
        "title": brick.title,
        "idea": brick.idea,
        "need": list(brick.need),
        "stages": [{"key": key, "label": label, "blurb": blurb,
                    "beats": [beat_dict(b) for b in beats]}
                   for key, label, blurb, beats in brick.stages],
        "hold": brick.hold,
    }


def world_dict(world) -> dict:
    return {
        "number": world.number,
        "slug": world.slug,
        "title": world.title,
        "promise": world.promise,
        "bricks": [brick_dict(b) for b in world.bricks],
    }


# --- the look --------------------------------------------------------------

CSS = """
 :root{--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
        --line:#e1e0d9;--card:#ffffff;--blue:#2a78d6;--green:#008300;
        --red:#d03b3b;--violet:#4a3aa7;}
 @media (prefers-color-scheme: dark){
   :root{--surface:#15150f;--ink:#f2f1ea;--ink2:#c9c7bd;--muted:#8d8b82;
         --line:#33322c;--card:#1c1c15;}
 }
 *{box-sizing:border-box}
 html{scroll-behavior:smooth}
 body{margin:0;padding:0 0 10vh;background:var(--surface);color:var(--ink);
   font:17.5px/1.75 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,
   sans-serif;}
 main{max-width:680px;margin:0 auto;padding:0 20px}
 header.top{position:sticky;top:0;z-index:5;background:var(--surface);
   border-bottom:1px solid var(--line);padding:10px 20px 0}
 header.top .inner{max-width:680px;margin:0 auto;display:flex;
   align-items:baseline;gap:12px;font-size:13px;color:var(--muted)}
 header.top a{color:var(--muted);text-decoration:none}
 header.top a:hover{color:var(--blue)}
 .bar{max-width:680px;margin:8px auto 0;height:3px;background:var(--line);
   border-radius:2px;overflow:hidden}
 .bar i{display:block;height:100%;width:0;background:var(--blue);
   transition:width .35s ease}
 h1{font-size:26px;line-height:1.25;margin:34px 0 8px}
 .promise{color:var(--ink2);font-style:italic;margin:0 0 12px}
 p{margin:1.05em 0}
 em{font-style:italic}
 a{color:var(--blue)}
 .step{animation:rise .28s ease both}
 @keyframes rise{from{opacity:0;transform:translateY(6px)}to{opacity:1;
   transform:none}}
 @media (prefers-reduced-motion: reduce){.step{animation:none}
   html{scroll-behavior:auto}}
 /* the brick opening */
 .brick{margin:52px 0 0;padding-top:26px;border-top:1px solid var(--line)}
 .brick .count{font-size:12px;letter-spacing:.09em;text-transform:uppercase;
   color:var(--violet);font-weight:600}
 .brick h2{font-size:21px;margin:6px 0 10px;line-height:1.3}
 .brick .idea{margin:0 0 16px;color:var(--ink)}
 .need{background:var(--card);border:1px solid var(--line);border-radius:10px;
   padding:12px 16px;margin:16px 0 0}
 .need span{font-size:12px;letter-spacing:.08em;text-transform:uppercase;
   color:var(--muted);font-weight:600}
 .need ul{margin:6px 0 0;padding-left:18px}
 .need li{margin:4px 0;color:var(--ink2);font-size:15.5px}
 /* stage headings */
 .stage{display:flex;align-items:baseline;gap:10px;margin:36px 0 2px}
 .stage b{font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;
   color:var(--blue);font-weight:700}
 .stage i{font-style:normal;font-size:13px;color:var(--muted)}
 .stage:before{content:"";flex:0 0 22px;height:1px;background:var(--blue);
   opacity:.5;align-self:center}
 /* the guess */
 .q{font-weight:600;margin:22px 0 4px}
 .chose{color:var(--muted);font-size:14.5px;margin:14px 0 2px}
 .reply{border-left:3px solid var(--green);padding:2px 0 2px 14px;
   margin:6px 0 0;color:var(--ink2)}
 /* the hands-on experiment */
 .doit{background:var(--card);border:1px solid var(--line);border-radius:10px;
   padding:14px 18px;margin:18px 0 0}
 .doit .lead{font-size:12px;letter-spacing:.08em;text-transform:uppercase;
   color:var(--violet);font-weight:600}
 .doit ol{margin:10px 0 0;padding-left:20px}
 .doit li{margin:6px 0}
 .found{border-left:3px solid var(--violet);padding:2px 0 2px 14px;
   margin:14px 0 0;color:var(--ink2)}
 /* the widget */
 .play{margin:20px 0 0}
 .play .prompt{font-weight:600;margin:0 0 10px}
 .play .notice{color:var(--ink2);font-size:15.5px;margin:14px 0 0}
 canvas.fig{width:100%;height:auto;display:block;border:1px solid var(--line);
   border-radius:10px;background:var(--card)}
 .controls{margin:12px 0 0}
 .row{display:flex;align-items:center;gap:12px;margin:9px 0;flex-wrap:wrap}
 .row .lbl{flex:0 0 168px;font-size:14px;color:var(--ink2)}
 input[type=range]{flex:1;min-width:140px;accent-color:var(--blue)}
 .val{flex:0 0 96px;text-align:right;font-family:ui-monospace,monospace;
   font-size:13px;color:var(--ink2)}
 .pick{display:flex;flex-wrap:wrap;gap:7px}
 .pick button{font:inherit;font-size:13.5px;padding:5px 12px;cursor:pointer;
   border:1px solid var(--line);border-radius:999px;background:transparent;
   color:var(--ink2)}
 .pick button:hover{border-color:var(--blue);color:var(--blue)}
 .pick button.on{background:var(--blue);border-color:var(--blue);color:#fff}
 .readout{margin-top:12px;padding:12px 15px;border:1px solid var(--line);
   border-radius:10px;font-size:14.5px;line-height:1.65;color:var(--ink2);
   background:var(--card)}
 .plain{font-size:14.5px;color:var(--muted);margin:0}
 /* naming and the mathematics */
 .card{border:1px solid var(--line);border-radius:12px;padding:4px 18px 16px;
   margin:22px 0 0;background:var(--card)}
 .card .kicker{display:block;font-size:12px;letter-spacing:.09em;
   text-transform:uppercase;font-weight:600;margin:14px 0 4px}
 .card.name{border-left:4px solid var(--green)}
 .card.name .kicker{color:var(--green)}
 .card.maths{border-left:4px solid var(--violet)}
 .card.maths .kicker{color:var(--violet)}
 .swap{font-size:17px;margin:2px 0 8px}
 .nota{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:15px;
   overflow-x:auto;color:var(--ink);margin:6px 0}
 .fx{font-family:"Latin Modern Math",Cambria,Georgia,serif;font-size:19px;
   text-align:center;overflow-x:auto;padding:10px 0;margin:6px 0;
   border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
 .cite{font-size:14px;color:var(--muted);margin:10px 0 0}
 .hold{margin:26px 0 0;padding:12px 16px;border-radius:10px;
   background:var(--card);border:1px solid var(--line);
   border-left:4px solid var(--blue);font-size:16px}
 .hold b{color:var(--blue);font-size:12px;letter-spacing:.08em;
   text-transform:uppercase;display:block;margin-bottom:3px}
 /* the action area */
 #act{position:sticky;bottom:0;background:var(--surface);padding:14px 0 20px;
   border-top:1px solid var(--line);margin-top:30px}
 /* an empty action bar is sticky and would paint over the page behind it */
 #act:empty{display:none}
 #act .opts{display:flex;flex-direction:column;gap:8px}
 button.go{font:inherit;font-size:16px;padding:11px 20px;cursor:pointer;
   border-radius:10px;border:1px solid var(--blue);background:var(--blue);
   color:#fff;text-align:left}
 button.go:hover{opacity:.9}
 button.opt{font:inherit;font-size:15.5px;padding:11px 16px;cursor:pointer;
   border-radius:10px;border:1px solid var(--line);background:var(--card);
   color:var(--ink);text-align:left;line-height:1.5}
 button.opt:hover{border-color:var(--blue);color:var(--blue)}
 button.quiet{background:transparent;border-color:var(--line);
   color:var(--ink2)}
 .hint{font-size:13px;color:var(--muted);margin:8px 0 0}
 /* the ending */
 .end{margin:40px 0 0;padding-top:24px;border-top:1px solid var(--line)}
 .end ul{padding-left:18px}
 .end li{margin:6px 0;color:var(--ink2)}
 .end a.next{display:inline-block;margin-top:14px;font-size:17px}
 /* the front page */
 .worlds{list-style:none;padding:0;margin:26px 0 0}
 .worlds li{border-top:1px solid var(--line);padding:16px 0}
 .worlds a{display:block;text-decoration:none;color:inherit}
 .worlds a:hover .wt{color:var(--blue)}
 .worlds .wn{font-size:12px;letter-spacing:.09em;text-transform:uppercase;
   color:var(--violet);font-weight:600}
 .worlds .wt{font-size:19px;margin:2px 0 4px}
 .worlds .wp{color:var(--ink2);font-size:15.5px;margin:0}
 .worlds .wd{color:var(--muted);font-size:13px;margin:6px 0 0}
 footer{max-width:680px;margin:60px auto 0;padding:18px 20px 40px;
   border-top:1px solid var(--line);color:var(--muted);font-size:14px}
 footer a{color:var(--muted)}
 @media (max-width:600px){
   body{font-size:16.5px}
   .row .lbl{flex:0 0 100%}
   .val{flex:0 0 auto}
 }
"""


# --- the reading engine ----------------------------------------------------

ENGINE = r"""
// The whole interface: a list of steps, one button, and a column that grows.
// Nothing here knows any mathematics; the widgets do that.

const STORY = document.getElementById('story');
const ACT = document.getElementById('act');
const BAR = document.getElementById('bar');

// flatten the world into a list of steps, one press each
const STEPS = [];
WORLD.bricks.forEach(function(brick, bi){
  STEPS.push({t:'brick', brick:brick, n:bi + 1, of:WORLD.bricks.length});
  brick.stages.forEach(function(stage){
    STEPS.push({t:'stage', stage:stage});
    stage.beats.forEach(function(beat){ STEPS.push({t:'beat', beat:beat}); });
  });
  STEPS.push({t:'hold', text:brick.hold});
});

const KEY = 'cm-game-' + WORLD.slug;
let idx = 0, choices = {}, replaying = false;

function el(tag, cls, parent, html){
  const e = document.createElement(tag);
  if(cls) e.className = cls;
  if(html !== undefined && html !== null) e.innerHTML = html;
  if(parent) parent.appendChild(e);
  return e;
}
function box(){ return el('div', 'step', STORY); }
function save(){
  try{ localStorage.setItem(KEY, JSON.stringify({idx:idx, choices:choices})); }
  catch(e){}
}
function progress(){
  const pct = Math.round(100 * idx / STEPS.length);
  if(BAR) BAR.style.width = pct + '%';
}
function scroll(node){
  if(replaying || !node || typeof node.scrollIntoView !== 'function') return;
  try{ node.scrollIntoView({behavior:'smooth', block:'center'}); }catch(e){}
}

// --- rendering one step ----------------------------------------------------

function renderBrick(s){
  const b = s.brick, host = box();
  host.className = 'step brick';
  el('div', 'count', host, 'Brick ' + s.n + ' of ' + s.of);
  el('h2', null, host, b.title);
  el('p', 'idea', host, b.idea);
  const need = el('div', 'need', host);
  el('span', null, need, 'What you need first');
  const ul = el('ul', null, need);
  b.need.forEach(function(n){ el('li', null, ul, n); });
  return host;
}

function renderStage(s){
  const host = box();
  host.className = 'step stage';
  el('b', null, host, s.stage.label);
  el('i', null, host, s.stage.blurb);
  return host;
}

function renderBeat(beat){
  const host = box();
  if(beat.kind === 'say'){
    el('p', null, host, beat.text);
  } else if(beat.kind === 'ask'){
    el('p', 'q', host, beat.question);
  } else if(beat.kind === 'try'){
    const d = el('div', 'doit', host);
    el('div', 'lead', d, beat.prompt);
    const ol = el('ol', null, d);
    beat.steps.forEach(function(t){ el('li', null, ol, t); });
  } else if(beat.kind === 'play'){
    const d = el('div', 'play', host);
    el('p', 'prompt', d, beat.prompt);
    const stage = el('div', null, d);
    try{
      WIDGETS[beat.widget](stage, beat.params || {});
    }catch(err){
      el('p', 'plain', stage, 'The simulation could not start.');
      if(typeof console !== 'undefined') console.error(err);
    }
    el('p', 'notice', d, beat.notice);
  } else if(beat.kind === 'name'){
    const c = el('div', 'card name', host);
    el('span', 'kicker', c, 'Standard name');
    el('p', 'swap', c, 'The idea described here as <b>' + beat.plain +
       '</b> is usually called <b>' + beat.standard + '</b>.');
    el('p', 'nota', c, beat.notation);
    if(beat.why) el('p', null, c, beat.why);
  } else if(beat.kind === 'math'){
    const c = el('div', 'card maths', host);
    el('span', 'kicker', c, 'In notation');
    el('div', 'fx', c, beat.statement);
    el('p', null, c, beat.reading);
    if(beat.cite){
      const p = el('p', 'cite', c);
      if(beat.url) el('a', null, p, beat.cite).setAttribute('href', beat.url);
      else p.innerHTML = beat.cite;
    }
  }
  return host;
}

function renderHold(s){
  const host = box();
  host.className = 'step hold';
  el('b', null, host, 'Key idea');
  el('span', null, host, s.text);
  return host;
}

// --- the action area -------------------------------------------------------

function clearAct(){ ACT.innerHTML = ''; }

function showContinue(label){
  clearAct();
  if(replaying) return;
  const b = el('button', 'go', ACT, label || 'Continue');
  b.addEventListener('click', advance);
  el('p', 'hint', ACT, 'Press Enter or Space to continue.');
}

function showOptions(beat, at){
  clearAct();
  if(replaying) return;
  const wrap = el('div', 'opts', ACT);
  beat.options.forEach(function(opt, i){
    const b = el('button', 'opt', wrap, opt[0]);
    b.addEventListener('click', function(){ answer(beat, i, at); });
  });
  el('p', 'hint', ACT, 'Choose an answer before continuing. Every choice gets '
     + 'an explanation.');
}

function answer(beat, i, at){
  choices[at] = i;
  const host = box();
  el('p', 'chose', host, 'You said: ' + beat.options[i][0]);
  el('p', 'reply', host, beat.options[i][1]);
  if(beat.after) el('p', null, host, beat.after);
  scroll(host);
  save();
  showContinue();
}

function showReveal(beat){
  clearAct();
  if(replaying) return;
  const b = el('button', 'go', ACT, 'I tried it — show me the result');
  b.addEventListener('click', function(){ reveal(beat); });
  el('p', 'hint', ACT, 'Try the steps first; the result will make more sense.');
}

function reveal(beat){
  const host = box();
  el('p', 'found', host, beat.found);
  scroll(host);
  showContinue();
}

// --- walking the list ------------------------------------------------------

function advance(){
  if(idx >= STEPS.length){ finish(); return; }
  const s = STEPS[idx], at = idx;
  idx += 1;
  let node = null, waiting = null;
  if(s.t === 'brick') node = renderBrick(s);
  else if(s.t === 'stage') node = renderStage(s);
  else if(s.t === 'hold') node = renderHold(s);
  else {
    node = renderBeat(s.beat);
    if(s.beat.kind === 'ask') waiting = 'ask';
    if(s.beat.kind === 'try') waiting = 'try';
  }
  progress();
  save();
  scroll(node);
  if(waiting === 'ask'){
    if(replaying){
      const pick = choices[at] === undefined ? 0 : choices[at];
      const beat = s.beat, h = box();
      el('p', 'chose', h, 'You said: ' + beat.options[pick][0]);
      el('p', 'reply', h, beat.options[pick][1]);
      if(beat.after) el('p', null, h, beat.after);
    } else showOptions(s.beat, at);
  } else if(waiting === 'try'){
    if(replaying) el('p', 'found', box(), s.beat.found);
    else showReveal(s.beat);
  } else if(idx >= STEPS.length){ finish(); }
  else showContinue();
}

function finish(){
  clearAct();
  const host = box();
  host.className = 'step end';
  el('p', null, host, 'You have completed world ' + WORLD.number + '. Here are '
     + 'the main ideas to take with you:');
  const ul = el('ul', null, host);
  WORLD.bricks.forEach(function(b){ el('li', null, ul, b.hold); });
  if(NEXT) el('a', 'next', host, 'Continue to world ' + NEXT.number + ': '
              + NEXT.title + ' →').setAttribute('href', NEXT.page);
  else el('p', null, host, 'You have reached the final world. The companion '
          + 'guide develops the same material in three parts.');
  const again = el('button', 'go quiet', ACT, 'Restart this world');
  again.addEventListener('click', function(){
    idx = 0; choices = {}; STORY.innerHTML = ''; save(); progress(); advance();
  });
  idx = STEPS.length;
  progress();
  save();
  scroll(host);
}

// --- start, or offer to resume ---------------------------------------------

function replay(to){
  replaying = true;
  idx = 0;
  STORY.innerHTML = '';
  while(idx < to && idx < STEPS.length) advance();
  replaying = false;
  if(idx >= STEPS.length) finish();
  else showContinue();
}

function begin(){
  let saved = null;
  try{ saved = JSON.parse(localStorage.getItem(KEY) || 'null'); }catch(e){}
  if(saved && saved.idx > 0 && saved.idx < STEPS.length){
    choices = saved.choices || {};
    clearAct();
    const on = el('button', 'go', ACT, 'Continue where you left off');
    on.addEventListener('click', function(){ replay(saved.idx); });
    const fresh = el('button', 'go quiet', ACT, 'Restart this world');
    fresh.addEventListener('click', function(){
      choices = {}; idx = 0; save(); advance();
    });
  } else {
    showContinue('Begin');
  }
}

if(typeof window !== 'undefined' && window.addEventListener){
  window.addEventListener('keydown', function(e){
    if(e.key !== 'Enter' && e.key !== ' ') return;
    const buttons = ACT.querySelectorAll ? ACT.querySelectorAll('button') : [];
    if(buttons.length === 1){ e.preventDefault(); buttons[0].click(); }
  });
}

begin();
"""


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TITLE</title>
<meta name="description" content="DESCRIPTION">
<style>CSS</style>
</head>
<body>
<header class="top">
  <div class="inner">NAVBAR</div>
  <div class="bar"><i id="bar"></i></div>
</header>
<main>
HEAD
<div id="story"></div>
<div id="act"></div>
</main>
<footer>FOOTER</footer>
SCRIPTS
</body>
</html>
"""


def page(title, description, navbar, head, footer, scripts,
         interactive=True) -> str:
    shell = SHELL if interactive else SHELL.replace(
        '<div id="story"></div>\n<div id="act"></div>', "")
    return (shell
            .replace("TITLE", title)
            .replace("DESCRIPTION", description)
            .replace("CSS", CSS)
            .replace("NAVBAR", navbar)
            .replace("HEAD", head)
            .replace("FOOTER", footer)
            .replace("SCRIPTS", scripts))


FOOTER = (
    'An interactive introduction to <a href="../index.html">condensed mathematics</a>, based on '
    f'Peter Scholze\'s <a href="{LECTURES}">Lectures on Condensed '
    'Mathematics</a>, developed with Dustin Clausen. Every value shown by a '
    'widget is calculated directly in the page. '
    '<a href="https://github.com/muchmirul/conjectures">Source</a>.'
)


def build_world(world, nxt) -> str:
    data = json.dumps(world_dict(world), ensure_ascii=False)
    nxt_json = ("null" if nxt is None else
                json.dumps({"number": nxt.number, "title": nxt.title,
                            "page": nxt.page}, ensure_ascii=False))
    navbar = ('<a href="index.html">← the game</a>'
              f'<span>World {world.number} of {len(WORLDS)}</span>')
    head = (f'<h1>World {world.number} · {world.title}</h1>'
            f'<p class="promise">{world.promise}</p>')
    scripts = ("<script>\n" + MATHS + WIDGET_JS
               + f"\nconst WORLD = {data};\nconst NEXT = {nxt_json};\n"
               + ENGINE + "\n</script>")
    return page(
        title=f"World {world.number}: {world.title} · condensed mathematics",
        description=world.promise.replace('"', "'"),
        navbar=navbar, head=head, footer=FOOTER, scripts=scripts)


HOW_IT_WORKS = """
<p>This course builds enough intuition to begin reading research on condensed
mathematics. It assumes no mathematical background: World 1 starts with three
ordinary objects on a table.</p>

<p>Each idea is presented as a <strong>brick</strong> with three stages:</p>

<ul>
<li><b>Concept</b> — a direct explanation of the idea.</li>
<li><b>Intuition</b> — a familiar way to picture it, followed by a question
you answer before seeing the explanation.</li>
<li><b>Experiment</b> — an interactive simulation or a short hands-on task,
followed by the standard terminology and a plain-language reading of the
notation.</li>
</ul>

<p>There are no scores or wrong turns. Your progress is saved in this browser,
so you can pause at any point and continue later.</p>
"""


def build_index() -> str:
    rows = []
    for w in WORLDS:
        bricks = len(w.bricks)
        plays = sum(1 for b in w.bricks for beat in b.beats
                    if getattr(beat, "kind", "") == "play")
        rows.append(
            f'<li><a href="{w.page}">'
            f'<span class="wn">World {w.number}</span>'
            f'<div class="wt">{w.title}</div>'
            f'<p class="wp">{w.promise}</p>'
            f'<p class="wd">{bricks} bricks · {plays} '
            f'{"simulation" if plays == 1 else "simulations"}</p>'
            f'</a></li>')
    head = ('<h1>Discover condensed mathematics</h1>'
            '<p class="promise">Eight interactive worlds take you from three '
            'objects on a table to the duality theorem developed in the '
            'lectures. You form an intuition, make a prediction, and test each '
            'idea yourself.</p>'
            + HOW_IT_WORKS
            + f'<ul class="worlds">{"".join(rows)}</ul>')
    return page(
        title="Discover condensed mathematics · an interactive course",
        description="An eight-world interactive introduction to condensed "
                    "mathematics, built around concepts, intuition, and "
                    "experiments.",
        navbar='<a href="../index.html">← condensed mathematics</a>'
               f'<span>{len(WORLDS)} worlds</span>',
        head=head, footer=FOOTER, scripts="", interactive=False)


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for i, world in enumerate(WORLDS):
        nxt = WORLDS[i + 1] if i + 1 < len(WORLDS) else None
        (OUT / world.page).write_text(build_world(world, nxt))
    (OUT / "index.html").write_text(build_index())
    bricks = sum(len(w.bricks) for w in WORLDS)
    beats = sum(len(b.beats) for w in WORLDS for b in w.bricks)
    print(f"wrote {len(WORLDS)} worlds, {bricks} bricks, {beats} beats "
          f"under {OUT}")


if __name__ == "__main__":
    build()

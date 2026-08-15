"""The twelve things the reader can move, as one block of JavaScript.

Each widget is a function of a host element and a small parameter object.  It
builds its own controls, draws into its own canvas and writes its own readout,
so a beat in a world only has to name it.

The mathematics is not reimplemented here.  `build_interactive.MATHS` already
carries probes, measures, the p-adic size, the merge ratio and Smith normal
form in JavaScript, and `tests/test_interactive.py` already checks that block
against the Python library point by point.  The game pages include the same
block, so a widget and a chapter simulation cannot disagree about a number.

What this file adds is only presentation, plus three small computations the
play pages had no use for: counting fractions inside a shrinking window, the
largest wobble of the base-two value function inside a box, and the finite
window used to display a kernel and a cokernel.  `tests/test_game.py` checks
those three against exact arithmetic in Python.
"""

from __future__ import annotations

# --- shared helpers --------------------------------------------------------

HELPERS = r"""
// theme-aware colours; falls back to the light palette when the page is being
// run outside a browser (the test stub has no getComputedStyle)
function css(name, fallback){
  try{
    if(typeof getComputedStyle !== 'function') return fallback;
    const v = getComputedStyle(document.documentElement).getPropertyValue(name);
    return (v && v.trim()) ? v.trim() : fallback;
  }catch(e){ return fallback; }
}
function palette(){
  return {ink:css('--ink','#0b0b0b'), ink2:css('--ink2','#52514e'),
          muted:css('--muted','#898781'), line:css('--line','#e1e0d9'),
          blue:css('--blue','#2a78d6'), green:css('--green','#008300'),
          red:css('--red','#d03b3b'), violet:css('--violet','#4a3aa7')};
}

const UI = {
  node(tag, cls, parent, html){
    const e = document.createElement(tag);
    if(cls) e.className = cls;
    if(html !== undefined && html !== null) e.innerHTML = html;
    if(parent) parent.appendChild(e);
    return e;
  },
  canvas(host, w, h){
    const c = document.createElement('canvas');
    c.className = 'fig'; c.width = w; c.height = h;
    host.appendChild(c);
    return c;
  },
  out(host){ return UI.node('div', 'readout', host, ''); },
  slider(host, label, lo, hi, step, val, fn){
    const row = UI.node('div', 'row', host);
    UI.node('span', 'lbl', row, label);
    const inp = document.createElement('input');
    inp.type = 'range'; inp.min = lo; inp.max = hi;
    inp.step = step; inp.value = String(val);
    row.appendChild(inp);
    const read = UI.node('span', 'val', row, '');
    const fire = () => fn(parseFloat(inp.value), read);
    inp.addEventListener('input', fire);
    fire();
    return inp;
  },
  pick(host, label, opts, fn){
    const row = UI.node('div', 'row', host);
    if(label) UI.node('span', 'lbl', row, label);
    const box = UI.node('div', 'pick', row);
    let cur = opts[0][0];
    for(let i = 0; i < opts.length; i++){
      const b = UI.node('button', i === 0 ? 'on' : '', box, opts[i][1]);
      b.dataset.v = String(opts[i][0]);
      b.addEventListener('click', function(){
        const kids = box.children;
        for(let k = 0; k < kids.length; k++) kids[k].className = '';
        b.className = 'on';
        cur = opts[i][0];
        fn(cur);
      });
    }
    fn(cur);
    return {get value(){ return cur; }};
  }
};

function clearCanvas(cv){
  const ctx = cv.getContext('2d');
  ctx.clearRect(0, 0, cv.width, cv.height);
  return ctx;
}
function caption(ctx, x, y, text, colour){
  ctx.fillStyle = colour; ctx.font = '12px system-ui';
  ctx.textAlign = 'left'; ctx.fillText(text, x, y);
}
function fmtPow(base, e){
  return base + '<sup>' + (e < 0 ? '&minus;' + (-e) : e) + '</sup>';
}

// how many fractions with denominator at most Q sit strictly inside
// (centre - half, centre + half).  An honest count, not an estimate.
function fractionsInWindow(centre, half, Q){
  const seen = {};
  let total = 0;
  for(let q = 1; q <= Q; q++){
    const lo = Math.ceil((centre - half) * q), hi = Math.floor((centre + half) * q);
    for(let k = lo; k <= hi; k++){
      const key = (k / q).toFixed(9);
      if(!seen[key]){ seen[key] = 1; total += 1; }
    }
  }
  return total;
}

// the base-two value function on the halving probe, x -> sum x_i 2^-i-1.
// Its largest wobble inside one stage-n box is 2^-n: never zero, so the
// function is constant on no box at any stage, so it is not locally constant.
function valueOf(word){
  let v = 0;
  for(let i = 0; i < word.length; i++) v += (word[i] === '1' ? 1 : 0) * Math.pow(2, -i - 1);
  return v;
}
function wobbleInBox(n){ return Math.pow(2, -n); }
"""


# --- the widgets themselves ------------------------------------------------

WIDGETS = r"""
const WIDGETS = {};

// 1. nearness: how crowded is a shrinking window
WIDGETS.zoom = function(host, P){
  const discrete = !!P.discrete, centre = P.target === undefined ? 1 : P.target;
  const cv = UI.canvas(host, 720, 200), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  let w = 2, Q = 12;
  const draw = function(){
    const c = palette(), ctx = clearCanvas(cv);
    const half = Math.pow(2, -w), y = 96;
    const X = x => 60 + (x - (centre - 0.6)) / 1.2 * 600;
    ctx.strokeStyle = c.line; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(60, y + 34); ctx.lineTo(660, y + 34); ctx.stroke();
    // the window
    ctx.fillStyle = c.blue; ctx.globalAlpha = 0.12;
    ctx.fillRect(X(centre - half), 40, Math.max(2, X(centre + half) - X(centre - half)), 90);
    ctx.globalAlpha = 1;
    if(discrete){
      for(let k = -12; k <= 12; k++){
        const x = centre + k * 0.05;
        ctx.fillStyle = (k === 0) ? c.violet : c.muted;
        ctx.beginPath(); ctx.arc(X(x), y, k === 0 ? 6 : 4, 0, 7); ctx.fill();
      }
      caption(ctx, 60, 172, 'the dust: every number stands alone', c.muted);
    } else {
      ctx.strokeStyle = c.ink; ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.moveTo(60, y); ctx.lineTo(660, y); ctx.stroke();
      for(let q = 1; q <= Q; q++)
        for(let k = Math.ceil((centre - 0.6) * q); k <= Math.floor((centre + 0.6) * q); k++){
          const x = k / q;
          ctx.fillStyle = Math.abs(x - centre) < half ? c.blue : c.muted;
          ctx.beginPath(); ctx.arc(X(x), y, 2.6, 0, 7); ctx.fill();
        }
      caption(ctx, 60, 172, 'the ruler: fractions with denominator up to ' + Q, c.muted);
    }
    ctx.fillStyle = c.violet;
    ctx.beginPath(); ctx.arc(X(centre), y, 5.5, 0, 7); ctx.fill();
    const inside = fractionsInWindow(centre, half, Q);
    if(discrete){
      out.innerHTML = 'The piece containing only ' + centre + ' is open on the dust, ' +
        'so no window is needed: it contains exactly <b>1</b> number.<br>' +
        'Shrinking changes nothing, because there was never anything else nearby.';
    } else {
      out.innerHTML = 'Window of width ' + fmtPow(2, -w + 1) + ' around ' + centre +
        ', looking only at denominators up to ' + Q + ':<br>' +
        '<b>' + inside + '</b> numbers inside. Raise the denominator and the count keeps ' +
        'climbing, at every width. On the ruler no window is ever empty.';
    }
  };
  UI.slider(ctrl, 'window width', 0, 8, 1, w, function(v, read){
    w = Math.round(v); read.innerHTML = fmtPow(2, -w + 1); draw();
  });
  UI.slider(ctrl, 'look this finely', 2, 60, 1, Q, function(v, read){
    Q = Math.round(v); read.textContent = 'q \u2264 ' + Q; draw();
  });
  draw();
};

// 1b. four rules, and the two independent questions asked of each
WIDGETS.undo = function(host, P){
  const cv = UI.canvas(host, 720, 230), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  const RULES = {
    id:      {label: 'send it to itself', f: k => k},
    double:  {label: 'double it',         f: k => 2 * k},
    floor2:  {label: 'round down to even', f: k => 2 * Math.floor(k / 2)},
    shift:   {label: 'add seven',         f: k => k + 7}
  };
  let which = 'id';
  const draw = function(){
    const c = palette(), ctx = clearCanvas(cv);
    const lo = -6, hi = 6, f = RULES[which].f;
    const X = k => 70 + (k - lo) / (hi - lo) * 580;
    const yTop = 74, yBot = 172;
    const image = {};
    let collides = false;
    for(let k = lo; k <= hi; k++){
      const v = f(k);
      if(image[v] !== undefined) collides = true;
      image[v] = k;
    }
    for(let k = lo; k <= hi; k++){
      const v = f(k);
      ctx.strokeStyle = c.line; ctx.lineWidth = 1;
      if(v >= lo && v <= hi){
        ctx.beginPath(); ctx.moveTo(X(k), yTop + 6); ctx.lineTo(X(v), yBot - 6);
        ctx.stroke();
      }
      ctx.fillStyle = c.blue;
      ctx.beginPath(); ctx.arc(X(k), yTop, 4, 0, 7); ctx.fill();
      ctx.fillStyle = image[k] === undefined ? c.line : c.blue;
      ctx.beginPath(); ctx.arc(X(k), yBot, 4, 0, 7); ctx.fill();
    }
    caption(ctx, 70, 40, 'every number, sent somewhere', c.muted);
    caption(ctx, 70, 210, 'pale = nothing lands here', c.muted);
    // does it survive addition, checked on every pair in the window
    let polite = true;
    for(let a = lo; a <= hi && polite; a++)
      for(let b = lo; a + b <= hi && b <= hi; b++)
        if(f(a + b) !== f(a) + f(b)) polite = false;
    const undoable = !collides;
    out.innerHTML = 'Rule: <b>' + RULES[which].label + '</b><br>' +
      'Can it be undone? <b>' + (undoable ? 'yes' : 'no') + '</b> &mdash; ' +
      (undoable ? 'no two numbers collide, so the way back always names one number'
                : 'two different numbers land on the same place, so the way back ' +
                  'cannot answer once') + '.<br>' +
      'Does it survive addition? <b>' + (polite ? 'yes' : 'no') + '</b> &mdash; ' +
      (polite ? 'adding first and crossing over agree, and 0 goes to ' + f(0)
              : 'adding first and crossing over disagree, and 0 goes to ' + f(0)) +
      '.<br>The two questions are independent: a rule can pass either one ' +
      'without the other.';
  };
  UI.pick(ctrl, 'the rule', [['id', 'send it to itself'], ['double', 'double it'],
          ['floor2', 'round down to even'], ['shift', 'add seven']],
          function(v){ which = v; draw(); });
  draw();
};

// 2. the one-way bridge
WIDGETS.bridge = function(host, P){
  const cv = UI.canvas(host, 720, 260), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  let n = 5, dir = 'across';
  const draw = function(){
    const c = palette(), ctx = clearCanvas(cv);
    const X = x => 70 + (x - 0.4) / 0.7 * 580;
    const yTop = 66, yBot = 196;
    ctx.strokeStyle = c.line; ctx.lineWidth = 1;
    for(let k = 0; k < 40; k++){
      const x = 0.42 + k * 0.017;
      ctx.beginPath(); ctx.arc(X(x), yTop, 2, 0, 7); ctx.fillStyle = c.line; ctx.fill();
    }
    ctx.strokeStyle = c.ink; ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(70, yBot); ctx.lineTo(660, yBot); ctx.stroke();
    caption(ctx, 70, 32, 'the dust', c.muted);
    caption(ctx, 70, 240, 'the ruler', c.muted);
    for(let k = 1; k <= n; k++){
      const x = 1 - Math.pow(2, -k);
      ctx.fillStyle = c.blue;
      ctx.beginPath(); ctx.arc(X(x), yTop, 4, 0, 7); ctx.fill();
      ctx.beginPath(); ctx.arc(X(x), yBot, 4, 0, 7); ctx.fill();
      ctx.strokeStyle = c.blue; ctx.globalAlpha = 0.5; ctx.lineWidth = 1;
      ctx.beginPath();
      if(dir === 'across'){ ctx.moveTo(X(x), yTop + 6); ctx.lineTo(X(x), yBot - 6); }
      else { ctx.moveTo(X(x), yBot - 6); ctx.lineTo(X(x), yTop + 6); }
      ctx.stroke(); ctx.globalAlpha = 1;
    }
    ctx.fillStyle = dir === 'across' ? c.green : c.red;
    ctx.beginPath(); ctx.arc(X(1), yTop, 6, 0, 7); ctx.fill();
    ctx.beginPath(); ctx.arc(X(1), yBot, 6, 0, 7); ctx.fill();
    const gap = Math.pow(2, -n);
    if(dir === 'across'){
      out.innerHTML = 'The crowd 1 &minus; ' + fmtPow(2, -1) + ', 1 &minus; ' + fmtPow(2, -2) +
        ', &hellip; arrives at the marked point.<br>' +
        'On the ruler the gap after ' + n + ' steps is <b>' + gap.toPrecision(3) +
        '</b>, and it is still shrinking. The walk is gentle: nothing was torn.';
    } else {
      out.innerHTML = 'The same crowd, read on the dust. Every gap is <b>1</b>, ' +
        'however far along you go, because on the dust two different numbers are ' +
        'never near.<br>The destination is torn off the crowd: this direction is ' +
        'not gentle.';
    }
  };
  UI.pick(ctrl, 'direction', [['across', 'dust → ruler'], ['back', 'ruler → dust']],
          function(v){ dir = v; draw(); });
  UI.slider(ctrl, 'how far along', 2, 12, 1, n, function(v, read){
    n = Math.round(v); read.textContent = n + ' steps'; draw();
  });
  draw();
};

// 3. kernel and cokernel, on a finite window of the whole numbers
WIDGETS.algebra = function(host, P){
  const bridge = !!P.bridge;
  const cv = UI.canvas(host, 720, 250), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  const maps = bridge
    ? [['bridge', 'the bridge: dust → ruler']]
    : [['id', 'do nothing'], ['double', 'double it'], ['clock', 'clock, 12 hours']];
  let which = maps[0][0];
  const draw = function(){
    const c = palette(), ctx = clearCanvas(cv);
    const lo = -12, hi = 12;
    const X = k => 70 + (k - lo) / (hi - lo) * 580;
    const yTop = 78, yBot = 186;
    let crushed = [], missed = [], verdict = '', kerText = '', cokText = '';
    for(let k = lo; k <= hi; k++){
      let img = k;
      if(which === 'double') img = 2 * k;
      if(which === 'clock') img = ((k % 12) + 12) % 12;
      if(which === 'double' && img === 0 && k !== 0) crushed.push(k);
      if(which === 'clock' && img === 0 && k !== 0) crushed.push(k);
      ctx.strokeStyle = c.line; ctx.lineWidth = 1;
      if(img >= lo && img <= hi){
        ctx.beginPath(); ctx.moveTo(X(k), yTop + 6); ctx.lineTo(X(img), yBot - 6); ctx.stroke();
      }
    }
    const hit = {};
    for(let k = lo; k <= hi; k++){
      let img = k;
      if(which === 'double') img = 2 * k;
      if(which === 'clock') img = ((k % 12) + 12) % 12;
      hit[img] = 1;
    }
    for(let k = lo; k <= hi; k++) if(!hit[k]) missed.push(k);
    for(let k = lo; k <= hi; k++){
      ctx.fillStyle = crushed.indexOf(k) >= 0 ? c.red : c.blue;
      ctx.beginPath(); ctx.arc(X(k), yTop, 4, 0, 7); ctx.fill();
      if(missed.indexOf(k) >= 0){
        ctx.strokeStyle = c.red; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.arc(X(k), yBot, 4.5, 0, 7); ctx.stroke();
      } else {
        ctx.fillStyle = c.blue;
        ctx.beginPath(); ctx.arc(X(k), yBot, 4, 0, 7); ctx.fill();
      }
    }
    caption(ctx, 70, 40, bridge ? 'the dust' : 'source', c.muted);
    caption(ctx, 70, 228, bridge ? 'the ruler' : 'target', c.muted);
    caption(ctx, 470, 228, 'hollow = never reached', c.red);
    if(which === 'id'){
      kerText = 'ker = 0, nothing is crushed';
      cokText = 'coker = 0, nothing is missed';
      verdict = 'the two measurements agree: a sameness, and it really is one';
    } else if(which === 'double'){
      kerText = 'ker = 0, nothing is crushed';
      cokText = 'coker = &#8484;/2, the odd numbers are never reached (' +
                missed.length + ' of them in this window)';
      verdict = 'not a sameness, and the cokernel says so';
    } else if(which === 'clock'){
      kerText = 'ker = 12&#8484;, every multiple of twelve is crushed to zero';
      cokText = 'coker = 0, every hour is reached';
      verdict = 'not a sameness, and the kernel says so';
    } else {
      kerText = 'ker = 0, different numbers stay different';
      cokText = 'coker = 0, every number on the ruler is reached';
      verdict = 'the two measurements say <b>sameness</b> &mdash; and that verdict ' +
                'is false, because the way back tears';
    }
    out.innerHTML = kerText + '<br>' + cokText + '<br><b>Verdict:</b> ' + verdict;
  };
  if(maps.length > 1) UI.pick(ctrl, 'the map', maps, function(v){ which = v; draw(); });
  else UI.node('p', 'plain', ctrl, 'The only map here is the bridge itself.');
  draw();
};

// 4. splitting a box forever
WIDGETS.split = function(host, P){
  const cv = UI.canvas(host, 720, 300), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  let kind = 'halving', depth = P.depth === undefined ? 3 : P.depth;
  const build = function(d){
    if(kind === 'halving') return cantorProbe(d);
    if(kind === 'three') return branchProbe(d, 3);
    return sequenceProbe(d);
  };
  const draw = function(){
    const c = palette(), ctx = clearCanvas(cv);
    const S = build(depth), sizes = probeSizes(S);
    drawTree(ctx, S, depth, {x: 40, y: 26, w: 640, h: 240},
             {edge: c.line, colour: (i, l) => i === depth ? c.blue : c.violet, r: 3.6});
    caption(ctx, 40, 292, 'each dot is a box; each line says which box it came out of', c.muted);
    out.innerHTML = 'Boxes at each stage: <b>' + sizes.join(', ') + '</b>.<br>' +
      'Stage ' + depth + ' has <b>' + sizes[depth] + '</b> boxes, and every one of them ' +
      'is on the screen. Nothing here is infinite except the number of stages.';
  };
  if(P.kind === 'pick')
    UI.pick(ctrl, 'the walker', [['halving', 'split in two'], ['three', 'split in three'],
            ['approaching', 'closing in on a point']],
            function(v){ kind = v; if(kind === 'three' && depth > 4) depth = 4; draw(); });
  UI.slider(ctrl, 'stages', 0, 6, 1, depth, function(v, read){
    const k = Math.round(v);
    depth = (kind === 'three' && k > 4) ? 4 : k;
    read.textContent = 'stage ' + depth; draw();
  });
  draw();
};

// 5. counting the gentle walks out of a probe
WIDGETS.landings = function(host, P){
  const cv = UI.canvas(host, 720, 220), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  let kind = 'halving', level = 2;
  const build = function(d){
    if(kind === 'halving') return cantorProbe(d);
    if(kind === 'three') return branchProbe(d, 3);
    return sequenceProbe(d);
  };
  const draw = function(){
    const c = palette(), ctx = clearCanvas(cv);
    const S = build(level), boxes = S.levels[level], n = boxes.length;
    const w = 620 / n;
    for(let k = 0; k < n; k++){
      const on = (k * 7 + level) % 3 === 0;
      ctx.fillStyle = on ? c.blue : c.line;
      ctx.fillRect(50 + k * w + 1, 70, Math.max(1, w - 2), 62);
    }
    ctx.strokeStyle = c.muted; ctx.lineWidth = 1;
    ctx.strokeRect(50, 70, 620, 62);
    caption(ctx, 50, 54, 'one box, one choice of value: that is a gentle walk', c.muted);
    caption(ctx, 50, 158, n + ' boxes at stage ' + level, c.ink2);
    const exact = n <= 30 ? Math.pow(2, n).toLocaleString() : null;
    out.innerHTML = 'Stage ' + level + ' has <b>' + n + '</b> boxes, so the gentle walks ' +
      'into a two-point target number ' + fmtPow(2, n) +
      (exact ? ' = <b>' + exact + '</b>' : '') + '.<br>' +
      'Every one of them is something the target says to this probe. The description ' +
      'is large because it is complete.';
  };
  UI.pick(ctrl, 'the probe', [['halving', 'split in two'], ['three', 'split in three'],
          ['approaching', 'closing in on a point']], function(v){ kind = v; draw(); });
  UI.slider(ctrl, 'stage', 0, 5, 1, level, function(v, read){
    level = Math.round(v); read.textContent = 'stage ' + level; draw();
  });
  draw();
};

// 6. cut and glue
WIDGETS.glue = function(host, P){
  const cv = UI.canvas(host, 720, 220), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  let meet = 'apart', left = 1, right = 1;
  const draw = function(){
    const c = palette(), ctx = clearCanvas(cv);
    const overlap = meet === 'overlap';
    const lx = 60, lw = overlap ? 340 : 290;
    const rx = overlap ? 320 : 390, rw = overlap ? 340 : 290;
    ctx.globalAlpha = 0.5;
    ctx.fillStyle = c.blue; ctx.fillRect(lx, 60, lw, 60);
    ctx.fillStyle = c.violet; ctx.fillRect(rx, 100, rw, 60);
    ctx.globalAlpha = 1;
    caption(ctx, lx + 8, 96, 'left piece says ' + left, '#ffffff');
    caption(ctx, rx + 8, 136, 'right piece says ' + right, '#ffffff');
    let ok, why;
    if(!overlap){
      ok = true;
      why = 'The two pieces share nothing, so there is nothing to disagree about. ' +
            'Exactly one answer glues, whatever you chose.';
    } else if(left === right){
      ok = true;
      why = 'The pieces meet, and on the shared part both say ' + left +
            '. Exactly one answer glues.';
    } else {
      ok = false;
      why = 'The pieces meet, and on the shared part one says ' + left + ' and the other ' +
            right + '. Nothing glues at all: there is no answer on the whole probe ' +
            'restricting to both.';
    }
    ctx.strokeStyle = ok ? c.green : c.red; ctx.lineWidth = 2;
    ctx.strokeRect(50, 176, 620, 30);
    caption(ctx, 60, 196, ok ? 'glues, and in exactly one way' : 'does not glue',
            ok ? c.green : c.red);
    out.innerHTML = why;
  };
  UI.pick(ctrl, 'how the pieces meet',
          [['apart', 'cut cleanly apart'], ['overlap', 'sharing a middle']],
          function(v){ meet = v; draw(); });
  UI.slider(ctrl, 'left piece says', 0, 3, 1, left, function(v, read){
    left = Math.round(v); read.textContent = String(left); draw();
  });
  UI.slider(ctrl, 'right piece says', 0, 3, 1, right, function(v, read){
    right = Math.round(v); read.textContent = String(right); draw();
  });
  draw();
};

// 7. the ghost: a continuous function that is constant on no box
WIDGETS.ghost = function(host, P){
  const cv = UI.canvas(host, 720, 250), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  let probe = 'halving', n = 3;
  const draw = function(){
    const c = palette(), ctx = clearCanvas(cv);
    if(probe === 'point'){
      ctx.fillStyle = c.violet;
      ctx.beginPath(); ctx.arc(360, 120, 9, 0, 7); ctx.fill();
      caption(ctx, 300, 156, 'the one-point probe', c.muted);
      out.innerHTML = 'On one point there is nothing to wobble: every function is ' +
        'constant, so every continuous function is locally constant.<br>' +
        'The leftover here is <b>0</b>. This is the row that asks which points the ' +
        'object has, and it reads empty.';
      return;
    }
    const S = cantorProbe(n), boxes = S.levels[n], m = boxes.length, w = 620 / m;
    for(let k = 0; k < m; k++){
      const lo = valueOf(boxes[k]), hi = lo + wobbleInBox(n);
      ctx.fillStyle = c.blue;
      ctx.fillRect(50 + k * w + 0.5, 190 - lo * 150, Math.max(1, w - 1),
                   Math.max(1.5, hi * 150 - lo * 150));
    }
    ctx.strokeStyle = c.line; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(50, 190); ctx.lineTo(670, 190); ctx.stroke();
    caption(ctx, 50, 30, 'the value function on the halving probe, box by box', c.muted);
    caption(ctx, 50, 212, m + ' boxes at stage ' + n +
            '; the height of each bar is the range of values inside it', c.ink2);
    const wob = wobbleInBox(n);
    out.innerHTML = 'Largest wobble inside a single stage-' + n + ' box: <b>' +
      fmtPow(2, -n) + ' = ' + wob + '</b>.<br>' +
      'It is never zero, at any stage, so this continuous function is constant on no ' +
      'box &mdash; it is not locally constant, and it is a non-zero member of the ' +
      'leftover. The row for this probe is <b>not 0</b>.';
  };
  UI.pick(ctrl, 'the row you are reading',
          [['point', 'the one-point probe'], ['halving', 'the halving probe']],
          function(v){ probe = v; draw(); });
  UI.slider(ctrl, 'stage', 1, 8, 1, n, function(v, read){
    n = Math.round(v); read.textContent = 'stage ' + n; draw();
  });
  draw();
};

// 8. the holes of a shape, by Smith normal form
WIDGETS.holes = function(host, P){
  const cv = UI.canvas(host, 720, 220), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  let shape = 'circle';
  const draw = function(){
    const c = palette(), ctx = clearCanvas(cv);
    const h = homology(shape);
    const w = 560 / h.length;
    let text = '';
    for(let k = 0; k < h.length; k++){
      const bars = h[k].free, x = 80 + k * w;
      ctx.fillStyle = c.blue;
      for(let b = 0; b < bars; b++)
        ctx.fillRect(x + b * 22, 150 - 0, 16, -60);
      if(h[k].torsion.length){
        ctx.fillStyle = c.red;
        for(let t = 0; t < h[k].torsion.length; t++)
          ctx.fillRect(x + (bars + t) * 22, 150, 16, -26);
      }
      caption(ctx, x, 172, 'degree ' + k, c.muted);
      text += 'degree ' + k + ': rank <b>' + h[k].free + '</b>' +
        (h[k].torsion.length ? ', torsion ' + h[k].torsion.map(t => '&#8484;/' + t).join(', ')
                             : '') + '<br>';
    }
    ctx.strokeStyle = c.line; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(60, 150); ctx.lineTo(680, 150); ctx.stroke();
    caption(ctx, 60, 34, 'tall bars: free ranks. short red bars: torsion.', c.muted);
    out.innerHTML = '<b>' + shape + '</b><br>' + text +
      'Computed here from the cell structure by Smith normal form over the whole numbers.';
  };
  UI.pick(ctrl, 'the shape', [['circle', 'circle'], ['figure eight', 'figure eight'],
          ['sphere', 'sphere'], ['torus', 'doughnut'], ['klein bottle', 'Klein bottle']],
          function(v){ shape = v; draw(); });
  draw();
};

// 9. one plus two plus four, under two different nearness rules
WIDGETS.series = function(host, P){
  const p = P.p || 2;
  const cv = UI.canvas(host, 720, 280), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  let mode = P.mode === 'padic' ? 'padic' : 'ordinary', terms = 6;
  const draw = function(){
    const c = palette();
    clearCanvas(cv);
    const sums = geomPartialSums(p, terms);
    const gaps = [];
    for(let i = 0; i < sums.length; i++)
      gaps.push(mode === 'ordinary' ? Math.abs(sums[i] + 1)
                                    : pAdicAbsInt(sums[i] + 1, p));
    const ys = gaps.map(g => Math.log(g) / Math.log(p));
    let lo = 0, hi = 0;
    for(const y of ys){ lo = Math.min(lo, y); hi = Math.max(hi, y); }
    const plot = Plot(cv, 0, Math.max(1, terms - 1), lo - 0.5, hi + 0.5);
    plot.axes('terms added', 'gap, as a power of ' + p);
    const xs = ys.map((_, i) => i);
    plot.line(xs, ys, mode === 'ordinary' ? c.red : c.green, 2.4);
    plot.dots(xs, ys, mode === 'ordinary' ? c.red : c.green, 4);
    plot.hline(0, c.line, [4, 4]);
    const last = sums[sums.length - 1], gap = gaps[gaps.length - 1];
    out.innerHTML = 'After ' + terms + ' terms the running total is <b>' + last + '</b>.<br>' +
      (mode === 'ordinary'
        ? 'Its ordinary distance from &minus;1 is <b>' + gap + '</b>, and it doubles at ' +
          'every step. Nothing is closing in on anything: this sum has no answer.'
        : 'Its base-' + p + ' distance from &minus;1 is <b>' + gap + '</b>, and it halves ' +
          'at every step. The totals are closing in on &minus;1, exactly.');
  };
  UI.pick(ctrl, 'measure the gap with',
          P.mode === 'padic'
            ? [['padic', 'the base-' + p + ' rule'], ['ordinary', 'ordinary distance']]
            : [['ordinary', 'ordinary distance'], ['padic', 'the base-' + p + ' rule']],
          function(v){ mode = v; draw(); });
  UI.slider(ctrl, 'terms added', 1, 12, 1, terms, function(v, read){
    terms = Math.round(v); read.textContent = terms + ' terms'; draw();
  });
  draw();
};

// 10. weights that agree, and an integral that does not care about the stage
WIDGETS.weights = function(host, P){
  const depth = P.depth === undefined ? 3 : P.depth;
  const cv = UI.canvas(host, 720, 300), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  let first = 1;
  const draw = function(){
    const c = palette(), ctx = clearCanvas(cv);
    const S = cantorProbe(depth), leaves = {};
    S.levels[depth].forEach(function(l, i){ leaves[l] = (i === 0 ? first : 1); });
    const w = measureFromLeaves(S, leaves);
    const pos = drawTree(ctx, S, depth, {x: 40, y: 26, w: 640, h: 200},
                         {edge: c.line, colour: () => c.violet, r: 3.4});
    ctx.font = '11px ui-monospace, monospace'; ctx.textAlign = 'center';
    for(let i = 0; i <= depth; i++)
      for(const l of S.levels[i]){
        const pt = pos[i + '|' + l];
        ctx.fillStyle = c.ink2;
        if(S.levels[i].length <= 8) ctx.fillText(String(w[i][l]), pt[0], pt[1] - 8);
      }
    const f = {};
    S.levels[1].forEach(function(l, k){ f[l] = 1 + 3 * k; });
    const coarse = integrate(S, w, f, 1);
    const fine = integrate(S, w, refineFn(S, f, 1, depth), depth);
    caption(ctx, 40, 292, 'the number above each dot is that box’s weight', c.muted);
    out.innerHTML = 'Agreement rule holds: <b>' + (measureOk(S, w) ? 'yes' : 'no') +
      '</b> &mdash; every box weighs exactly what is inside it.<br>' +
      'A step function averaged at stage 1: <b>' + coarse + '</b>. The same function ' +
      'averaged at stage ' + depth + ': <b>' + fine + '</b>.<br>' +
      (coarse === fine ? 'Identical, as the compatibility forces.'
                       : 'These differ, which would mean the weights are not compatible.');
  };
  UI.slider(ctrl, 'weight on the first box', -3, 4, 1, first, function(v, read){
    first = Math.round(v); read.textContent = String(first); draw();
  });
  draw();
};

// 11. the exponent ceiling
WIDGETS.merge = function(host, P){
  const boxes = P.boxes || 4;
  const cv = UI.canvas(host, 720, 300), out = UI.out(host);
  const ctrl = UI.node('div', 'controls', host);
  let p = 1;
  const draw = function(){
    const c = palette();
    clearCanvas(cv);
    const plot = Plot(cv, 0.4, 2.2, 0, 2.6);
    plot.axes('the exponent', 'merged size / original');
    plot.curve(x => Math.min(2.6, worstMergeRatio(boxes, x)), c.violet, 2.4);
    plot.hline(1, c.line, [4, 4]);
    plot.vline(p, c.blue, [3, 3]);
    const vals = [];
    for(let i = 0; i < boxes; i++) vals.push(1);
    const groups = [[]];
    for(let i = 0; i < boxes; i++) groups[0].push(i);
    const ratio = mergeRatio(vals, groups, p);
    plot.dots([p], [Math.min(2.6, ratio)], c.blue, 5);
    plot.label(0.45, 1.06, 'no change', c.muted);
    const ok = ratio <= 1 + 1e-12;
    out.innerHTML = 'Exponent <b>' + p.toFixed(2) + '</b>: merging ' + boxes +
      ' equal boxes into one multiplies the size by <b>' + ratio.toFixed(3) + '</b>.<br>' +
      'Closed form for the worst case: ' + boxes + '<sup>1&minus;1/p</sup> = <b>' +
      worstMergeRatio(boxes, p).toFixed(3) + '</b>. ' +
      (ok ? 'A coarser view does not weigh more: <b>allowed</b>.'
          : 'A coarser view weighs more than the thing viewed: <b>forbidden</b>.');
  };
  UI.slider(ctrl, 'exponent', 0.4, 2.2, 0.05, p, function(v, read){
    p = v; read.textContent = 'p = ' + v.toFixed(2); draw();
  });
  draw();
};
"""


WIDGET_JS = HELPERS + WIDGETS

# every widget name the worlds are allowed to ask for
NAMES = ("undo", "zoom", "bridge", "algebra", "split", "landings", "glue",
         "ghost", "holes", "series", "weights", "merge")

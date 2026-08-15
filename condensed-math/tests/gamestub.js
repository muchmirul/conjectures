// A DOM stub rich enough to play one world of the game from start to finish.
//
// The game builds its own elements as it goes, so unlike the play pages there
// is no fixed markup to parse: the stub has to supply createElement and let
// the page construct itself.  The driver then walks the world by clicking
// whatever button the page is offering, which is exactly what a reader does,
// and afterwards moves every control every widget created.
//
// A page that throws anywhere in that walk fails here rather than in front of
// a reader.  Every drawing call is a counted no-op, so a widget that silently
// draws nothing is visible too.
//
// Usage:  node gamestub.js <world.html>

const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync(process.argv[2], 'utf8');

let drawCalls = 0;
function ctx2d() {
  const noop = () => { drawCalls += 1; };
  const target = {
    canvas: null,
    fillStyle: '', strokeStyle: '', lineWidth: 1, font: '', textAlign: '',
    globalAlpha: 1,
    measureText: () => ({ width: 10 }),
    createLinearGradient: () => ({ addColorStop: noop }),
  };
  return new Proxy(target, {
    get(o, k) { return (k in o) ? o[k] : noop; },
    set(o, k, v) { o[k] = v; return true; },
  });
}

const all = [];

function matches(el, sel) {
  if (sel === 'button') return el.tagName === 'BUTTON';
  if (sel.charAt(0) === '.') return String(el.className).split(/\s+/)
    .indexOf(sel.slice(1)) >= 0;
  return el.tagName === sel.toUpperCase();
}
function collect(root, sel, out) {
  out = out || [];
  for (const c of root.children) {
    if (matches(c, sel)) out.push(c);
    collect(c, sel, out);
  }
  return out;
}

function makeElement(tag) {
  const el = {
    tagName: String(tag).toUpperCase(),
    children: [], style: {}, dataset: {}, className: '', textContent: '',
    width: 720, height: 400, type: '', min: 0, max: 1, step: 1, value: '',
    _html: '', _listeners: {},
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); if (v === '') this.children = []; },
    appendChild(c) { this.children.push(c); return c; },
    setAttribute(k, v) { this[k] = v; },
    addEventListener(kind, fn) {
      (this._listeners[kind] = this._listeners[kind] || []).push(fn);
    },
    dispatch(kind, ev) {
      (this._listeners[kind] || []).forEach(f => f(ev || { preventDefault() {} }));
    },
    click() { this.dispatch('click', { preventDefault() {} }); },
    getContext() { return ctx2d(); },
    scrollIntoView() {},
    querySelectorAll(sel) { return collect(this, sel); },
    querySelector(sel) { return collect(this, sel)[0] || null; },
    classList: {
      _s: new Set(),
      add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); },
      contains(c) { return this._s.has(c); },
    },
  };
  all.push(el);
  return el;
}

const story = makeElement('div');
const act = makeElement('div');
const bar = makeElement('i');
const fixed = { story: story, act: act, bar: bar };

const document = {
  createElement: makeElement,
  getElementById: id => fixed[id] || null,
  documentElement: makeElement('html'),
  body: makeElement('body'),
};

const sandbox = {
  document, console, Math, JSON, Array, Object, Number, String, Set, Map,
  Infinity, NaN, isNaN, parseInt, parseFloat, Date: undefined,
  Uint8ClampedArray,
};
vm.createContext(sandbox);

const script = html.split('<script>')[1].split('</script>')[0];
vm.runInContext(script, sandbox, { timeout: 60000 });

// --- walk the world by pressing whatever is on offer ------------------------

let clicks = 0, rotate = 0, finished = false;
for (let i = 0; i < 6000; i += 1) {
  const buttons = collect(act, 'button');
  if (!buttons.length) break;
  const button = buttons.length > 1
    ? buttons[rotate++ % buttons.length]
    : buttons[0];
  if (/Restart this world/.test(button.innerHTML)) { finished = true; break; }
  button.click();
  clicks += 1;
}

// --- then move every control every widget put on the page -------------------

let moves = 0;
for (const el of all) {
  if (el.tagName !== 'INPUT') continue;
  const lo = parseFloat(el.min), hi = parseFloat(el.max);
  const step = parseFloat(el.step) || 1;
  for (const v of [lo, lo + step, (lo + hi) / 2, hi - step, hi]) {
    el.value = String(Math.max(lo, Math.min(hi, v)));
    el.dispatch('input');
    moves += 1;
  }
}
for (const box of collect(story, '.pick')) {
  for (const b of box.children) { box.dispatch('click', { target: b }); b.click(); moves += 1; }
}

let text = 0, canvases = 0;
for (const el of all) {
  text += String(el.innerHTML || '').length;
  if (el.tagName === 'CANVAS') canvases += 1;
}

console.log(JSON.stringify({
  drawCalls: drawCalls, clicks: clicks, moves: moves,
  textLength: text, canvases: canvases, finished: finished,
}));

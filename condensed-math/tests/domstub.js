// A canvas and DOM stub just rich enough to run one play page's widget.
//
// The widgets draw to a canvas and read sliders.  Running them here catches
// the errors a syntax check cannot: a misspelt variable, a control that is
// read before it exists, an arithmetic slip that throws.  Every drawing call
// is a no-op that records it was made, so a widget that silently draws
// nothing is also visible.
//
// Usage:  node domstub.js <page.html>

const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync(process.argv[2], 'utf8');

let calls = 0;
function ctx2d() {
  const noop = () => { calls += 1; };
  const target = {
    canvas: null,
    fillStyle: '', strokeStyle: '', lineWidth: 1, font: '', textAlign: '',
    globalAlpha: 1,
    measureText: () => ({ width: 10 }),
    createImageData: (w, h) => ({ data: new Uint8ClampedArray(w * h * 4) }),
    getImageData: (x, y, w, h) => ({ data: new Uint8ClampedArray(w * h * 4) }),
    createLinearGradient: () => ({ addColorStop: noop }),
  };
  return new Proxy(target, {
    get(o, k) {
      if (k in o) return o[k];
      return noop;                 // every drawing verb is a counted no-op
    },
    set(o, k, v) { o[k] = v; return true; },
  });
}

function makeElement(id, tag, attrs) {
  const listeners = {};
  const el = {
    id, tagName: tag.toUpperCase(), dataset: Object.assign({}, attrs.data || {}),
    value: attrs.value !== undefined ? attrs.value : '',
    min: attrs.min, max: attrs.max, step: attrs.step,
    textContent: '', className: attrs.className || '',
    width: attrs.width || 720, height: attrs.height || 400,
    children: [],
    classList: {
      _s: new Set((attrs.className || '').split(/\s+/).filter(Boolean)),
      add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); },
      contains(c) { return this._s.has(c); },
    },
    style: {},
    getContext: () => ctx2d(),
    getBoundingClientRect: () => ({ left: 0, top: 0, width: 720, height: 400 }),
    addEventListener(kind, fn) { (listeners[kind] = listeners[kind] || []).push(fn); },
    dispatch(kind, ev) { (listeners[kind] || []).forEach(f => f(ev || {})); },
    _listeners: listeners,
    querySelector(sel) { return el.children.find(c => c.classList.contains(
      sel.replace(/^button\./, ''))) || null; },
    querySelectorAll() { return el.children; },
    appendChild(c) { el.children.push(c); },
  };
  return el;
}

// --- read the page's controls out of its markup ---------------------------

const elements = {};
function put(el) { elements[el.id] = el; return el; }

put(makeElement('c', 'canvas', { width: 720, height: 400 }));
put(makeElement('out', 'div', {}));

for (const m of html.matchAll(
    /<input type="range" id="([^"]+)" min="([^"]+)" max="([^"]+)" step="([^"]+)" value="([^"]+)">/g)) {
  put(makeElement(m[1], 'input',
    { min: m[2], max: m[3], step: m[4], value: m[5] }));
}
for (const m of html.matchAll(/<span class="val" id="([^"]+)">/g)) {
  put(makeElement(m[1], 'span', {}));
}
for (const m of html.matchAll(
    /<div class="pick" id="([^"]+)" style="flex:1">([\s\S]*?)<\/div>/g)) {
  const box = put(makeElement(m[1], 'div', { className: 'pick' }));
  for (const b of m[2].matchAll(/<button data-v="([^"]*)" class="([^"]*)">/g)) {
    const btn = makeElement('', 'button', { data: { v: b[1] }, className: b[2] });
    box.appendChild(btn);
  }
  box.querySelector = sel => box.children.find(c => c.classList.contains('on'))
    || box.children[0];
  box.querySelectorAll = () => box.children;
}

const document = {
  getElementById: id => elements[id] || null,
  body: makeElement('body', 'body', {}),
  querySelectorAll: () => [],
};

const sandbox = { document, location: { search: '' }, console, Math, JSON,
                  Array, Object, Number, String, Set, Map, Uint8ClampedArray,
                  Infinity, NaN, isNaN, parseInt, parseFloat };
// browsers expose every element with an id as a global of that name, and the
// pages rely on it for their readout spans, so the stub does the same
for (const id of Object.keys(elements)) sandbox[id] = elements[id];

const script = html.split('<script>')[1].split('</script>')[0];
vm.createContext(sandbox);
vm.runInContext(script, sandbox, { timeout: 20000 });

// --- exercise every control ------------------------------------------------

let moves = 0;
for (const id of Object.keys(elements)) {
  const el = elements[id];
  if (el.tagName !== 'INPUT') continue;
  const lo = parseFloat(el.min), hi = parseFloat(el.max);
  const step = parseFloat(el.step) || 1;
  const stops = [lo, lo + step, (lo + hi) / 2, hi - step, hi];
  for (const v of stops) {
    el.value = String(Math.max(lo, Math.min(hi, v)));
    el.dispatch('input');
    moves += 1;
  }
}
for (const id of Object.keys(elements)) {
  const box = elements[id];
  if (!box.classList.contains('pick')) continue;
  for (const btn of box.children) {
    box.dispatch('click', { target: btn });
    moves += 1;
  }
}
const canvas = elements['c'];
canvas.dispatch('click', { clientX: 200, clientY: 120 });
canvas.dispatch('click', { clientX: 640, clientY: 300 });

const readout = elements['out'].textContent;
console.log(JSON.stringify({ drawCalls: calls, moves: moves,
                             readoutLength: readout.length }));

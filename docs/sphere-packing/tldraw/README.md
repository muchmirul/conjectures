# The chapter 0 stack, rebuilt on a tldraw canvas

An experiment, kept apart from the article on purpose.

`index.html` is the same stack as [chapter 0's play page](../play/00.html): one
ball and the twelve that touch it, in the greengrocer's arrangement. Two things
are added.

**Turning it.** The original is dragged with the mouse. Dragging is what a
tldraw canvas already uses to pan the camera, so the turn and tilt are on
dials instead, with a spin button for a hands-off rotation. The projection is
copied from the original page, and a test confirms it is rigid: every ball
keeps its exact distance from the middle one at every angle.

**Opening the gaps.** The separation between centres is adjustable from
touching up to double, and the share of space filled is an editable box that
solves the other way round: type a percentage and the stack drifts apart to
match it. This is the point chapter 0 states but cannot show. The balls never
change size; only the spacing does, so the share of space falls with the cube
of the separation. Pulling the centres a quarter further apart drops the
tightest stack from 74.05 percent to 37.91.

Both arrangements from the article are drawn: the greengrocer's stack, with
twelve balls touching the middle one and 74.05 percent of space filled, and
plain rows and columns, with six touching and 52.36 percent.

## Running it

```bash
cd docs/sphere-packing/tldraw
python3 -m http.server 8000
# then open http://localhost:8000/
```

Opening the file directly with a double click may work, but some browsers
refuse to load JavaScript modules from a `file://` page. The page says so and
prints these instructions if that happens.

## Why it is not in the article

The pages under [`../play/`](../play/) carry no libraries and make no network
requests, so they work offline and straight from a file, and their arithmetic
is checked against the Python library in `sphere-packing/tests/`. This page
breaks the first two of those promises: tldraw is a React SDK, and both React
and tldraw are fetched from a CDN at load time. That is why it sits in its own
folder and is not embedded in `index.html`.

## What the percentage means

The thirteen or twenty-seven balls on the canvas are a fragment. The figure is
the share of space filled by the endless arrangement they are cut from, not by
the handful on screen, which would depend on where the boundary was drawn. The
page says this too.

## Licensing, in short

tldraw is **not open source**. It is free in development, which covers this
page opened locally, and needs a licence key in production, which includes any
copy served over HTTPS from the published site. A free hobby licence covers
non-commercial use and shows a "made with tldraw" watermark on the canvas; the
commercial licence is paid and priced by arrangement. See
[tldraw's licence key documentation](https://tldraw.dev/sdk-features/license-key)
and [LICENSE.md](https://github.com/tldraw/tldraw/blob/main/LICENSE.md).

Nothing else in this repository depends on tldraw. Deleting this folder removes
the dependency completely.

## What was checked, and what was not

Verified before committing:

- every CDN URL in the import map resolves, and the module script parses
- the two densest shares, 74.05 and 52.36 percent, are computed here and match
  `sphere_packing_guide.examples.known_density` to ten decimal places
- the drawn cluster really is the middle ball plus exactly twelve at the
  touching distance, and the cubic one has exactly six
- separation and percentage invert each other exactly, in both arrangements
- the projection preserves every distance from the middle ball, at every angle
- 37.91 percent, the figure quoted in the page's own text, is what the formula
  gives at a separation of 1.25
- every shape property and style value is legal against tldraw 5's schema

One real bug was caught this way and fixed: depth ordering was first written
with `editor.bringToFront`, which returns early when every shape on the page is
moving, so it would have done nothing at all. The balls are stacked by
assigning index keys instead.

Not verified: how it actually looks in a browser. There is no headless browser
on the machine this was written on, so the page has never been rendered. Treat
the layout and spacing as a first draft.

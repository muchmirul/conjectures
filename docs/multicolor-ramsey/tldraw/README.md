# The chapter 3 idea, rebuilt on a tldraw canvas

An experiment, kept apart from the article on purpose.

`index.html` is the same idea as [chapter 3's play page](../play/03.html): take
the first n people of the sixteen-person, three-colour table and watch the
one-colour triangle count stay at zero all the way to sixteen. The difference
is that here the people are real objects on an infinite canvas. You can drag
them anywhere and the connections follow, which makes the point the static
drawing cannot: the circle is only a convenient arrangement, and safety lives
in the pattern of colours rather than in where anybody is standing.

## Running it

```bash
cd docs/multicolor-ramsey/tldraw
python3 -m http.server 8000
# then open http://localhost:8000/
```

Opening the file directly with a double click may work, but some browsers
refuse to load JavaScript modules from a `file://` page. The page says so and
prints these instructions if that happens.

## Why it is not in the article

The pages under [`../play/`](../play/) carry no libraries and make no network
requests, so they work offline and straight from a file, and their arithmetic
is checked against the Python library in `multicolor-ramsey/tests/`. This page
breaks the first two of those promises: tldraw is a React SDK, and both React
and tldraw are fetched from a CDN at load time. That is why it sits in its own
folder and is not embedded in `index.html`.

The mathematics is not re-derived here. The colouring, the triangle check and
the ring layout are copied verbatim from `play/03.html`, and their outputs were
compared function by function for every n from 3 to 16 before this page was
committed.

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

- every CDN URL in the import map resolves
- the module script parses
- the colourings, triangle counts and layout coordinates match `play/03.html`
  exactly for n = 3 to 16
- every shape property, binding property and style value used here is legal
  against tldraw 5's published schema (`geo`, `arrow` and `arrow` binding
  records)

Not verified: how it actually looks in a browser. There is no headless browser
on the machine this was written on, so the page has never been rendered. Treat
the layout and spacing as a first draft.

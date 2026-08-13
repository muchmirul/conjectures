# Research notes: delivery, formats and rendering

How the guide reaches a reader, and the things that had to be worked out to make
that reliable.

## Three formats, one source of truth

| format | file | for |
|---|---|---|
| chapter folders | `guide/NN-slug/README.md` | reading on GitHub, one idea at a time |
| one long article | `ARTICLE.md` | copy-paste into anything that takes Markdown |
| web article | `../docs/kakeya-conjecture/index.html` | GitHub Pages, real LaTeX via MathJax |

The web article sits in the repository's root `docs/` folder, one subfolder per
topic, because GitHub Pages can only publish from the root or from `/docs`.
`make docs` rebuilds it from `ARTICLE.md`.

The chapter folders are the source of truth: the article and the web page follow
them. Media lives beside the text that uses it, because GitHub renders a folder's
README.md automatically, which gives click-through navigation for free.

## GitHub markdown gotchas

- Use ```` ```math ```` fences for display math. `$...$` inline math works but is
  fragile; keep it short and avoid `|` inside it.
- No math inside table cells.
- `<img src="..." width="...">` is honoured; markdown image syntax cannot set a
  width. Every image gets a real `alt` describing what it shows, not what it is.
- Relative links between chapter folders (`../05-the-perron-tree/README.md`) work
  both on github.com and in most local previewers.

## Which figures move, and which do not

A figure is a GIF only when the motion **is** the point, and there are exactly
two reasons for that:

1. the motion is the mathematics: the needle turning, the slivers sliding, the
   sweep line climbing;
2. the subject has a dimension the page cannot show standing still, so the
   camera turns right round it. `spin_gif` in `plotting.py` does the turning.
   Three dimensions get a real 3D scene; four dimensions get a real 4D
   rotation, projected down the way a cube's shadow is drawn, because a
   picture of 4D that only turns in 3D is a lie. The direction sets come from
   `sphere_directions(n, count)`, which works in every dimension, so the same
   figure extends to n = 5 or 10 by changing one argument.

Everything else, meaning every chart and every diagram, is a static PNG.
Motion is reserved for the figures whose movement is the mathematics.

And a third rule, learned the hard way: **a picture that is only words is not a
picture.** Cards of text, step lists, timelines and status tables were drawn as
PNGs at first. They are now typed straight into the chapters, where they can be
selected, searched, translated, read aloud by a screen reader, and diffed in
git. A figure earns its file only if something is actually drawn in it.

Fifteen GIFs, fourteen PNGs, and seven pictures deleted in favour of typing.
`tests/test_guide.py` reads the typed tables back and compares them with the
data in `kakeya_guide.examples`, so the text cannot drift from the numbers, and
it also fails if any chapter grows a figure nothing points at.

The rule matters for reading, not just for file size. An animated bar chart
makes the reader wait to see a number they could have read at a glance, and it
cannot be scanned back and forth. Where an animation used to reveal its values
one at a time, the static version labels them all.

The stack is matplotlib plus Pillow, with no ffmpeg needed. The ten figures
that move are written as GIF so they play inline on GitHub.

Two problems were worth solving properly on the GIF side:

1. **Odd pixel widths shear the GIF.** A figure of 9.2 inches at 110 dpi comes
   out 1011 pixels wide, and the writer produces frames where every row slips one
   pixel sideways: the picture arrives visibly skewed. Fix: `save_anim` snaps the
   canvas to even pixel dimensions before writing (`_snap_to_even_pixels` in
   `plotting.py`). Naive rounding is not enough, because `9.2 * 110` is
   1011.9999999999999 in floating point and gets floored back to 1011; the helper
   adds a quarter pixel of slack.

2. **Blank first frames.** Animations that build up from nothing start with an
   empty canvas, which is what a reader sees as the static preview, and it also
   confuses some GIF decoders. Every reveal animation now shows its first element
   on frame 0.

Other conventions:

- 2 to 14 fps depending on whether the frames are a story or a slideshow.
- A few frames of hold at the end so the loop reads as a loop.
- Figures render on a near-white surface so they read on both light and dark
  GitHub themes.
- Keep each GIF under about 1.5 MB; the whole `guide/` folder is under 10 MB.
- PNGs are saved with `bbox_inches="tight"`, so a chart is cropped to its own
  content and the chapters do not have to guess at padding.

## Colour language

Fixed across all chapters, from a colourblind-safe palette:

- blue: the needle, and the directions it must hit
- green: a region doing its job
- red: wasted area, or trouble
- yellow: the patch of area currently under discussion
- warm gray: scaffolding, the original triangle, grid lines

## Making sure the pictures actually appear

`docs/index.html` used to point every figure at raw.githubusercontent.com,
which fails the moment the page is opened from disk before the repo is pushed:
a page of broken images. Each figure now carries a list of places to look, in
order: beside the repo (`../guide/...`), at the site root (`guide/...`), then
GitHub raw. A short script at the bottom of the page walks the list on error,
and marks the figure visibly if every candidate fails, instead of leaving a
silent gap. Lazy loading is off on purpose: an animation that has not begun
when the reader arrives reads as a broken one.

## Reproducibility

`make venv && make test && make figures` rebuilds everything from nothing. The
figure scripts import from `src/kakeya_guide`, so a number in a picture and a
number in a test come from the same function. Nothing in `guide/` is drawn by
hand or typed in from a paper.

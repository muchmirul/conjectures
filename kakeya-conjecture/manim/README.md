# Manim scenes (optional)

Every image committed under `guide/` was produced by the matplotlib scripts in
`src/viz/`, with no Manim involved. This folder is a bonus: the same four
stories, rendered by [Manim Community Edition](https://www.manim.community/) if
you want fancier motion.

## Install

```bash
../../.venv/bin/pip install -e "..[manim]"   # the shared venv; pulls manim>=0.18
```

Manim needs a working `ffmpeg` on your PATH. It does **not** need LaTeX here:
every scene uses `Text` (Pango), never `Tex`.

## Render

```bash
cd manim
manim -qm --format=gif scenes.py PerronTree      # medium quality GIF
manim -qh scenes.py NeedleTurn                   # high quality MP4
```

Output lands in `manim/media/`, which is git-ignored.

## The scenes

| scene | chapter | what it shows |
|---|---|---|
| `PerronTree` | 5 | 16 slivers sliding together stage by stage, area falling |
| `NeedleTurn` | 6 | the needle pivoting through each sliver's wedge of directions |
| `OverlapIsFree` | 3 | two halves of a triangle merging, area down to two thirds |
| `PalJoin` | 4 | crossing to a parallel line by way of a long thin detour |

The geometry comes from `kakeya_guide.core`, the same module the tests check, so
these scenes cannot drift away from the mathematics either.

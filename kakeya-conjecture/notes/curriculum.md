# Curriculum design, "Zero to the Kakeya Conjecture"

**Goal.** A reader with no math background reads short chapters, looks at pictures and
animations, and ends up genuinely understanding what the Kakeya conjecture says, why
its answer astonished everyone, and what was finally proved in February 2025.

**Design principles:**

1. **Picture first, words second, symbols last.** Every concept gets a visual before
   it gets a name, and a name before it gets a formula.
2. **One idea per chapter.** Each chapter is readable in ~5 minutes and ends with a
   single boxed take-away sentence.
3. **Simple sentences.** Short sentences. Everyday words. Jargon only after the idea
   already exists in the reader's head, introduced in **bold**.
4. **Everything is runnable.** Every figure in the guide is produced by a script in
   this repo. Readers can tweak numbers and re-render.
5. **Honest math.** No lies-to-children that must be unlearned later. Simplify by
   omission, never by falsehood. Where a claim cannot be checked by computer, say so
   in the chapter, not in a footnote.
6. **Words are typed, not drawn.** If a figure would contain only text, it is
   text. Pictures are for things with a shape.

## The learning journey (chapter map)

| # | Chapter | The one idea | Flagship visual |
|---|---------|--------------|-----------------|
| 0 | Start here | A needle turns inside almost nothing | hero: needle turning in a Perron tree |
| 1 | The needle | Only direction matters; all directions fit in a half circle | rotating needle + direction dial |
| 2 | Turning around | Disc, triangle, deltoid: the rooms people tried | three real turning motions, side by side |
| 3 | How much space | Overlap is charged once, and sliding keeps directions | two halves sliding together, area curve |
| 4 | The free slide | Sliding along your own line is free; Pal's join | the join, with area and travel readouts |
| 5 | The Perron tree | Cut and slide; one fixed squeeze stalls at 1/6 | the tree assembling, exact areas |
| 6 | Area zero | There is no smallest room (Besicovitch 1919/1928) | trees shrinking, needle turning through the fan |
| 7 | Zero but big | Dimension is a second ruler; Cantor set has length 0, dimension 0.63 | box counting with the slope appearing |
| 8 | The conjecture | Volume can be zero, dimension cannot drop | the forbidden band; directions in 2D, 3D and 4D, all turning |
| 9 | Why it matters | Needles become tubes become wave packets | tubes at four thicknesses |
| 10 | On a grid | Finite fields: the conjecture is a theorem you can run | the smallest grid Kakeya set; the same grid in 3D, rotating |
| 11 | Why it was hard | Tubes hug without being lines; a century of inches | the bounds step chart; bush vs hairbrush, in 3D |
| 12 | The proof | Wang-Zahl, Feb 2025, dimension 3 in 3D; n >= 4 open | tubes over the sphere, and the tree extruded, both rotating |

## Chapter template

1. *Promise*: "By the end of this page you will ..." (one sentence)
2. *Picture/animation* immediately
3. Short explanation in simple sentences, interleaved with figures
4. *Try it*: command to re-render / tweak the figure, plus a few lines of API
5. *The one thing to remember* (boxed sentence)
6. Links to previous and next chapter

## Deliberate ordering choices

- **Area before dimension.** The reader must feel the shock of "area zero" before
  being handed a second ruler, otherwise dimension looks like an arbitrary
  definition instead of a repair.
- **The two definitions kept apart from chapter 1.** Kakeya *set* (holds every
  direction) versus Kakeya *needle set* (the needle can turn). Most popular
  accounts blur these, and then the 1919 and 1928 results look like one result.
- **The finite field chapter before the "why it was hard" chapter.** The reader
  should meet a complete, runnable proof first; only then does the question "why
  does this not work in the plane?" have teeth.
- **The proof chapter is not the climax of the hands-on thread.** Chapter 10 is.
  A 127 page proof cannot be run, and pretending otherwise would break principle 5.

## Repo layout

```
guide/NN-slug/README.md   one chapter per folder, figures alongside
src/kakeya_guide/         core.py (exact sliver geometry), finite.py (grids and
                          Dvir), shapes.py (disc/triangle/deltoid), dimension.py
                          (box counting), examples.py, plotting.py
src/viz/                  per-chapter figure scripts (chNN_*.py), runnable standalone
manim/                    optional Manim scenes (fancier renders)
tests/                    every claim about a computable object
notes/                    research + this design doc
Makefile                  `make figures` / `make chNN_x` re-render media, `make test`
```

## Toolchain decisions

- **matplotlib + Pillow GIFs** are the workhorse: render everywhere, embed inline on
  GitHub, no LaTeX needed. Every animation is snapped to an even pixel size first:
  an odd width comes out of the GIF writer sheared.
- **Exact rational arithmetic** (`fractions.Fraction`) for every area the guide
  quotes. Floating point appears only in the numeric estimator used for searching,
  and in the classical shapes, where the answers involve pi and sqrt(3) anyway.
- **No sympy dependency in the hot paths.** The geometry is elementary enough that
  exact arithmetic on fractions is faster and easier to audit than a CAS.
- GitHub markdown renders ```math fences; keep formulas few and small anyway.

## Correctness guardrails (facts the text must respect)

- Besicovitch 1919 gives measure zero sets holding every direction; the 1928 paper
  gives *needle* sets of arbitrarily small area. Different statements, different
  years, both his.
- The equilateral triangle of height 1 is the smallest *convex* Kakeya needle set
  (Pal 1921). The deltoid, at pi/8, is smaller and not convex.
- The Perron tree's area falls like 1/log(number of slivers), and Keich (1999)
  proved that rate is sharp. Do not let the animations imply it falls fast.
- Davies 1971: plane Kakeya sets have Hausdorff dimension 2. Not the same as
  "measure zero is impossible", which is false.
- Dvir 2008 proves the finite field version; it does not transfer to R^n, and the
  chapter must say why.
- Wang-Zahl 2025 is three dimensional. n >= 4 is open, and the guide never implies
  the conjecture is finished.

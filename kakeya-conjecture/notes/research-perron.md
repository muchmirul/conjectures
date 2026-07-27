# Research notes: choosing the squeeze schedule for the Perron trees

The guide needs a tree whose area visibly falls. Getting one took a scan, and the
scan produced a fact worth putting in the guide itself.

## The construction, and the one parameter

At stage `j` the tree merges pairs of bunches by sliding the right bunch left by
`2 * W * (1 - alpha_j)`, where `W` is the base width of one bunch's original
triangle. `alpha_j` is the fraction of its width the merged pair keeps.

The single merge has a closed form (derived in `merged_pair_area`, verified in
`tests/test_core.py`): sliding by `t` half-widths leaves area
`1 - t + 3t^2/4`, minimised at `t = 2/3`, that is `alpha = 2/3`, with two thirds
of the area surviving.

## What one fixed alpha does

The obvious choice is that locally optimal `alpha = 2/3` at every stage. Exact
areas, computed with `union_area`:

```
k=0  1/2      = 0.500000
k=1  1/3      = 0.333333
k=2  1/4      = 0.250000
k=3  5/24     = 0.208333
k=4  3/16     = 0.187500
k=5  17/96    = 0.177083
k=6  11/64    = 0.171875
k=7  65/384   = 0.169271
k=8  43/256   = 0.167969
k=9  257/1536 = 0.167318
```

which is exactly `1/6 + 1/(3 * 2^k)`. It converges to 1/6 and stops. The picture
shows why: a constant alpha makes the figure self similar, every sliver passes
through one point, and the solid triangle below it never thins.

Scanning alpha at fixed k confirms 2/3 is the best *constant*, and that all
constants stall (numeric estimator, k = 12):

```
alpha   0.50   0.55   0.60   0.65   0.70   0.75   0.80   0.85   0.90   0.95
area   0.250  0.208  0.180  0.168  0.170  0.188  0.220  0.268  0.330  0.408
```

## Varying alpha with scale

Squeeze hard where the slivers are thin, gently where they are fat. Family
`alpha_j = 1 - c/(j + s)`, scanned over `c` in quarter steps and `s` in 1..4:

```
k=8    c=5/2,s=4 -> 0.1243   c=11/4,s=4 -> 0.1255   c=9/4,s=4 -> 0.1260
k=10   c=11/4,s=4 -> 0.1088  c=3,s=4 -> 0.1097      c=5/2,s=4 -> 0.1105
k=12   c=3,s=4 -> 0.0982     c=11/4,s=4 -> 0.0992   c=5/2,s=4 -> 0.1026
```

`c = 3, s = 4` wins at the depth the guide illustrates, and it has the pleasant
closed form `alpha_j = (j+1)/(j+4)`: 1/4, 2/5, 1/2, 4/7, 5/8, 2/3, 7/10, ...
That is `ramped_alphas` and it is what `examples.tree(k)` uses.

Areas (numeric estimator, matching the exact values where those were computed):

```
k     0      1      2      3      4      5      6      7      8      9     10     12     14
area 0.500  0.469  0.393  0.316  0.244  0.198  0.167  0.145  0.129  0.118  0.110  0.098  0.091
```

Slow. That is not a defect of the scan: Keich (1999) proved the Perron tree's
area is Theta(1/log n) in the number of slivers, and that the rate cannot be
improved. So the honest story for the guide is "it falls, it never stops, and it
falls like 1/log n", not "watch it plunge".

## Note on exactness

The exact areas past k = 4 have denominators with a hundred digits: even though
the sliver coordinates are simple fractions, the crossing heights that the sweep
integrates over are ratios of them, and the denominators multiply. The guide
quotes decimals past k = 4 and the tests check the exact fractions where they are
small and the decimals to 1e-6 elsewhere. Snapping the alphas to sixteenths was
tried; it does not tame the denominators (the crossings still make them) and it
costs about 2 percent of area, so it was dropped.

## Note on the area routine

Two implementations, on purpose:

- `union_area`: a kinetic sweep, exact, O(crossings). Fast enough for 512 slivers
  in about 15 seconds.
- `union_area_reference`: every crossing height, sorted, trapezoids. Obviously
  correct, unusably slow past a few dozen slivers.

The tests demand they agree, on random figures and on real trees. A third
routine, `union_area_numeric`, samples heights with numpy and is used only for
scanning: an earlier attempt to run the kinetic sweep in floating point produced
*negative* areas, because these trees are full of exactly coincident crossings
and floating point turns those ties into inconsistent orderings. That attempt is
the reason the numeric estimator samples instead of sweeping.

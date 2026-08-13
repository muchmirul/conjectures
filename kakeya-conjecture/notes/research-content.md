# Research notes: the mathematical content, and where each claim comes from

Every factual claim in the guide is listed here with its source and, where it
applies, the test that re-checks it. Claims fall into three buckets:

- **[computed]** the repo derives it from scratch, exactly, in `tests/`
- **[classical]** a theorem from the literature, quoted, not verified here
- **[recent]** an announced or published result whose status is stated in the text

---

## History and attribution

| year | claim | bucket | source |
|---|---|---|---|
| 1917 | Soichi Kakeya asks for the smallest area in which a unit needle can be turned through 180 degrees | [classical] | Kakeya, Tohoku Math. J. 1917; Kakeya and Fujiwara |
| 1919 | Besicovitch constructs sets of measure zero containing a unit segment in every direction | [classical] | Besicovitch 1919 (Perm), restated in Math. Z. 27 (1928) 312-320 |
| 1921 | Pal: the equilateral triangle of height 1 is the smallest **convex** Kakeya needle set; the "Pal join" for moving a needle between parallel lines | [classical] | Pal, Math. Ann. 83 (1921) |
| 1928 | Besicovitch: needle sets of arbitrarily small area exist, so Kakeya's question has no answer | [classical] | Besicovitch, Math. Z. 27 (1928) |
| 1928 | Perron simplifies the construction to the "Perron tree" | [classical] | Perron, Math. Z. 28 (1928) |
| 1971 | Davies: every Kakeya set in the plane has Hausdorff dimension 2 | [classical] | Davies, Proc. Cambridge Philos. Soc. 69 (1971) |
| 1971 | Cunningham: simply connected Kakeya needle sets of arbitrarily small area exist inside a disc of radius 1 | [classical] | Cunningham, Amer. Math. Monthly 78 (1971) |
| 1991 | Bourgain pushes the dimension bound past (n+1)/2 | [classical] | Bourgain, GAFA 1 (1991) |
| 1995 | Wolff's hairbrush argument: dimension at least (n+2)/2, so 5/2 in R^3 | [classical] | Wolff, Rev. Mat. Iberoamericana 11 (1995) |
| 1999 | Wolff poses the finite field Kakeya problem | [classical] | Wolff, "Recent work connected with the Kakeya problem" |
| 2000 | Katz, Laba, Tao: Minkowski dimension at least 5/2 + 10^(-10) in R^3 | [classical] | Katz-Laba-Tao, Ann. of Math. 152 (2000) |
| 2008 | Dvir: the finite field Kakeya conjecture, by the polynomial method | [classical] | Dvir, J. Amer. Math. Soc. 22 (2009); the improved constant is due to Alon and Tao, see Dvir-Kopparty-Saraf-Sudan |
| 2019 | Katz and Zahl: Hausdorff dimension at least 5/2 + epsilon in R^3 | [classical] | Katz-Zahl, J. Amer. Math. Soc. 32 (2019) |
| 2025 | Wang and Zahl: every Kakeya set in R^3 has Hausdorff and Minkowski dimension 3 | [recent] | arXiv:2502.17655, submitted 24 Feb 2025, 127 pages, 14 figures |

Status of the 2025 paper as this guide is written (July 2026): posted to arXiv,
publicly analysed (Tao's blog post of 25 Feb 2025 works through the strategy),
built on the same authors' earlier sticky Kakeya work (arXiv:2210.09581). The
guide states it as a theorem the community has checked, and says explicitly that
nothing in this repo verifies it.

---

## The classical rooms (chapter 2)

- Disc of diameter 1: area pi/4 = 0.785398... **[computed]** `test_shapes.py`
- Equilateral triangle of height 1: area 1/sqrt(3) = 0.577350... **[computed]**
- Deltoid with tangent chord of length 1 (rolling circle radius a = 1/4):
  area 2*pi*a^2 = pi/8 = 0.392699... **[computed]**
- The deltoid's tangent chord: for the parametrisation
  x = 2a cos t + a cos 2t, y = 2a sin t - a sin 2t, the tangent at parameter t
  meets the curve again at parameters -t/2 and pi - t/2, and that chord has
  length exactly 4a. **[computed]** to 1e-12 over the whole curve.
- Pal's turn inside the triangle: three 60 degree pivots about the corners,
  joined by three slides along the sides, gives a full 180 degree turn with the
  needle inside the triangle at every instant. **[computed]** over 600 frames.
- Minimality of the triangle among convex sets is Pal's theorem **[classical]**;
  the repo only checks that a unit needle fits at every angle, and that it stops
  fitting when the height drops to 0.99.

---

## Perron trees (chapters 5 and 6)

Setup: the triangle with base [0,1] and apex (1/2, 1) is cut into 2^k slivers
and merged in k stages. The right member of each pair slides left by
2*W*(1-alpha), where W is the base width of one member's original triangle.

- **Steady squeeze (alpha = 2/3 at every stage).** Exact area
  1/6 + 1/(3*2^k). **[computed]** for k = 0..6 as exact fractions; the tests also
  confirm the area never drops to 1/6.
  The picture explains the formula: with one fixed alpha the figure is self
  similar, all slivers pass through a single point, and the solid triangle below
  that point never thins out (see `stall.gif`).
- **Varying squeeze (alpha_j = (j+1)/(j+4)).** Exact areas
  1/2, 15/32, 629/1600, 3029/9600, 13133/53760, then decimals
  0.197952, 0.166697, 0.145032, 0.129469, 0.118088 for k = 5..9. **[computed]**
  This schedule was found by scanning, not derived; see research-perron.md.
- Every sliver of a finished tree is a translate of the elementary sliver it came
  from, and the union of their direction intervals is the full fan [-1/2, 1/2].
  **[computed]** for k = 0..6.
- The single merge of two half slivers, slid by t, has area exactly
  1 - t + 3t^2/4, minimised at t = 2/3 with value 2/3. **[computed]**
- **[classical]** The Perron tree's area is Theta(1/log n) in the number of
  slivers n, and that rate is sharp (Keich, Bull. London Math. Soc. 31 (1999)).
  So no finite table can show the area getting genuinely small, and the guide
  says so rather than implying otherwise.
- **[classical]** Tree plus Pal joins gives Besicovitch's 1928 theorem. The limit
  itself is a proof, not a computation, and is quoted.

---

## Dimension (chapter 7)

- Middle-thirds Cantor set: length (2/3)^m at level m, box count exactly 2^m at
  scale 3^(-m), measured box dimension log2/log3 = 0.6309297535714574 to 1e-12.
  **[computed]** `test_dimension.py`
- Self-similar sets with p pieces at ratio r have dimension log p / log(1/r);
  checked for (2,1/3), (2,1/4), (3,1/5), (4,1/9). **[computed]**
- Cantor set times an interval: box counts exactly 6^m, dimension
  1 + log2/log3. Cantor set squared: dimension 2*log2/log3. **[computed]**
- A Besicovitch set in the plane has area 0 and dimension 2. **[classical]**
  (Davies 1971.) Nothing here computes it.

---

## The finite grid (chapter 10)

All of these are for prime q. The module refuses non-prime input rather than
pretending to handle it.

- Number of directions in F_q^n is (q^n - 1)/(q - 1), so q+1 in the plane.
  **[computed]**
- Dvir's bound: |K| >= C(q+n-1, n), which equals the number of monomials of
  degree at most q-1 in n variables. **[computed]** that the two counts agree.
- Smallest Kakeya sets in the plane, by exhaustive search with pruning:
  q=2: 3, q=3: 7, q=5: 17, q=7: 31. **[computed]**
  These match Blokhuis and Mazzocca's formula q(q+1)/2 + (q-1)/2 for odd q and
  q(q+1)/2 for even q **[classical]** (Blokhuis-Mazzocca, "The finite field
  Kakeya problem"; see also arXiv:0911.4370).
- The tangent-lines-to-a-parabola construction attains those minima:
  for each slope m take the line y = m x - m^2/4, then add one vertical line.
  A point (x,y) is on some tangent line exactly when x^2 - y is a square, which
  gives q(q+1)/2 points, and the vertical line adds (q-1)/2 more. **[computed]**
  that the result is Kakeya and has exactly the minimum size.
- Dvir's proof, step by step, all **[computed]**:
  1. a set smaller than the coefficient count carries a nonzero vanishing
     polynomial of degree <= q-1 (nullspace over F_q);
  2. such a polynomial, restricted to a line inside the set, is the zero
     polynomial in one variable;
  3. the coefficient of t^d in g(a + tb) equals g_d(b), where g_d is the top
     homogeneous part (checked on random polynomials);
  4. the evaluation matrix of all monomials of degree <= q-1 over the whole grid
     has full column rank, so nothing nonzero of low degree vanishes everywhere.
  Together these are the proof. The tests also confirm the conclusion directly
  for q = 3 and q = 5 by brute force: no set below the bound holds every
  direction.
- In three dimensions exhaustive search is hopeless, so the repo reports greedy
  upper bounds alongside Dvir's proved lower bound, and labels them as such.

---

## Things deliberately left out

- **Hausdorff measure and dimension, properly defined.** The guide uses box
  counting, which is honest, computable, and gives the same answer for the sets
  it actually computes. Chapter 8 tells the reader that the conjecture is usually
  stated for the Hausdorff version and that it is the stronger claim.
- **Maximal function formulations.** The Kakeya maximal conjecture and its
  relation to the set conjecture are one level of abstraction above this guide.
- **The proof strategy of Wang-Zahl in any detail.** Chapter 12 states the
  theorem and the shape of the main estimate, and points at Tao's exposition.
- **Kakeya over other fields and rings**, and the Assouad/packing dimension
  variants.

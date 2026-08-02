"""The computable core of the multicolor Ramsey story.

Four groups of things live here.

1. **Colorings and the triangle check.** An edge coloring is a symmetric
   integer matrix; `monochromatic_triangles` walks every triple of vertices
   and reports the one-color triangles.  The named colorings the guide draws
   (the pentagon, the sixteen-vertex three-color one) are built here from
   scratch and re-verified in `tests/`.

2. **The two staircases.** The simple upper bound recursion that gives roughly
   factorial growth, and the product construction that multiplies two safe
   colorings into a bigger one but can never make the growth rate per color
   climb.

3. **The 2026 construction's small parts.** The saturated matrix, the two
   fixed answer maps built from it, and the palette parity rule.  For two
   colors the matrix parameters are small enough that everything is found and
   then verified exhaustively, case by case, with no randomness left in the
   claim.

4. **The two-block trap, in miniature.** A five-vertex block plus one outside
   vertex, colored once ignoring the label rule and once obeying it, so the
   tests can show the rule is exactly what removes the last kind of triangle.

Everything returns ordinary Python numbers and lists.  The quantities the
guide quotes are checked in `tests/`, and the ones that are theorems of other
people are quoted, not re-proved; `notes/research-content.md` says which is
which.
"""

from __future__ import annotations

import itertools
import math
import random
from typing import Callable, Sequence

import numpy as np

# --- colorings and the triangle check ---------------------------------------

NO_EDGE = -1


def empty_coloring(n: int) -> np.ndarray:
    """An n-vertex table with every edge still uncolored."""
    c = np.full((n, n), NO_EDGE, dtype=int)
    return c


def color_edge(coloring: np.ndarray, i: int, j: int, color: int) -> None:
    coloring[i, j] = color
    coloring[j, i] = color


def is_complete(coloring: np.ndarray) -> bool:
    """Every pair of distinct vertices carries a color."""
    n = len(coloring)
    return all(coloring[i, j] != NO_EDGE
               for i in range(n) for j in range(i + 1, n))


def monochromatic_triangles(coloring: np.ndarray) -> list[tuple[int, int, int]]:
    """Every triple of vertices whose three edges share one color.

    This is the referee of the whole guide: a coloring is safe exactly when
    this list comes back empty.  It checks all triples, so it is honest and
    slow, which is fine at the sizes the guide draws.
    """
    n = len(coloring)
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            c = coloring[i, j]
            if c == NO_EDGE:
                continue
            for k in range(j + 1, n):
                if coloring[i, k] == c and coloring[j, k] == c:
                    out.append((i, j, k))
    return out


def is_triangle_free(coloring: np.ndarray) -> bool:
    return not monochromatic_triangles(coloring)


def colors_used(coloring: np.ndarray) -> int:
    values = {int(v) for v in coloring.ravel() if v != NO_EDGE}
    return len(values)


def circulant_coloring(n: int, color_of_step: dict[int, int]) -> np.ndarray:
    """Color each edge by how far apart its endpoints sit on a circle.

    `color_of_step[d]` is the color given to every edge whose endpoints are
    `d` steps apart around the circle, for d from 1 to n // 2.  Colorings like
    this treat every vertex identically, which is why the famous small
    record-holders all have this shape.
    """
    c = empty_coloring(n)
    for i in range(n):
        for j in range(i + 1, n):
            d = min((j - i) % n, (i - j) % n)
            color_edge(c, i, j, color_of_step[d])
    return c


def pentagon_coloring() -> np.ndarray:
    """Five vertices, two colors, no one-color triangle.

    The ring edges take one color and the star edges the other.  Each color's
    graph is a five-cycle, and a five-cycle has no triangle at all, let alone
    a one-color one.  This is the largest safe table for two colors: six
    people always force a one-color triangle, which is the 1955 theorem of
    Greenwood and Gleason the guide walks through.
    """
    return circulant_coloring(5, {1: 0, 2: 1})


# --- sixteen vertices, three colors ------------------------------------------

#: multiplication table logic for the sixteen-element field, built on the
#: irreducible polynomial x^4 = x + 1 over the two-element field
_GF16_REDUCE = 0b10011


def gf16_mul(a: int, b: int) -> int:
    """Multiply two of the sixteen field elements (each held as 4 bits)."""
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        if a & 0b10000:
            a ^= _GF16_REDUCE
        b >>= 1
    return out


def gf16_powers(base: int = 2) -> list[int]:
    """The fifteen nonzero elements, listed as successive powers of a generator."""
    powers, x = [], 1
    for _ in range(15):
        powers.append(x)
        x = gf16_mul(x, base)
    return powers


def gf16_cube_class(v: int) -> int:
    """Which of the three cube classes a nonzero element falls into.

    The fifteen nonzero elements are the powers of one generator, and the
    exponent modulo three splits them into three classes of five.  Adding two
    elements of a class never lands back in that class, and that is the whole
    reason the coloring below has no one-color triangle.
    """
    powers = gf16_powers()
    return powers.index(v) % 3


def gf16_coloring() -> np.ndarray:
    """Sixteen vertices, three colors, no one-color triangle.

    Vertices are the sixteen field elements; the edge between two of them is
    colored by the cube class of their difference (which over this field is
    the same as their sum).  Greenwood and Gleason published this in 1955 and
    it is still the record for three colors: seventeen vertices always force
    a one-color triangle.
    """
    c = empty_coloring(16)
    for i in range(16):
        for j in range(i + 1, 16):
            color_edge(c, i, j, gf16_cube_class(i ^ j))
    return c


def class_is_sum_free(cls: int) -> bool:
    """No two members of a cube class add up to a third member of it."""
    members = [v for v in range(1, 16) if gf16_cube_class(v) == cls]
    return all(a ^ b not in members for a in members for b in members if a != b)


# --- the product construction ------------------------------------------------

def product_coloring(outer: np.ndarray, inner: np.ndarray,
                     outer_colors: int) -> np.ndarray:
    """Blow each vertex of `outer` up into a full copy of `inner`.

    Two vertices in different copies take the color of the outer edge between
    their copies.  Two vertices inside one copy take the inner color, shifted
    up so the two color sets stay disjoint.  If neither ingredient had a
    one-color triangle, the product has none either: a triangle either sits
    inside one copy (an inner triangle) or spans copies that form an outer
    triangle.  The tests verify this on the actual products the guide draws
    rather than taking the argument on faith.
    """
    no, ni = len(outer), len(inner)
    n = no * ni
    c = empty_coloring(n)
    for a in range(n):
        for b in range(a + 1, n):
            pa, ua = divmod(a, ni)
            pb, ub = divmod(b, ni)
            if pa == pb:
                color_edge(c, a, b, outer_colors + inner[ua, ub])
            else:
                color_edge(c, a, b, outer[pa, pb])
    return c


def product_tower_sizes(base_size: int, base_colors: int,
                        steps: int) -> list[tuple[int, int]]:
    """(colors, safe vertices) after repeatedly multiplying one coloring.

    Each step multiplies the vertex count by the same factor and adds the
    same number of colors, so the vertices-per-color rate is stuck at
    `base_size ** (1 / base_colors)` forever.  This is the precise sense in
    which no fixed product can answer the growth question.
    """
    out, size, colors = [], 1, 0
    for _ in range(steps):
        size *= base_size
        colors += base_colors
        out.append((colors, size))
    return out


# --- the two staircases -------------------------------------------------------

def upper_staircase(k: int) -> list[int]:
    """Party sizes that force a one-color triangle, color count by color count.

    One color forces at three people.  From there, each extra color multiplies
    the previous figure by about the number of colors: stand at one person,
    split everyone else by the color toward that person, and the biggest group
    avoids its own color inside itself.  The recursion is
    forced(k) = k * (forced(k-1) - 1) + 2, and it grows like a factorial.
    """
    values = [3]
    for colors in range(2, k + 1):
        values.append(colors * (values[-1] - 1) + 2)
    return values


#: the record safe blocks the multiplication recipe can use: colors -> people.
#: 2 and 3 are rebuilt and verified in this repository; 4 is Chung's 1973
#: fifty-person table, quoted.  The famous 3.28-per-color rate is deliberately
#: NOT a block here: it is an asymptotic rate from Schur-type machinery that
#: loses a constant-size slice at each step, and no literal five-color block
#: could reach it, since the staircase caps five colors at 327 people
RECORD_BLOCKS = {1: 2, 2: 5, 3: 16, 4: 50}


def best_product_lower(k: int) -> int:
    """The biggest safe table the multiplication recipe can actually prove.

    Combines the record blocks in every way (a 380-person block costs five
    colors, a 16-person block costs three, and so on) and keeps the best.
    This is the honest floor at every color count, unlike a smooth
    fixed-base curve, which overstates what is proven at small counts.
    """
    best = [1] * (k + 1)
    for i in range(1, k + 1):
        for colors, size in RECORD_BLOCKS.items():
            if colors <= i:
                best[i] = max(best[i], best[i - colors] * size)
    return best[k]


def factorial_record(k: int) -> float:
    """The best proven forcing size, about e minus one sixth times k factorial.

    Quoted from the source chapter, which lists it as the current record for
    four or more colors.  It refines the staircase above by constant factors
    only: the factorial shape is unchanged.
    """
    return (math.e - 1 / 6) * math.factorial(k) + 1


def explicit_new_base(k: int) -> float:
    """The 2026 paper's fully explicit per-color base at k colors.

    The theorem says the safe table size is at least this base raised to the
    k-th power, for every k from 2 up.  The constant six times e to the 38 is
    deliberately not optimized; the content is that the base grows without
    bound, not the day-one size of the constant.
    """
    return k ** (1 / 3) / (6 * math.e ** 38 * math.log(k))


def crossover_estimate() -> float:
    """Roughly where the explicit new base first beats the old fixed base.

    Solves base(k) = 380 ** (1/5) by iteration.  The answer is astronomically
    large, which the article states plainly: at any size a person will ever
    draw, the older constructions give bigger colorings, and the theorem's
    content is the shape of the growth, not a new record at small k.
    """
    old = 380 ** (1 / 5)
    k = 1e20
    for _ in range(200):
        k = (6 * math.e ** 38 * math.log(k) * old) ** 3
    return k


# --- the saturated matrix and the two fixed maps ------------------------------

def saturated_params(H: int) -> tuple[int, int]:
    """The matrix sizes the construction uses at alphabet size H.

    m is the coupon-collector length: how many random draws it takes to see
    all H colors with a little room to spare.  s is chosen so that one union
    bound can pay for every set of m + 1 columns at once.
    """
    m = math.ceil(2 * H * math.log(H))
    return m, m * (m + 1) + 1


def is_saturated(matrix: np.ndarray, H: int, m: int) -> bool:
    """Does every choice of m + 1 columns contain a row showing all H colors?

    Checked exhaustively over all column sets, so it is only run at alphabet
    size two, where there are seventy sets to check.  This is the matrix
    property the whole construction leans on.
    """
    n_cols = matrix.shape[1]
    for cols in itertools.combinations(range(n_cols), m + 1):
        if not any(len(set(int(v) for v in matrix[r, list(cols)])) == H
                   for r in range(matrix.shape[0])):
            return False
    return True


def find_saturated_matrix(H: int = 2, seed: int = 0) -> np.ndarray:
    """Search random matrices until one has the saturated-row property.

    The existence proof says a random matrix works with probability better
    than a coin flip, so the search below ends quickly.  The found matrix is
    then verified exhaustively by `is_saturated`, so nothing about the final
    object depends on chance.
    """
    m, s = saturated_params(H)
    rng = random.Random(seed)
    n_cols = H ** m
    while True:
        matrix = np.array([[rng.randrange(H) for _ in range(n_cols)]
                           for _ in range(s)], dtype=int)
        if is_saturated(matrix, H, m):
            return matrix


def column_index(word: Sequence[int], H: int, m: int) -> int:
    """Read the first m letters of a word as the index of a matrix column."""
    idx = 0
    for d in range(m):
        idx = idx * H + int(word[d])
    return idx


def exceptional_columns(matrix: np.ndarray, y: Sequence[int],
                        H: int, m: int) -> list[int]:
    """The columns that dodge the word y in every single row.

    The saturated-row property caps how many of these there can be: more than
    m of them would hand over m + 1 columns among which some row shows every
    color, and that row would have to hit y somewhere.
    """
    s = matrix.shape[0]
    return [z for z in range(H ** m)
            if all(int(matrix[r, z]) != int(y[r]) for r in range(s))]


def answer_maps(matrix: np.ndarray, H: int,
                m: int) -> tuple[Callable, Callable]:
    """The two fixed maps f and g built once from the saturated matrix.

    g answers for x using only its first m letters: it reads the matrix
    column those letters name.  f answers for y by listing y's few
    exceptional columns and spending one coordinate on each.  Between them,
    any two words x and y agree somewhere: either x's column is ordinary and
    g finds the agreement, or it is one of y's exceptions and f does.
    """
    s = matrix.shape[0]

    def g(x: Sequence[int]) -> list[int]:
        col = column_index(x, H, m)
        return [int(matrix[r, col]) for r in range(s)]

    def f(y: Sequence[int]) -> list[int]:
        exceptions = exceptional_columns(matrix, y, H, m)
        out = []
        for d in range(s):
            if d < len(exceptions):
                digits = []
                z = exceptions[d]
                for _ in range(m):
                    digits.append(z % H)
                    z //= H
                digits.reverse()
                out.append(digits[d] if d < m else 0)
            else:
                out.append(0)
        return out

    return f, g


def cover_holds_everywhere(matrix: np.ndarray, H: int, m: int) -> bool:
    """The meeting guarantee, checked over every possible pair of words.

    For every x and y, some position d has x agreeing with f(y) or y agreeing
    with g(x).  Whether that happens depends on y and on only the first m
    letters of x, so at alphabet size two the check runs over every one of
    the 8 times 8192 genuinely different pairs and is exhaustive.
    """
    s = matrix.shape[0]
    f, g = answer_maps(matrix, H, m)
    for y in itertools.product(range(H), repeat=s):
        fy = f(y)
        exceptions = exceptional_columns(matrix, y, H, m)
        for col in range(H ** m):
            digits = []
            z = col
            for _ in range(m):
                digits.append(z % H)
                z //= H
            digits.reverse()
            x = digits + [0] * (s - m)
            gx = g(x)
            # only agreements that cannot depend on the letters of x past
            # position m count, so the check covers every word x whose first
            # m letters name this column, whatever its remaining letters are
            hit = (any(y[d] == gx[d] for d in range(s))
                   or any(x[d] == fy[d] for d in range(m)))
            if not hit:
                return False
            # the proof also says which side answers: g for ordinary columns
            if col not in exceptions:
                assert any(y[d] == gx[d] for d in range(s))
    return True


# --- palettes and the parity rule ---------------------------------------------

def three_block_patterns() -> list[tuple[int, int, int]]:
    """Every way one color can sit inside or outside three palettes.

    Each pattern is (in P, in Q, in R) with 1 for in.  A triangle touching
    three blocks would need the color to be in exactly one of each pair,
    which `pattern_allows_triangle` shows never happens: the tests run all
    eight cases, so the parity argument is verified by exhaustion rather than
    told as a story.
    """
    return list(itertools.product((0, 1), repeat=3))


def pattern_allows_triangle(p: int, q: int, r: int) -> bool:
    """Could a color with this membership pattern color all three sides?

    A cross edge may only use a color held by exactly one of its two blocks,
    so all three of the pairwise mismatches would have to hold at once.
    """
    return (p != q) and (q != r) and (p != r)


def stage_colors(H: int) -> int:
    """How many colors the construction has used once all H stages are built."""
    m, s = saturated_params(H)
    return H * s * math.ceil(math.log(H))


# --- a triangle-free net that needs many teams -----------------------------------

def groetzsch_graph() -> np.ndarray:
    """Eleven people, no triangle anywhere, and three teams are not enough.

    The classical Mycielski construction applied to the five-ring: an outer
    ring of five, an inner five each connected to the outer neighbours of its
    twin, and one hub connected to all five inner people.  It contains no
    triangle, yet its people cannot be split into three teams with no
    connection inside any team; four teams are needed.  Taller versions of
    the same construction push that number as high as you like, which is
    what sank the hope that triangle-free nets are simple.
    """
    g = empty_coloring(11)
    for i in range(5):
        color_edge(g, i, (i + 1) % 5, 0)              # the outer ring
        color_edge(g, 5 + i, (i + 1) % 5, 0)          # twin to ring neighbours
        color_edge(g, 5 + i, (i - 1) % 5, 0)
        color_edge(g, 10, 5 + i, 0)                   # the hub
    return g


def proper_team_split(graph: np.ndarray, teams: int) -> tuple | None:
    """Some split of the people into that many connection-free teams, or None.

    Brute force over every assignment, so it is only run on small nets.  A
    split is proper when no connection stays inside one team.
    """
    n = len(graph)
    for assignment in itertools.product(range(teams), repeat=n):
        if all(assignment[i] != assignment[j]
               for i in range(n) for j in range(i + 1, n)
               if graph[i, j] != NO_EDGE):
            return assignment
    return None


# --- the failed permutation shortcut --------------------------------------------

def first_difference_coloring(n: int) -> tuple[list, np.ndarray]:
    """Color pairs of orderings by the first position where they disagree.

    The tempting shortcut: the orderings of n items number n factorial, and
    the first disagreement position gives only n - 1 colors, so this would be
    factorial growth from linearly many colors.  It fails, and the tests
    exhibit the failure: three orderings can pairwise first-disagree at the
    same position, making a one-color triangle.
    """
    perms = list(itertools.permutations(range(n)))
    size = len(perms)
    c = empty_coloring(size)
    for i in range(size):
        for j in range(i + 1, size):
            d = next(p for p in range(n) if perms[i][p] != perms[j][p])
            color_edge(c, i, j, d)
    return perms, c


# --- the two-block trap, in miniature -------------------------------------------

#: a proper labeling of the pentagon's ring color: adjacent ring vertices
#: never share a label, using three labels
RING_LABELS = (0, 1, 0, 1, 2)


# --- the five-symbol channel, for the payoff chapter -----------------------------

def pentagon_confusable(a: int, b: int) -> bool:
    """Whether the noisy five-symbol channel can turn one symbol into the other.

    Shannon's classic example: five symbols on a ring, and the noise can slide
    any symbol into either neighbour.  A symbol is always confusable with
    itself.
    """
    return a == b or (a - b) % 5 in (1, 4)


def words_distinguishable(u: Sequence[int], v: Sequence[int]) -> bool:
    """Two words survive the noise if some position cannot be confused."""
    return any(not pentagon_confusable(a, b) for a, b in zip(u, v))


#: five two-letter words over the five-symbol channel, pairwise safe: the
#: reason capacity is counted per letter rather than per alphabet
C5_CODEBOOK = ((0, 0), (1, 2), (2, 4), (3, 1), (4, 3))


def trap_coloring(obey_rule: bool) -> np.ndarray:
    """A pentagon block plus one outside vertex, with and without the rule.

    The block holds the two-color pentagon; the outside vertex is vertex 5.
    Its edges into the block all use the ring color (color 0), which the
    block actively uses.  Ignoring the rule, two of those edges land on ring
    neighbours, and together with the ring edge between them they close a
    one-color triangle.  Obeying the rule, every color-0 edge from outside
    lands in one label class of `RING_LABELS`, and label classes never carry
    an internal ring edge, so no triangle can close.  Edges the rule refuses
    fall back to a fresh color the block does not use internally (a missing
    color), which cannot close a triangle either.
    """
    c = empty_coloring(6)
    c[:5, :5] = pentagon_coloring()
    for u in range(5):
        if obey_rule:
            color_edge(c, 5, u, 0 if RING_LABELS[u] == 0 else 2)
        else:
            color_edge(c, 5, u, 0 if u in (0, 1) else 2)
    return c

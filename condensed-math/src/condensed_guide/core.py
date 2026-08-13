"""The computable core behind the condensed mathematics guide.

Condensed mathematics is a foundational subject: most of its statements are
about whole categories, and no program can check those.  What a program *can*
check is the finite machinery underneath them, and that is what lives here.

Everything in this file is exact integer or float arithmetic on finite
objects:

* a profinite set is stored as an honest inverse system of finite sets, so
  the sets, the transition maps and the inverse limit are all real data;
* a measure is a compatible family of integer weights on that system, so the
  claim that integrating against it does not depend on the level you read is
  a claim the tests verify;
* the homology of a shape is computed from a chain complex by Smith normal
  form, over the integers, torsion included;
* the norms, the ranks and the series truncations are computed, not quoted.

Where a statement of the lectures is genuinely infinitary, this module
computes its finite shadow and `notes/research-content.md` says so.  Nothing
here is a transcription of a result dressed up as a calculation, with the one
declared exception of `SOLID_TENSOR_TABLE`, which is Example 6.4 of the
lectures written down so the article and the tests quote one copy of it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import combinations

import numpy as np

# ---------------------------------------------------------------------------
# 1.  Profinite sets, as inverse systems of finite sets
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Profinite:
    """A profinite set, stored as the finite pictures it is a limit of.

    `levels[i]` is the finite set S_i, given as a tuple of hashable labels.
    `parents[i]` maps each label of S_{i+1} to its label in S_i, i.e. it is
    the transition map S_{i+1} -> S_i.  Every transition map here is
    surjective, which is the only case the guide needs.

    The profinite set itself is the inverse limit: a point is a thread that
    picks one label at every level, each mapping to the one before.  For a
    finite depth the threads are exactly the labels of the deepest level,
    which is why the pictures in the guide are always drawn at a depth.
    """

    name: str
    levels: tuple[tuple, ...]
    parents: tuple[dict, ...]

    @property
    def depth(self) -> int:
        return len(self.levels) - 1

    def size(self, i: int) -> int:
        return len(self.levels[i])

    def sizes(self) -> list[int]:
        return [len(s) for s in self.levels]

    def project(self, label, frm: int, to: int):
        """Follow a label at level `frm` down to its label at level `to`."""
        if to > frm:
            raise ValueError("can only project towards coarser levels")
        for i in range(frm - 1, to - 1, -1):
            label = self.parents[i][label]
        return label

    def fibre(self, label, at: int, over: int) -> list:
        """Every label at level `at` sitting above `label` at level `over`."""
        return [x for x in self.levels[at]
                if self.project(x, at, over) == label]

    def check(self) -> None:
        """The stored system really is an inverse system of finite sets."""
        assert self.levels[0] and self.depth >= 0
        for i, par in enumerate(self.parents):
            assert set(par) == set(self.levels[i + 1]), "parent map is partial"
            assert set(par.values()) <= set(self.levels[i]), "parent escapes"
            assert set(par.values()) == set(self.levels[i]), "not surjective"


def cantor(depth: int) -> Profinite:
    """The Cantor set: every level splits every box in two.

    S_i is the set of binary strings of length i, so it has 2**i elements,
    and the transition map drops the last letter.  This is the profinite set
    the guide draws as a branching tree.
    """
    levels, parents = [("",)], []
    for i in range(depth):
        nxt = tuple(s + b for s in levels[i] for b in "01")
        parents.append({s: s[:-1] for s in nxt})
        levels.append(nxt)
    return Profinite("cantor", tuple(levels), tuple(parents))


def convergent_sequence(depth: int) -> Profinite:
    """The probe that is one convergent sequence: the points 1, 1/2, 1/3, ...
    together with their limit 0.

    Level i is {0, 1, ..., i-1} together with a label "oo" standing for
    everything not yet separated.  The transition map keeps the small labels
    and folds the newest one into "oo".  This is the profinite set written
    N u {oo} in the lectures, and it is the probe that detects convergence.
    """
    levels, parents = [("oo",)], []
    for i in range(depth):
        nxt = tuple(list(range(i + 1)) + ["oo"])
        par = {k: (k if k != i else "oo") for k in range(i + 1)}
        par["oo"] = "oo"
        parents.append(par)
        levels.append(nxt)
    return Profinite("convergent sequence", tuple(levels), tuple(parents))


def p_adic(p: int, depth: int) -> Profinite:
    """The p-adic integers: level i is the residues modulo p**i."""
    levels, parents = [(0,)], []
    for i in range(depth):
        nxt = tuple(range(p ** (i + 1)))
        parents.append({k: k % (p ** i) for k in nxt})
        levels.append(nxt)
    return Profinite(f"{p}-adic integers", tuple(levels), tuple(parents))


def finite_set(n: int) -> Profinite:
    """A plain finite set, which is a profinite set with nothing to refine."""
    return Profinite(f"{n} points", (tuple(range(n)),), ())


# ---------------------------------------------------------------------------
# 2.  Continuous functions to Z, and measures
# ---------------------------------------------------------------------------


def locally_constant_rank(S: Profinite, level: int) -> int:
    """Rank of the continuous maps S -> Z that are decided by `level`.

    A continuous map from a profinite set to the integers is constant on
    small enough boxes, so it is a function on some finite level, and the
    functions on a finite set of size n form a free group of rank n.  The
    union over all levels is the group C(S, Z) of the lectures.
    """
    return S.size(level)


@dataclass
class Measure:
    """A weight for every box, agreeing whenever boxes merge.

    This is one element of the inverse limit lim Z[S_i] that the lectures
    write Z[S] with a small square, the free solid abelian group on S.  The
    only rule is the one enforced by `check`: the weight of a box equals the
    total weight of the boxes inside it.
    """

    S: Profinite
    weights: list[dict]           # weights[i][label] for each level i

    def check(self) -> None:
        for i in range(len(self.weights) - 1):
            for label in self.S.levels[i]:
                inner = sum(self.weights[i + 1][x]
                            for x in self.S.levels[i + 1]
                            if self.S.parents[i][x] == label)
                assert self.weights[i][label] == inner, (
                    f"level {i} label {label!r}: {self.weights[i][label]} "
                    f"is not the total {inner} of the boxes inside it")

    def total(self) -> int:
        return sum(self.weights[0].values())

    def integrate(self, f: dict, level: int) -> int:
        """Integrate a locally constant function read at `level`.

        `f` gives an integer to every box at that level.  The answer must not
        depend on which level the function is read at, and the tests check
        exactly that on refinements of the same function.
        """
        return sum(f[label] * self.weights[level][label]
                   for label in self.S.levels[level])


def dirac(S: Profinite, point) -> Measure:
    """All the weight on one thread: the measure a single point carries."""
    weights = []
    for i in range(S.depth + 1):
        here = S.project(point, S.depth, i)
        weights.append({label: (1 if label == here else 0)
                        for label in S.levels[i]})
    return Measure(S, weights)


def refine(S: Profinite, f: dict, frm: int, to: int) -> dict:
    """Read the same function at a finer level: pull it back along the map."""
    return {x: f[S.project(x, to, frm)] for x in S.levels[to]}


def measure_from_leaves(S: Profinite, leaf_weights: dict) -> Measure:
    """Build a measure by choosing the finest weights and adding upward."""
    weights = [dict(leaf_weights)]
    for i in range(S.depth - 1, -1, -1):
        coarse = {label: 0 for label in S.levels[i]}
        for x in S.levels[i + 1]:
            coarse[S.parents[i][x]] += weights[0][x]
        weights.insert(0, coarse)
    return Measure(S, weights)


def counting_measure(S: Profinite) -> Measure:
    """Weight one on every box of the finest level drawn."""
    return measure_from_leaves(S, {x: 1 for x in S.levels[S.depth]})


# ---------------------------------------------------------------------------
# 3.  Nobeling's basis: continuous integer functions are a free group
# ---------------------------------------------------------------------------


def nobeling_basis(points: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    """Bergman's basis of the integer functions on a finite set of 0/1 points.

    Theorem 5.4 of the lectures says C(S, Z) is a free abelian group for every
    profinite S, by an argument of Bergman: order the products of coordinate
    functions, and keep every product that is not already a combination of
    smaller ones.  This runs that construction on a finite level, where the
    answer can be checked against the rank the group is known to have.

    A point is a tuple of 0s and 1s.  A basis element is returned as the tuple
    of coordinates whose product it is, so `()` is the constant function one.
    """
    if not points:
        return []
    width = len(points[0])
    kept: list[tuple[int, ...]] = []
    rows: list[list[int]] = []            # the kept functions, as value lists
    # the lectures order the products lexicographically by their largest
    # coordinate first; over a finite level, taking the subsets in order of
    # size and then lexicographically is the same order restricted
    for size in range(width + 1):
        for subset in combinations(range(width), size):
            vals = [int(all(pt[c] == 1 for c in subset)) for pt in points]
            if _rank_over_q(rows + [vals]) > len(rows):
                kept.append(subset)
                rows.append(vals)
    return kept


def _rank_over_q(rows: list[list[int]]) -> int:
    """Rank of an integer matrix, computed in exact rational arithmetic."""
    if not rows:
        return 0
    m = [[Fraction(v) for v in row] for row in rows]
    rank, ncols = 0, len(m[0])
    for col in range(ncols):
        pivot = next((r for r in range(rank, len(m)) if m[r][col] != 0), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        head = m[rank][col]
        m[rank] = [v / head for v in m[rank]]
        for r in range(len(m)):
            if r != rank and m[r][col] != 0:
                factor = m[r][col]
                m[r] = [a - factor * b for a, b in zip(m[r], m[rank])]
        rank += 1
        if rank == len(m):
            break
    return rank


def cantor_points(depth: int) -> list[tuple[int, ...]]:
    """Every branch of the Cantor tree at a given depth, as 0/1 coordinates."""
    return [tuple(int(c) for c in f"{k:0{depth}b}") for k in range(2 ** depth)]


# ---------------------------------------------------------------------------
# 4.  Products, sums, and the shape of a solid group
# ---------------------------------------------------------------------------


def product_rank(index_sizes: list[int]) -> int:
    """The rank of a finite product of copies of Z."""
    return sum(index_sizes)


def tensor_index(I: list, J: list) -> list[tuple]:
    """Proposition 6.3: solid tensor multiplies the index sets of products.

    A product of copies of Z indexed by I, completed-tensored with one indexed
    by J, is the product indexed by I x J.  Both sides are finite here, so the
    statement becomes a statement about lists, and the tests check it against
    the power series picture: the monomials of two series in separate
    variables pair off with the monomials of a series in both.
    """
    return [(i, j) for i in I for j in J]


def power_series_monomials(order: int) -> list[int]:
    """The exponents of a one-variable formal power series, truncated."""
    return list(range(order))


def double_series_monomials(order: int) -> list[tuple[int, int]]:
    """The exponents of a two-variable formal power series, truncated."""
    return [(i, j) for i in range(order) for j in range(order)]


#: Example 6.4 of the lectures, transcribed.  This is the one table in this
#: module that is quoted rather than computed; the tests check that it is
#: self-consistent and symmetric, not that it is true.
SOLID_TENSOR_TABLE: dict[frozenset, str] = {
    frozenset({"Z_p", "R"}): "0",
    frozenset({"Z_p", "Z_l"}): "0",
    frozenset({"Z_p"}): "Z_p",
    frozenset({"Z_p", "Z[[T]]"}): "Z_p[[T]]",
    frozenset({"Z[[U]]", "Z[[T]]"}): "Z[[T,U]]",
}

#: What each object contributes, in the reading the lectures suggest: the
#: completed tensor product asks both sides which adic direction they carry
#: and then keeps all of them.  `None` marks the real numbers, which carry no
#: adic direction at all and whose solidification is zero.
ADIC_DIRECTIONS: dict[str, tuple] = {
    "Z": (),
    "Z_p": ("p",),
    "Z_l": ("l",),
    "Z[[T]]": ("T",),
    "Z[[U]]": ("U",),
    "Z_p[[T]]": ("p", "T"),
    "Z[[T,U]]": ("T", "U"),
    "R": None,
}


def name_directions(directions) -> str:
    """Write down the object carrying a given set of nestings.

    A prime direction names the base ring, and the remaining directions are
    formal variables, so the object is that base ring's formal power series
    in those variables.  This is only a naming convention, and it is the one
    the lectures' own examples use.
    """
    primes = sorted(d for d in directions if d in ("p", "l"))
    variables = sorted(d for d in directions if d not in ("p", "l"))
    base = f"Z_{primes[0]}" if primes else "Z"
    if not variables:
        return base
    return f"{base}[[{','.join(variables)}]]"


def solid_tensor(a: str, b: str) -> str:
    """The completed tensor product of two of the guide's sample objects.

    The rule read off Example 6.4: the real numbers annihilate everything,
    because their solidification is zero; two different residue
    characteristics annihilate each other; otherwise the adic directions of
    the two sides are collected together.

    Only the five combinations in `SOLID_TENSOR_TABLE` are stated in the
    lectures.  The others are the same rule applied to relabelled variables,
    and `quoted_tensor` says which is which so the figures can mark them.
    """
    da, db = ADIC_DIRECTIONS[a], ADIC_DIRECTIONS[b]
    if da is None or db is None:
        return "0"
    directions = set(da) | set(db)
    if len({d for d in directions if d in ("p", "l")}) > 1:
        return "0"
    return name_directions(directions)


def quoted_tensor(a: str, b: str) -> bool:
    """Is this entry one the lectures state outright, or the rule extended?"""
    return frozenset({a, b}) in SOLID_TENSOR_TABLE


# ---------------------------------------------------------------------------
# 5.  Homology, by Smith normal form over the integers
# ---------------------------------------------------------------------------


def smith_normal_form(matrix: list[list[int]]) -> list[int]:
    """The nonzero invariant factors of an integer matrix, each dividing the
    next.

    Only the diagonal is returned, which is all the homology needs: its
    length is the rank of the matrix, and its entries carry the torsion.
    Diagonalising is not quite enough on its own, because a diagonal like
    2, 3 describes the same group as 1, 6 without being in the normal form,
    so the chain is repaired at the end.
    """
    m = [row[:] for row in matrix]
    if not m or not m[0]:
        return []
    rows, cols, divisors, t = len(m), len(m[0]), [], 0
    while t < rows and t < cols:
        pivot = None
        best = None
        for i in range(t, rows):
            for j in range(t, cols):
                if m[i][j] and (best is None or abs(m[i][j]) < best):
                    best, pivot = abs(m[i][j]), (i, j)
        if pivot is None:
            break
        pi, pj = pivot
        m[t], m[pi] = m[pi], m[t]
        for row in m:
            row[t], row[pj] = row[pj], row[t]
        while True:
            for i in range(t + 1, rows):
                if m[i][t]:
                    q = m[i][t] // m[t][t]
                    m[i] = [a - q * b for a, b in zip(m[i], m[t])]
            if any(m[i][t] for i in range(t + 1, rows)):
                nz = next(i for i in range(t + 1, rows) if m[i][t])
                m[t], m[nz] = m[nz], m[t]
                continue
            for j in range(t + 1, cols):
                if m[t][j]:
                    q = m[t][j] // m[t][t]
                    for row in m:
                        row[j] -= q * row[t]
            if any(m[t][j] for j in range(t + 1, cols)):
                nz = next(j for j in range(t + 1, cols) if m[t][j])
                for row in m:
                    row[t], row[nz] = row[nz], row[t]
                continue
            break
        divisors.append(abs(m[t][t]))
        t += 1
    return _divisibility_chain(divisors)


def _divisibility_chain(divisors: list[int]) -> list[int]:
    """Make each entry divide the next, without changing the group described.

    Replacing a neighbouring pair by their greatest common divisor and their
    least common multiple leaves the product alone and the group alone, and
    repeating it sorts the list into the chain the normal form asks for.
    """
    d = sorted(divisors)
    changed = True
    while changed:
        changed = False
        for i in range(len(d) - 1):
            a, b = d[i], d[i + 1]
            if b % a:
                g = math.gcd(a, b)
                d[i], d[i + 1] = g, a // g * b
                changed = True
    return d


@dataclass
class Complex:
    """A finite cell complex, as the boundary matrices between its cells.

    `boundary[k]` is the matrix of the boundary map from k-cells to
    (k-1)-cells, with one column per k-cell and one row per (k-1)-cell.
    """

    name: str
    cell_counts: list[int]
    boundary: dict[int, list[list[int]]] = field(default_factory=dict)

    def homology(self) -> list[tuple[int, list[int]]]:
        """Betti number and torsion, degree by degree.

        Returns [(free rank, [torsion orders]), ...] with one entry per
        degree, computed from the boundary matrices by Smith normal form.
        """
        out = []
        for k in range(len(self.cell_counts)):
            n = self.cell_counts[k]
            d_k = self.boundary.get(k)
            d_next = self.boundary.get(k + 1)
            rank_k = len(smith_normal_form(d_k)) if d_k else 0
            divisors = smith_normal_form(d_next) if d_next else []
            rank_next = len(divisors)
            free = n - rank_k - rank_next
            torsion = [d for d in divisors if d > 1]
            out.append((free, torsion))
        return out


def circle() -> Complex:
    """One vertex, one edge: the boundary of the edge is zero."""
    return Complex("circle", [1, 1], {1: [[0]]})


def figure_eight() -> Complex:
    return Complex("figure eight", [1, 2], {1: [[0, 0]]})


def sphere() -> Complex:
    """One vertex, no edge, one face."""
    return Complex("sphere", [1, 0, 1], {2: []})


def torus() -> Complex:
    """One vertex, two edges, one face glued along a b a-inverse b-inverse."""
    return Complex("torus", [1, 2, 1], {1: [[0], [0]], 2: [[0], [0]]})


def klein_bottle() -> Complex:
    """One vertex, two edges, one face glued along a b a b-inverse.

    The second edge is traversed twice the same way, so the boundary of the
    face is twice that edge, which is where the two-torsion comes from.
    """
    return Complex("klein bottle", [1, 2, 1], {1: [[0], [0]], 2: [[0], [2]]})


SHAPES = {"circle": circle, "figure eight": figure_eight, "sphere": sphere,
          "torus": torus, "klein bottle": klein_bottle}


def exterior_ranks(n: int) -> list[int]:
    """Proposition 3.1: the cohomology of a product of n circles.

    The lectures show the cohomology of a product of circles is the exterior
    algebra on one generator per circle, so degree i has rank n choose i.
    """
    return [math.comb(n, i) for i in range(n + 1)]


# ---------------------------------------------------------------------------
# 6.  Convergence that needs a rule: the p-adic size
# ---------------------------------------------------------------------------


def p_adic_valuation(n: int, p: int) -> int:
    if n == 0:
        return math.inf
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def p_adic_abs(x: Fraction, p: int) -> float:
    """How small a rational number is, p-adically: p to the minus valuation."""
    if x == 0:
        return 0.0
    v = p_adic_valuation(x.numerator, p) - p_adic_valuation(x.denominator, p)
    return float(p) ** (-v)


def geometric_partial_sums(p: int, terms: int) -> list[Fraction]:
    """The partial sums of 1 + p + p^2 + ..., which run away in ordinary size."""
    return [Fraction(sum(p ** k for k in range(n + 1))) for n in range(terms)]


def geometric_limit(p: int) -> Fraction:
    """What that series adds up to p-adically: one over one minus p."""
    return Fraction(1, 1 - p)


# ---------------------------------------------------------------------------
# 7.  The measure sizes of Lecture VII: why the exponent must not pass one
# ---------------------------------------------------------------------------


def lp_size(values, p: float) -> float:
    """The size the lectures measure a real-valued measure by."""
    return float(sum(abs(v) ** p for v in values) ** (1.0 / p))


def merge(values: list[float], groups: list[list[int]]) -> list[float]:
    """Push a measure to a coarser level: boxes merge, weights add."""
    return [float(sum(values[i] for i in g)) for g in groups]


def merge_ratio(values: list[float], groups: list[list[int]], p: float) -> float:
    """How the size changes when boxes merge.

    A measure on a profinite set is a compatible family, so a measure of size
    at most r at a fine level must still have size at most r once boxes are
    merged.  That asks the size never to grow under merging, and the ratio
    computed here is at most one exactly when the exponent is at most one.
    """
    before = lp_size(values, p)
    after = lp_size(merge(values, groups), p)
    return after / before if before else 0.0


def worst_merge_ratio(boxes: int, p: float) -> float:
    """Merging `boxes` equal boxes into one, in closed form.

    Each box holds weight one, so the size before merging is the box count
    raised to the reciprocal of the exponent, and after merging it is the box
    count itself.  The ratio is therefore the box count raised to one minus
    the reciprocal of the exponent, which is at most one exactly when the
    exponent is at most one.  This is the whole reason Example 7.10 of the
    lectures cannot let the exponent pass one.

    Two different statements are worth keeping apart, and the tests check
    both.  At or below exponent one, merging never increases the size, for
    every choice of weights, because raising to a power at most one is
    subadditive.  Above exponent one it can increase, and equal weights is
    the case where it increases most.
    """
    return float(boxes) ** (1.0 - 1.0 / p)


def lp_ball(p: float, samples: int = 721) -> np.ndarray:
    """The unit ball of the size above, in two coordinates, as a closed curve."""
    theta = np.linspace(0, 2 * np.pi, samples)
    c, s = np.cos(theta), np.sin(theta)
    scale = (np.abs(c) ** p + np.abs(s) ** p) ** (1.0 / p)
    return np.stack([c / scale, s / scale], axis=1)


def is_convex(p: float, samples: int = 240) -> bool:
    """Does the unit ball hold the straight line between any two of its points?"""
    pts = lp_ball(p, samples)
    rng = np.random.default_rng(0)
    for _ in range(400):
        a, b = pts[rng.integers(0, samples, 2)]
        mid = (a + b) / 2
        if lp_size(mid, p) > 1 + 1e-9:
            return False
    return True


# ---------------------------------------------------------------------------
# 8.  Functions near the edge: Laurent tails on the line and on the cross
# ---------------------------------------------------------------------------


def polynomial_monomials(top: int) -> list[int]:
    """The exponents of the polynomials in one variable, up to a degree."""
    return list(range(top + 1))


def laurent_tail_monomials(top: int, bottom: int) -> list[int]:
    """The exponents a series near the edge is allowed, from `top` downward."""
    return list(range(top, bottom - 1, -1))


def line_edge_quotient_rank(top: int, tails: int) -> int:
    """Functions near the edge of the line, modulo functions everywhere.

    Truncate: allow powers of the coordinate from `top` down to minus
    `tails`.  The functions near the edge then span `top + tails + 1`
    monomials, and the polynomials among them span `top + 1`.  What survives
    is exactly the strictly negative powers, so the count is `tails`, and it
    does not depend on how far up the truncation reaches.
    """
    near_edge = top + tails + 1
    everywhere = top + 1
    return near_edge - everywhere


def cross_edge_quotient_rank(top: int, tails: int) -> int:
    """The same count for the coordinate cross, two lines glued at a point.

    Each branch carries its own edge, so functions near the edge of the cross
    are a pair of expansions, one per branch.  The functions on the whole
    cross are a pair of polynomials that must agree at the crossing point,
    since the crossing point lies on both branches and a function has one
    value there.  That single shared constant is the only thing tying the two
    branches together.

    Counting: two branches of `top + tails + 1` monomials each, minus the
    polynomials, which are two lots of `top + 1` sharing one constant.  What
    is left is the two branches' tails plus one extra piece, and that extra
    piece is the arithmetic trace of the crossing.  Remark 8.5 of the
    lectures computes the same object, untruncated, for the cross.
    """
    near_edge = 2 * (top + tails + 1)
    everywhere = 2 * (top + 1) - 1
    return near_edge - everywhere


# ---------------------------------------------------------------------------
# 9.  Winding: the invariant the circle's first cohomology counts
# ---------------------------------------------------------------------------


def winding_number(angles: np.ndarray) -> int:
    """How many whole turns a path around the circle makes."""
    steps = np.diff(np.unwrap(angles))
    return int(round(float(np.sum(steps)) / (2 * np.pi)))

"""Kakeya on a grid: lines, Kakeya sets, and Dvir's polynomial method.

Replace the plane by the finite grid F_q^n, where F_q is arithmetic modulo a
prime q.  A *line* is the q points a + t*b as t runs over the field, and a
*Kakeya set* is a set of grid points holding a whole line in every direction.
The finite-field Kakeya conjecture, posed by Wolff in 1999, says such a set
must have at least c_n * q^n points.  Dvir proved it in 2008 in about half a
page, with the polynomial method.

Everything here is exact integer arithmetic modulo q, so this module does not
illustrate Dvir's proof: it *runs* it.  See tests/test_finite.py, which checks
each link of the argument, and `dvir_report` for the whole chain at once.

Only prime q is supported (fields of prime-power order need arithmetic this
module deliberately does not carry).
"""

from __future__ import annotations

import itertools
from math import comb
from typing import Iterable, Sequence

Point = tuple[int, ...]
Poly = dict[tuple[int, ...], int]      # exponent tuple -> coefficient mod q


def is_prime(q: int) -> bool:
    return q > 1 and all(q % d for d in range(2, int(q ** 0.5) + 1))


def _check(q: int) -> None:
    if not is_prime(q):
        raise ValueError(f"q must be prime here, got {q}")


# ---------------------------------------------------------------------------
# The grid, its lines, and its directions
# ---------------------------------------------------------------------------

def grid(q: int, n: int) -> list[Point]:
    """Every point of F_q^n."""
    return list(itertools.product(range(q), repeat=n))


def directions(q: int, n: int) -> list[Point]:
    """One representative per direction: first nonzero coordinate scaled to 1.

    b and 2b point along the same line, so directions are counted projectively:
    there are (q^n - 1)/(q - 1) of them, which is q + 1 in the plane.
    """
    out = []
    for b in itertools.product(range(q), repeat=n):
        first = next((c for c in b if c), None)
        if first == 1:
            out.append(b)
    return out


def line(a: Point, b: Point, q: int) -> frozenset[Point]:
    """The q points a + t*b, t in F_q."""
    return frozenset(tuple((ai + t * bi) % q for ai, bi in zip(a, b))
                     for t in range(q))


def lines_in_direction(b: Point, q: int, n: int) -> list[frozenset[Point]]:
    """The q^(n-1) parallel lines pointing along b."""
    seen, out = set(), []
    for a in grid(q, n):
        L = line(a, b, q)
        if L not in seen:
            seen.add(L)
            out.append(L)
    return out


def is_kakeya(K: Iterable[Point], q: int, n: int) -> bool:
    """True if K holds a full line in every direction."""
    K = set(K)
    for b in directions(q, n):
        if not any(line(a, b, q) <= K for a in K):
            return False
    return True


def missing_directions(K: Iterable[Point], q: int, n: int) -> list[Point]:
    """The directions in which K holds no line (empty when K is Kakeya)."""
    K = set(K)
    return [b for b in directions(q, n)
            if not any(line(a, b, q) <= K for a in K)]


# ---------------------------------------------------------------------------
# How small can a Kakeya set be?
# ---------------------------------------------------------------------------

def dvir_bound(q: int, n: int) -> int:
    """Dvir's lower bound: every Kakeya set in F_q^n has at least this many
    points.  It is the number of monomials of degree at most q-1 in n
    variables, C(q + n - 1, n)."""
    return comb(q + n - 1, n)


def tangent_line_kakeya(q: int) -> set[Point]:
    """The classical small Kakeya set of the plane: a parabola's tangent lines.

    For each slope m the line y = m*x - m^2/4 touches the parabola y = x^2, and
    one vertical line finishes the job.  For odd q this hits exactly
    q(q+1)/2 + (q-1)/2 points, which Blokhuis and Mazzocca proved is the
    smallest possible.
    """
    _check(q)
    inv4 = pow(4, q - 2, q) if q > 2 else 1
    K: set[Point] = set()
    for m in range(q):
        for x in range(q):
            K.add((x, (m * x - m * m * inv4) % q))
    K |= {(0, y) for y in range(q)}          # the vertical direction
    return K


def min_kakeya_size(q: int, n: int = 2, return_set: bool = False):
    """The smallest Kakeya set in F_q^n, found by exhaustive search.

    A smallest Kakeya set is a union of one line per direction, so the search
    runs over those choices, ordering directions and pruning with the fact that
    a fresh line meets each line already chosen in at most one point (so it
    must bring in at least q - (lines so far) new points).
    """
    _check(q)
    dirs = directions(q, n)
    pts = grid(q, n)
    index = {p: i for i, p in enumerate(pts)}
    choices = [[_mask(L, index) for L in lines_in_direction(b, q, n)]
               for b in dirs]
    # cheapest-looking directions first: fewer distinct lines prunes sooner
    choices.sort(key=len)
    d = len(choices)

    # tail[i] = fewest new points the remaining directions i..d-1 can add
    tail = [0] * (d + 1)
    for i in range(d - 1, -1, -1):
        tail[i] = tail[i + 1] + max(0, q - i)

    best = [None, 10 ** 9]       # best mask, best size

    def walk(i: int, mask: int, size: int) -> None:
        if size + tail[i] >= best[1]:
            return
        if i == d:
            best[0], best[1] = mask, size
            return
        nxt = sorted(((mask | m).bit_count(), m) for m in choices[i])
        for new_size, m in nxt:
            walk(i + 1, mask | m, new_size)

    walk(0, 0, 0)
    size = best[1]
    if not return_set:
        return size
    return size, {pts[i] for i in range(len(pts)) if best[0] >> i & 1}


def _mask(points: Iterable[Point], index: dict[Point, int]) -> int:
    m = 0
    for p in points:
        m |= 1 << index[p]
    return m


def greedy_kakeya_set(q: int, n: int) -> set[Point]:
    """A small Kakeya set for dimensions where exhaustive search is hopeless.

    Sweeps the directions and always takes the line that adds fewest new
    points.  Greedy, so it proves nothing except that Kakeya sets this small
    exist; the proved floor is `dvir_bound`.
    """
    _check(q)
    K: set[Point] = set()
    for b in directions(q, n):
        best = min(lines_in_direction(b, q, n), key=lambda L: len(L - K))
        K |= best
    return K


def greedy_kakeya_size(q: int, n: int) -> int:
    """How big that greedy set is."""
    return len(greedy_kakeya_set(q, n))


# ---------------------------------------------------------------------------
# Polynomials over F_q, in n variables
# ---------------------------------------------------------------------------

def monomials(n: int, d: int) -> list[tuple[int, ...]]:
    """Every exponent tuple of total degree at most d, in n variables."""
    if n == 0:
        return [()]
    out = []
    for e in range(d + 1):
        for rest in monomials(n - 1, d - e):
            out.append((e,) + rest)
    return out


def poly_eval(g: Poly, p: Point, q: int) -> int:
    total = 0
    for exps, c in g.items():
        if c % q == 0:
            continue
        term = c
        for xi, e in zip(p, exps):
            term = term * pow(xi, e, q) % q
        total = (total + term) % q
    return total % q


def poly_degree(g: Poly) -> int:
    """Total degree; -1 for the zero polynomial."""
    live = [sum(e) for e, c in g.items() if c]
    return max(live) if live else -1


def homogeneous_part(g: Poly, d: int) -> Poly:
    """The degree-d slice of g (its top part when d is g's degree)."""
    return {e: c for e, c in g.items() if sum(e) == d and c}


def top_part(g: Poly) -> Poly:
    """The highest-degree homogeneous piece of g."""
    return homogeneous_part(g, poly_degree(g))


def vanishing_polynomial(S: Sequence[Point], q: int, n: int,
                         d: int) -> Poly | None:
    """A nonzero polynomial of degree <= d vanishing on every point of S.

    This is Dvir's first move, and it is pure linear algebra: asking a
    polynomial to vanish at a point is one linear equation on its
    coefficients, so if the number of coefficients C(n+d, n) beats the number
    of points, the system has a nonzero solution.  Returns None when the
    points pin every coefficient down to zero.
    """
    _check(q)
    mons = monomials(n, d)
    rows = [[_mono_eval(m, pt, q) for m in mons] for pt in S]
    vec = _nullspace_vector(rows, len(mons), q)
    if vec is None:
        return None
    return {m: c for m, c in zip(mons, vec) if c}


def _mono_eval(m: tuple[int, ...], pt: Point, q: int) -> int:
    v = 1
    for xi, e in zip(pt, m):
        v = v * pow(xi, e, q) % q
    return v


def _nullspace_vector(rows: list[list[int]], width: int,
                      q: int) -> list[int] | None:
    """One nonzero solution of rows * v = 0 over F_q, or None if only v = 0."""
    mat = [r[:] for r in rows]
    pivot_of_col: dict[int, int] = {}
    r = 0
    for c in range(width):
        piv = next((i for i in range(r, len(mat)) if mat[i][c] % q), None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        inv = pow(mat[r][c], q - 2, q)
        mat[r] = [v * inv % q for v in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c] % q:
                f = mat[i][c]
                mat[i] = [(a - f * b) % q for a, b in zip(mat[i], mat[r])]
        pivot_of_col[c] = r
        r += 1
        if r == len(mat):
            break
    free = [c for c in range(width) if c not in pivot_of_col]
    if not free:
        return None
    f0 = free[0]
    v = [0] * width
    v[f0] = 1
    for c, row in pivot_of_col.items():
        v[c] = (-mat[row][f0]) % q
    return v


def evaluation_rank(q: int, n: int, d: int) -> int:
    """Rank of 'evaluate every monomial of degree <= d at every grid point'.

    When this equals the number of monomials, no nonzero polynomial of degree
    <= d can vanish on the whole grid: the last step of Dvir's argument.
    """
    _check(q)
    mons = monomials(n, d)
    rows = [[_mono_eval(m, pt, q) for m in mons] for pt in grid(q, n)]
    return _rank(rows, len(mons), q)


def _rank(rows: list[list[int]], width: int, q: int) -> int:
    mat = [r[:] for r in rows]
    r = 0
    for c in range(width):
        piv = next((i for i in range(r, len(mat)) if mat[i][c] % q), None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        inv = pow(mat[r][c], q - 2, q)
        mat[r] = [v * inv % q for v in mat[r]]
        for i in range(r + 1, len(mat)):
            if mat[i][c] % q:
                f = mat[i][c]
                mat[i] = [(a - f * b) % q for a, b in zip(mat[i], mat[r])]
        r += 1
        if r == len(mat):
            break
    return r


# ---------------------------------------------------------------------------
# Restricting a polynomial to a line: where the top part shows up
# ---------------------------------------------------------------------------

def _mul1(u: list[int], v: list[int], q: int) -> list[int]:
    out = [0] * (len(u) + len(v) - 1)
    for i, a in enumerate(u):
        if a:
            for j, b in enumerate(v):
                out[i + j] = (out[i + j] + a * b) % q
    return out


def restrict_to_line(g: Poly, a: Point, b: Point, q: int) -> list[int]:
    """g(a + t*b) as a list of coefficients in t, lowest power first."""
    out = [0]
    for exps, c in g.items():
        if not c % q:
            continue
        term = [c % q]
        for ai, bi, e in zip(a, b, exps):
            factor = [ai % q, bi % q]        # (a_i + t b_i)
            for _ in range(e):
                term = _mul1(term, factor, q)
        if len(term) > len(out):
            out = out + [0] * (len(term) - len(out))
        for i, v in enumerate(term):
            out[i] = (out[i] + v) % q
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


# ---------------------------------------------------------------------------
# The whole argument, run rather than recited
# ---------------------------------------------------------------------------

def dvir_report(K: Iterable[Point], q: int, n: int) -> dict:
    """Run Dvir's argument against a candidate small Kakeya set.

    Returns what each step found:

    * `bound`         the number of coefficients available, C(q+n-1, n)
    * `too_small`     is |K| below it, so that step 1 can find a polynomial?
    * `g`             a nonzero polynomial of degree <= q-1 vanishing on K
    * `top`           its top homogeneous part, which the lines force to zero
    * `top_kills`     the directions where the top part vanishes, and how many
    * `contradiction` True when the top part is forced to vanish on the entire
      grid while being a nonzero polynomial of degree < q, which cannot happen

    A genuinely Kakeya K never reaches a contradiction: it is too big for step
    one.  Feed it something smaller and watch the argument bite.
    """
    _check(q)
    K = sorted(set(K))
    report: dict = {"size": len(K), "bound": dvir_bound(q, n),
                    "kakeya": is_kakeya(K, q, n)}
    report["too_small"] = report["size"] < report["bound"]
    g = vanishing_polynomial(K, q, n, q - 1)
    report["g"] = g
    if g is None:
        report["contradiction"] = False
        return report
    top = top_part(g)
    report["degree"] = poly_degree(g)
    report["top"] = top
    dirs = directions(q, n)
    killed = []
    for b in dirs:
        a = next((p for p in K if line(p, b, q) <= set(K)), None)
        if a is None:
            continue                          # no line here: nothing forced
        coeffs = restrict_to_line(g, a, b, q)
        assert all(c == 0 for c in coeffs), "g must vanish along a line in K"
        killed.append(b)
    report["top_kills"] = killed
    report["all_directions_killed"] = len(killed) == len(dirs)
    # a homogeneous polynomial vanishing in every direction vanishes everywhere
    everywhere = all(poly_eval(top, p, q) == 0 for p in grid(q, n))
    report["top_vanishes_everywhere"] = everywhere
    report["contradiction"] = bool(top) and everywhere
    return report


def kakeya_table(q_values: Sequence[int] = (2, 3, 5, 7)) -> list[dict]:
    """The plane's numbers: grid size, Dvir's bound, and the true minimum."""
    rows = []
    for q in q_values:
        rows.append({
            "q": q,
            "grid": q * q,
            "directions": q + 1,
            "dvir_bound": dvir_bound(q, 2),
            "minimum": min_kakeya_size(q, 2),
            "tangent_construction": len(tangent_line_kakeya(q)),
        })
    return rows

"""The computable core of the sphere packing story.

Three groups of things live here.

1. **Room counting.** How much space a ball takes in `d` dimensions, and how
   fast that shrinks.  This is what makes high dimensions strange.

2. **Certificates.** The Cohn-Elkies method proves an upper bound on packing
   density by exhibiting one function that obeys two sign rules.  A certificate
   is built here from the Fourier eigenfunction basis, so its Fourier transform
   is known exactly rather than approximated, and the density bound it proves
   is then plain arithmetic.

3. **The sharp radius.** The 2026 proof pins the best possible certificate by
   showing that a certain radius cannot fall below one over pi, times the
   square root of the dimension.  The constant one over pi is assembled here
   from the three ingredients the proof uses: a logistic density, its
   logarithmic potential, and Wallis's product.

Everything returns ordinary floats.  The quantities the guide quotes are
checked in `tests/` against independent computations, and the ones that are
theorems of other people are quoted, not re-proved; `notes/research-content.md`
says which is which.
"""

from __future__ import annotations

import math
from typing import Callable, Sequence

import numpy as np

# --- how much room a ball has ----------------------------------------------


def log_ball_volume(d: int) -> float:
    """Natural log of the unit ball's volume in `d` dimensions.

    The log is the honest way to hold this number: by dimension 340 the volume
    itself is smaller than the smallest positive number a computer keeps, so
    every high dimensional statement here is made in logs and only turned back
    into a plain number when it is safe.
    """
    return (d / 2) * math.log(math.pi) - math.lgamma(d / 2 + 1)


def ball_volume(d: int) -> float:
    """Volume of the unit ball in `d` dimensions.

    Written with the gamma function, which is the factorial stretched to
    non-whole numbers.  In two dimensions this is pi, in three it is 4/3 pi,
    and after dimension five it starts falling towards zero.
    """
    return math.exp(log_ball_volume(d))


def sphere_area(d: int) -> float:
    """Surface area of the unit sphere in `d` dimensions."""
    return 2 * math.pi ** (d / 2) / math.gamma(d / 2)


def ball_volume_root(d: int) -> float:
    """The `d`-th root of the unit ball's volume.

    Taking the d-th root is how you compare volumes across dimensions on a
    fair footing: it answers "how big is the ball per dimension".
    """
    return math.exp(log_ball_volume(d) / d)


def stirling_volume_root(d: int) -> float:
    """The large-dimension value the d-th root of the ball volume approaches.

    Stirling's formula turns the gamma function into something explicit, and
    what comes out is the square root of 2 pi e over d.
    """
    return math.sqrt(2 * math.pi * math.e / d)


def ball_fraction_of_cube(d: int) -> float:
    """What fraction of a cube is taken up by the largest ball inside it.

    One in one dimension, about 0.785 in two, about 0.524 in three, and it
    keeps falling.  The room is in the corners.
    """
    return math.exp(log_ball_volume(d) - d * math.log(2))


# --- packings we know the answer for ---------------------------------------


def lattice_density(d: int, covolume: float, min_distance: float) -> float:
    """Density of the ball packing centred on a lattice.

    A lattice tiles space with one repeating cell of volume `covolume`, and
    carries one ball centre per cell.  If the closest two centres are
    `min_distance` apart then the balls have half that radius, and the density
    is one ball's volume divided by one cell's volume.
    """
    radius = min_distance / 2
    return ball_volume(d) * radius ** d / covolume


# --- the two sign rules a certificate has to obey --------------------------


def laguerre(k: int, alpha: float, y: float | np.ndarray) -> float | np.ndarray:
    """The generalised Laguerre polynomial, evaluated by its finite sum.

    These polynomials are the building blocks that behave simply under the
    Fourier transform, which is the only reason they appear here.
    """
    total = np.zeros_like(np.asarray(y, dtype=float))
    for i in range(k + 1):
        coeff = (math.gamma(k + alpha + 1)
                 / (math.gamma(i + alpha + 1) * math.gamma(k - i + 1)))
        total = total + coeff * (-np.asarray(y, dtype=float)) ** i / math.factorial(i)
    return total


def eigenfunction(k: int, d: int, r: float | np.ndarray) -> float | np.ndarray:
    """The `k`-th radial Fourier eigenfunction in `d` dimensions.

    A Gaussian multiplied by a Laguerre polynomial.  Its Fourier transform is
    itself again, times plus one when `k` is even and minus one when `k` is
    odd.  That sign flip is the whole reason the basis is used: it turns "what
    does the transform look like" into a question with a one line answer.
    """
    r = np.asarray(r, dtype=float)
    return laguerre(k, d / 2 - 1, 2 * math.pi * r ** 2) * np.exp(-math.pi * r ** 2)


def certificate(coeffs: Sequence[float], d: int) -> Callable[[np.ndarray], np.ndarray]:
    """A radial function built as a weighted sum of the eigenfunctions."""
    def f(r):
        r = np.asarray(r, dtype=float)
        return sum(c * eigenfunction(k, d, r) for k, c in enumerate(coeffs))
    return f


def transform_coeffs(coeffs: Sequence[float]) -> list[float]:
    """The same function's Fourier transform, in the same basis.

    Every odd numbered building block changes sign and nothing else happens.
    """
    return [c * (-1) ** k for k, c in enumerate(coeffs)]


def transform(coeffs: Sequence[float], d: int) -> Callable[[np.ndarray], np.ndarray]:
    """The Fourier transform of `certificate(coeffs, d)`, exactly."""
    return certificate(transform_coeffs(coeffs), d)


def radial_fourier_1d(f: Callable, rho: float, limit: float = 12.0,
                      n: int = 200_001) -> float:
    """The radial Fourier transform in one dimension, by direct integration.

    In one dimension the transform of an even function is a cosine integral.
    This exists only to check the sign flip rule above against something that
    knows nothing about Laguerre polynomials.
    """
    r = np.linspace(0.0, limit, n)
    return 2 * float(np.trapezoid(f(r) * np.cos(2 * math.pi * r * rho), r))


def radial_fourier_3d(f: Callable, rho: float, limit: float = 12.0,
                      n: int = 200_001) -> float:
    """The radial Fourier transform in three dimensions, by direct integration.

    In three dimensions the Bessel kernel collapses to a sine, which makes an
    independent check possible without any special function library.
    """
    if rho == 0:
        r = np.linspace(0.0, limit, n)
        return 4 * math.pi * float(np.trapezoid(f(r) * r ** 2, r))
    r = np.linspace(0.0, limit, n)
    return (2 / rho) * float(np.trapezoid(f(r) * r * np.sin(2 * math.pi * r * rho), r))


def is_admissible(coeffs: Sequence[float], d: int, outer: float = 8.0,
                  samples: int = 6000, margin: float = 0.0) -> bool:
    """Does this function obey both sign rules of the Cohn-Elkies method?

    Rule one: the function is at or below zero everywhere from radius one
    outward.  Rule two: its Fourier transform is at or above zero everywhere,
    and strictly above zero at the centre.

    `margin` asks for the rules to hold with room to spare, which matters when
    a search is choosing the function.  The best certificates sit exactly on
    the boundary, touching zero, so a search that is allowed right up to the
    boundary will always find a function that passes on the grid it was given
    and fails on a finer one.  Searching with a margin and checking without it
    is what makes the recorded answer survive re-checking.

    The check samples both profiles out to `outer`.  Past that radius the
    Gaussian factor has crushed every term, so the sign there is settled by the
    leading term instead, in `tail_sign_ok`.  This is a numerical check on a
    grid, not a proof.
    """
    if float(polynomial_part(transform_coeffs(coeffs), d, 0.0)) <= 0:
        return False
    outside = np.linspace(1.0, outer, samples)
    if float(np.max(polynomial_part(coeffs, d, outside))) > -margin:
        return False
    everywhere = np.linspace(0.0, outer, samples)
    hat = polynomial_part(transform_coeffs(coeffs), d, everywhere)
    if float(np.min(hat)) < margin:
        return False
    return tail_sign_ok(coeffs, d, outer)


def polynomial_part(coeffs: Sequence[float], d: int,
                    r: float | np.ndarray) -> float | np.ndarray:
    """The factor that decides the sign, with the Gaussian divided out.

    Every function here is a polynomial times the same positive Gaussian, so
    the Gaussian can never change a sign; it only makes everything small.
    Testing the polynomial on its own is both exact for sign questions and the
    only way a margin means anything far from the origin, where the Gaussian
    has pushed the function itself below any fixed threshold.
    """
    r = np.asarray(r, dtype=float)
    return sum(c * laguerre(k, d / 2 - 1, 2 * math.pi * r ** 2)
               for k, c in enumerate(coeffs))


def tail_sign_ok(coeffs: Sequence[float], d: int, outer: float) -> bool:
    """Beyond the sampled window, does the leading term give the right signs?

    For large radius the highest Laguerre term dominates, and its sign is the
    sign of its leading coefficient times minus one to the power of its index.
    Checking it keeps `is_admissible` honest about the part of the line no grid
    can visit.
    """
    top = max(k for k, c in enumerate(coeffs) if c != 0)
    lead = coeffs[top] * (-1) ** top / math.factorial(top)
    lead_hat = coeffs[top] * (-1) ** top * (-1) ** top / math.factorial(top)
    return lead <= 0 and lead_hat >= 0


def density_bound(coeffs: Sequence[float], d: int) -> float:
    """The packing density upper bound this certificate proves.

    The Gorbachev-Cohn-Elkies inequality: the ball volume, times the value of
    the function at the centre, divided by two to the power of the dimension
    times the value of its transform at the centre.
    """
    f = certificate(coeffs, d)
    fhat = transform(coeffs, d)
    return ball_volume(d) * float(f(0.0)) / (2 ** d * float(fhat(0.0)))


def seed_certificate(d: int, rho: float = 0.9) -> list[float]:
    """A certificate whose sign change happens strictly inside radius one.

    Same shape as `simple_certificate`, but the function crosses zero at `rho`
    rather than exactly at one, so both sign rules hold with room to spare.  A
    search needs a starting point like this: one that is not already pressed
    against the wall it is being asked to move along.

    The transform stays non-negative at the centre only while `rho` squared is
    above the dimension over two pi, which is why this family runs out at
    dimension seven and stops being a starting point at all.
    """
    b = 1 / (2 * math.pi * rho ** 2)
    a = 1 - d / (4 * math.pi * rho ** 2)
    return [a, b]


def seed_exists(d: int, rho: float = 0.9) -> bool:
    """Is there a starting certificate of that shape in this dimension?"""
    return rho ** 2 > d / (2 * math.pi)


def simple_certificate(d: int) -> list[float]:
    """The simplest certificate anyone would write down, in the same basis.

    It is one minus radius squared, times a Gaussian, which obviously obeys the
    first sign rule.  Its transform stays non-negative only while the dimension
    is below two pi, so this certificate exists only up to dimension six.  It
    is included because seeing a real certificate fail is the fastest way to
    feel what the two rules cost.
    """
    return [1 - d / (4 * math.pi), 1 / (2 * math.pi)]


def improve_certificate(coeffs: Sequence[float], d: int, iterations: int = 4000,
                        step: float = 0.15, margin: float = 1e-4,
                        samples: int = 20_000, seed: int = 0) -> tuple[float, list[float]]:
    """Nudge a working certificate towards a smaller bound, at random.

    Starts from something that already obeys both rules and repeatedly tries a
    random nudge, keeping it only when the bound improves and the rules still
    hold with the margin.  It is a plain hill climb, not the semidefinite
    machinery the literature uses, and it is here so the guide can show the
    method producing a real number rather than only describing it.

    Returns the bound and the coefficients that achieved it.
    """
    import random

    rng = random.Random(seed)

    def value(c):
        if not is_admissible(c, d, samples=samples, margin=margin):
            return math.inf
        return density_bound(c, d)

    current = list(coeffs)
    best = value(current)
    if best == math.inf:
        return best, current
    stale = 0
    for _ in range(iterations):
        trial = [current[0]] + [current[i] + step * rng.gauss(0, 1)
                                for i in range(1, len(current))]
        v = value(trial)
        if v < best - 1e-14:
            current, best, stale = trial, v, 0
            step *= 1.15
        else:
            stale += 1
            if stale > 40:
                step *= 0.7
                stale = 0
        if step < 1e-8:
            break
    return best, current


# --- rebuilding a certificate into a balanced function ---------------------


def sign_radius(coeffs: Sequence[float], d: int) -> float:
    """The radius the balancing trick produces from a certificate.

    The ratio of the function's value at the centre to its transform's value
    at the centre, taken to the power one over the dimension.  This is the
    number the whole 2026 argument is about: the smaller it can be made, the
    better the certificate, and the theorem says it cannot be made smaller
    than one over pi times the square root of the dimension.
    """
    f0 = float(certificate(coeffs, d)(0.0))
    fhat0 = float(transform(coeffs, d)(0.0))
    return (f0 / fhat0) ** (1 / d)


def balanced_pair(coeffs: Sequence[float], d: int):
    """Stretch a certificate until it and its transform agree at the centre.

    Stretching a function by a factor makes its transform shrink by the same
    factor and gain a height, so there is exactly one stretch that levels the
    two values at the centre.  After it, subtracting one from the other leaves
    a function that is zero at the centre and turns into minus itself under the
    Fourier transform.

    Returns three callables, the stretched function, its transform, and their
    difference, together with the radius beyond which the difference is never
    negative.
    """
    f = certificate(coeffs, d)
    fhat = transform(coeffs, d)
    a = (float(fhat(0.0)) / float(f(0.0))) ** (1 / d)

    def h(r):
        return f(np.asarray(r, dtype=float) * a)

    def h_hat(r):
        return a ** (-d) * fhat(np.asarray(r, dtype=float) / a)

    def g(r):
        return h_hat(r) - h(r)

    return h, h_hat, g, 1 / a


# --- the radius that cannot shrink -----------------------------------------


def mellin_multiplier(lam: float, t: float) -> complex:
    """The factor that Fourier transformation becomes in Mellin coordinates.

    Along the real axis this number always has size exactly one: it only
    rotates.  Its behaviour away from the real axis is what carries the
    dimension information the proof needs.
    """
    a = _log_gamma_complex((lam - 1j * t) / 2)
    b = _log_gamma_complex((lam + 1j * t) / 2)
    return complex(np.exp(1j * t * math.log(math.pi) + a - b))


def _log_gamma_complex(z: complex) -> complex:
    """Log gamma for complex argument, by the Lanczos approximation."""
    g = 7
    p = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
         771.32342877765313, -176.61502916214059, 12.507343278686905,
         -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]
    if z.real < 0.5:
        # reflection, so the series is only ever used on the right half plane
        return (complex(math.log(math.pi))
                - _log_complex(_sin_complex(math.pi * z))
                - _log_gamma_complex(1 - z))
    z = z - 1
    x = complex(p[0])
    for i in range(1, g + 2):
        x += p[i] / (z + i)
    t = z + g + 0.5
    return (0.5 * math.log(2 * math.pi) + (z + 0.5) * _log_complex(t) - t
            + _log_complex(x))


def _log_complex(z: complex) -> complex:
    return complex(math.log(abs(z)), math.atan2(z.imag, z.real))


def _sin_complex(z: complex) -> complex:
    return complex(math.sin(z.real) * math.cosh(z.imag),
                   math.cos(z.real) * math.sinh(z.imag))


def logistic_density(u: float | np.ndarray) -> float | np.ndarray:
    """The density the harmonic measure turns into at the decisive edge.

    A bell shaped probability density.  It is the limit of the weighting the
    proof puts on frequencies as the argument is pushed to the boundary of the
    strip, and it is what makes the final constant come out clean.
    """
    u = np.asarray(u, dtype=float)
    return (math.pi / 4) / np.cosh(math.pi * u / 2) ** 2


def logistic_characteristic(t: float) -> float:
    """The Fourier side of that density: the argument divided by its sinh.

    Equal to one at zero, and this is the identity that makes the digamma
    function appear in the potential below.
    """
    if t == 0:
        return 1.0
    return t / math.sinh(t)


def digamma(x: float) -> float:
    """The derivative of log gamma, by the standard recurrence and series."""
    result = 0.0
    while x < 6:
        result -= 1 / x
        x += 1
    f = 1 / (x * x)
    return (result + math.log(x) - 0.5 / x
            + f * (-1 / 12 + f * (1 / 120 + f * (-1 / 252 + f * (1 / 240)))))


def log_potential(x: float) -> float:
    """The logarithmic potential of the logistic density, in closed form.

    The proof needs the average of the log of the distance from a point to a
    random sample of that density.  It evaluates to a digamma value plus log
    two, and `tests/` checks that against direct numerical integration.
    """
    return digamma((x + 1) / 2) + math.log(2)


def log_potential_numeric(x: float, limit: float = 60.0,
                          n: int = 400_001) -> float:
    """The same potential by brute force integration, for checking."""
    u = np.linspace(-limit, limit, n)
    return float(np.trapezoid(logistic_density(u)
                              * np.log(np.sqrt(x ** 2 + u ** 2)), u))


def wallis_integral(limit: float = 60.0, n: int = 800_001) -> float:
    """The integral that Wallis's product evaluates to the log of pi over two.

    This is the number that moves the Gaussian's natural radius to the radius
    the obstruction demands, and it is the reason pi appears in the answer.
    """
    a = np.linspace(1e-9, limit, n)
    return float(np.trapezoid(np.exp(-2 * a) * np.tanh(a) / a, a))


def saddle_radius_constant() -> float:
    """The constant the construction lands on: one over pi.

    A Gaussian on its own gives one over the square root of two pi.  The
    deformation moves it by minus one half of the log of pi over two, which is
    exactly the Wallis number, and the two combine to one over pi.
    """
    gaussian = 1 / math.sqrt(2 * math.pi)
    displacement = -0.5 * math.log(math.pi / 2)
    return gaussian * math.exp(displacement)


def harmonic_measure(sigma: float, T: float | np.ndarray) -> float | np.ndarray:
    """How much weight the maximum principle puts on each frequency.

    `sigma` says how close to the decisive edge of the strip the argument
    sits.  The total weight is deliberately not one; keeping it at its true
    value is what preserves the exponential constant.
    """
    theta = math.pi * (1 + sigma) / 2
    T = np.asarray(T, dtype=float)
    return math.sin(theta) / (4 * (np.cosh(math.pi * T / 2) - math.cos(theta)))


def harmonic_mass(sigma: float, limit: float = 200.0, n: int = 400_001) -> float:
    """The total weight above, which is one minus sigma, over two."""
    T = np.linspace(-limit, limit, n)
    return float(np.trapezoid(harmonic_measure(sigma, T), T))


# --- what the two directions add up to -------------------------------------


def sign_radius_constant() -> float:
    """One over pi: the sharp constant for the sign radius, per square root d.

    Both directions of the 2026 proof meet here.  No certificate can have a
    smaller radius, and a certificate exists that reaches it.
    """
    return 1 / math.pi


def lp_rate() -> float:
    """The exact exponential rate of the linear program: root of e over 2 pi.

    Assembled from the pieces: the d-th root of the ball volume tends to the
    square root of 2 pi e over d, it is halved by the two-to-the-d, and the
    certificate contributes the square root of d over pi.  The dimension
    cancels and this number is left.
    """
    return math.sqrt(math.e / (2 * math.pi))


def lp_rate_from_pieces(d: int) -> float:
    """The same rate, assembled the way the proof assembles it.

    Used by `tests/` to check that the pieces really do combine to `lp_rate()`
    as the dimension grows, rather than the value being asserted by hand.
    """
    return stirling_volume_root(d) / 2 * (math.sqrt(d) * sign_radius_constant())


def alpha_star() -> float:
    """The new packing exponent: one half of the log to base two of 2 pi over e.

    The density bound is two to the minus this number, times the dimension.
    Bigger is better, because it means the bound falls faster.
    """
    return 0.5 * math.log2(2 * math.pi / math.e)


def exponent_advantage(d: int, old: float, new: float) -> float:
    """How many times smaller the new bound is than the old one, in dimension d.

    Each bound is two to the minus its exponent, times the dimension, so the
    ratio of the new bound to the old one is two to the old exponent minus the
    new one, times the dimension.  A number below one means the new bound is
    the smaller, and smaller is stronger.
    """
    return 2 ** ((old - new) * d)

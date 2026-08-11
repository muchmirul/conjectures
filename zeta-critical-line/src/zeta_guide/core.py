"""The mathematics behind the guide: zeta, its zeros, and the paper's toys.

Everything here is honest and small.  The zeta values come from a plain
Euler-Maclaurin sum (cross-checked against mpmath in the tests), the zeros
from a shipped table computed once by mpmath's root finder, and the matrix
experiments follow the recipe of the paper's section 8 at a height a laptop
holds comfortably.  Nothing in this file proves the 2026 theorem; it builds
the objects the theorem talks about, so the article's pictures and numbers
can be re-derived from scratch.

Paper: "More than two thirds of the zeros of the Riemann zeta function lie
on the critical line" (Claude, Anthropic, August 2026), kept in
docs/zeta-critical-line/paper/ at the repository root.
"""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parent / "data"


# --- zeta itself ------------------------------------------------------------

def zeta_em(s: complex, terms: int = 60) -> complex:
    """Zeta by Euler-Maclaurin: the same recipe the playable pages run.

    Sum the reciprocal powers up to a cutoff, then add the standard tail
    corrections (integral, half-term, and two Bernoulli terms).  The cutoff
    grows with the height, because the corrections only converge once it
    passes the height's scale; with it, the recipe is good to about ten
    digits everywhere this guide evaluates it.  Not valid at s = 1.
    """
    s = complex(s)
    N = max(terms, int(1.3 * abs(s.imag)) + 20)
    out = sum(n ** (-s) for n in range(1, N))
    out += N ** (1 - s) / (s - 1)
    out += 0.5 * N ** (-s)
    out += s * N ** (-s - 1) / 12
    out -= s * (s + 1) * (s + 2) * N ** (-s - 3) / 720
    out += s * (s + 1) * (s + 2) * (s + 3) * (s + 4) * N ** (-s - 5) / 30240
    return out


def zeta_on_line(t: float) -> complex:
    """Zeta at height t on the critical line."""
    return zeta_em(0.5 + 1j * t)


# --- the zeros --------------------------------------------------------------

@lru_cache(maxsize=1)
def zero_heights() -> tuple[float, ...]:
    """The first 300 zero heights, from the shipped table.

    The table was computed by mpmath.zetazero at 20 digits (the script is
    quoted in the table's header).  `tests/test_core.py` recomputes a sample
    live and checks zeta really vanishes at every shipped height, so the
    file cannot silently rot.
    """
    lines = (DATA / "zeros300.txt").read_text().splitlines()
    return tuple(float(l) for l in lines if l and not l.startswith("#"))


def compute_zeros(n: int) -> list[float]:
    """Recompute the first n zero heights live with mpmath (slow)."""
    import mpmath

    mpmath.mp.dps = 20
    return [float(mpmath.zetazero(k).imag) for k in range(1, n + 1)]


def counting_main_term(t1: float, t2: float) -> float:
    """The Riemann-von Mangoldt prediction for the zero count in (t1, t2].

    This is the smooth main term N(t) = (t/2pi) log(t/2pi) - t/2pi + 7/8
    evaluated at both ends; the paper's equation (1.2) is its [T, 2T] form.
    """
    def main(t):
        return t / (2 * math.pi) * math.log(t / (2 * math.pi)) \
            - t / (2 * math.pi) + 7 / 8

    return main(t2) - main(t1)


def zero_count(t1: float, t2: float) -> int:
    """How many shipped zeros have height in (t1, t2]."""
    return sum(1 for g in zero_heights() if t1 < g <= t2)


# --- primes and the staircase ----------------------------------------------

def primes_up_to(x: int) -> list[int]:
    sieve = np.ones(x + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(x ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p:: p] = False
    return [int(p) for p in np.nonzero(sieve)[0]]


def von_mangoldt_terms(x: int) -> list[tuple[int, float]]:
    """(n, weight) for every prime power n up to x; the weight is log p."""
    out = []
    for p in primes_up_to(x):
        q = p
        while q <= x:
            out.append((q, math.log(p)))
            q *= p
    return sorted(out)


def psi_staircase(xs: np.ndarray) -> np.ndarray:
    """The weighted prime staircase: at each x, the sum of weights up to x.

    Every prime power contributes the logarithm of its prime.  This is the
    tally the explicit formula rebuilds from zeros, and the guide calls it
    "the prime staircase" (the plain prime count has the same wobble but a
    messier formula).
    """
    terms = von_mangoldt_terms(int(np.max(xs)) + 1)
    ns = np.array([n for n, _ in terms], dtype=float)
    ws = np.array([w for _, w in terms])
    return np.array([ws[ns <= x].sum() for x in np.asarray(xs, dtype=float)])


def psi_from_waves(xs: np.ndarray, n_zeros: int) -> np.ndarray:
    """The explicit formula's rebuild of the staircase from n_zeros waves.

    Start from the smooth ramp x - log(2 pi), then subtract one wave per
    zero: the wave of the zero at height g is
    2 sqrt(x) cos(g log x - angle) / |rho|, with rho = 1/2 + i g.  (This is
    the classical pairing of x^rho / rho with its mirror; the tiny correction
    from the trivial zeros is included for honesty, it is invisible at the
    scale drawn.)
    """
    xs = np.asarray(xs, dtype=float)
    out = xs - math.log(2 * math.pi) - 0.5 * np.log1p(-xs ** -2.0)
    lx = np.log(xs)
    for g in zero_heights()[:n_zeros]:
        rho = 0.5 + 1j * g
        amp = 2 * np.sqrt(xs) / abs(rho)
        out = out - amp * np.cos(g * lx - np.angle(rho))
    return out


def prime_density(taus: np.ndarray, x_cut: float) -> np.ndarray:
    """The prime-built density of zeros: the paper's nu built from primes.

    The smooth part is the average spacing law (the paper's mu, equation
    (2.3), here in its simple large-height form log(tau/2pi)/2pi); each
    prime power up to x_cut then adds a cosine wave.  The result dips and
    spikes, and the spikes sit at the true zero heights: that is Riemann's
    duet run in the prime-to-zero direction.
    """
    taus = np.asarray(taus, dtype=float)
    out = np.log(taus / (2 * math.pi)) / (2 * math.pi)
    for n, w in von_mangoldt_terms(int(x_cut)):
        out = out - (w / (math.pi * math.sqrt(n))) * np.cos(taus * math.log(n))
    return out


# --- the paper's shape functions and constants ------------------------------

def shape_h(lam: float) -> float:
    """The paper's H (equation (1.3), page 3): the certified proportion of
    distinct on-line zeros at dial value lam.  Two, minus one over the dial,
    minus a third of the dial."""
    return 2 - 1 / lam - lam / 3


def shape_hd(lam: float) -> float:
    """The paper's H_d: the distinct-zero proportion, halfway between H and
    one."""
    return (1 + shape_h(lam)) / 2


def shape_f(lam: float) -> float:
    """The paper's F: the weaker Cauchy-Schwarz certificate."""
    return lam / (1 + lam ** 2 / 3)


#: below this dial value the Cauchy-Schwarz route wins for distinct zeros;
#: the paper computes it as three minus the square root of six (page 3)
CROSSOVER_DIAL = 3 - math.sqrt(6)


def energy_per_count(lam: float) -> float:
    """The prime-measured energy of the table, per zero counted.

    Montgomery's second moment: one over the dial, plus a third of the dial
    (the paper's equation (5.12) divided through by the count).  At dial one
    this is four thirds, the number the two-thirds budget spends.
    """
    return 1 / lam + lam / 3


def fejer_integral(lam: float, grid: int = 200_001) -> float:
    """The pair-correlation integral behind the energy: the integral of
    (lam - |a|) |a| over |a| <= lam, done numerically.

    Equals lam cubed over three; adding the diagonal's lam and dividing by
    lam squared gives energy_per_count.  Kept numerical so the test that
    checks the identity is not the identity itself.
    """
    a = np.linspace(-lam, lam, grid)
    return float(np.trapezoid((lam - np.abs(a)) * np.abs(a), a))


def window_functional(v: np.ndarray, s: np.ndarray, lam: float = 1.0) -> float:
    """The paper's window score c_lambda (equation (7.3), page 20).

    v is a nonnegative window profile sampled on the grid s over [-1/2, 1/2].
    Score: lam times the square of the area, divided by the energy plus
    lam^2 times the gap-weighted double integral.  The flat window scores
    3/4 at dial one; the Montgomery-Taylor cosine window scores 0.7532960...
    """
    ds = s[1] - s[0]
    area = float(np.sum(v) * ds)
    sq = float(np.sum(v ** 2) * ds)
    gaps = np.abs(s[:, None] - s[None, :])
    double = float(v @ gaps @ v * ds * ds)
    return lam * area ** 2 / (sq + lam ** 2 * double)


def montgomery_taylor_constant(grid: int = 4001) -> float:
    """The optimised window score c_1^* = 0.7532960..., computed numerically.

    The optimiser is the cosine profile cos(sqrt(2) s) on [-1/2, 1/2]
    (the paper's equation (7.4), page 21); its score in closed form is
    2 tan(1/sqrt 2) / (sqrt 2 + tan(1/sqrt 2)).  This function evaluates the
    functional at the optimiser; the test compares it with the closed form
    and checks perturbations do not beat it.
    """
    s = np.linspace(-0.5, 0.5, grid)
    return window_functional(np.cos(math.sqrt(2) * s), s)


def montgomery_taylor_closed_form() -> float:
    """The same constant from the paper's closed form."""
    t = math.tan(1 / math.sqrt(2))
    return 2 * t / (math.sqrt(2) + t)


def whole_number_charge(m: int) -> int:
    """The energy charge of a zero repeated m times: m squared."""
    return m * m


def whole_number_floor(m: int) -> int:
    """The trick's floor 3m - 2: what the charge is always at least."""
    return 3 * m - 2


# --- the toy listening experiment (the paper's section 8, shrunk) -----------

def ramp(x: np.ndarray) -> np.ndarray:
    """The paper's smooth ramp profile x - sin(2 pi x)/(2 pi), clipped."""
    x = np.clip(x, 0.0, 1.0)
    return x - np.sin(2 * math.pi * x) / (2 * math.pi)


class ToyFamily:
    """The listening family at a toy height: window, microphones, tables.

    Follows the paper's section 2.2 and its section 8 numerics: a flat-top
    window of length L = dial * log(T / 2pi) with smooth ramps, microphones
    at frequencies T + k * (2 pi / L) for k = 0 .. d-1, d = floor(L T / 2pi).
    The two ways of filling in the table of overlaps:

    * from zeros: each zero contributes its response at both microphones
      (the paper's equation (2.20), first expression)
    * from primes: integrate the microphone responses against the
      prime-built density nu (second expression; Weil's explicit formula
      says the two agree)
    """

    def __init__(self, T: float = 100.0, dial: float = 1.0,
                 ramp_frac: float = 0.2):
        self.T = T
        self.dial = dial
        self.L = dial * math.log(T / (2 * math.pi))
        self.w = ramp_frac * self.L / 2
        self.h = 2 * math.pi / self.L
        self.d = int(self.L * T / (2 * math.pi))
        self.mics = np.array([T + k * self.h for k in range(self.d)])
        # the window's transform, sampled once on a fine u-grid for reuse
        self._us = np.linspace(0, self.L / 2, 2001)
        self._phi = ramp((self.L / 2 - self._us) / self.w)

    def window(self, us: np.ndarray) -> np.ndarray:
        """The taper: 1 on the flat top, easing to 0 over the ramps."""
        return ramp((self.L / 2 - np.abs(np.asarray(us, dtype=float)))
                    / self.w)

    def response(self, r) -> np.ndarray | complex:
        """The window's transform: how hard a mic rings at offset r.

        phi is even, so the transform is 2 * integral of phi(u) cos(r u).
        Accepts real arrays (prime side) and complex scalars (a zero off
        the line has a complex offset).
        """
        r = np.asarray(r)
        us, phi = self._us, self._phi
        vals = 2 * np.trapezoid(phi * np.cos(np.multiply.outer(r, us)),
                                us, axis=-1)
        return vals if vals.shape else complex(vals)

    # -- the zero side -------------------------------------------------------

    def table_from_zeros(self, zeros: list[tuple[complex, int]]) -> np.ndarray:
        """The d-by-d table from a list of (zero offset gamma, multiplicity).

        gamma is the zero's position read on the height axis: real for a
        zero on the line, complex for one off it (the paper's gamma_rho).
        Includes each entry's mirror through the line automatically when
        gamma is complex, as the true zero multiset does.
        """
        G = np.zeros((self.d, self.d))
        for gamma, m in zeros:
            gs = [gamma] if abs(complex(gamma).imag) < 1e-12 \
                else [gamma, np.conj(gamma)]
            for g in gs:
                v = np.array([self.response(complex(g) - tk)
                              for tk in self.mics])
                # both factors at the zero itself, no conjugate (the paper's
                # equation (2.20)); the mirror partner in gs supplies the
                # conjugate copy, and the real part of the pair's sum is the
                # signature-(1,1) saddle
                G += m * np.real(np.outer(v, v))
        return G / self.L

    def real_zero_config(self, lo: float, hi: float) \
            -> list[tuple[complex, int]]:
        """The genuine zeros with heights in [lo, hi], all simple, on line."""
        return [(complex(g), 1) for g in zero_heights() if lo <= g <= hi]

    # -- the prime side ------------------------------------------------------

    def nu(self, taus: np.ndarray) -> np.ndarray:
        """The paper's explicit-formula density (equation (2.6)): the smooth
        spacing law, the pole's bump, and one cosine per prime power up to
        the reach X = exp(L)."""
        import mpmath

        taus = np.asarray(taus, dtype=float)
        mu = np.array([
            float(mpmath.re(mpmath.digamma(0.25 + 0.5j * t))) / (2 * math.pi)
            - math.log(math.pi) / (2 * math.pi) for t in taus])
        X = math.exp(self.L)
        s = 0.5 + 1j * taus
        pole = 1 / (2 * math.pi * (0.25 + taus ** 2)) \
            + np.real((X ** s - 1) / s) / math.pi
        px = np.zeros_like(taus)
        for n, w in von_mangoldt_terms(int(X)):
            px -= (w / (math.pi * math.sqrt(n))) * np.cos(taus * math.log(n))
        return mu + pole + px

    def table_from_primes(self, pad: float = 60.0, step: float = 0.02) \
            -> np.ndarray:
        """The same table, filled in from primes and smooth terms only.

        Integrates each pair of microphone responses against nu over a
        grid extending `pad` beyond the mic range on both sides (the
        responses die off like one over distance squared, so the truncation
        error is small and the tests measure it rather than assume it).
        """
        taus = np.arange(self.T - pad, 2 * self.T + pad, step)
        nu = self.nu(taus)
        resp = np.array([self.response(taus - tk) for tk in self.mics])
        return (resp * nu * step) @ resp.T / self.L


# --- certificates (the paper's counting inequalities, at toy scale) ---------

def positive_directions(R: np.ndarray, theta: float = 0.0) -> int:
    """How many eigenvalues of the symmetric table R exceed theta."""
    return int(np.sum(np.linalg.eigvalsh(R) > theta))


def cs_certificate(R: np.ndarray) -> float:
    """The Cauchy-Schwarz certificate 2 (tr R)^2 / tr(R^2) - N-with-pairs.

    Used on the toy tables with N replaced by the configured count; the
    caller supplies the count, this returns 2 C where C is the squared-trace
    ratio (the paper's section 8 notation C = (tr R)^2 / tr R^2).
    """
    return 2 * float(np.trace(R)) ** 2 / float(np.trace(R @ R))


def rank_trace_floor(P: np.ndarray, Q: np.ndarray, b: int) -> float:
    """The floor the rank-trace inequality (equation (3.1), c = 2) puts on
    the rank of P: 2 tr P + 4 tr Q - 4 b - ||P + Q||_F^2."""
    return (2 * float(np.trace(P)) + 4 * float(np.trace(Q)) - 4 * b
            - float(np.sum((P + Q) ** 2)))

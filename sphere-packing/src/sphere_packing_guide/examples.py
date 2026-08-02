"""The named numbers the guide keeps coming back to.

Anything marked "computed" is derived by `core.py` and re-checked in `tests/`.
Anything marked "quoted" is somebody else's theorem, written down here so the
guide and the tests refer to one copy of it.  `notes/research-content.md`
carries the sources.
"""

from __future__ import annotations

import math

from .core import (alpha_star, ball_volume, lattice_density, lp_rate,
                   sign_radius_constant, simple_certificate)

# --- the headline constants ------------------------------------------------

#: computed: the exponential rate of the linear program, root of e over 2 pi
LP_RATE = lp_rate()

#: computed: the new packing exponent, 0.6044005442916777
ALPHA_STAR = alpha_star()

#: quoted: the exponent that stood from 1978 until 2026
KL_EXPONENT = 0.59905576

#: computed: the sharp sign radius constant, one over pi
SIGN_RADIUS = sign_radius_constant()

#: quoted: the digits the paper prints for the new exponent
ALPHA_STAR_PRINTED = "0.604400544291677695"

# --- packings whose exact answer is known ----------------------------------

#: quoted densities, each recomputed from its lattice by `lattice_density`
KNOWN_DENSITIES = {
    1: ("the line", 1.0, "trivial"),
    2: ("hexagonal", math.pi / math.sqrt(12), "Thue 1910, Fejes Toth 1943"),
    3: ("face centred cubic", math.pi / math.sqrt(18), "Hales 1998, published 2005"),
    8: ("E8", math.pi ** 4 / 384, "Viazovska 2017"),
    24: ("Leech", math.pi ** 12 / math.factorial(12), "Cohn, Kumar, Miller, "
         "Radchenko, Viazovska 2017"),
}

#: the same five packings as lattices: dimension, cell volume, closest distance
KNOWN_LATTICES = {
    1: (1.0, 1.0),
    2: (math.sqrt(3) / 2, 1.0),
    3: (1 / math.sqrt(2), 1.0),
    8: (1.0, math.sqrt(2)),
    24: (1.0, 2.0),
}


def known_density(d: int) -> float:
    """Recompute a known optimal density from its lattice."""
    covolume, min_distance = KNOWN_LATTICES[d]
    return lattice_density(d, covolume, min_distance)


# --- the simplest certificate, and where it gives up -----------------------

#: the largest dimension in which one minus radius squared still works
SIMPLE_CERTIFICATE_LIMIT = 6

#: the dimensions the guide walks through with that certificate
SIMPLE_CERTIFICATE_DIMS = (1, 2, 3, 4, 5, 6)


#: certificates this repository found by hill climbing from `seed_certificate`,
#: each re-checked in `tests/` for both sign rules and for the bound it proves
FOUND_CERTIFICATES = {
    2: [1.0, 0.03530634, -0.09737948, 0.03676317, 0.00747249, -0.00609293,
        -0.00082869, 0.00166722, -6e-07, 1e-08],
    3: [1.0, 0.11596158, -0.05874362, -0.00082876, 0.01482563, 0.00539376,
        -0.00068756, -0.00089985, -7.22e-05, 0.0001643],
}

#: the bounds those certificates prove, to the digits the article quotes
FOUND_BOUNDS = {2: 0.911648, 3: 0.784806}

#: the first dimension in which the default starting certificate no longer
#: exists, because its transform at the centre can no longer be kept positive
SEED_FAILS_FROM = 6

#: the first dimension in which even the simplest certificate stops existing
SIMPLE_FAILS_FROM = 7


def simple_bound(d: int) -> float:
    """The density bound the simplest certificate proves in dimension `d`.

    In dimensions one, two, three and six it gives a number above one, and a
    density above one is no news at all.  In dimensions four and five it does
    better than that and proves something true, though far from the best known.
    The guide uses it to show that obeying both sign rules is easy and that
    obeying them *well* is the whole difficulty.
    """
    from .core import density_bound
    return density_bound(simple_certificate(d), d)


# --- history, in the order the guide tells it ------------------------------

#: quoted: the milestones the article names, with the year each landed
MILESTONES = (
    (1611, "Kepler guesses that no packing of equal balls in space beats the "
           "greengrocer's stack"),
    (1978, "Kabatianskii and Levenshtein prove the exponent 0.59905576"),
    (2000, "Gorbachev, and independently Cohn, write down the Fourier "
           "certificate method"),
    (2003, "Cohn and Elkies publish it and compute with it"),
    (2005, "Hales's proof of the Kepler conjecture appears in print"),
    (2014, "Cohn and Zhao show the certificate method is at least as strong as "
           "the 1978 bound"),
    (2017, "Viazovska settles dimension eight; Cohn, Kumar, Miller, Radchenko "
           "and Viazovska settle dimension twenty four"),
    (2020, "Afkhami-Jeddi, Cohn, Hartman, de Laat and Tajdini conjecture the "
           "exact rate of the method"),
    (2026, "the rate is proved, and the exponent 0.6044005442916777 replaces "
           "the 1978 one"),
)

__all__ = [
    "ALPHA_STAR", "ALPHA_STAR_PRINTED", "KL_EXPONENT", "KNOWN_DENSITIES",
    "KNOWN_LATTICES", "LP_RATE", "MILESTONES", "SIGN_RADIUS",
    "SIMPLE_CERTIFICATE_DIMS", "SIMPLE_CERTIFICATE_LIMIT", "ball_volume",
    "known_density", "simple_bound",
]

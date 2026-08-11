"""The named numbers the guide keeps coming back to.

Anything marked "computed" is derived by `core.py` and re-checked in `tests/`.
Anything marked "quoted" is somebody else's theorem (or the 2026 paper's own
statement), written down here so the guide and the tests refer to one copy of
it.  `notes/research-content.md` carries the sources.
"""

from __future__ import annotations

import math

from .core import (montgomery_taylor_closed_form, shape_f, shape_h, shape_hd,
                   zero_heights)

# --- the first zeros, for the prose ------------------------------------------

#: computed: the height of the first zero, 14.13...
FIRST_ZERO = zero_heights()[0]

#: computed: how many zeros the shipped table holds
SHIPPED_ZEROS = len(zero_heights())

# --- the record race (all quoted; the guide's chapter 4) ---------------------

#: quoted: the proportion-on-the-line record before 2026, and who held it.
#: Every entry after 1942 is by Levinson's method.  Selberg's 1942 constant
#: was positive but tiny and not explicit, recorded here as 0.
RECORD_RACE = (
    (1914, 0.0, "Hardy: infinitely many zeros on the line"),
    (1942, 0.0, "Selberg: a positive (tiny, inexplicit) proportion"),
    (1974, 1 / 3, "Levinson: one third"),
    (1989, 2 / 5, "Conrey: two fifths"),
    (2011, 0.41, "Bui, Conrey and Young: past 41 percent"),
    (2012, 0.4128, "Feng"),
    (2020, 5 / 12, "Pratt, Robles, Zaharescu and Zeindler: five twelfths"),
    (2026, 2 / 3, "this paper: two thirds, simple and on the line"),
)

#: quoted: the record for distinct zeros before 2026 (Farmer 1995, Wu 2015)
DISTINCT_BEFORE = {1995: 0.6395, 2015: 0.6603}

#: quoted: Montgomery 1973 had 2/3 simple *assuming* the Riemann hypothesis;
#: Montgomery-Taylor 1975 pushed that conditional constant to 0.6725
CONDITIONAL_SIMPLE_1973 = 2 / 3

#: quoted for context (not from the paper): the first 10 trillion zeros have
#: been checked numerically and all sit on the line (Gourdon 2004)
ZEROS_CHECKED_NUMERICALLY = 10 ** 13

# --- the 2026 paper's constants ----------------------------------------------

#: computed: the shape function at dial one, the headline proportion
NEW_PROPORTION = shape_h(1.0)                     # 2/3

#: computed: the distinct-zero proportion at dial one
NEW_DISTINCT = shape_hd(1.0)                      # 5/6

#: computed: the Cauchy-Schwarz shape at dial one
CS_AT_ONE = shape_f(1.0)                          # 3/4

#: computed: the optimised window constant 0.7532960...
MT_CONSTANT = montgomery_taylor_closed_form()

#: computed from it: the optimised proportions of Theorem D
MT_ON_LINE = 2 - 1 / MT_CONSTANT                  # 0.67250...
MT_DISTINCT = (3 - 1 / MT_CONSTANT) / 2           # 0.83625...

#: quoted: the hard ceiling for any certificate of the paper's kind
#: (bandwidth one, two moments; Remark 1.1, page 4)
METHOD_CEILING = 0.68185

#: quoted: the bandwidths Remark 1.1 says would be needed to reach higher
#: proportions by the same route
BANDWIDTH_NEEDED = {0.70: 1.04, 0.80: 1.26, 0.90: 1.70}

#: quoted: what the same machine gives for the derivative of the completed
#: zeta function (Remark 7.3, page 23): simple-and-on-line, then distinct
XI_PRIME_FLAT = (0.85838, 0.92919)
XI_PRIME_QUARTIC = (0.86864, 0.93432)

#: quoted: the previous record proportion, for the prose
OLD_RECORD = 5 / 12

#: quoted: the paper's energy identity at dial one: the prime-measured
#: energy per zero is four thirds
ENERGY_AT_ONE = 4 / 3

# --- history, in the order the guide tells it --------------------------------

MILESTONES = (
    (1859, "Riemann's eight-page memoir states the hypothesis in passing"),
    (1914, "Hardy proves infinitely many zeros sit on the line"),
    (1942, "Selberg proves a positive proportion does"),
    (1973, "Montgomery's pair correlation: two thirds simple, if RH holds"),
    (1974, "Levinson reaches one third unconditionally"),
    (1989, "Conrey reaches two fifths"),
    (2020, "Pratt, Robles, Zaharescu and Zeindler reach five twelfths"),
    (2024, "Baluyot, Goldston, Suriajaya and Turnage-Butterbaugh show "
           "Montgomery's prime side never needed RH"),
    (2026, "the zero side is replaced by linear algebra: two thirds, "
           "unconditionally"),
)

__all__ = [
    "BANDWIDTH_NEEDED", "CONDITIONAL_SIMPLE_1973", "CS_AT_ONE",
    "DISTINCT_BEFORE", "ENERGY_AT_ONE", "FIRST_ZERO", "METHOD_CEILING",
    "MILESTONES", "MT_CONSTANT", "MT_DISTINCT", "MT_ON_LINE",
    "NEW_DISTINCT", "NEW_PROPORTION", "OLD_RECORD", "RECORD_RACE",
    "SHIPPED_ZEROS", "XI_PRIME_FLAT", "XI_PRIME_QUARTIC",
    "ZEROS_CHECKED_NUMERICALLY",
]

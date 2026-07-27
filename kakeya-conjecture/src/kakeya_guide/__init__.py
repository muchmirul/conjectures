"""Code behind the zero-to-Kakeya-Conjecture visual guide.

Modules:

* `core`      exact rational geometry: slivers, unions of slivers, Perron trees
* `shapes`    the classical rooms (disc, triangle, deltoid) and what motion costs
* `dimension` box counting, Cantor sets, zero size with positive dimension
* `finite`    Kakeya sets on the grid F_q^n, and Dvir's polynomial method
* `examples`  the named objects the guide keeps coming back to
* `plotting`  the shared matplotlib palette and animation helpers

Everything the guide states about a computable object is re-derived here and
checked in `tests/`.
"""

__all__ = ["core", "shapes", "dimension", "finite", "examples", "plotting"]

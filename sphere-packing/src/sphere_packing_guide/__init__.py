"""Code behind the zero-to-sphere-packing-linear-program visual guide.

Modules:

* `core`      ball volumes, the certificate functions and their transforms,
              and the Mellin ingredients that fix the sharp radius
* `examples`  the named numbers the guide keeps coming back to
* `plotting`  the shared matplotlib palette and animation helpers

Everything the guide states about a computable object is re-derived here and
checked in `tests/`.  Claims that come from the literature instead of from this
code are marked as such in `notes/research-content.md`.
"""

__all__ = ["core", "examples", "plotting"]

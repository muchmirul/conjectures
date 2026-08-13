"""Named facts from the lectures, in one place, with where each one lives.

The guide quotes numbers and statements in its prose, and a quoted thing in
two files drifts.  Everything the article asserts about the lectures is
recorded here once, with the numbered result it comes from, and the tests
read this file rather than the prose.

`SOURCE` entries point at a numbered result of

    Peter Scholze, "Lectures on Condensed Mathematics",
    arXiv:2605.03658v1, May 2026

and the page numbers are the printed pages of that PDF.
"""

from __future__ import annotations

ARXIV = "https://arxiv.org/abs/2605.03658"
PDF = "https://arxiv.org/pdf/2605.03658v1"


def pdf_page(page: int) -> str:
    """A link that opens the lectures at one printed page."""
    return f"{PDF}#page={page}"


#: Every result the guide names, as
#: key -> (what the guide calls it, the lectures' label, printed page)
SOURCE: dict[str, tuple[str, str, int]] = {
    "site": ("the probe list", "Definition 1.2", 6),
    "space_to_condensed": ("a space read by probes", "Example 1.3", 7),
    "first_countable": ("one sequence is enough for a metric space",
                        "Remark 1.6", 9),
    "fully_faithful": ("no space is lost", "Proposition 1.7", 9),
    "two_real_lines": ("the two real lines", "Example 1.9", 9),
    "abelian": ("subtraction always works", "Theorem 1.10", 9),
    "abelian_kappa": ("subtraction always works, with the size bound fixed",
                      "Theorem 2.2", 11),
    "compact_hausdorff_site": ("compact shapes are probes too",
                               "Proposition 2.3", 11),
    "extremally_disconnected": ("a probe that never needs folding",
                                "Definition 2.4", 11),
    "stone_cech": ("the free unfoldable probe", "Example 2.5", 11),
    "no_convergence": ("nothing converges in an unfoldable probe",
                       "Warning 2.6", 12),
    "ed_site": ("unfoldable probes are enough", "Proposition 2.8", 12),
    "qcqs": ("compact shapes, exactly", "Theorem 2.16", 17),
    "torus_cohomology": ("the holes of a stack of circles",
                         "Proposition 3.1", 20),
    "cohomology_agrees": ("the holes are the ones you already knew",
                          "Theorem 3.2", 21),
    "real_cohomology": ("smooth measurements see no holes", "Theorem 3.3", 22),
    "lca_structure": ("what a locally compact group looks like",
                      "Theorem 4.1", 24),
    "torus_hom": ("the key computation", "Theorem 4.3", 25),
    "breen_deligne": ("the universal resolution", "Theorem 4.5", 25),
    "lca_faithful": ("locally compact groups embed", "Corollary 4.9", 27),
    "solid_def": ("the solid rule", "Definition 5.1", 33),
    "nobeling": ("every continuous integer function is a stack of steps",
                 "Theorem 5.4", 34),
    "free_solid_is_product": ("the free solid group is a product",
                              "Corollary 5.5", 34),
    "solid_free_is_solid": ("the free solid group really is solid",
                            "Proposition 5.7", 35),
    "solid_category": ("the solid category", "Theorem 5.8", 35),
    "solid_generators": ("what the building blocks are", "Corollary 6.1", 42),
    "real_solidifies_to_zero": ("the real line solidifies to nothing",
                                "Corollary 6.1 (iii)", 42),
    "solid_tensor": ("the completed tensor product", "Theorem 6.2", 43),
    "product_tensor": ("index sets multiply", "Proposition 6.3", 43),
    "tensor_examples": ("the multiplication table", "Example 6.4", 44),
    "solidify_a_shape": ("solidify a shape and its holes fall out",
                         "Example 6.5", 44),
    "measures_def": ("a theory of measures", "Definition 7.1", 45),
    "analytic_ring": ("an analytic ring", "Definition 7.4", 46),
    "analytic_examples": ("two that work", "Proposition 7.8", 48),
    "real_measures": ("the real line's own sizes", "Example 7.10", 49),
    "liquid": ("the real line does get a rule", "Theorem 7.11", 50),
    "solid_modules": ("solid modules over a polynomial ring",
                      "Theorem 8.1", 53),
    "compact_support": ("cohomology with compact support", "Theorem 8.2", 53),
    "serre_duality_local": ("duality, locally", "Remark 8.4", 54),
    "dualizing_formula": ("a new formula for the dualizing complex",
                          "Remark 8.5", 54),
    "huber_pairs": ("which subring you keep", "Proposition 9.2", 63),
    "gluing": ("the local pictures glue", "Theorem 9.8", 65),
    "coherent_duality": ("duality, globally", "Theorem 11.1", 71),
}


def cite(key: str) -> str:
    """A Markdown link to the numbered result behind one of the guide's claims."""
    _, label, page = SOURCE[key]
    return f"[{label}, page {page} of the lectures]({pdf_page(page)})"


# --- numbers the article quotes -------------------------------------------

#: The Cantor probe's finite pictures double at every level.
CANTOR_LEVEL_SIZES = [1, 2, 4, 8, 16, 32]

#: Example 6.4 of the lectures, as the guide names the objects.  The last
#: entry is written there with the variables the other way round, which is
#: the same object; this module always lists variables in sorted order so
#: that one object has exactly one name.
TENSOR_CLAIMS = [
    ("Z_p", "Z_l", "0"),
    ("Z_p", "R", "0"),
    ("Z_p", "Z_p", "Z_p"),
    ("Z_p", "Z[[T]]", "Z_p[[T]]"),
    ("Z[[U]]", "Z[[T]]", "Z[[T,U]]"),
]

#: Homology of the shapes the guide solidifies (Example 6.5), written as
#: (free rank, torsion orders) in degrees 0, 1, 2.
SHAPE_HOMOLOGY = {
    "circle": [(1, []), (1, [])],
    "figure eight": [(1, []), (2, [])],
    "sphere": [(1, []), (0, []), (1, [])],
    "torus": [(1, []), (2, []), (1, [])],
    "klein bottle": [(1, []), (1, [2]), (0, [])],
}

#: The exponent above which merging boxes can make a measure larger, so the
#: projective system stops making sense (Example 7.10).
MEASURE_EXPONENT_CEILING = 1.0

#: The record of what changed, for the closing chapter of part three.
TIMELINE = [
    (1950, "Specker", "a map out of a product only reads finitely many slots"),
    (1958, "Gleason", "the probes that never need folding"),
    (1968, "Nobeling", "continuous integer functions form a free group"),
    (1979, "Ribe", "an extension that is complete but not convex"),
    (2019, "Clausen and Scholze",
     "the Bonn course these lectures record"),
    (2026, "Scholze", "this stable version of the notes"),
]

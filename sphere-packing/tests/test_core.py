"""Every number the guide quotes about room, certificates and the sharp radius.

The rule for this repo is that a sentence in the article and a test in here
must not be able to disagree.  Where a claim is somebody else's theorem the
test checks the *arithmetic we do with it*, never the theorem itself.
"""

import math

import numpy as np
import pytest

from sphere_packing_guide.core import (alpha_star, ball_fraction_of_cube,
                                       ball_volume, ball_volume_root,
                                       certificate, density_bound, digamma,
                                       eigenfunction, exponent_advantage,
                                       harmonic_mass, harmonic_measure,
                                       is_admissible, lattice_density,
                                       log_potential, log_potential_numeric,
                                       logistic_characteristic,
                                       logistic_density, lp_rate,
                                       lp_rate_from_pieces, mellin_multiplier,
                                       radial_fourier_1d, radial_fourier_3d,
                                       saddle_radius_constant, seed_certificate,
                                       seed_exists, sphere_area,
                                       stirling_volume_root, transform,
                                       transform_coeffs, wallis_integral)
from sphere_packing_guide.examples import (ALPHA_STAR, ALPHA_STAR_PRINTED,
                                           FOUND_BOUNDS, FOUND_CERTIFICATES,
                                           KL_EXPONENT, KNOWN_DENSITIES,
                                           LP_RATE, SEED_FAILS_FROM,
                                           SIGN_RADIUS,
                                           SIMPLE_CERTIFICATE_DIMS,
                                           SIMPLE_CERTIFICATE_LIMIT,
                                           known_density, simple_bound)


# --- how much room a ball has (chapters 2 and 3) ---------------------------

def test_low_dimensional_ball_volumes_are_the_familiar_ones():
    assert ball_volume(1) == pytest.approx(2.0)
    assert ball_volume(2) == pytest.approx(math.pi)
    assert ball_volume(3) == pytest.approx(4 * math.pi / 3)
    assert ball_volume(4) == pytest.approx(math.pi ** 2 / 2)
    assert ball_volume(8) == pytest.approx(math.pi ** 4 / 24)


def test_the_ball_volume_peaks_at_dimension_five_then_falls():
    volumes = [ball_volume(d) for d in range(1, 21)]
    assert volumes.index(max(volumes)) == 4          # index 4 is dimension 5
    assert all(volumes[i] > volumes[i + 1] for i in range(4, 19))


def test_the_ball_eventually_fills_almost_none_of_its_box():
    assert ball_fraction_of_cube(2) == pytest.approx(0.7853981, abs=1e-6)
    assert ball_fraction_of_cube(3) == pytest.approx(0.5235987, abs=1e-6)
    assert ball_fraction_of_cube(10) < 0.0025
    assert ball_fraction_of_cube(30) < 1e-13
    assert ball_fraction_of_cube(40) < 1e-20


def test_sphere_area_is_the_derivative_of_ball_volume():
    for d in range(1, 12):
        assert sphere_area(d) == pytest.approx(d * ball_volume(d))


def test_stirling_matches_the_true_volume_root_in_high_dimensions():
    for d in (100, 1000, 10_000):
        assert ball_volume_root(d) == pytest.approx(stirling_volume_root(d),
                                                    rel=0.03)
    # and the agreement improves as the dimension grows
    errors = [abs(ball_volume_root(d) / stirling_volume_root(d) - 1)
              for d in (100, 1000, 10_000)]
    assert errors[0] > errors[1] > errors[2]


# --- packings whose answer is known (chapter 1) ----------------------------

def test_the_known_densities_come_back_out_of_their_lattices():
    for d, (_, density, _) in KNOWN_DENSITIES.items():
        assert known_density(d) == pytest.approx(density, rel=1e-12)


def test_the_hexagonal_packing_beats_the_square_one():
    square = ball_volume(2) * 0.5 ** 2 / 1.0        # one circle per unit square
    assert known_density(2) > square
    assert known_density(2) == pytest.approx(0.9068996, abs=1e-6)
    assert square == pytest.approx(0.7853981, abs=1e-6)


def test_density_falls_off_a_cliff_with_dimension():
    assert known_density(3) == pytest.approx(0.7404804, abs=1e-6)
    assert known_density(8) == pytest.approx(0.2536695, abs=1e-6)
    assert known_density(24) == pytest.approx(0.0019295, abs=1e-6)


# --- the certificate basis (chapters 4 and 5) ------------------------------

def test_the_building_blocks_are_their_own_fourier_transforms_up_to_sign():
    """The sign flip rule, checked against direct integration.

    `transform_coeffs` claims that the k-th building block transforms into
    itself times minus one to the k.  Dimensions one and three let us check
    that without any Bessel function library.
    """
    for k in range(4):
        f = certificate([0] * k + [1], 1)
        for rho in (0.0, 0.3, 0.9, 1.7):
            expected = (-1) ** k * float(f(rho))
            assert radial_fourier_1d(f, rho) == pytest.approx(expected, abs=1e-7)
    for k in range(4):
        f = certificate([0] * k + [1], 3)
        for rho in (0.4, 1.1, 2.0):
            expected = (-1) ** k * float(f(rho))
            assert radial_fourier_3d(f, rho) == pytest.approx(expected, abs=1e-6)


def test_transforming_twice_gives_back_the_original():
    coeffs = [0.7, -0.2, 0.4, 0.1]
    assert transform_coeffs(transform_coeffs(coeffs)) == pytest.approx(coeffs)


def test_the_eigenfunctions_start_at_the_expected_height():
    for d in (1, 2, 3, 8):
        assert float(eigenfunction(0, d, 0.0)) == pytest.approx(1.0)
        assert float(eigenfunction(1, d, 0.0)) == pytest.approx(d / 2)


# --- the simplest certificate, and its limits (chapter 4) ------------------

def test_the_simple_certificate_obeys_both_sign_rules_up_to_dimension_six():
    for d in SIMPLE_CERTIFICATE_DIMS:
        assert is_admissible(_simple(d), d)
    assert SIMPLE_CERTIFICATE_LIMIT == 6


def test_the_simple_certificate_breaks_in_dimension_seven():
    """Its transform at the centre turns negative once the dimension passes 2 pi."""
    assert 6 < 2 * math.pi < 7
    assert not is_admissible(_simple(7), 7)


def test_the_simple_certificate_is_useless_in_four_of_its_six_dimensions():
    """Above one it proves nothing, because density is at most one anyway.

    The article says it gives news only in dimensions four and five, so that
    split is pinned here.
    """
    useless = [d for d in SIMPLE_CERTIFICATE_DIMS if simple_bound(d) > 1.0]
    useful = [d for d in SIMPLE_CERTIFICATE_DIMS if simple_bound(d) <= 1.0]
    assert useless == [1, 2, 3, 6]
    assert useful == [4, 5]
    assert simple_bound(4) == pytest.approx(0.8488, abs=1e-4)
    assert simple_bound(5) == pytest.approx(0.8055, abs=1e-4)


def _simple(d):
    from sphere_packing_guide.core import simple_certificate
    return simple_certificate(d)


def test_the_found_certificates_obey_both_rules_at_high_resolution():
    """The recorded certificates, re-checked far past the grid that found them.

    A search that is allowed right up to the constraint always finds something
    that passes on its own grid and fails on a finer one, so the recorded
    answers are re-checked here on a grid thirty times finer and three times
    wider than the one used during the search.
    """
    for d, coeffs in FOUND_CERTIFICATES.items():
        assert is_admissible(coeffs, d, outer=24.0, samples=600_000)


def test_the_found_certificates_prove_the_bounds_the_article_quotes():
    for d, expected in FOUND_BOUNDS.items():
        assert density_bound(FOUND_CERTIFICATES[d], d) == pytest.approx(
            expected, abs=5e-7)


def test_the_found_bounds_are_true_but_not_sharp():
    """Each bound sits above the density that is actually achievable."""
    for d, expected in FOUND_BOUNDS.items():
        assert expected > known_density(d)
    # in the plane the gap is under half a percentage point
    assert FOUND_BOUNDS[2] - known_density(2) < 0.005


def test_the_density_bound_is_the_stated_ratio():
    coeffs = FOUND_CERTIFICATES[2]
    f = certificate(coeffs, 2)
    fhat = transform(coeffs, 2)
    expected = ball_volume(2) * float(f(0.0)) / (2 ** 2 * float(fhat(0.0)))
    assert density_bound(coeffs, 2) == pytest.approx(expected)


def test_the_starting_certificate_runs_out_before_dimension_six():
    """Why the search cannot even begin in dimension eight."""
    assert all(seed_exists(d) for d in (1, 2, 3, 4, 5))
    assert not seed_exists(SEED_FAILS_FROM)
    assert not seed_exists(8)
    assert is_admissible(seed_certificate(2), 2, margin=1e-4)


# --- the Mellin ingredients (chapters 8 and 9) -----------------------------

def test_the_mellin_multiplier_only_rotates_on_the_real_axis():
    for lam in (0.5, 1.0, 4.0, 12.0):
        for t in (-3.1, -0.4, 0.0, 0.7, 5.5):
            assert abs(mellin_multiplier(lam, t)) == pytest.approx(1.0, abs=1e-9)


def test_the_logistic_density_is_a_probability_density():
    u = np.linspace(-80, 80, 400_001)
    assert float(np.trapezoid(logistic_density(u), u)) == pytest.approx(1.0, abs=1e-9)
    assert float(np.min(logistic_density(u))) >= 0.0


def test_the_logistic_density_has_the_stated_fourier_side():
    """Its characteristic function is the argument over its sinh."""
    u = np.linspace(-80, 80, 400_001)
    for t in (0.3, 1.0, 2.2):
        got = float(np.trapezoid(logistic_density(u) * np.cos(t * u), u))
        assert got == pytest.approx(logistic_characteristic(t), abs=1e-9)


def test_the_log_potential_has_the_digamma_closed_form():
    for x in (0.05, 0.3, 0.5, 1.0, 2.0):
        assert log_potential(x) == pytest.approx(log_potential_numeric(x), abs=1e-7)


def test_digamma_agrees_with_its_defining_recurrence():
    for x in (0.4, 1.0, 2.7, 9.3):
        assert digamma(x + 1) - digamma(x) == pytest.approx(1 / x, abs=1e-12)


def test_harmonic_measure_carries_the_stated_non_unit_mass():
    for sigma in (-0.5, 0.0, 0.4, 0.8):
        assert harmonic_mass(sigma) == pytest.approx((1 - sigma) / 2, abs=1e-9)
    assert float(np.min(harmonic_measure(0.4, np.linspace(-50, 50, 1001)))) > 0


def test_wallis_gives_the_saddle_displacement():
    assert wallis_integral() == pytest.approx(math.log(math.pi / 2), abs=1e-8)


def test_the_gaussian_radius_moves_exactly_to_one_over_pi():
    assert saddle_radius_constant() == pytest.approx(1 / math.pi, rel=1e-14)
    assert SIGN_RADIUS == pytest.approx(0.3183098, abs=1e-7)


# --- what the two directions add up to (chapters 10 and 11) ----------------

def test_the_pieces_multiply_to_the_stated_rate():
    for d in (10_000, 1_000_000):
        assert lp_rate_from_pieces(d) == pytest.approx(lp_rate(), rel=1e-12)


def test_the_rate_is_root_e_over_two_pi():
    assert LP_RATE == pytest.approx(math.sqrt(math.e / (2 * math.pi)), rel=1e-15)
    assert LP_RATE == pytest.approx(0.6577446, abs=1e-7)


def test_the_exponent_matches_the_digits_the_paper_prints():
    assert ALPHA_STAR == pytest.approx(alpha_star())
    assert f"{ALPHA_STAR:.18f}".startswith(ALPHA_STAR_PRINTED[:18])
    assert ALPHA_STAR == pytest.approx(0.604400544291677695, rel=1e-15)


def test_the_rate_and_the_exponent_are_two_ways_of_saying_one_thing():
    """Two to the minus alpha star is the same number as the rate over one."""
    assert 2 ** -ALPHA_STAR == pytest.approx(LP_RATE, rel=1e-14)


def test_the_new_exponent_beats_the_one_from_1978():
    assert ALPHA_STAR > KL_EXPONENT
    assert ALPHA_STAR - KL_EXPONENT == pytest.approx(0.00534478, abs=1e-8)


def test_how_much_the_improvement_is_worth_in_high_dimensions():
    """The article quotes these three factors, so they are pinned here."""
    assert exponent_advantage(100, KL_EXPONENT, ALPHA_STAR) == pytest.approx(
        0.6904, abs=1e-4)
    assert exponent_advantage(1000, KL_EXPONENT, ALPHA_STAR) == pytest.approx(
        0.02461, abs=1e-5)
    assert 1 / exponent_advantage(1000, KL_EXPONENT, ALPHA_STAR) == pytest.approx(
        40.6, abs=0.1)

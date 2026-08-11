"""Re-derive every number the guide quotes, from scratch, on this machine.

The layout follows the article: zeta and its zeros first, then the explicit
formula, then the paper's constants, then the toy listening experiment, then
the linear-algebra lemmas under random attack.
"""

import math

import numpy as np
import pytest

from zeta_guide import core as C
from zeta_guide import examples as E


# --- zeta and the shipped zeros ---------------------------------------------

def test_the_zero_table_matches_mpmath_and_the_classical_values():
    """A sample of shipped heights, recomputed live with the root finder."""
    import mpmath

    mpmath.mp.dps = 20
    zs = C.zero_heights()
    assert len(zs) == 300
    # the classical first three, to the digits every reference prints
    assert zs[0] == pytest.approx(14.134725141734693, abs=1e-9)
    assert zs[1] == pytest.approx(21.022039638771554, abs=1e-9)
    assert zs[2] == pytest.approx(25.010857580145688, abs=1e-9)
    for n in (1, 7, 50, 300):
        live = float(mpmath.zetazero(n).imag)
        assert zs[n - 1] == pytest.approx(live, abs=1e-9)


def test_zeta_vanishes_at_the_shipped_heights():
    """Every shipped height really is a zero, and really is on the line."""
    import mpmath

    mpmath.mp.dps = 15
    for g in C.zero_heights():
        assert abs(complex(mpmath.zeta(0.5 + 1j * g))) < 1e-9


def test_the_guides_zeta_agrees_with_mpmath():
    """The Euler-Maclaurin recipe against independent software."""
    import mpmath

    mpmath.mp.dps = 20
    for s in (0.5 + 14.1j, 0.5 + 99.7j, 0.9 + 33.3j, 0.1 + 21.0j,
              2.0 + 0.0j, 0.5 + 250.2j):
        ours = C.zeta_em(s)
        theirs = complex(mpmath.zeta(s))
        assert ours == pytest.approx(theirs, abs=1e-8)


def test_the_counting_formula_matches_the_zero_table():
    """The Riemann-von Mangoldt main term against the real counts."""
    for t1, t2 in ((0, 100), (100, 200), (100, 300), (200, 400), (0, 500)):
        true = C.zero_count(t1, t2)
        predicted = C.counting_main_term(max(t1, 2), t2)
        assert abs(true - predicted) < 2.0, (t1, t2, true, predicted)


def test_the_zeros_thicken_the_way_the_formula_says():
    """Higher stretches hold more zeros: the count from 100 to 200 exceeds
    the count from 0 to 100, as the log factor demands."""
    assert C.zero_count(100, 200) > C.zero_count(0, 100)


# --- the explicit formula, seen ----------------------------------------------

def test_adding_zero_waves_improves_the_prime_staircase():
    xs = np.linspace(2.0, 50.0, 700)
    target = C.psi_staircase(xs)
    errors = [np.sqrt(np.mean((C.psi_from_waves(xs, k) - target) ** 2))
              for k in (0, 5, 20, 100)]
    assert errors[1] < errors[0]
    assert errors[2] < errors[1]
    assert errors[3] < errors[2]
    # with a hundred waves the rebuild is genuinely close
    assert errors[3] < 0.35


def test_the_prime_density_peaks_at_the_zero_heights():
    """The spikes point at the zeros, at the resolution the primes allow.

    With only the primes up to 13 playing, the profile resolves heights to
    about two units, so two crowded zeros merge into one broad spike between
    them.  The honest checks: every spike sits within 0.65 of a true zero,
    and every isolated zero (no neighbour within 2) gets a spike within
    0.35 of it.
    """
    taus = np.linspace(100.0, 140.0, 8001)
    dens = C.prime_density(taus, 16)
    peaks = taus[1:-1][(dens[1:-1] > dens[:-2]) & (dens[1:-1] > dens[2:])]
    zs = np.array([g for g in C.zero_heights() if 95 <= g <= 145])
    for p in peaks:
        assert np.min(np.abs(zs - p)) < 0.65, p
    for g in zs:
        if 101 <= g <= 139 and np.sort(np.abs(zs - g))[1] > 2.0:
            assert np.min(np.abs(peaks - g)) < 0.35, g


# --- the paper's constants ----------------------------------------------------

def test_the_shape_function_gives_the_papers_constants():
    assert C.shape_h(1.0) == pytest.approx(2 / 3)
    assert C.shape_hd(1.0) == pytest.approx(5 / 6)
    assert C.shape_f(1.0) == pytest.approx(3 / 4)
    # the dial's natural setting is the best setting
    lams = np.linspace(0.05, 1.0, 500)
    assert max(C.shape_h(l) for l in lams) == pytest.approx(C.shape_h(1.0))


def test_the_budget_assembly():
    """Four, minus two, minus the energy, is the shape function."""
    for lam in (0.4, 0.7, 1.0):
        assert 4 - 2 - C.energy_per_count(lam) == pytest.approx(
            C.shape_h(lam))
    assert C.energy_per_count(1.0) == pytest.approx(E.ENERGY_AT_ONE)


def test_the_fejer_integral_gives_four_thirds():
    """The numerical pair-correlation integral plus the diagonal, per the
    square of the dial, reproduces the energy at several dial values."""
    for lam in (0.5, 0.8, 1.0):
        energy = (lam + C.fejer_integral(lam)) / lam ** 2
        assert energy == pytest.approx(C.energy_per_count(lam), abs=1e-6)


def test_the_crossover_dial_value():
    """The paper's three-minus-root-six: below it the weaker certificate
    beats the distinct-shape, above it the roles flip."""
    x = C.CROSSOVER_DIAL
    assert x == pytest.approx(3 - math.sqrt(6))
    assert C.shape_hd(x) == pytest.approx(C.shape_f(x), abs=1e-12)
    assert C.shape_hd(x + 0.01) > C.shape_f(x + 0.01)
    assert C.shape_hd(x - 0.01) < C.shape_f(x - 0.01)


def test_the_window_functional_at_the_flat_window():
    """The flat window scores exactly three quarters at dial one."""
    s = np.linspace(-0.5, 0.5, 4001)
    v = np.ones_like(s)
    assert C.window_functional(v, s) == pytest.approx(0.75, abs=2e-4)


def test_the_optimised_window_constant():
    closed = C.montgomery_taylor_closed_form()
    assert closed == pytest.approx(0.7532960, abs=1e-7)
    assert C.montgomery_taylor_constant() == pytest.approx(closed, abs=2e-4)
    assert E.MT_ON_LINE == pytest.approx(0.67250, abs=1e-5)
    assert E.MT_DISTINCT == pytest.approx(0.83625, abs=1e-5)
    # nearby windows score worse: perturb the optimiser several ways
    s = np.linspace(-0.5, 0.5, 2001)
    best = np.cos(math.sqrt(2) * s)
    score = C.window_functional(best, s)
    for other in (np.ones_like(s), np.cos(1.1 * math.sqrt(2) * s),
                  np.cos(0.9 * math.sqrt(2) * s), 1 - 1.8 * s ** 2,
                  np.cos(math.sqrt(2) * s) ** 2):
        assert C.window_functional(np.clip(other, 0, None), s) < score + 1e-9


def test_the_whole_number_trick():
    for m in range(1, 40):
        assert C.whole_number_charge(m) >= C.whole_number_floor(m)
    assert C.whole_number_charge(1) == C.whole_number_floor(1)
    assert C.whole_number_charge(2) == C.whole_number_floor(2)
    assert C.whole_number_charge(3) > C.whole_number_floor(3)


def test_the_record_race_numbers():
    race = dict((y, v) for y, v, _ in E.RECORD_RACE)
    assert race[1974] == pytest.approx(1 / 3)
    assert race[1989] == pytest.approx(2 / 5)
    assert race[2020] == pytest.approx(5 / 12)
    assert race[2026] == pytest.approx(2 / 3)
    assert E.OLD_RECORD == pytest.approx(0.41666, abs=1e-4)
    # the race is monotone: no later record is smaller
    vals = [v for _, v, _ in E.RECORD_RACE]
    assert vals == sorted(vals)


def test_the_ceiling_and_the_gap():
    """Both new constants sit under the method's ceiling, which sits under
    one; the flat-window 2/3 is within the 0.016 the paper states."""
    assert 2 / 3 < E.MT_ON_LINE < E.METHOD_CEILING < 1
    assert E.METHOD_CEILING - 2 / 3 == pytest.approx(0.01518, abs=1e-4)
    assert E.METHOD_CEILING - 2 / 3 < 0.016
    assert E.METHOD_CEILING - E.MT_ON_LINE < 0.01


# --- the toy listening experiment ---------------------------------------------

@pytest.fixture(scope="module")
def toy():
    fam = C.ToyFamily(T=100.0, dial=1.0)
    Gz = fam.table_from_zeros(fam.real_zero_config(40, 400))
    return fam, Gz


def test_prime_side_equals_zero_side_at_toy_height(toy):
    """The flagship check, the paper's section 8 item (1), at our height:
    the two computations share no input and agree to a few parts in a
    hundred million."""
    fam, Gz = toy
    Gp = fam.table_from_primes()
    disc = np.max(np.abs(Gz - Gp)) / np.max(np.abs(Gz))
    assert disc < 1e-6


def test_the_trace_tracks_the_zero_count(toy):
    """The diagonal total is the window constant times the window length
    times the zeros in the stretch, up to edge effects."""
    fam, Gz = toy
    us = np.linspace(-fam.L / 2, fam.L / 2, 4001)
    a = float(np.trapezoid(fam.window(us) ** 2, us)) / fam.L
    n = C.zero_count(100, 200)
    assert float(np.trace(Gz)) == pytest.approx(a * fam.L * n, rel=0.04)


def test_an_on_line_zero_makes_a_bowl(toy):
    fam, _ = toy
    one = fam.table_from_zeros([(150.0 + 0j, 1)])
    ev = np.linalg.eigvalsh(one)
    assert np.all(ev > -1e-10)
    assert int(np.sum(ev > 1e-9)) == 1


def test_an_off_line_pair_makes_a_saddle(toy):
    fam, _ = toy
    pair = fam.table_from_zeros([(150.0 + 0.3j, 1)])
    ev = np.linalg.eigvalsh(pair)
    assert int(np.sum(ev > 1e-9)) == 1
    assert int(np.sum(ev < -1e-9)) == 1


def test_the_real_table_is_a_sum_of_bowls(toy):
    """Built from genuine zeros, every direction curves up or is flat."""
    _, Gz = toy
    assert np.all(np.linalg.eigvalsh(Gz) > -1e-9)


def test_the_certificate_never_exceeds_the_truth_on_synthetic_configurations(toy):
    """The paper's section 8 item (5), at toy height: pairing and doubling
    always lower the certificate, never raise it above the truth."""
    fam, Gz = toy
    base = [g for g in C.zero_heights() if 40 <= g <= 400]
    n_stretch = C.zero_count(100, 200)

    def full_count(zeros):
        """The configuration's own full count in the stretch: multiplicity
        counts, and a mirror pair is two pins (the paper's N(I'))."""
        return sum(m * (2 if abs(complex(g).imag) > 1e-12 else 1)
                   for g, m in zeros if 100 <= complex(g).real <= 200)

    def cert(zeros):
        return (C.cs_certificate(fam.table_from_zeros(zeros))
                - full_count(zeros))

    real = cert([(complex(g), 1) for g in base])
    assert 0 < real <= n_stretch

    paired = cert([(g + 0.25j, 1) for g in base])
    assert paired <= 0

    doubled = cert([(complex(g), 2) for g in base])
    assert doubled <= 0 + 1e-9

    half = cert([(complex(g), 1) if i % 2 else (g + 0.25j, 1)
                 for i, g in enumerate(base)])
    truth_half = sum(1 for i, g in enumerate(base)
                     if i % 2 and 100 <= g <= 200)
    assert half <= truth_half


def test_the_see_saw_bound_on_synthetic_configurations(toy):
    """Positive directions never exceed distinct points: Sylvester's law
    in the form the paper's Proposition 4.1 uses, checked on mixtures."""
    fam, _ = toy
    rng = np.random.default_rng(3)
    base = [g for g in C.zero_heights() if 90 <= g <= 210]
    for trial in range(3):
        config = []
        distinct = 0
        for g in base:
            kind = rng.integers(0, 3)
            if kind == 0:
                config.append((complex(g), 1))
                distinct += 1
            elif kind == 1:
                config.append((complex(g), 2))
                distinct += 1
            else:
                config.append((g + 0.2j, 1))
                distinct += 2
        G = fam.table_from_zeros(config)
        assert C.positive_directions(G, theta=1e-6) <= distinct


# --- the linear-algebra lemmas under random attack ----------------------------

def _random_instance(rng, d=12):
    r = int(rng.integers(1, d + 1))
    V = rng.normal(size=(d, r)) * rng.choice([0.25, 1.0, 3.0])
    P = V @ V.T
    b = int(rng.integers(0, 4))
    W = rng.normal(size=(d, b)) if b else np.zeros((d, 1))
    U = rng.normal(size=(d, int(rng.integers(1, 3))))
    Q = W @ W.T - U @ U.T * rng.choice([0.0, 0.7, 2.0])
    return P, Q


def test_the_rank_trace_inequality_on_random_instances():
    """Lemma 3.2 with c = 2: the floor never exceeds the true rank."""
    rng = np.random.default_rng(11)
    for _ in range(4000):
        P, Q = _random_instance(rng)
        b = int(np.sum(np.linalg.eigvalsh(Q) > 1e-9))
        floor = C.rank_trace_floor(P, Q, b)
        rank = int(np.linalg.matrix_rank(P, tol=1e-9))
        assert rank >= floor - 1e-7


def test_the_rank_trace_equality_case():
    """The paper's stated equality case: P a projection, Q twice an
    orthogonal projection."""
    d, r, b = 9, 3, 2
    P = np.diag([1.0] * r + [0.0] * (d - r))
    Q = np.diag([0.0] * r + [2.0] * b + [0.0] * (d - r - b))
    assert C.rank_trace_floor(P, Q, b) == pytest.approx(r)


def test_the_cauchy_schwarz_count_on_random_instances():
    """Lemma 3.3: the thresholded count against its quadratic floor."""
    rng = np.random.default_rng(5)
    for _ in range(2000):
        d = int(rng.integers(3, 14))
        A = rng.normal(size=(d, d))
        R = (A + A.T) / 2 + np.diag(rng.uniform(0, 2, d))
        theta = float(rng.uniform(0, 0.4))
        if np.trace(R) <= theta * d:
            continue
        floor = (np.trace(R) - theta * d) ** 2 / np.trace(R @ R)
        count = int(np.sum(np.linalg.eigvalsh(R) > theta))
        assert count >= floor - 1e-9


def test_weyls_lemma_on_random_instances():
    """Lemma 3.4: a perturbation no bigger than the threshold cannot
    manufacture positive directions."""
    rng = np.random.default_rng(9)
    for _ in range(1000):
        d = int(rng.integers(3, 12))
        A = rng.normal(size=(d, d))
        A = (A + A.T) / 2
        F = rng.normal(size=(d, d))
        Err = (F + F.T) / 2
        norm = float(np.max(np.abs(np.linalg.eigvalsh(Err))))
        theta = norm * float(rng.uniform(1.0, 2.0))
        lhs = int(np.sum(np.linalg.eigvalsh(A + Err) > theta))
        rhs = int(np.sum(np.linalg.eigvalsh(A) > 0))
        assert lhs <= rhs

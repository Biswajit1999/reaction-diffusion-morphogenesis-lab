import numpy as np
import pytest

from research.gray_scott_robustness import (
    evolve, homogeneous_euler_limit, laplacian9, seed_fields,
    spectrum_diagnostics, stencil_eigenvalue, step, time_step_convergence,
)


def test_laplacian_conserves_periodic_sum_and_constant():
    rng = np.random.default_rng(42)
    f = rng.normal(size=(16, 20))
    assert abs(laplacian9(f).sum()) < 1e-12
    assert np.max(abs(laplacian9(np.ones((12, 12))))) < 1e-14


def test_exact_fourier_eigenvalue():
    n = 32
    y, x = np.indices((n, n))
    kx, ky = 2 * np.pi * 3 / n, 2 * np.pi * 5 / n
    f = np.cos(kx * x + ky * y)
    assert laplacian9(f) == pytest.approx(stencil_eigenvalue(kx, ky) * f, abs=1e-13)


def test_stencil_extreme_and_browser_dt_instability_risk():
    assert stencil_eigenvalue(np.pi, np.pi) == pytest.approx(-1.6)
    assert homogeneous_euler_limit(1, .5, .055, .062) > 1
    assert homogeneous_euler_limit(1.5, .5, .055, .062) < 1


def test_high_frequency_diffusion_mode_grows_above_euler_limit():
    n = 32
    yy, xx = np.indices((n, n))
    mode = (-1.) ** (xx + yy)
    a = 1 + 1e-4 * mode
    b = np.zeros_like(a)
    after, _ = step(a, b, da=1.5, db=.5, feed=.055, kill=.062, dt=1)
    assert np.std(after) > np.std(a)
    safe, _ = step(a, b, da=1.5, db=.5, feed=.055, kill=.062, dt=.5)
    assert np.std(safe) < np.std(a)


def test_unclipped_reaction_diffusion_mass_balance():
    rng = np.random.default_rng(11)
    a = rng.uniform(.2, .9, size=(16, 16))
    b = rng.uniform(.05, .5, size=(16, 16))
    # With feed=kill=0, reaction transfers A to B and periodic diffusion
    # conserves their combined sum to rounding error.
    a1, b1 = step(a, b, feed=0, kill=0, dt=.2)
    assert (a1 + b1).sum() == pytest.approx((a + b).sum(), abs=1e-12)


def test_timestep_refinement():
    r = time_step_convergence(n=32, time=12.)
    e = r['rms_to_finest']
    assert e[0] > e[1] > e[2] > e[3] == 0


def test_spectrum_sinusoid_and_axis_swap():
    n = 64
    x = np.arange(n)
    f = np.tile(np.cos(2 * np.pi * 4 * x / n), (n, 1))
    s = spectrum_diagnostics(f)
    assert s['dominant_frequency_cycles_per_cell'] == pytest.approx(4 / n)
    assert s['dominant_wavelength_cells'] == pytest.approx(n / 4)
    assert s['spectral_anisotropy'] == pytest.approx(1)
    assert spectrum_diagnostics(f.T)['spectral_anisotropy'] == pytest.approx(-1)


def test_spectrum_rejects_constant_and_bad_shape():
    with pytest.raises(ValueError):
        spectrum_diagnostics(np.ones((16, 16)))
    with pytest.raises(ValueError):
        laplacian9(np.ones((3, 5)))


def test_seeded_evolution_deterministic():
    a, b = seed_fields(24)
    x1, y1 = evolve(a, b, time=5., dt=.5)
    x2, y2 = evolve(a, b, time=5., dt=.5)
    assert np.array_equal(x1, x2) and np.array_equal(y1, y2)
    assert np.isfinite(x1).all() and np.isfinite(y1).all()

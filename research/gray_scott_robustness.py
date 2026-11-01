"""Reproducible Gray–Scott numerical diagnostics matching the browser stencil.

Periodic nine-point stencil: centre -1, axial neighbours 0.2 each,
corner neighbours 0.05 each. The browser uses explicit Euler dt=1 and
clips both fields to [0, 1.2]; this research integrator leaves clipping
OFF to expose numerical instability rather than hide it.
"""
from __future__ import annotations

import numpy as np


def laplacian9(field: np.ndarray) -> np.ndarray:
    """Nine-point periodic stencil in units of one browser grid cell."""
    f = np.asarray(field, dtype=float)
    if f.ndim != 2 or min(f.shape) < 4 or not np.isfinite(f).all():
        raise ValueError('expected finite 2D field at least 4x4')
    axial = sum(np.roll(f, s, axis=a) for a in (0, 1) for s in (-1, 1))
    corners = sum(np.roll(np.roll(f, sy, axis=0), sx, axis=1)
                  for sy in (-1, 1) for sx in (-1, 1))
    return -f + .2 * axial + .05 * corners


def stencil_eigenvalue(kx: np.ndarray | float, ky: np.ndarray | float) -> np.ndarray:
    """Exact Fourier eigenvalue for the browser's periodic nine-point stencil."""
    return -1 + .4 * (np.cos(kx) + np.cos(ky)) + .2 * np.cos(kx) * np.cos(ky)


def homogeneous_euler_limit(da: float, db: float, feed: float, kill: float) -> float:
    """Linear Euler dt bound around A=1, B=0 (not nonlinear stability proof).

    At that equilibrium, the Jacobian is diagonal with eigenvalues
    D_A*lambda-F and D_B*lambda-(F+k). The most negative stencil eigenvalue
    is -1.6, giving dt <= min(2/(1.6*DA+F), 2/(1.6*DB+F+k)).
    """
    values = np.array([da, db, feed, kill], dtype=float)
    if not np.isfinite(values).all() or (values < 0).any() or da == 0 or db == 0:
        raise ValueError('require finite nonnegative parameters and positive diffusion')
    return float(min(2 / (1.6 * da + feed), 2 / (1.6 * db + feed + kill)))


def seed_fields(n: int = 64) -> tuple[np.ndarray, np.ndarray]:
    """Deterministic central patch; not a biological observation."""
    if n < 16:
        raise ValueError('n must be at least 16')
    yy, xx = np.indices((n, n))
    radius2 = (xx - n / 2)**2 + (yy - n / 2)**2
    b = np.where(radius2 < (n / 10)**2, .7, 0.)
    a = np.where(radius2 < (n / 10)**2, .5, 1.)
    return a, b


def step(a: np.ndarray, b: np.ndarray, *, da: float = 1., db: float = .5,
         feed: float = .055, kill: float = .062, dt: float = .5) -> tuple[np.ndarray, np.ndarray]:
    """One unclipped explicit-Euler update; never silently clips divergences."""
    if np.shape(a) != np.shape(b) or not np.isfinite(dt) or dt <= 0:
        raise ValueError('matching fields and positive dt required')
    if min(da, db, feed, kill) < 0 or not np.isfinite([da, db, feed, kill]).all():
        raise ValueError('invalid coefficients')
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    reaction = a * b * b
    next_a = a + dt * (da * laplacian9(a) - reaction + feed * (1 - a))
    next_b = b + dt * (db * laplacian9(b) + reaction - (feed + kill) * b)
    if not np.isfinite(next_a).all() or not np.isfinite(next_b).all():
        raise FloatingPointError('non-finite Euler update')
    return next_a, next_b


def evolve(a: np.ndarray, b: np.ndarray, *, time: float, dt: float, **kwargs) -> tuple[np.ndarray, np.ndarray]:
    """Evolve to an exact requested time using an integer number of steps."""
    nsteps = round(time / dt)
    if time <= 0 or nsteps < 1 or not np.isclose(nsteps * dt, time, rtol=0, atol=1e-10):
        raise ValueError('time must be a positive integer multiple of dt')
    a, b = np.array(a, dtype=float, copy=True), np.array(b, dtype=float, copy=True)
    for _ in range(nsteps):
        a, b = step(a, b, dt=dt, **kwargs)
    return a, b


def time_step_convergence(*, n: int = 40, time: float = 24.,
                          steps: tuple[float, ...] = (1., .5, .25, .125)) -> dict[str, list[float]]:
    """Compare finite-dt solutions to the smallest-step reference at fixed T."""
    if len(steps) < 3 or any(d <= 0 for d in steps) or sorted(steps, reverse=True) != list(steps):
        raise ValueError('descending positive steps required')
    a0, b0 = seed_fields(n)
    solutions = [evolve(a0, b0, time=time, dt=d) for d in steps]
    ref_a, ref_b = solutions[-1]
    errors = [float(np.sqrt(np.mean((a - ref_a)**2 + (b - ref_b)**2)))
              for a, b in solutions]
    return {'steps': list(steps), 'rms_to_finest': errors}


def spectrum_diagnostics(field: np.ndarray) -> dict[str, float]:
    """Non-DC 2D Fourier power and dominant spatial frequency (cycles/cell).

    Dominant wavelength and kx/ky second moments are descriptive morphology
    diagnostics, not a classification of Turing instability or biology.
    """
    f = np.asarray(field, dtype=float)
    if f.ndim != 2 or min(f.shape) < 8 or not np.isfinite(f).all():
        raise ValueError('finite 2D field >=8x8 required')
    power = np.abs(np.fft.fft2(f - np.mean(f)))**2
    power[0, 0] = 0
    total = float(power.sum())
    if total <= 1e-20:
        raise ValueError('field has no measurable spatial variation')
    ky = np.fft.fftfreq(f.shape[0])[:, None]
    kx = np.fft.fftfreq(f.shape[1])[None, :]
    idx = np.unravel_index(np.argmax(power), power.shape)
    dominant = float(np.hypot(kx[0, idx[1]], ky[idx[0], 0]))
    x2 = float((power * kx**2).sum() / total)
    y2 = float((power * ky**2).sum() / total)
    return {'dominant_frequency_cycles_per_cell': dominant,
            'dominant_wavelength_cells': float(1 / dominant),
            'kx2_power_moment': x2, 'ky2_power_moment': y2,
            'spectral_anisotropy': float((x2 - y2) / (x2 + y2)),
            'field_variance': float(np.var(f))}

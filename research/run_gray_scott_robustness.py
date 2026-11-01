"""Reproducible synthetic Gray–Scott stability, convergence and morphology report."""
import json
from pathlib import Path

from research.gray_scott_robustness import (
    evolve, homogeneous_euler_limit, seed_fields,
    spectrum_diagnostics, time_step_convergence,
)


def main() -> None:
    a, b = seed_fields(64)
    _, final_b = evolve(a, b, time=60, dt=.5)
    payload = {
        'data_kind': 'deterministic_synthetic_Gray_Scott',
        'stencil': 'periodic 9-point (-1 centre, 0.2 axial, 0.05 diagonal)',
        'browser_dt': 1.0, 'browser_clips_to': [0, 1.2],
        'research_integrator_clips': False,
        'homogeneous_euler_dt_limit_default': homogeneous_euler_limit(1, .5, .055, .062),
        'homogeneous_euler_dt_limit_high_DA': homogeneous_euler_limit(1.5, .5, .055, .062),
        'time_step_convergence': time_step_convergence(),
        'morphology_spectrum': spectrum_diagnostics(final_b),
        'limitations': 'Linear homogeneous equilibrium bound, not full nonlinear stability proof; no biological data.',
    }
    out = Path('results/gray_scott_robustness.json')
    out.parent.mkdir(exist_ok=True, parents=True)
    out.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    print(json.dumps({'dt_limit_default': payload['homogeneous_euler_dt_limit_default'],
                      'dt_limit_high_DA': payload['homogeneous_euler_dt_limit_high_DA'],
                      'rms_to_finest': payload['time_step_convergence']['rms_to_finest']}))


if __name__ == '__main__':
    main()

# Research Quality Upgrade

This repository has been upgraded with a compact research-quality layer: reference anchors, validation checks, and explicit scientific/software boundaries.

## Scope

Gray-Scott reaction-diffusion lab for nonlinear pattern formation, stability and morphogenesis visualisation.

## Equations And Models

- du/dt = Du laplacian(u) - uv^2 + F(1-u)
- dv/dt = Dv laplacian(v) + uv^2 - (F+k)v

## Reference Anchors

The file `data/research-reference.json` stores benchmark anchors used by `scripts/validate_repository.mjs`. These are intentionally small and auditable so the repository can be checked without network access.

## Browser Upgrade

If this repository contains a browser interface, `research-overlay.js` adds a non-invasive mission-control quality panel with validation status and benchmark telemetry.

## References

- Pearson, J.E., 1993. Complex patterns in a simple system. Science, 261(5118), pp.189-192.

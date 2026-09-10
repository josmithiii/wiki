---
title: Ladder Nonlinearity Ablation
created: 2026-09-10
updated: 2026-09-10
type: comparison
tags: [ladder-filter, nonlinear, tpt-zdf, spice, benchmark, comparison]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_29.pdf
  - raw/DAFx26_paper_29.txt
---

# Ladder Nonlinearity Ablation

A controlled structure/function ablation on one fixed digital ladder core,
answering which nonlinear design choices actually change the sound. Companion to
[[moog-ladder-filter-models]], which supplies the SPICE reference, the metrics
and the cross-implementation results.[^1]

## Common-core ablation (Zavalishin TPT/ZDF core, Newton-Raphson solve)

Only saturator function and placement change; state update and feedback topology
are fixed. Spectra / Cutoff / Drive in %H1:[^1]

| Variant | Spectra | Cutoff | Drive |
|---|---|---|---|
| 1+4 stage tanh (baseline) | 0.05 | 0.14 | 0.06 |
| 1+4 stage atan | 0.59 | 3.07 | 1.33 |
| 1+4 stage soft clip $u/(1+\lvert u\rvert)$ | 0.96 | 7.04 | 1.98 |
| tanh(in) + tanh(FB) (JUCE-like) | 0.29 | 1.98 | 1.71 |
| tanh(in + FB) | 0.38 | 2.17 | 1.71 |
| partial ablations (2 or 3 stages linearized) | 0.17-0.34 | 1.09-2.33 | 1.48-2.92 |

All three saturators share unit origin slope and $\pm 2V_T$ asymptotes, differing
only in curvature - yet swapping tanh for soft clip is worse than moving the
nonlinearity to the boundaries: function and placement are partly independent
levers. **Stage result:** keeping the nonlinear input stage and linearizing
ladder stages, removing the *later* stages stays closest to SPICE (stages 3,4
linearized: 0.20 %H1; stages 1,2,3: 0.34 %). Earlier stages see larger
excursions before the lowpass sections attenuate, so they dominate harmonic
balance.

## Fidelity-versus-cost guidance

1. Boundary saturation can look fine linearly and in averaged summaries while
   missing the analog nonlinear operating behavior.
2. Cutting the nonlinear budget is stage-dependent, not interchangeable: keep
   **earlier-stage** nonlinearity first; several such variants match or beat
   boundary saturation at the same nonlinear count.
3. Preserving *distributed placement* matters at least as much as matching the
   exact saturator law.

**Limitations:** SPICE is a simulation baseline, not measured hardware (no
tolerances, mismatch, $V_T$ drift, parasitics); static/quasi-static only;
aliasing is deliberately not an axis (it depends on each model's internal
oversampling); H2-H9 RMSE is comparative, not an audibility threshold - no
listening tests. Testbench: `https://github.com/oyama/ladder-filter-testbench`.

## See also

[[moog-ladder-filter-models]] - [[tpt-zdf-filters]] - [[virtual-analog-overview]]

## References

[^1]: [[entities/source-papers#paper-oyama-moog-ladder-nonlinearity-2026]] - Oyama, "Quantifying Nonlinear Behavior in Digital Moog Ladder Filters", DAFx26.

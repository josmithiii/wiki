---
title: Stochastic Modal Synthesis
created: 2026-04-10
updated: 2026-04-10
type: concept
tags: [modal-synthesis, acoustics, physical-modeling, dsp, vibration]
sources: []
---

# Stochastic Modal Synthesis

At high frequencies, individual modes become too dense to resolve or control
individually. Stochastic methods model the aggregate behavior of many
overlapping modes as filtered noise, bridging modal synthesis and statistical
approaches.

## Mode Density and the Schroeder Frequency

Mode density increases with frequency and object dimensionality:
- 1D (string, tube): constant mode spacing $= c / (2L)$
- 2D (plate, membrane): mode density $\sim f$ (grows linearly)
- 3D (room, solid): mode density $\sim f^2$ (grows quadratically)

The **Schroeder frequency** $f_S$ marks where modes begin to overlap:
- $f_S = 2000\sqrt{T_{60} / V}$ for rooms ($V$ = volume in m³)
- Below f_S: individual modes are resolvable → deterministic modal synthesis
- Above f_S: modes overlap heavily → statistical/stochastic treatment

## Statistical Energy Analysis (SEA)

SEA models energy flow between coupled subsystems at high frequencies:
- Each subsystem characterized by modal density $n(f)$, damping $\eta$, and input power
- Energy balance: $P_{\text{in}} = P_{\text{diss}} + P_{\text{coupled}}$
- Coupling loss factors $\eta_{ij}$ govern energy exchange between subsystems
- Output: average energy per subsystem, not individual mode amplitudes
- Developed for aerospace vibro-acoustics as early as Lyon (1975)

### Connection to Modal Synthesis
- SEA gives the spectral envelope (energy density vs. frequency)
- Modal synthesis provides the fine structure (individual peaks)
- Hybrid: deterministic modes below crossover, noise-shaped envelope above

## Noise-Band Synthesis Above the Mode Resolution Limit

When individual modes cannot be resolved:
- Model the contribution as filtered noise with the correct spectral envelope
- Envelope shape follows the modal density and average damping
- Temporal envelope: exponential decay with frequency-dependent T60
- Phase is randomized — no individual resonance peaks

### Implementation
1. Compute modal density n(f) from geometry (analytic or FEM)
2. Estimate average damping eta(f) from material properties
3. Generate band-limited noise shaped by n(f) * |H_avg(f)|^2
4. Apply exponential decay envelope per frequency band
5. Add to deterministic low-frequency modal output

## Perceptual Justification

- Human frequency resolution (ERB) broadens with frequency
- Above ~2-4 kHz, individual partials of most objects are unresolvable
- Noise-band representation is perceptually transparent in this range
- Significant computational savings: $O(B)$ bands vs. $O(N)$ modes, $B \ll N$

## Texture Synthesis for Contact Sounds

Rolling, scraping, and sliding produce quasi-stationary stochastic excitation:
- Surface texture → stochastic force signal → drives modal resonators
- The excitation is noise-like; the response retains modal coloring
- Can be modeled as: y(t) = noise(t) * h_modal(t)
- Related to granular synthesis but with physical motivation

## Related Concepts
- [[modal-synthesis-overview]] — deterministic modal synthesis
- [[damping-models]] — damping determines crossover frequency
- [[radiation-and-directivity]] — high-frequency radiation characteristics
- [[material-properties-and-modes]] — mode density depends on material/geometry
- [[realtime-modal-synthesis]] — computational budget motivates the crossover

## References
[^1]: Lyon, R.H. (1975). "Statistical Energy Analysis of Dynamical Systems." MIT Press.
[^2]: Schroeder, M.R. (1962). "Frequency-Correlation Functions of Frequency Responses in Rooms." JASA.
[^3]: Traer, J. & McDermott, J.H. (2016). "Statistics of natural reverberation enable perceptual separation of sound and space." PNAS.

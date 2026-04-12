---
title: SMS — Sines Plus Noise (Plus Transients)
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [sms, sinusoidal, residual, applications]
sources:
  - /w/sasp/sms-intro.tex
  - /w/sasp/sms-overview.tex
  - /w/sasp/sms-analysis.tex
  - /w/sasp/sms-sines-plus-noise.tex
  - /w/sasp/sms-sines-plus-noise-plus-transients.tex
  - /w/sasp/snt.tex
---

# SMS — Sines Plus Noise (Plus Transients)

**Spectral Modeling Synthesis** (Serra, 1989) extends sinusoidal
modeling by adding a **stochastic residual** for the noise-like part
of a sound that sinusoids can't capture. Later extended with a
**transient** layer for attacks.

## Decomposition

$$x(n) \;=\; \underbrace{\sum_p A_p(n)\cos\phi_p(n)}_{\text{deterministic (sines)}} \;+\; \underbrace{e(n)}_{\text{stochastic}} \;+\; \underbrace{t(n)}_{\text{transients (optional)}}$$

- **Sines**: tracked partials via [[sinusoidal-modeling]] + QIFFT
- **Residual** $e(n)$: $x(n) -$ resynthesized sines
- **Transients** $t(n)$: sharp onsets pulled out separately to avoid
  smearing

## Analysis Pipeline

1. Run sinusoidal analysis on $x$.
2. Resynthesize deterministic part $s(n)$ (oscillator bank or IFFT).
3. **Time-align** and subtract: $e(n) = x(n) - s(n)$.
4. Characterize the residual as filtered noise — fit a **spectral
   envelope** to $|E_m(k)|$ per frame (LPC, cepstrum, or line segments).
5. Optionally detect transients (energy / spectral-flux spikes) and
   model them separately.

## Residual Model

The residual is treated as **wide-sense stationary noise within a
frame**, colored by a per-frame envelope $H_m(\omega)$:
$$E_m(\omega) \;=\; H_m(\omega)\cdot N_m(\omega)$$
where $N_m$ is white noise. Resynthesis:
- Generate white noise, STFT it, shape by $H_m$, inverse STFT.
- Or: add randomized magnitude + random phase spectra per frame.

Phase information in the residual is discarded — noise is
characterized entirely by its magnitude envelope.

## Why Model Transients Separately

- Sines blur attacks (window must be long to resolve partials).
- Noise model averages over frames, destroying sharp onsets.
- Pre-extract transients via onset detection, store as short PCM
  fragments or as spectral "impulses", subtract, then model the
  remainder with sines + noise.

SMS-T (sines + noise + transients) is the basis of many modern
time-scale and pitch-scale algorithms.

## Resynthesis

$$\hat{x}(n) \;=\; s(n) + e(n) + t(n)$$
with:
- $s$ from oscillator bank / IFFT synthesis
- $e$ from filtered noise
- $t$ from stored transients, time-aligned

Time-scaling and pitch-shifting act on each layer **independently**:
- Sines: interpolate $A, f, \phi$ at new rate (see [[sinusoidal-parameter-interpolation]])
- Noise: stretch the envelope, regenerate noise
- Transients: kept at original rate (time-scaled only in position)

This separation is why SMS gives higher-quality time-stretching than
pure phase vocoders on percussive or noisy material.

## Applications

- High-quality time/pitch scaling of speech and music
- Sound morphing between two recordings (interpolate each layer)
- Instrument modeling (deterministic = harmonics, stochastic = bow noise)
- Compression (parametric audio coding)

## Related Concepts
- [[sinusoidal-modeling]] — deterministic layer
- [[noise-spectrum-analysis]] — stochastic layer analysis
- [[phase-vocoder-and-tsm]] — compare; SMS is an alternative
- [[f0-and-spectral-envelope]] — envelope estimation for residual

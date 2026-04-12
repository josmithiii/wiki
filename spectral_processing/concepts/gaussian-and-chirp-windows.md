---
title: Gaussian and Chirp Windows
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [gauss, windows, main-lobe]
sources:
  - /w/sasp/gauss.tex
  - /w/sasp/gauss-intro.tex
  - /w/sasp/gauss-elementary.tex
  - /w/sasp/gauss-complex.tex
  - /w/sasp/gauss-chirp.tex
  - /w/sasp/chirplets.tex
---

# Gaussian and Chirp Windows

The Gaussian window is the theoretically "optimal" analysis window —
it saturates the time-frequency uncertainty principle and makes QIFFT
peak estimation exact. Its complex-chirp generalization underlies
**chirplet** analysis of frequency-swept signals.

## Gaussian Window

$$w(n) \;=\; e^{-\tfrac{1}{2}(n/\sigma)^2}$$

- Fourier transform of a Gaussian is a Gaussian:
$$W(\omega) \;=\; \sigma\sqrt{2\pi}\; e^{-\tfrac{1}{2}\sigma^2\omega^2}$$
- In **dB** (log-magnitude), the transform is an **exact parabola**:
$$20\log_{10}|W(\omega)| \;=\; \text{const} - \tfrac{1}{2}\sigma^2\omega^2 \cdot \tfrac{20}{\ln 10}$$
- This is why [[qifft-peak-estimation]] (which fits parabolas to
  log magnitude) is **exact** for Gaussian windows.

## Uncertainty Principle

Duration-bandwidth product:
$$\Delta t \cdot \Delta\omega \;\ge\; \tfrac{1}{2}$$
with equality for the Gaussian. No window can be simultaneously more
concentrated in both domains.

## Practical Drawback

The Gaussian has **no finite support** — it must be truncated, which
introduces discontinuities $\Rightarrow$ leakage. Typical choice:
truncate at $\pm 3\sigma$ to $\pm 4\sigma$ (extremely close to zero).

The **Kaiser** window is a near-optimal, finite-support approximation
of a time-limited Gaussian and is usually used in practice.

## Complex Gaussian and Modulation

Multiply by a complex exponential to heterodyne:
$$w_c(n) \;=\; e^{-\tfrac{1}{2}(n/\sigma)^2}\, e^{j\omega_0 n}$$
- Still Gaussian in magnitude; analytic signal.
- Spectrum is a Gaussian centered at $\omega_0$.

## Chirp Gaussian (Chirplet)

Add a **quadratic phase** term:
$$w_{\text{chirp}}(n) \;=\; e^{-\tfrac{1}{2}(n/\sigma)^2}\, e^{j(\omega_0 n + \tfrac{1}{2}\alpha n^2)}$$

- $\alpha$ = chirp rate (rad/sample$^2$).
- Spectrum is a (rotated) Gaussian in the time-frequency plane, tilted
  along a line of slope $\alpha$.
- Matches the local structure of a frequency-swept sinusoid
  (glissando, FM tone, bird song).

## Chirplet Analysis

Generalized STFT using chirp-Gaussian atoms:
$$C(m, k, \alpha) \;=\; \sum_n x(n)\, \overline{w_{\text{chirp}}(n - mR;\, \omega_k, \alpha)}$$

Search over $(m, k, \alpha)$ to find the best chirplet for each time
slot. Yields sharper representations for chirps than classical STFT.
Applied to:
- Time-varying pitch analysis (vibrato, glissando)
- Radar signals
- Transient detection
- Compressed sensing of wave packets

**Time-frequency reassignment** + Gaussian window yields similar
sharpening without the search.

## Relationship to Wigner Distribution

The Gaussian-windowed spectrogram is a Gaussian-smoothed Wigner
distribution; the Gaussian is the unique window that yields a
non-negative smoothed TFD without cross-terms of a single Gaussian
atom.

## Related Concepts
- [[spectrum-analysis-windows]] — window zoo including Kaiser
- [[qifft-peak-estimation]] — parabolic interpolation, exact for Gaussian
- [[short-time-fourier-transform]] — host transform

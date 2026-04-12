---
title: Sinusoidal Modeling
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [sinusoidal, peak-detection, parshl, stft]
sources:
  - /w/sasp/sinespecanal.tex
  - /w/sasp/additivesynth.tex
  - /w/sasp/parshl.tex
  - /w/sasp/peaks.tex
---

# Sinusoidal Modeling

Model a sound as a sum of time-varying sinusoids:
$$x(n) \;\approx\; \sum_{p=1}^{P(n)} A_p(n)\cos\!\big[\phi_p(n)\big]$$
where $P(n)$ partials are born, evolve, and die over time. The
canonical pipeline is **analysis → peak tracking → resynthesis**.

## Pipeline

1. **STFT** with a long, low-leakage window (Hann, Blackman, Kaiser)
   and heavy zero-padding. See [[spectrum-analysis-windows]],
   [[zero-padding-and-interpolation]].
2. **Peak picking** in each frame: find local maxima of $|X_m(k)|$
   above threshold.
3. **Parabolic (quadratic) interpolation** around each peak bin to
   get amplitude, frequency, phase. See [[qifft-peak-estimation]].
4. **Peak matching / tracking**: link peaks across frames into
   partials (tracks).
5. **Birth/death logic**: tracks start when a new peak appears and
   end when no match is found within a frequency tolerance.
6. **Resynthesis**: IFFT-based or oscillator-bank.

## Peak-to-Partial Matching

For frame $m \to m+1$, for each active partial at frequency $f_p(m)$:
- Search frame $m+1$ peaks within $\Delta f$ of $f_p(m)$.
- Best match = closest frequency (optionally amplitude-weighted).
- Unmatched peaks spawn new tracks; unmatched tracks die (fade out).

Typical $\Delta f$: a fraction of the bin spacing, e.g. $0.1\cdot f_s/M$.

## PARSHL

**PA**rtial **R**esynthesis **SH**ell (Smith & Serra, 1987) — the
original sinusoidal analyzer/synthesizer that set the template for
modern sinusoidal and SMS systems. Key ideas:
- Zero-padded FFT + parabolic peak interpolation.
- Guide-track matching with frequency tolerance.
- Linear amplitude, cubic phase interpolation for resynthesis.
- Birth/death with fade-in/fade-out envelopes.

See [[sms-sines-plus-noise]] for the SMS extension with a noise residual.

## Choice of Window

| Goal | Window |
|------|--------|
| Sharp peaks, few partials | Rectangular (but aliasing-prone) |
| Well-separated partials | Hann (good resolution, decent side lobes) |
| Crowded spectra | Blackman / Blackman-Harris (flat tops, low leakage) |
| Tunable trade-off | Kaiser ($\beta \sim 9$) |

Window length ≥ 4 periods of the lowest partial being tracked.

## Limits

- **Unresolved partials**: if frequency spacing < main-lobe width,
  QIFFT biases both peaks.
- **Fast transients**: sinusoidal model blurs attacks; add a
  **transient model** (see [[sms-sines-plus-noise]]).
- **Modulations**: heavy vibrato/tremolo blurs peaks; use
  multi-resolution STFT or chirplets ([[gaussian-and-chirp-windows]]).

## Applications

- Sound modeling, morphing, cross-synthesis
- Time-scale and pitch-scale modification (outside phase vocoder)
- Source separation guided by tracks
- Spectral envelope estimation via partial amplitudes
- Physical model calibration from recorded tones

## Related Concepts
- [[qifft-peak-estimation]] — the core estimator
- [[sinusoidal-parameter-interpolation]] — resynthesis interpolation
- [[sms-sines-plus-noise]] — sinusoidal + residual
- [[f0-and-spectral-envelope]] — harmonic structure extraction

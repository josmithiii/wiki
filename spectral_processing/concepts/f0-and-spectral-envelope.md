---
title: f0 Estimation and Spectral Envelope
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [f0-estimation, spec-envelope]
sources:
  - /w/sasp/f0est.tex
  - /w/sasp/tf0est.tex
  - /w/sasp/mlpitch.tex
  - /w/sasp/specenv.tex
  - https://ccrma.stanford.edu/~jos/sasp/Spectral_Envelope_Extraction.html
  - https://ccrma.stanford.edu/~jos/sasp/Fundamental_Frequency_Estimation_Spectral.html
---

# f0 Estimation and Spectral Envelope

Two complementary aspects of a voiced sound: the **fundamental
frequency** $f_0$ (pitch) and the **spectral envelope** (timbre /
formants). Separating them is the basis of vocoders, cross-synthesis,
pitch shifting, and speech coding.

## Fundamental Frequency Estimation

### Time-domain methods
- **Autocorrelation**: peak of $r_{xx}(\tau)$ at $\tau = 1/f_0$.
- **YIN**: cumulative mean normalized difference function,
  $d(\tau) = \sum[x(n) - x(n+\tau)]^2$, normalized; pick first dip.
- **Zero-crossing**: cheap, noise-prone, only for clean signals.

### Frequency-domain methods
- **Harmonic matching**: fit an ideal harmonic comb $k f_0$ to
  detected spectral peaks; pick $f_0$ maximizing total matched
  amplitude.
- **Approximate maximum likelihood from peaks** ([SASP](https://ccrma.stanford.edu/~jos/sasp/Fundamental_Frequency_Estimation_Spectral.html)): histogram the
  differences between measured peak frequencies to get the most common
  harmonic spacing, then refine by least-squares regression of the
  line $f_k = k f_0$ through the harmonic peaks (slope $= f_0$).
- **Cepstral f0**: the first significant quefrency peak above the
  envelope cut-off corresponds to the fundamental period.

### Robustness Tricks
- Median-filter the $f_0$ track to remove octave errors.
- Downsample before autocorrelation to focus on voiced band.
- Bias toward previous frame's $f_0$ (temporal smoothing / Viterbi).

## Spectral Envelope Estimation

The spectral envelope $E(\omega)$ is the smooth magnitude shape
underneath the harmonic structure — roughly the vocal tract / body
response.

### Linear Prediction (LPC)
Model $x$ as all-pole filtered white noise:
$$X(z) \;\approx\; \frac{G}{1 - \sum_{k=1}^p a_k z^{-k}}$$
- Solve normal equations (Levinson-Durbin) from autocorrelation.
- Order $p \approx f_s/1000$ for speech (e.g., $p=10$ at 10 kHz).
- Envelope = magnitude response of the all-pole filter.
- **Peak-sensitive** — follows formants tightly.

### Cepstral Smoothing
$$c(n) \;=\; \operatorname{IDFT}\!\big(\log|X(k)|\big)$$
- Envelope = low quefrency portion (liftering).
- Harmonics = high quefrency.
- Low-pass ("lifter") the cepstrum with cutoff $n_c$ below the pitch
  period $f_s/f_0$ samples to keep only the envelope.
- Less tied to all-pole assumption; works for non-speech too.

### Discrete / True Envelope
- Iterate cepstral smoothing, replacing low-magnitude points with
  previous envelope, until the envelope touches all harmonic peaks
  from above. Avoids dipping between peaks.

### Channel Vocoder Bank
- Smooth $|X_m(k)|$ in $k$ with a fixed filter bank $\Rightarrow$
  coarse envelope per critical band.
- Used in classical vocoders ([[cross-synthesis-and-morphing]]).

## Relation to Sinusoidal Modeling

- $f_0$ tells [[sinusoidal-modeling]] which peaks are harmonics.
- Envelope can be fit to the partial amplitudes instead of the raw
  spectrum, yielding a cleaner curve.

## Applications

- **Pitch-preserving time-scale**: keep envelope, modify source.
- **Pitch shifting**: resample source, re-apply original envelope.
- **Voice conversion**: swap envelopes.
- **Speech coding**: transmit $f_0$ + envelope + residual energy.

## Related Concepts
- [[sinusoidal-modeling]] — harmonic partials
- [[cross-synthesis-and-morphing]] — source/filter recombination
- [[noise-spectrum-analysis]] — smoothing for non-harmonic parts
- [[sms-sines-plus-noise]] — envelope for residual

## JOS online books
- [[jos_books/entities/sasp-book|SASP]]: [F0 Estimation from Spectral Peaks](https://ccrma.stanford.edu/~jos/sasp/Fundamental_Frequency_Estimation_Spectral.html), [Fundamental Frequency Estimation](https://ccrma.stanford.edu/~jos/sasp/Fundamental_Frequency_Estimation.html), [Cepstral Windowing](https://ccrma.stanford.edu/~jos/sasp/Cepstral_Windowing.html), [Linear Prediction Spectral Envelope](https://ccrma.stanford.edu/~jos/sasp/Linear_Prediction_Spectral_Envelope.html)
- [[jos_books/entities/mdft-book|MDFT]]: [Autocorrelation](https://ccrma.stanford.edu/~jos/mdft/Autocorrelation.html)

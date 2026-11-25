---
title: Sinusoidal Modeling
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [sinusoidal, peak-detection, parshl, stft]
sources:
  - /w/sasp/sinespecanal.tex
  - /w/sasp/additivesynth.tex
  - /w/sasp/parshl.tex
  - /w/sasp/peaks.tex
  - https://ccrma.stanford.edu/~jos/sasp/PARSHL_Program.html
  - https://ccrma.stanford.edu/~jos/sasp/Spectrum_Analysis_Sinusoids.html
  - /l/dttd/DAFx26/ - DAFx26 papers catalogued in entities/source-papers.md
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

Typical $\Delta f$: a fraction of the side-lobe width $f_s/M$, e.g. $0.1\cdot f_s/M$.

## PARSHL

[PARSHL](https://ccrma.stanford.edu/~jos/sasp/PARSHL_Program.html) (Smith & Serra; written 1985, published ICMC 1987) — an
"inharmonic phase vocoder" built for piano modeling that set the template
for modern sinusoidal and SMS systems. It follows *partials* rather than
harmonics; the name is "partial" squeezed into the six-character filename
limit of the SAIL PDP-10. Key ideas:
- Zero-padded FFT + parabolic peak interpolation.
- Guide-track matching with frequency tolerance.
- Oscillator-bank resynthesis with linear amplitude interpolation; phase
  tracking (McAulay-Quatieri cubic phase) was added later by Serra.
- Birth/death with fade-in/fade-out envelopes.

See [[sms-sines-plus-noise]] for the SMS extension with a noise residual.

## Choice of Window

| Goal | Window |
|------|--------|
| Sharp peaks, few partials | Rectangular (narrowest main lobe, but $-13$ dB leakage) |
| Well-separated partials | Hann (good resolution, decent side lobes) |
| Crowded spectra | Blackman / Blackman-Harris (flat tops, low leakage) |
| Tunable trade-off | Kaiser ($\beta \sim 9$) |

Window length: $M \ge K f_s/\Delta f$ to resolve partials $\Delta f$ Hz apart,
where $K$ is the main-lobe width in bins (2 rectangular, 4 Hann/Hamming,
6 Blackman) — e.g. 4 periods of $f_0$ for a Hamming window on a harmonic tone.

## Limits

- **Unresolved partials**: if frequency spacing < main-lobe width,
  both peaks are biased in frequency and amplitude.
- **Fast transients**: sinusoidal model blurs attacks; add a
  **transient model** (see [[sms-sines-plus-noise]]).
- **Modulations**: heavy vibrato/tremolo blurs peaks; use
  multi-resolution STFT or chirplets ([[gaussian-and-chirp-windows]]).

## Applications

Sound modeling, morphing and [[cross-synthesis-and-morphing|cross-synthesis]];
time- and pitch-scale modification without a phase vocoder; track-guided
source separation; spectral envelopes from partial amplitudes; calibrating
physical models from recorded tones ([[modal_synthesis/concepts/modal-analysis-measurement|modal analysis]]).

## DAFx26 additions

- Caetano 2026 models instrument sounds with **polynomial AM-FM sinusoids** estimated by the **distribution derivative method**, capturing intra-frame modulation (especially in attacks) better than SM+ or eaQHM and scoring nearly indistinguishable from the originals in a MUSHRA test: [[entities/source-papers#paper-caetano-ddm-polynomial-amfm-2026]]
- On the additive-synthesis side, alias-free oscillator synchronization is obtained by a linear **spectral-resampling transform** on the Fourier-series coefficients of a bandlimited waveform: [[virtual_analog/entities/source-papers#paper-roth-alias-free-oscillator-sync-2026]]

## Related Concepts
- [[qifft-peak-estimation]] — the core estimator
- [[nonstationary-sinusoidal-estimation-ddm]] - intra-frame AM-FM estimation (DAFx26)
- [[sinusoidal-parameter-interpolation]] — resynthesis interpolation
- [[sms-sines-plus-noise]] — sinusoidal + residual
- [[f0-and-spectral-envelope]] — harmonic structure extraction

## JOS online books
- [[jos_books/entities/sasp-book|SASP]]: [Resolving Sinusoids](https://ccrma.stanford.edu/~jos/sasp/Resolving_Sinusoids.html), [Additive Synthesis Analysis](https://ccrma.stanford.edu/~jos/sasp/Additive_Synthesis_Analysis.html), [Tracking Sinusoidal Peaks in a Sequence of FFTs](https://ccrma.stanford.edu/~jos/sasp/Tracking_Sinusoidal_Peaks_Sequence.html), [The PARSHL Program](https://ccrma.stanford.edu/~jos/sasp/PARSHL_Program.html), [Spectral Modeling Synthesis](https://ccrma.stanford.edu/~jos/sasp/Spectral_Modeling_Synthesis.html)

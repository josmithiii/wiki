# Wiki Schema

## Domain
Spectral audio signal processing -- FFT-based analysis, modification, and resynthesis of music and audio signals. Covers the DFT/DTFT/STFT, spectrum analysis windows, overlap-add (OLA) and filter-bank summation (FBS) views of the STFT, sinusoidal and sines-plus-noise (SMS) modeling, peak detection and QIFFT, phase vocoder and time-scale modification, multirate filter banks, FIR/window design, and spectral modeling applications (cross-synthesis, spectral envelope, f0 estimation, audio coding). Adjacent: physical modeling (waveguide_synthesis, modal_synthesis), general DSP.

## Primary Source
Julius O. Smith III, *Spectral Audio Signal Processing* (SASP), LaTeX source at `/w/sasp/`.

## Context Budget
This wiki is used by agents with as little as 32k token context. Rules:
- **Read at most 3 wiki pages per query** -- if more are needed, synthesize from index summaries first
- **Split pages at 100 lines** -- break into sub-topics with cross-links
- **Keep index.md entries to one short line each** -- the index must fit in context alongside a few pages
- **Prefer dense, scannable content** -- bullet points over prose, tables over paragraphs

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `overlap-add.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **All math must be written in LaTeX**, using `$...$` for inline and
  `$$...$$` for display equations (rendered via MathJax by the HTML build).
  Use `\begin{aligned}...\end{aligned}` for multi-line equations.
  Do not use plain-text notation like `omega`, `X_m(k)`, `w[n]` -- write
  `$\omega$`, `$X_m(k)$`, `$w[n]$` instead.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources:
  - /w/sasp/<file>.tex
  - https://ccrma.stanford.edu/~jos/sasp/...
---
```

## Source Attribution
- Primary source is the SASP LaTeX book at `/w/sasp/`. Cite the specific
  `.tex` files a page distills in its `sources:` frontmatter list.
- Web version: `https://ccrma.stanford.edu/~jos/sasp/`.
- Use markdown footnotes in the body when citing a specific result.

## Tag Taxonomy

### Core transforms
- dft -- discrete Fourier transform
- dtft -- discrete-time Fourier transform
- stft -- short-time Fourier transform
- fft -- fast Fourier transform algorithms, zero-padding
- ft-theorems -- Fourier theorems (linearity, shift, modulation, convolution, Parseval)

### Windows & FIR design
- windows -- spectrum analysis windows (rectangular, Hann, Hamming, Blackman-Harris, Kaiser, Dolph-Chebyshev, DPSS)
- main-lobe -- main-lobe width, side-lobe level, trade-offs
- fir-design -- window method, frequency sampling, least-squares, linear programming, Parks-McClellan
- optimal-fir -- Chebyshev/minimax, L2, Hilbert transformers

### STFT interpretations
- ola -- overlap-add (transform) view of STFT
- fbs -- filter-bank summation (filter-bank) view of STFT
- cola -- constant overlap-add constraint
- perfect-reconstruction -- conditions for PR in analysis/resynthesis
- downsampling -- hop size, aliasing in STFT
- dft-filter-bank -- DFT filter bank derivation
- portnoff -- Portnoff window, modulated filter banks

### Sinusoidal & SMS modeling
- sinusoidal -- sinusoidal modeling, additive resynthesis
- qifft -- quadratically-interpolated FFT, peak estimation bias
- peak-detection -- spectral peak finding, parabolic interpolation
- sms -- sines + noise (+ transients) modeling
- residual -- stochastic/residual modeling
- f0-estimation -- fundamental frequency estimation
- spec-envelope -- spectral envelope estimation, LPC, cepstrum
- parshl -- PARSHL sinusoidal analyzer

### Phase vocoder & modifications
- phase-vocoder -- phase vocoder analysis/synthesis
- tsm -- time-scale modification
- cross-synthesis -- spectral cross-synthesis, morphing
- modifications -- spectral modifications, ifftsynth, oscillator bank
- phase-unwrap -- phase unwrapping

### Noise & statistical DSP
- noise -- noise spectrum analysis, averaging, Welch, Bartlett
- statistical-dsp -- expectation, variance, estimator bias
- gauss -- Gaussian and chirp-Gaussian theory
- bbt -- Blackman-Tukey spectrum estimation

### Filter banks
- filter-banks -- general filter bank theory
- multirate -- multirate filter banks, decimation, expansion, noble identities
- wavelets -- wavelets, constant-Q, auditory filter banks

### Applications
- audio-coding -- perceptual audio coding, MPEG/AAC basics
- loudness -- loudness and masking, auditory models
- applications -- spectrum-based synthesis, analysis, modification
- cross-synthesis -- cross-synthesis, convolution effects

### Meta
- history -- historical notes, futurists, Hammond, Telharmonium, voder/vocoder

## Directory Structure
- `entities/` -- specific methods, tools, historical items (e.g., PARSHL, phase vocoder)
- `concepts/` -- core theory and techniques
- `comparisons/` -- OLA vs FBS, sinusoidal vs SMS, etc.
- `queries/` -- curated entry points for common questions
- `raw/` -- optional cached raw sources (the book lives at `/w/sasp/`)

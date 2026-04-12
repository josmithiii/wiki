# TODO — Deferred Concepts

Topics that came up during the initial SASP ingest (2026-04-11) but were
merged or skipped. Candidates for standalone concept pages in a later pass.

## Deferred from initial ingest

- **Reassigned spectrogram / time-frequency reassignment** — currently
  mentioned briefly in [[qifft-peak-estimation]] and
  [[gaussian-and-chirp-windows]]. Deserves its own page covering the
  Auger-Flandrin reassignment method, instantaneous frequency/group delay
  estimators, and relationship to QIFFT.

- **FFT convolution in depth** — source `/w/sasp/fftconv.tex`.
  Currently folded into [[overlap-add-stft]]. A standalone page could
  cover overlap-add vs overlap-save, block sizes, zero-padding for
  linear convolution, and cost comparisons.

- **Nyquist windows / frequency-domain COLA duality** — sources
  `/w/sasp/poisson.tex`, `/w/sasp/nyquist.tex`. The dual of time-domain
  COLA (which governs OLA) is a frequency-domain Nyquist condition
  governing FBS. Worth a dedicated page tying Poisson summation, COLA,
  and the frequency-domain perfect-reconstruction constraint together.

## Other topics noticed but not ingested

- **Spectral modeling synthesis history** — `/w/sasp/sms-history.tex`,
  `/w/sasp/history-sasp.tex`, `/w/sasp/futurists.tex`,
  `/w/sasp/telharmonium.tex`, `/w/sasp/hammondorgan.tex`,
  `/w/sasp/voder.tex`. Would go in `entities/` or a dedicated history page.

- **PARSHL entity page** — `/w/sasp/parshl.tex`. The specific
  analyzer is referenced from [[sinusoidal-modeling]] but has no
  entity page of its own.

- **Linear programming for FIR design (deep dive)** —
  `/w/sasp/linprog-fir.tex`, `/w/sasp/linprog-doc.tex`,
  `/w/sasp/glpk-doc.tex`, `/w/sasp/gl-ck.tex`. Condensed into
  [[window-design-methods]]; could be expanded.

- **Chirplets and chirp-Gaussian theory** — `/w/sasp/chirplets.tex`,
  `/w/sasp/gauss-chirp.tex`. Briefly touched in
  [[gaussian-and-chirp-windows]].

- **Statistical DSP appendix** — `/w/sasp/statdsp.tex`,
  `/w/sasp/estimator-variance.tex`. Folded into
  [[noise-spectrum-analysis]]; could become its own foundations page.

- **Problem sets** — all `*-problems.tex` files intentionally skipped
  (exercises, not reference material).

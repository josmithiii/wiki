# Activity Log

## [2026-05-04] ingest | Laroche & Dolson 1999 improved phase-vocoder TSM
- Converted `/l/dttd/Improved_phase_vocoder_time-scale_modification_of_audio.pdf` with `pdf2txt.py` to `raw/Improved_phase_vocoder_time-scale_modification_of_audio.txt`.
- Added `raw/MANIFEST.md` and `raw/SUMMARIES.md` records for the PDF/text mapping and distillation notes.
- Created `entities/source-papers.md` with `paper-laroche-dolson-improved-pv-1999`.
- Updated `concepts/phase-vocoder-and-tsm.md` with the vertical phase-coherence diagnosis, identity/scaled phase locking summary, source citation, and source frontmatter.
- Updated `index.md` Entities with the new source catalog and paper anchor.

## [2026-04-11] create | spectral_processing sub-wiki scaffold
- SCHEMA.md, index.md, log.md, entities/, concepts/, comparisons/, queries/, raw/
- Primary source: /w/sasp/ (Spectral Audio Signal Processing book by JOS)
- Added to ~/wiki/README.md
- create concepts/sasp-overview.md — big picture, chapter map
- create concepts/dtft-and-fourier-theorems.md — four cases, DTFT, theorems, Poisson
- create concepts/zero-padding-and-interpolation.md — zp = spectral interp, min-zp tables
- create concepts/spectrum-analysis-windows.md — window zoo and trade-offs
- create concepts/window-design-methods.md — window method, LS, LP, Remez
- create concepts/short-time-fourier-transform.md — STFT definition and parameters
- create concepts/overlap-add-stft.md — OLA view, COLA, FFT convolution
- create concepts/filter-bank-summation-stft.md — FBS view, DFT filter bank, Portnoff
- create concepts/stft-modifications.md — safe modifications, IFFT synth, oscbank
- create concepts/sinusoidal-modeling.md — PARSHL pipeline, peak tracking
- create concepts/qifft-peak-estimation.md — parabolic peak interp, bias tables
- create concepts/sinusoidal-parameter-interpolation.md — McAulay-Quatieri cubic phase
- create concepts/sms-sines-plus-noise.md — SMS deterministic + stochastic + transients
- create concepts/phase-vocoder-and-tsm.md — phase vocoder, TSM, phase locking
- create concepts/cross-synthesis-and-morphing.md — vocoder-style effects and morphing
- create concepts/f0-and-spectral-envelope.md — f0 estimation, LPC, cepstrum
- create concepts/noise-spectrum-analysis.md — Welch, Bartlett, Blackman-Tukey
- create concepts/multirate-filter-banks.md — polyphase, noble ids, PR, wavelets
- create concepts/spectral-audio-applications.md — coding, loudness, vocoders, effects
- create concepts/gaussian-and-chirp-windows.md — Gaussian optimality, chirplets

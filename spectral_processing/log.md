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

## [2026-09-08] ingest | DAFx26 proceedings - pass 1 (catalog only)
- Source: /l/dttd/DAFx26/ (29th Int. Conf. on Digital Audio Effects, Cambridge MA, 1-4 Sept 2026), annotated bibliography at /l/dttd/DAFx26/README_JOS.md
- Copied 4 pdftotext extractions into raw/ (gitignored); added a DAFx26 section to raw/MANIFEST.md and raw/SUMMARIES.md.
- Appended 4 catalog entries to entities/source-papers.md: paper_34 (Caetano, distribution derivative method with polynomial AM-FM sinusoids), paper_02 (Apel, group delay manipulation with the Giant FFT), paper_21 (Nielsen, keyframe time stretching via extrema sampling), paper_44 (Badia, Belloch, Valimaki, parallel linear-phase octave filter bank).
- Added a cross-reference to paper_49 (Roth et al., alias-free oscillator synchronization via additive synthesis), catalogued in the new virtual_analog sub-wiki.
- Updated concepts/sinusoidal-modeling.md with a "DAFx26 additions" bullet list; added a DAFx26 see-also pointer plus a sources: entry to concepts/phase-vocoder-and-tsm.md and concepts/multirate-filter-banks.md (both at the 100-line limit, so the bullets stay in the source-papers entries).
- Updated index.md Entities with the four new source-paper anchors.
- Pass 2 (deep distillation of the three-star papers into concept pages) is pending.

## [2026-09-10] ingest | DAFx26 proceedings - pass 2 (deep distillation)
- Distilled four DAFx26 papers from /l/dttd/DAFx26/txt/ into new concept pages, one per paper, each citing its pass-1 catalog anchor in entities/source-papers.md.
- create concepts/nonstationary-sinusoidal-estimation-ddm.md (paper_34, Caetano) - polynomial modulation sinusoid model, the DDM integration-by-parts identity and its windowed-DFT linear system, window-derivative transform, alpha_0 by least squares, peak-selection thresholds, model order Q=3, the 39-sound SM+/eaQHM comparison (RMS-LSM, ISD, SRR) and the MUSHRA/ANOVA result.
- create concepts/giant-fft-group-delay-domain.md (paper_02, Apel) - group delay as temporal centre of gravity, the exactly invertible first-difference/cumulative-sum pair, zero padding against temporal aliasing after Valimaki et al., Gaussian-smoothed peak-region segmentation and group-delay grouping, and the three transformations (reordering, amplitude-proportional displacement, sinusoidal group-delay modulation).
- create concepts/extrema-sampling-time-stretch.md (paper_21, Nielsen) - B-spline bandlimited derivative and thresholded extrema, tangent-free smoothstep reconstruction, the keyframe-leash adaptive splice, the Cortex-M7 cost table, passthrough fidelity/THD numbers and the webMUSHRA plus LAT results.
- create concepts/linear-phase-octave-filter-bank-implementation.md (paper_44, Badia/Belloch/Valimaki) - stretched-FIR complementary cascade and its alignment shifts, blocked schedule with compact circular state, the OpenMP stage-block task graph with explicit dependencies and thread-local reduction, and the Jetson Orin Nano throughput/speedup/power/energy numbers.
- Added one-line see-also pointers (and bumped updated) in concepts/sinusoidal-modeling.md, concepts/qifft-peak-estimation.md, concepts/sinusoidal-parameter-interpolation.md, concepts/phase-vocoder-and-tsm.md, concepts/stft-modifications.md and concepts/multirate-filter-banks.md.
- index.md: four new Concepts entries; total pages 21 -> 25.

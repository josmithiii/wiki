# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Source book: Julius O. Smith III, *Spectral Audio Signal Processing* (`/w/sasp/`).
> Last updated: 2026-09-10 | Total pages: 25

## Entities
<!-- specific methods, tools, historical items -->
- [[source-papers]] — distilled source-paper catalog for spectral-processing research PDFs
- [paper-laroche-dolson-improved-pv-1999](entities/source-papers.md#paper-laroche-dolson-improved-pv-1999) — Laroche & Dolson 1999: vertical phase coherence diagnosis, identity/scaled phase locking, 50% overlap phase-vocoder TSM
- [paper-caetano-ddm-polynomial-amfm-2026](entities/source-papers.md#paper-caetano-ddm-polynomial-amfm-2026) - Caetano 2026: polynomial AM-FM sinusoids via the distribution derivative method; beats SM+ and eaQHM, MUSHRA-transparent
- [paper-apel-giant-fft-group-delay-2026](entities/source-papers.md#paper-apel-giant-fft-group-delay-2026) - Apel 2026: coherent temporal manipulation in the group-delay domain of a whole-file Giant FFT
- [paper-nielsen-keyframe-extrema-tsm-2026](entities/source-papers.md#paper-nielsen-keyframe-extrema-tsm-2026) - Nielsen 2026: extrema-density-driven adaptive OLA time stretching for embedded hardware
- [paper-badia-octave-filter-bank-parallelism-2026](entities/source-papers.md#paper-badia-octave-filter-bank-parallelism-2026) - Badia, Belloch & Valimaki 2026: parallel, energy-aware multistage linear-phase octave filter bank on an edge SoC

## Concepts
<!-- core theory pages -->
- [[sasp-overview]] — big picture of the SASP book, chapter map, three views
- [[dtft-and-fourier-theorems]] — four Fourier cases, DTFT, key theorems, Poisson summation
- [[zero-padding-and-interpolation]] — zero padding as DTFT interpolation; minimum-zp tables
- [[spectrum-analysis-windows]] — window zoo; main-lobe vs side-lobe trade-off
- [[window-design-methods]] — window method, least-squares, LP/Chebyshev, Parks-McClellan
- [[short-time-fourier-transform]] — STFT definition, parameters, two dual views
- [[overlap-add-stft]] — OLA interpretation, COLA constraint, FFT convolution
- [[filter-bank-summation-stft]] — FBS interpretation, DFT filter bank, Portnoff windows
- [[stft-modifications]] — safe spectral modifications, time-varying filtering
- [[sinusoidal-modeling]] — analysis, peak tracking, birth/death, PARSHL pipeline
- [[qifft-peak-estimation]] — parabolic peak interpolation, bias vs window
- [[sinusoidal-parameter-interpolation]] — cubic phase / McAulay-Quatieri partial continuation
- [[sms-sines-plus-noise]] — SMS deterministic + stochastic (+ transients) decomposition
- [[phase-vocoder-and-tsm]] — phase vocoder, TSM, phase locking, transient handling
- [[cross-synthesis-and-morphing]] — envelope × carrier, magnitude/phase exchange
- [[f0-and-spectral-envelope]] — f0 estimation, LPC/cepstral envelope extraction
- [[noise-spectrum-analysis]] — Bartlett, Welch, Blackman-Tukey; bias/variance trade-off
- [[multirate-filter-banks]] — polyphase, noble identities, PR FB, wavelets
- [[spectral-audio-applications]] — audio coding, loudness, vocoders, effects
- [[gaussian-and-chirp-windows]] — Gaussian optimality, chirplets, uncertainty principle
- [[nonstationary-sinusoidal-estimation-ddm]] - polynomial AM-FM sinusoids estimated by the distribution derivative method
- [[giant-fft-group-delay-domain]] - whole-file DFT edited in the group-delay domain: peak grouping and time displacement
- [[extrema-sampling-time-stretch]] - sparse extrema keyframes driving an adaptive-crossfade OLA time stretcher
- [[linear-phase-octave-filter-bank-implementation]] - blocked and OpenMP-task realization of a multistage IFIR octave bank on an edge SoC

## Comparisons
<!-- See also sibling wikis: ../waveguide_synthesis/ and ../modal_synthesis/ -->

## Queries

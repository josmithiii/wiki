---
title: "MDFT - Mathematics of the Discrete Fourier Transform"
created: 2026-11-25
updated: 2026-11-25
type: entity
tags: [book, mdft, dsp-foundations, reference]
sources:
  - https://ccrma.stanford.edu/~jos/mdft/
  - /w/mdft/mdft.tex
---

# MDFT - Mathematics of the Discrete Fourier Transform

Julius O. Smith III, *Mathematics of the Discrete Fourier Transform (DFT)
with Audio Applications*, Second Edition, W3K Publishing, 2007, ISBN
978-0-9745607-4-8.  Free online at <https://ccrma.stanford.edu/~jos/mdft/>.
First book of the series ([[book-series-overview]]): everything in the DFT
formula and its constituents, built up from high-school math.

No sub-wiki distills MDFT; it is the background that the other three books
and every sub-wiki assume.  Link to it when a page leans on complex
sinusoids, the DFT and its theorems, sampling and aliasing, decibels,
correlation, or power spectra.  Page names for deep links:
`jos_books/catalog/mdft.tsv` (301 pages).

## Chapter map

Each bullet: chapter, selected sections, then (->) the wiki pages with the
most links into that chapter (`make book-usage` lists them all).

- **1 [Introduction to the DFT](https://ccrma.stanford.edu/~jos/mdft/Introduction_DFT.html)** - [DFT Definition](https://ccrma.stanford.edu/~jos/mdft/DFT_Definition.html), [Inverse DFT](https://ccrma.stanford.edu/~jos/mdft/Inverse_DFT.html)
- **2 [Complex Numbers](https://ccrma.stanford.edu/~jos/mdft/Complex_Numbers.html)** - [The Complex Plane](https://ccrma.stanford.edu/~jos/mdft/Complex_Plane.html), [Euler's Identity](https://ccrma.stanford.edu/~jos/mdft/Euler_s_Identity.html), [De Moivre's Theorem](https://ccrma.stanford.edu/~jos/mdft/De_Moivre_s_Theorem.html)
- **3 [Proof of Euler's Identity](https://ccrma.stanford.edu/~jos/mdft/Proof_Euler_s_Identity.html)** - [Roots of Unity](https://ccrma.stanford.edu/~jos/mdft/Roots_Unity.html)
- **4 [Sinusoids and Exponentials](https://ccrma.stanford.edu/~jos/mdft/Sinusoids_Exponentials.html)** - [Sinusoids](https://ccrma.stanford.edu/~jos/mdft/Sinusoids.html), [Exponentials](https://ccrma.stanford.edu/~jos/mdft/Exponentials.html), [Audio Decay Time (T60)](https://ccrma.stanford.edu/~jos/mdft/Audio_Decay_Time_T60.html), [Complex Sinusoids](https://ccrma.stanford.edu/~jos/mdft/Complex_Sinusoids.html), [Analytic Signals and Hilbert Transform Filters](https://ccrma.stanford.edu/~jos/mdft/Analytic_Signals_Hilbert_Transform.html) -> [[active_absorbers/concepts/tonal-periodic-anc|tonal-periodic-anc]], [[modal_synthesis/concepts/corpus-driven-parametric-modal-reverb|corpus-driven-parametric-modal-reverb]], [[modal_synthesis/concepts/damping-models|damping-models]], [[waveguide_synthesis/concepts/artificial-reverberation|artificial-reverberation]]
- **5 [Geometric Signal Theory](https://ccrma.stanford.edu/~jos/mdft/Geometric_Signal_Theory.html)** - [Signal Metrics](https://ccrma.stanford.edu/~jos/mdft/Signal_Metrics.html), [The Inner Product](https://ccrma.stanford.edu/~jos/mdft/Inner_Product.html), [Signal Reconstruction from Projections](https://ccrma.stanford.edu/~jos/mdft/Signal_Reconstruction_Projections.html)
- **6 [The DFT Derived](https://ccrma.stanford.edu/~jos/mdft/DFT_Derived.html)** - [Orthogonality of Sinusoids](https://ccrma.stanford.edu/~jos/mdft/Orthogonality_Sinusoids.html), [Frequencies in the "Cracks"](https://ccrma.stanford.edu/~jos/mdft/Frequencies_Cracks.html), [Matrix Formulation of the DFT](https://ccrma.stanford.edu/~jos/mdft/Matrix_Formulation_DFT.html) -> [[waveguide_synthesis/concepts/circular-buffer-topology-monodromy|circular-buffer-topology-monodromy]]
- **7 [Fourier Theorems for the DFT](https://ccrma.stanford.edu/~jos/mdft/Fourier_Theorems_DFT.html)** - [Signal Operators](https://ccrma.stanford.edu/~jos/mdft/Signal_Operators.html), [Fourier Theorems](https://ccrma.stanford.edu/~jos/mdft/Fourier_Theorems.html), [Zero Padding](https://ccrma.stanford.edu/~jos/mdft/Zero_Padding.html), [Power Theorem](https://ccrma.stanford.edu/~jos/mdft/Power_Theorem.html), [Rayleigh Energy Theorem (Parseval's Theorem)](https://ccrma.stanford.edu/~jos/mdft/Rayleigh_Energy_Theorem_Parseval_s.html) -> [[spectral_processing/concepts/giant-fft-group-delay-domain|giant-fft-group-delay-domain]], [[spectral_processing/concepts/zero-padding-and-interpolation|zero-padding-and-interpolation]], [[spectral_processing/concepts/dtft-and-fourier-theorems|dtft-and-fourier-theorems]], [[spectral_processing/concepts/multirate-filter-banks|multirate-filter-banks]], [[spectral_processing/concepts/overlap-add-stft|overlap-add-stft]], +2 more
- **8 [DFT Applications](https://ccrma.stanford.edu/~jos/mdft/Example_Applications_DFT.html)** - [Spectrum Analysis of a Sinusoid](https://ccrma.stanford.edu/~jos/mdft/Spectrum_Analysis_Sinusoid_Windowing.html), [Spectrograms](https://ccrma.stanford.edu/~jos/mdft/Spectrograms.html), [Filters and Convolution](https://ccrma.stanford.edu/~jos/mdft/Filters_Convolution.html), [Correlation Analysis](https://ccrma.stanford.edu/~jos/mdft/Correlation_Analysis.html), [Power Spectral Density](https://ccrma.stanford.edu/~jos/mdft/Power_Spectral_Density_Estimation.html), [Coherence Function](https://ccrma.stanford.edu/~jos/mdft/Coherence_Function.html), [FIR System Identification](https://ccrma.stanford.edu/~jos/mdft/FIR_System_Identification.html) -> [[active_absorbers/concepts/lms-algorithm|lms-algorithm]], [[active_absorbers/concepts/tonal-periodic-anc|tonal-periodic-anc]], [[spectral_processing/concepts/f0-and-spectral-envelope|f0-and-spectral-envelope]], [[spectral_processing/concepts/noise-spectrum-analysis|noise-spectrum-analysis]], [[spectral_processing/concepts/short-time-fourier-transform|short-time-fourier-transform]], +4 more

## Appendix map

- **A [Fast Fourier Transforms (FFT)](https://ccrma.stanford.edu/~jos/mdft/Fast_Fourier_Transform_FFT.html)** - [Mixed-Radix Cooley-Tukey FFT](https://ccrma.stanford.edu/~jos/mdft/Mixed_Radix_Cooley_Tukey_FFT.html), [Bluestein's FFT Algorithm](https://ccrma.stanford.edu/~jos/mdft/Bluestein_s_FFT_Algorithm.html), [Fast Transforms in Audio DSP](https://ccrma.stanford.edu/~jos/mdft/Fast_Transforms_Audio_DSP.html)
- **B [Continuous/Discrete Transforms](https://ccrma.stanford.edu/~jos/mdft/Fourier_Transforms_Continuous_Discrete_Time_Frequency.html)** - [Discrete Time Fourier Transform (DTFT)](https://ccrma.stanford.edu/~jos/mdft/Discrete_Time_Fourier_Transform.html), [Fourier Transform (FT) and Inverse](https://ccrma.stanford.edu/~jos/mdft/Fourier_Transform_FT_Inverse.html) -> [[spectral_processing/concepts/dtft-and-fourier-theorems|dtft-and-fourier-theorems]], [[virtual_analog/concepts/alias-free-oscillator-sync|alias-free-oscillator-sync]]
- **C [Continuous Fourier Theorems](https://ccrma.stanford.edu/~jos/mdft/Selected_Continuous_Time_Fourier_Theorems.html)** - [Differentiation Theorem](https://ccrma.stanford.edu/~jos/mdft/Differentiation_Theorem.html), [The Uncertainty Principle](https://ccrma.stanford.edu/~jos/mdft/Uncertainty_Principle.html)
- **D [Sampling Theory](https://ccrma.stanford.edu/~jos/mdft/Sampling_Theory.html)** - [Aliasing of Sampled Signals](https://ccrma.stanford.edu/~jos/mdft/Aliasing_Sampled_Signals.html), [Sampling Theorem](https://ccrma.stanford.edu/~jos/mdft/Sampling_Theorem.html) -> [[virtual_analog/concepts/antiderivative-antialiasing|antiderivative-antialiasing]], [[virtual_analog/concepts/alias-free-oscillator-sync|alias-free-oscillator-sync]], [[virtual_analog/concepts/fourier-neural-operators-va|fourier-neural-operators-va]]
- **E [Taylor Series Expansions](https://ccrma.stanford.edu/~jos/mdft/Taylor_Series_Expansions.html)**
- **F [Logarithms and Decibels](https://ccrma.stanford.edu/~jos/mdft/Logarithms_Decibels.html)** - [Decibels](https://ccrma.stanford.edu/~jos/mdft/Decibels.html), [DB SPL](https://ccrma.stanford.edu/~jos/mdft/DB_SPL.html) -> [[active_absorbers/concepts/psychoacoustic-anc|psychoacoustic-anc]], [[active_absorbers/concepts/rooftop-fan-contenders|rooftop-fan-contenders]]
- **G [Digital Audio Number Systems](https://ccrma.stanford.edu/~jos/mdft/Number_Systems_Digital_Audio.html)** - [Round-Off Error Variance](https://ccrma.stanford.edu/~jos/mdft/Round_Off_Error_Variance.html)
- **H [Matrices](https://ccrma.stanford.edu/~jos/mdft/Matrices.html)**
- **I [Matlab/Octave Examples](https://ccrma.stanford.edu/~jos/mdft/Matlab_Octave_Examples.html)** - [Spectrogram Computation](https://ccrma.stanford.edu/~jos/mdft/Spectrogram_Computation.html)

## Where the series continues

- The DTFT and continuous-time theorems of appendices B and C are developed
  fully in [[sasp-book|SASP]] chapter 2 and appendix B.
- "Filters and Convolution" (chapter 8) is the bridge to
  [[filters-book|Filters]].
- Windowing a sinusoid (chapter 8) grows into SASP chapters 3 and 5.

## Related

- [[book-series-overview]] - how the four books fit together
- [[book-topic-finder]] - topic to book-section lookup

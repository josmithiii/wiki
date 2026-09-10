---
title: Giant FFT Group Delay Domain
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [fft, dft, phase-unwrap, modifications, applications, stft]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_02.pdf
  - spectral_processing/raw/DAFx26_paper_02.txt
---

# Giant FFT Group Delay Domain

The **Giant FFT** is a single DFT over an entire audio file: no window,
no hop, one complex spectrum encoding the whole temporal evolution.
Manipulating its magnitude or phase directly smears discrete events
into drones. Apel's contribution is to transform the phase spectrum
into its frequency derivative - the **group delay spectrum** - where
each bin's value *is a time*, and to move grouped bins coherently.[^apel-2026]

## Why group delay

- An event at time $t$ contributes phase $-2\pi f t$ at every frequency $f$, so the *slope* of phase across frequency, not the phase value, carries temporal position.
- Group delay $\tau_g(\omega) = -\,d\phi/d\omega$ reads that slope per bin, in units of time: the **temporal centre of gravity** (amplitude-weighted mean temporal position) of the energy at that bin.
- Bins belonging to one event share one slope, hence cluster at one group-delay value. That clustering is the grouping cue.
- Individual phase values, even unwrapped, are not perceptually meaningful at Giant-FFT lengths; group delay values are.

## Discrete form (exactly invertible)

$$\tau(k) \;=\; -\big(\Phi(k+1)-\Phi(k)\big)$$
with $\Phi$ the unwrapped phase, $\tau$ in radians per bin. This
first-order difference differs from $-d\Phi/d\omega$ only by the bin
spacing $2\pi f_s/N$ (divide by it to read seconds), and is preferred
over the direct complex-spectrum formula[^jos-groupdelay] because
resynthesis is its exact inverse:
$$\Phi_\mathrm{new}(k) \;=\; \Phi(0) - \sum_{j=0}^{k-1}\tau_\mathrm{new}(j).$$
With no modification, analysis-resynthesis recovers the input to
floating-point precision. A real-input FFT is used, negative
frequencies implied by conjugate symmetry.

## Zero padding against temporal aliasing

- The input is first padded with silence sized to the intended displacement - *before* the signal for backward shifts, *after* it for forward shifts.
- The padded signal is then zero-padded to the next power of two, preventing circular (temporal) aliasing in the output.
- This follows Valimaki et al.'s zero-phase Giant FFT study, which introduced zero padding to remove an entire class of artifacts from earlier Giant-FFT systems (Hammer and Sundt's *Mammut*, 1999).

## Peak-region grouping

1. Smooth $|X(k)|$ with a Gaussian kernel of specified width in bins.
2. Contiguous regions where the smoothed magnitude exceeds a threshold relative to the global peak are **spectral peaks**.
3. Each peak is extended to a chosen **segment width**, limited by the midpoint between neighbouring peaks (examples use 8000-12000 bins; wide segments are needed to carry the broadband transient energy around a sharp onset).
4. Each segment's temporal position is the magnitude-weighted mean of its group-delay values in seconds; segments whose means fall within a tolerance are **grouped**, so one group can span many peaks.
5. Optionally, bins in no segment are zeroed. Otherwise the magnitude spectrum is left completely unaltered.

The "region of influence" idea is borrowed from phase-vocoder phase
locking (Laroche and Dolson), see
[[entities/source-papers#paper-laroche-dolson-improved-pv-1999]].

## The three transformations

| Transformation | Rule | Result |
|---|---|---|
| Event reordering | $\tau_\mathrm{new}(k)=\tau(k)+C$ per group | Notes replayed in any order, each keeping its own amplitude envelope (unlike time reversal) |
| Amplitude-proportional displacement | $C$ set from each peak's amplitude | One note unfolds into a sequence of its partials over a chosen duration |
| Sinusoidal group-delay modulation | $\tau_\mathrm{new}(k)=\tau(k)+MT\sin\!\big(2\pi k T f_s/N\big)$ | Periodically spaced temporal *copies*; $T$ sets spacing, $M$ the number of copies |

- A constant added across a segment is a linear phase ramp, i.e. a pure time shift; keeping the *shape* of $\tau(k)$ within the segment is what preserves onset and decay structure.
- The $T$ factor before the sine makes copy count depend on $M$ alone, independent of period. Per-segment modulation frequencies give polyrhythmic textures; examples use $M \in [0.4, 2]$, $T \in [0.01, 4]$ s, output extended to 20x the original duration.
- Segmentation is what separates this from incoherent Giant-FFT effects: the same amplitude-proportional displacement applied per bin smears into a drone.

## Versus the STFT view

- Spectral delays in an STFT delay *frequency bands* by prescribed amounts; here the transformation is specified in terms of *spectral features and their positions in time*, which the representation makes explicit.
- A windowed analysis must commit to a window length, trading frequency resolution against temporal extent; no window both resolves close partials and contains a partial's full evolution. The Giant FFT has no such trade-off - a partial's whole envelope lives in the bins around its peak. See [[short-time-fourier-transform]] and [[stft-modifications]].

## Limits

- Whole-file and offline by construction (Python/NumPy/SciPy/librosa prototype).
- Works only when events do not share bins. For overlapping/polyphonic material a shared bin's group delay is the amplitude-weighted average of all contributors, so those events can only move together.
- Segment width is a trade-off: too narrow leaves low-level energy behind, too wide drags other events along.
- Grouping is a creative heuristic, not a validated event segmentation.
- Suggested next steps: other periodic modulation patterns, and "temporal filtering" - keeping or zeroing bins by *when* they occur.

## Related Concepts
- [[stft-modifications]] - the windowed counterpart of these edits
- [[short-time-fourier-transform]] - the resolution trade-off avoided here
- [[zero-padding-and-interpolation]] - zero padding as aliasing insurance
- [[entities/source-papers#paper-apel-giant-fft-group-delay-2026]] - catalog entry

[^apel-2026]: Ted Apel, "Group Delay Manipulation for Creative Sound Transformation with the Giant FFT," *Proc. DAFx26*, Cambridge MA, Sept. 2026, pp. 19-24. Distilled in [[entities/source-papers#paper-apel-giant-fft-group-delay-2026]].
[^jos-groupdelay]: The paper cites JOS, "Numerical Computation of Group Delay" (`https://ccrma.stanford.edu/~jos/fp/`), for computing $\tau_g$ from the complex spectrum without unwrapping.

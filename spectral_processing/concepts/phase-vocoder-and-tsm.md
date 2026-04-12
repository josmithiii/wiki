---
title: Phase Vocoder and Time-Scale Modification
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [phase-vocoder, tsm, stft, phase-unwrap, modifications]
sources:
  - /w/sasp/phase-vocoder.tex
  - /w/sasp/tsm.tex
  - /w/sasp/tsmpv.tex
  - /w/sasp/unwrap.tex
  - /w/sasp/phasewrap.tex
---

# Phase Vocoder and Time-Scale Modification

The **phase vocoder** is an STFT in filter-bank form where each bin
is interpreted as an oscillator, allowing independent modification of
magnitude and phase. Its most famous application is **time-scale
modification** (TSM) — changing duration without changing pitch, or
pitch without changing duration.

## Bin Signal as Oscillator

In FBS form ([[filter-bank-summation-stft]]):
$$X_m(k) \;=\; |X_m(k)|\, e^{j\angle X_m(k)}$$
Between frames $m$ and $m+1$ (hop $R_a$), the **phase increment** of
bin $k$ should be near $\omega_k R_a$ if a sinusoid near $\omega_k$ is
present. Measured increment:
$$\Delta\phi_m(k) \;=\; \angle X_{m+1}(k) - \angle X_m(k)$$

## Phase Unwrapping and Instantaneous Frequency

Heterodyned phase increment:
$$\Delta_{\text{het}} \;=\; \Delta\phi_m(k) - \omega_k R_a$$
Wrap $\Delta_{\text{het}}$ to $(-\pi, \pi]$ — this is the **principal
argument** — and estimate instantaneous frequency:
$$\hat\omega_m(k) \;=\; \omega_k + \frac{\operatorname{princ}(\Delta_{\text{het}})}{R_a}$$

This is the key measurement: the true frequency of the dominant
sinusoid in bin $k$.

## TSM Recipe (Classic Phase Vocoder)

Target time-scale factor $\alpha$ (analysis hop $R_a$, synthesis hop
$R_s = \alpha R_a$):

1. Compute STFT with analysis hop $R_a$.
2. For each bin: measure $\hat\omega_m(k)$ via unwrapping.
3. Accumulate synthesis phase:
$$\phi^s_{m+1}(k) \;=\; \phi^s_m(k) + R_s\, \hat\omega_m(k)$$
4. Synthesis spectrum: $|X_m(k)|\, e^{j\phi^s_m(k)}$.
5. Inverse STFT with synthesis hop $R_s$.

For pitch shifting by factor $\beta$: TSM by $\alpha = 1/\beta$ then
resample by $\beta$.

## Phasiness and Phase Locking

Classical phase vocoder treats bins independently, which destroys
cross-bin phase relationships around peaks $\Rightarrow$ the dreaded
**phasiness** (reverberant, loose artifact).

**Phase-locked PV** (Puckette, Laroche-Dolson):
- Detect peaks in $|X_m(k)|$ each frame.
- Lock phases of bins inside a peak's main lobe to the phase of the
  peak bin, preserving rigid-body phase structure.
- Dramatically reduces phasiness.

**Rigid phase locking**: all bins in a peak region share the peak's
phase offset. **Scaled phase locking**: offsets scale with distance
from peak center.

## Transient Handling

TSM smears sharp onsets because phase continuation assumes local
stationarity. Mitigations:
- Detect transients and **reset phases** to original at transient
  frames (phase re-init).
- Treat transients separately (SMS-T, see [[sms-sines-plus-noise]]).

## Trade-offs vs Alternatives

| Method | Pros | Cons |
|--------|------|------|
| Classical PV | Simple, generic | Phasiness, transient smear |
| Phase-locked PV | Clean on tonal | Still smears transients |
| SMS-based TSM | Handles noise + transients | More complex, needs tracking |
| WSOLA | No FFT, cheap | Pitch artifacts, limited range |

## Related Concepts
- [[short-time-fourier-transform]], [[filter-bank-summation-stft]]
- [[sinusoidal-modeling]] — peak model view
- [[sms-sines-plus-noise]] — alternative TSM framework
- [[stft-modifications]] — general safe-modification rules

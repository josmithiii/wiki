---
title: Alias-Free Oscillator Sync
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [oscillator-sync, oscillator, additive, antialiasing, asic, real-time]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_49.pdf
  - raw/DAFx26_paper_49.txt
---

# Alias-Free Oscillator Sync

Oscillator sync is alias-free *by construction* if the synchronized waveform is
computed in the Fourier-series domain and resynthesized additively, instead of being
generated with a discontinuity and then corrected.[^1]

## Hard sync

Two oscillators, a **leading** one at $f_\text{lead}$ and a **following** one at
$f_\text{follow}$; whenever the leading oscillator completes a period, the following
oscillator's phase is reset. Depending on the following oscillator's amplitude at that
instant the reset introduces a waveform discontinuity, hence high-frequency content
absent from the free-running waveform, and the reset instant falls at an arbitrary
sub-sample time, so a naive digital reset aliases badly. Prior remedies - BLIT,
BLEP/BLAMP, polynomial transition regions, waveform-specific Fourier derivations for
synced sine or sawtooth - correct the discontinuity after the fact or work for only
one waveform.

## Spectral resampling

Let the bandlimited free-running following-oscillator waveform be
$r(t) = \sum_{n=-N}^{N} c_n\, e^{\,j 2\pi n t / T_\text{follow}}$. Only the period
ratio matters, so define

$$P \triangleq \frac{T_\text{lead}}{T_\text{follow}} = \frac{f_\text{follow}}{f_\text{lead}}, \qquad \text{normalizing } T_\text{follow} = 1, \ T_\text{lead} = P .$$

1. **Pre-rotation.** The derivation is simpler over $[-P/2, P/2]$ than $[0, P]$, so
   time-shift by $\tau = -P/2$: $\mathring{c}_n = c_n e^{-j2\pi\tau n}$, a plane rotation
   of $(\Re c_n, \Im c_n)$.
2. **Resampling.** Recompute the Fourier coefficients of the *same* signal over the
   new period $P$ - which is exactly resetting the following oscillator at rate $1/P$:

$$\bar{c}_n = \frac{1}{P}\int_{-P/2}^{P/2}\mathring{r}(t)\,e^{-j\frac{2\pi}{P}nt}\,dt
= \sum_{k=-N}^{N} \mathring{c}_k\, \operatorname{sinc}(n - kP),
\qquad \operatorname{sinc}(x) = \frac{\sin \pi x}{\pi x}$$

A **linear transform** from $2N{+}1$ input to $2N{+}1$ output coefficients (a different
output count $N'$ is allowed, giving independent input/output bandlimiting). In real
coefficients, for $n = 1,\dots,N$:

$$\bar{a}_n = \sum_{k=1}^{N}\mathring{a}_k\big[\operatorname{sinc}(n-kP) + \operatorname{sinc}(n+kP)\big], \quad
\bar{b}_n = \sum_{k=1}^{N}\mathring{b}_k\big[\operatorname{sinc}(n-kP) - \operatorname{sinc}(n+kP)\big]$$

with $\bar{a}_0 = \mathring{a}_0 + \sum_k \mathring{a}_k \operatorname{sinc}(kP)$.

3. **Additive resynthesis** at sample rate $f_s$, summing *only* harmonics below
   Nyquist - this is what makes the output alias-free: $\bar{s}[\ell] = \bar{a}_0 +
   \sum_{n \in \mathcal{N}} \bar{a}_n \cos(\tfrac{2\pi n}{T_\text{lead} f_s}\ell) +
   \bar{b}_n \sin(\cdot)$, with $\mathcal{N} = \{n \le N : n/T_\text{lead} < f_s/2\}$.

## Two soft-sync modes

- **Mirrored sync** reflects the waveform at the reset instead of resetting it:
  $\hat{s}(t) = r(t)$ on $[0,T_\text{lead})$ and $r(2T_\text{lead}-t)$ on
  $[T_\text{lead}, 2T_\text{lead})$, total period $2T_\text{lead}$. Pre-rotation uses
  $\tau = -P$; the transform picks up **versinc** terms,
  $\operatorname{versinc}(x) = (1-\cos \pi x)/(\pi x)$, alongside sinc, and all
  $\hat{b}_n$ vanish by the even symmetry of $\hat{s}$.
- **Pulsar sync** mutes the following oscillator after each of its own periods:
  $\ddot{s}(t) = r(t)$ on $[0, T_\text{follow})$ and $0$ on
  $[T_\text{follow}, T_\text{lead})$ - conceptually pulsar synthesis with the
  waveform as pulsaret and a rectangular window. Pre-rotation $\tau = -1/2$; with
  $c_0 = 0$, $\ddot{a}_n = \sum_k \frac{\mathring{a}_k}{P}[\operatorname{sinc}(\frac{n}{P}-k) + \operatorname{sinc}(\frac{n}{P}+k)]$
  and similarly for $\ddot{b}_n$ with a minus sign. Derived for $P \ge 1$; it appears
  to extend to $P < 1$ (overlapping cycles), untested.

## Complexity

The transform is $O(N^2)$ and every term needs a trigonometric evaluation and a
division: hard sync with $N = 512$ needs $512^2 \cdot 2 = 524{,}288$ sinc evaluations.
An unoptimized NumPy implementation takes 2.7-5.8 ms on an M2 Pro, i.e. a coefficient
update rate of only 172-370 Hz - too slow to modulate $f_\text{lead}$ cleanly. That
motivated a tapeout: see [[hasy-asic]], which computes the transform within five audio
sample periods at 96 kHz with 512 harmonics.

**Limitations:** cost scales with harmonic count, so on a general-purpose CPU the
method is expensive for low-pitched, harmonic-rich waveforms; rapid modulation of
$T_\text{lead}$ can still alias at each recompute; and resampling can only redistribute
harmonics already present in the free-running coefficient set, so $P < 1$ degrades at
fixed $N$. Reference Python at `https://github.com/IIP-Group/hasy-python`.

## See also

[[virtual-analog-overview]] - [[hasy-asic]] - [[antiderivative-antialiasing]] / [[polyadaa]] (the correction-based alternative)

## References

[^1]: [[entities/source-papers#paper-roth-alias-free-oscillator-sync-2026]] - Roth, Keller, Castaneda, Studer, "Alias-Free Oscillator Synchronization via Additive Synthesis", DAFx26.

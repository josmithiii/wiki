---
title: Allpass Clipping Prevention
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [allpass, time-varying, stability, va-filters, real-time, embedded]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_45.pdf
  - raw/DAFx26_paper_45.txt
---

# Allpass Clipping Prevention

A modulated allpass section can drive its output past full scale even when the input
never does. This is an algebraic *prevention* method for first- and second-order
sections: check whether the new coefficient value would clip, and if so clamp the
coefficient *increment* to the largest value keeping $|y[n]| \le M$.[^1]

## Structures and the deviation bound

Direct Form I allpass sections, first- and second-order:

$$\begin{aligned}
y[n] &= c(n)\big(x[n] - y[n-1]\big) + x[n-1] &&(1)\\
y[n] &= c_0(n)\big(x[n]-y[n-2]\big) + c_1(n)\big(x[n-1]-y[n-1]\big) + x[n-2] &&(8)
\end{aligned}$$

Higher orders follow by cascade decomposition. Allpasses are the target because an
$N$th-order section has only $N$ coefficients, keeping the clipping condition
tractable, and because they build parametric EQs, phasers, and the diffusers in
[[artificial-reverberation]].

Assume $|x[n]| \le M$ and $|y[n-1]| \le M$ (no clipping yet). Define the **static
counterpart** - the same structure with the *previous* coefficient frozen:
$w[n] = c(n-1)(x[n] - y[n-1]) + x[n-1]$. If $w[n]$ does not clip, the deviation
caused by the update $\Delta c(n) = c(n) - c(n-1)$ is exactly
$\tau[n] = y[n] - w[n] = \Delta c(n)(x[n] - y[n-1])$, so the non-clipping
condition $|w[n] + \tau[n]| \le M$ is *linear* in $\Delta c(n)$:

$$\big|\,w[n] + \Delta c(n)\,(x[n] - y[n-1])\,\big| \le M \tag{4}$$

This assumes nothing about internal energy evolution - only that the input is not
already clipping. Energy-preserving (WDF-style) time-varying allpasses, built for
stability under coefficient change, are *not* anti-clipping and do overshoot for some
directions of coefficient travel.

## The runtime bound

Solving (4) gives an interval for $\Delta c(n)$ with endpoints $-\frac{M + w[n]}{d}$
and $\frac{M - w[n]}{d}$, $d = x[n]-y[n-1]$; the two swap roles with the sign of $d$.
The applied increment $\widehat{\Delta c}(n)$ is $\Delta c(n)$ clamped (a `min` of a
`max`) to that interval, and $\hat c(n) = c(n-1) + \widehat{\Delta c}(n)$. If $d = 0$
then $\tau[n] = 0$, the block is a unit delay, and no action is needed.

**Second order.** The two-coefficient condition has no unique solution pair, so a
"clipping prevention budget" is split evenly: each term must respect half the bound,
$|w[n]/2 + \Delta c_0(n)(x[n]-y[n-2])| \le M/2$ and
$|w[n]/2 + \Delta c_1(n)(x[n-1]-y[n-1])| \le M/2$, which implies the joint condition
by the triangle inequality. Each is clamped as above with $w[n]/2$, $M/2$; in the
sinusoidal case study the two terms are nearly symmetric, so the even split is a
good accuracy/efficiency compromise.

The procedure runs at *every* sample rather than on detection, giving constant
processing time - the right choice for embedded DSP. It intervenes only during short
transients (a few ms), after which coefficients are released to their targets. It is
not merely a slew limiter: clipping can occur *after* the coefficients have settled,
and is still caught. Safe for Direct Form I (state is past inputs and outputs,
guaranteed unclipped); other recombinations may clip internally, since it does not
act on state. Since (4) forces $|y[n]| \le M$ whenever $|c(n)|<1$ and $|x[n]| \le M$,
the modified sequence is BIBO stable by definition - a runtime counterpart to
[[time-varying-filter-stability]].

## Results and cost

- 100 Hz sine, amplitude 0.99, $f_s = 48$ kHz, $M = 1$, $c$ swept linearly between
  $+0.99$ and $-0.99$ over about 1 ms at an input peak. One direction clips the
  standard structure (prevented here); the opposite clips the energy-preserving WDF
  structure while the standard one does not, and the procedure stays inactive.
- Second order: $(c_0, c_1)$ swept between $(0.98, -1.96)$ and $(-0.98, 0.01)$; one
  direction needs a large impulsive correction, which also smooths the following
  samples. Verified on a music excerpt at 44.1 kHz, $M = 0.99$.
- Cost (1 s input in MATLAB, 10 s in C++ `-O3 -ffast-math`, 4.7 GHz i7):

| Structure | MATLAB 1st | MATLAB 2nd | C++ 1st | C++ 2nd |
|---|---|---|---|---|
| standard (DF I) | 9.2 ms | 9.5 ms | 1.1 ms | 1.5 ms |
| energy-preserving | 10.2 ms | 40.2 ms | 1.7 ms | 2.2 ms |
| proposed | 14.7 ms | 33.7 ms | 3.8 ms | 4.9 ms |

- Numerically undemanding: with $M = 1$ all quantities stay below magnitude 2; on DSPs without accurate division the clamp can be found by bisection instead.

**Limitations:** first- and second-order Direct Form I only; long cascades and other
realizations untested, and the mild transient nonlinearity is not perceptually
evaluated. Future work: combining it with energy preservation, i.e.
[[wave-digital-filters]]. See also [[virtual-analog-overview]].

## References

[^1]: [[entities/source-papers#paper-fontana-allpass-clipping-prevention-2026]] - Fontana, Pasin, Bernardini, D'Angelo, "A Clipping Prevention Method for All-Pass Digital Filters with Time-Varying Coefficients", DAFx26.

---
title: Window and FIR Design Methods
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [fir-design, optimal-fir, windows]
sources:
  - /w/sasp/firdesign.tex
  - /w/sasp/firdesignintro.tex
  - /w/sasp/linprog-fir.tex
  - /w/sasp/optimal-fir.tex
  - /w/sasp/opt-fir-td.tex
  - /w/sasp/freqsamp.tex
---

# Window and FIR Design Methods

Linear-phase FIR filter (and custom analysis window) design.

## Window Method

1. Choose ideal frequency response $H_d(\omega)$ (e.g. brick-wall LPF).
2. Inverse DTFT $\to$ ideal impulse response $h_d(n)$ (often a sinc).
3. Truncate + taper: $h(n) = w(n)\, h_d(n)$.
4. Shift by $(M-1)/2$ for causal linear phase.

Side-lobe level of $H(\omega)$ ≈ side-lobe level of $W(\omega)$.
Transition width ≈ main-lobe width of $w$. Simple, near-optimal with
Kaiser. See [[spectrum-analysis-windows]].

## Frequency Sampling

Specify $H(k)$ at $N$ equally spaced bins and inverse-DFT. Exact
interpolation at sample points, arbitrary in between — add
"transition band" samples as free variables and optimize.

## Least-Squares (L2)

Minimize
$$\int_{-\pi}^{\pi} W(\omega)\,|H(\omega) - H_d(\omega)|^2\, d\omega$$
with weighting $W(\omega) \ge 0$. Closed form via Gram matrix
$\Rightarrow$ linear system. Related to matrix pseudoinverse.
Good for audio where L2 energy matters.

## Chebyshev (Minimax / L∞)

Minimize the **maximum** weighted error:
$$\min_h \max_\omega\; W(\omega)\,|H(\omega) - H_d(\omega)|$$
Solutions are **equi-ripple**. Two main paths:

### Parks-McClellan / Remez Exchange
- Uses Chebyshev alternation theorem: optimal error alternates in
  sign at $L+2$ extrema.
- Solved iteratively by Remez exchange of extrema.
- Matlab `firpm`, Octave `remez`.

### Linear Programming (LP)
- Reformulate: minimize $\delta$ subject to
  $-\delta \le W(\omega_i)[H(\omega_i) - H_d(\omega_i)] \le \delta$
  over a dense grid $\{\omega_i\}$.
- Arbitrary constraints (time-domain, positivity, complex targets,
  monotone windows) trivially added.
- JOS uses LP in SASP to design custom Chebyshev-like **analysis
  windows** with shaped side-lobe envelopes, impossible with Remez.
- Solvers: `linprog` (Matlab), GLPK (Octave).

## Second-Order Cone (SOCP)

Generalizes LP to L2-cone constraints. Enables mixed L2/L∞ objectives
and convex magnitude-squared constraints. Used for audio FIRs where
stopband energy (not just peak) matters.

## Time-Domain Optimal Design

Directly solve for $h(n)$ minimizing weighted time-domain error to a
target impulse response (`opt-fir-td`). Natural for matching measured
impulse responses or imposing sparsity / length constraints.

## Linear-Phase Types

| Type | Length | Symmetry | Constraints |
|------|--------|----------|-------------|
| I | odd | even | no restriction |
| II | even | even | $H(\pi)=0$ (no HPF) |
| III | odd | odd | $H(0)=H(\pi)=0$ (BPF/diff) |
| IV | even | odd | $H(0)=0$ (HPF/Hilbert) |

Type III/IV used for **Hilbert transformers** and **differentiators**.

## Related Concepts
- [[spectrum-analysis-windows]] — windows as a special FIR design case
- [[dtft-and-fourier-theorems]] — theoretical foundation

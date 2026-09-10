---
title: ERA Bridge Admittance Identification
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [modal, eigenmode, impulse-response, string, dsp, comparison, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_41.pdf
  - /l/dttd/DAFx26/txt/DAFx26_paper_41.txt
---

# ERA Bridge Admittance Identification

The Eigensystem Realization Algorithm (ERA), NASA's Hankel-SVD method for
structural dynamics, applied to measured violin **bridge admittance** impulse
responses: one algebraic step replaces the usual multi-stage modal fit, and it
beats both Maestre baselines on six violins[^1]. See [[modal-analysis-measurement]],
[[coupled-structures]] and [[resonator-bank-implementation]].

## Problem
Assume the bridge admittance (force in, velocity out) is a finite-dimensional
proper rational system, i.e. there exists a discrete-time realization
$$x[k+1] = Ax[k] + b\,u[k],\quad y[k] = c^{\!\top}x[k] + d\,u[k],\qquad
Y(z) = c^{\!\top}(zI-A)^{-1}b + d .$$
Bridge-admittance modeling is then just: find $(A,b,c,d)$ from a measured IR.
In modal (diagonal) form $A = \mathrm{diag}(p_1,\dots,p_M)$ this is a parallel
resonator bank.

## ERA construction
For a unit pulse the response gives the **Markov parameters**
$y[0]=d$, $y[1]=c^{\!\top}b$, $y[k]=c^{\!\top}A^{k-1}b$ for $k\ge2$. Stack them into
a Hankel matrix $H_0$ ($r\times s$, entries $y[i+j-1]$) and its shift $H_1$
(entries $y[i+j]$). Noise-free, $H_0 = \mathcal{O}_r\mathcal{C}_s$ factors into the
extended observability and controllability matrices, so $\mathrm{rank}\,H_0$ is the
minimal order; with measurement noise $H_0$ is full rank and the order must be
inferred by separating dominant from noise-dominated singular values. Take the SVD
$H_0 = U\Sigma V^{\!\top}$, truncate to the $m$ largest singular values
($H_0 \approx U_m\Sigma_m V_m^{\!\top}$), and read off
$$\hat A = \Sigma_m^{-1/2}U_m^{\!\top}H_1V_m\Sigma_m^{-1/2},\quad
\hat b = \Sigma_m^{1/2}V_m^{\!\top}e_1^{(s)},\quad
\hat c = \Sigma_m^{1/2}U_m^{\!\top}e_1^{(r)},\quad \hat d = y[0].$$
$\hat A$ is dense; if diagonalizable, $\hat A = Q\Lambda Q^{-1}$ and the coordinate
change $\hat A\!\leftarrow\!\Lambda$, $\hat b\!\leftarrow\!Q^{-1}\hat b$,
$\hat c\!\leftarrow\!Q^{\!\top}\hat c$ gives the modal form used for analysis.

**Model order.** $r,s$ must be large enough not to truncate the dominant dynamics
but small enough to avoid noise sensitivity and ill-conditioning. The SVD
truncation is the explicit complexity-versus-fidelity knob that makes ERA a
reduced-order modeler, not just a realization algorithm.

## Baselines compared
| Method | Poles from | Gains from |
|---|---|---|
| Maestre et al. 2013 | peak picking (M-1 peaks in $[f_{\min},f_{\max}]$ plus one bridge-hill peak), half-power bandwidths, then nonlinear optimization of $\xi=[f_1..f_M,B_1..B_M]$ minimizing $\sum_k \big\lvert\log\lvert Y\rvert - \log\lvert\hat Y\rvert\big\rvert$ under $B_m>0$, ordering and box constraints | non-negative constrained least squares on the modal basis |
| Maestre et al. 2021 | AR all-pole fit on a **frequency-warped** IR ($z\leftarrow(\zeta+\rho)/(1+\rho\zeta)$, $\rho=0.85$), roots mapped back | unconstrained least squares, $\min\lVert y - Hc\rVert_2^2$ |
| ERA | Hankel SVD, one step | contained in $\hat b,\hat c$ |

2013 settings: $f_{\min}=50$ Hz, $f_{\max}=1300$ Hz, spectrum capped at 6000 Hz.

## Data
Six violins - five modern ones (f1-f5) from the Stradivari Triennial Competition
collection and one 18th-century Stradivari (f6). Free-free approximation by four
rubber bands; PCB 086E80 hammer with a vinyl cap (protects historical instruments,
weakens high-frequency excitation), PCB 352A12 accelerometer on the opposite
bridge edge. Six two-second acquisitions at 48 kHz per instrument;
accelerometer integrated to velocity, normalized by force, averaged, converted to
a minimum-phase sequence with the same real cepstrum, then cropped to
$L\in[0.15,0.30]$ s to avoid fitting noise.

## Metrics and results
Time-domain NMSE$_t$, magnitude-response NMSE$_f$, and NMAE between Energy Decay
Relief representations, $R[t_n,\omega_k]=10\log_{10}\sum_{t_m\ge t_n}|S[t_m,\omega_k]|^2$
(STFT: 20 ms Hann, 1024-point FFT, 5 ms hop). Model order swept $M=2,4,\dots,50$;
the best aggregate order is $M=50$ in most cases for both ERA (46-50) and Maestre
2021, whereas Maestre 2013 saturates at $M=13$-24 because peak picking runs out of
peaks. Metrics at those orders ($\times10^{-2}$, lower is better):

| Violin | NMSE$_t$ [2013 / 2021 / ERA] | NMSE$_f$ [2013 / 2021 / ERA] | NMAE$_{\rm EDR}$ [2013 / 2021 / ERA] |
|---|---|---|---|
| f1 | 38.65 / 8.13 / **1.54** | 21.40 / 4.36 / **0.79** | 1.14 / 1.25 / **0.79** |
| f2 | 65.78 / 5.17 / **2.13** | 44.77 / 2.59 / **1.07** | 0.99 / 1.14 / **0.70** |
| f3 | 36.59 / 9.25 / **2.81** | 22.05 / 4.66 / **1.47** | 1.12 / 1.11 / **0.72** |
| f4 | 31.09 / 6.11 / **2.23** | 16.79 / 3.20 / **1.18** | 1.18 / 1.11 / **0.62** |
| f5 | 36.97 / 7.16 / **2.09** | 20.17 / 3.84 / **1.04** | 1.25 / 1.18 / **0.72** |
| f6 | 18.03 / 6.02 / **1.64** | 8.39 / 3.00 / **0.85** | 1.15 / 1.16 / **0.93** |

ERA wins every cell: about one order of magnitude better than the 2013 method in
NMSE$_t$, 3-5$\times$ better than 2021. It is most accurate over 200 Hz-3 kHz
(where the characteristic violin resonances live) while Maestre 2021 fits better
above 3 kHz; both ERA and the 2013 method capture a 130 Hz mounting-rig peak that
frequency warping hides. On the EDR, the 2013 fit has almost no energy above
1.5 kHz and the 2021 fit loses it within milliseconds, while ERA tracks the
measured decay at both ends of the band.

## Caveats
- **Passivity is not guaranteed.** The paper motivates modal methods by noting that IIR fitting can be unstable for lack of guaranteed passivity, but the ERA realization carries no passivity guarantee either and none is enforced or tested - a real concern when the body filter sits inside a bowed-string feedback loop.
- No method reproduces the measured EDR exactly (ERA is only the closest); six instruments, one drive point, no listening test.

[^1]: [[entities/source-papers#paper-giampiccolo-era-violin-bridge-2026]] - Giampiccolo, Mezza, Malvermi, Pezzoli, Bernardini & Antonacci, "Eigensystem Realization of Violin Bridge Admittances," DAFx26.

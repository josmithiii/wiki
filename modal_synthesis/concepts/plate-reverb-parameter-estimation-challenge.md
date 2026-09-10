---
title: Plate Reverb Parameter Estimation Challenge
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [modal, eigenmode, resonator, room, damping, ml, comparison, reference, dataset]
sources:
  - /l/dttd/DAFx26/DAFx26_challenge_76.pdf
  - /l/dttd/DAFx26/DAFx26_challenge_82.pdf
  - /l/dttd/DAFx26/DAFx26_challenge_83.pdf
  - /l/dttd/DAFx26/txt/DAFx26_challenge_76.txt
  - /l/dttd/DAFx26/txt/DAFx26_challenge_82.txt
  - /l/dttd/DAFx26/txt/DAFx26_challenge_83.txt
---

# Plate Reverb Parameter Estimation Challenge

The 1st DAFx Parameter Estimation Challenge (Gabrielli and Ducceschi, announced DAFx25, run early 2026): recover a
plate's **physical** parameters (Task A) or its **modal** parameters (Task B) from one impulse response[^1]. 13
participants, 22 methods (12 A, 10 B), scored on 16 secret IRs. See [[ml-modal-parameter-estimation]],
[[modal-analysis-measurement]] and [[modal-pole-harvesting-from-irs]] for the Task B methods.

## The reference model
Everything is synthetic - no real plate is measured. Transverse displacement obeys the damped
**Kirchhoff-Love** equation with simply supported edges, $D = Eh^3/12(1-\nu^2)$:
$$\rho h\,\partial_t^2 u = -\rho h\,\mathcal{K}u - 2\rho h(\eta_0+\eta_1\mathcal{K})\partial_t u
+ \delta(\mathbf{x}-\mathbf{x}_i)f(t),\qquad
\mathcal{K} := -\frac{T_0}{\rho h}\Delta + \frac{D}{\rho h}\Delta\Delta .$$
Simply supported edges give the analytic modes, $\gamma_m=(m_x^2\pi^2/L_x^2+m_y^2\pi^2/L_y^2)^{1/2}$:
$$\Phi_m = \frac{2}{\sqrt{L_xL_y}}\sin\frac{m_x\pi x}{L_x}\sin\frac{m_y\pi y}{L_y},
\qquad \Omega_m=(\rho h)^{-1/2}\gamma_m\left(T_0+D\gamma_m^2\right)^{1/2}.$$
Modal projection decouples the PDE into
$\ddot q_m = -\Omega_m^2 q_m - 2\sigma_m\dot q_m + (\rho h)^{-1}\Phi_m(\mathbf{x}_i)\delta(t)$ with
frequency-dependent loss $\sigma_m := \eta_0+\eta_1\Omega_m^2$: each mode is a second-order all-pole
section with residue $\Phi_m(x_i,y_i)\Phi_m(x_o,y_o)$ and the response at $\mathbf{x}_o$ is the
parallel sum of $M$ of them (see [[resonator-bank-implementation]]), discretised exactly as
$q_m[k+1]=2r_m\cos(\Omega_m T)q_m[k]-r_m^2q_m[k-1]+b_m f[k]$, $r_m=e^{-\sigma_m T}$,
$b_m=4T^2\Phi_m(x_i,y_i)\Phi_m(x_o,y_o)r_m/(\rho h L_xL_y)$. Losses are set through decay times
$\tau_m = 3\log(10)/\sigma_m$ at $\Omega_0=0$ and $\Omega_1=2\pi\cdot500$ Hz ($\tau_0=6$ s, $\tau_1=2$ s,
$\tau_0>\tau_1$ enforced). IRs are 1 s at 44.1 kHz; $L_x$, $\nu$, $\eta_0$, $\eta_1$ and the input
position are fixed, while $L_y\in[1.1,4]$ m, $h\in[1,5]$ mm, $T_0\in[0.01,1000]$ N/m,
$\rho\in[2430,21230]$ kg/m$^3$, $E\in[6.7,22]\times10^{10}$ Pa and $x_o,y_o\in[0.51L,L]$ vary.

## Task A: six identifiable physical parameters
$$S(P) = \{\mu := \rho h,\; D/\mu,\; T_0/\mu,\; L_y,\; x_o,\; y_o\}$$
The raw $(\rho,h,E,T_0)$ enter the equation of motion **only** through those invariants, so a one-parameter family of
raw tuples gives an identical IR; using $S(P)$ makes the ground truth unique. All six are identifiable only if
**absolute IR amplitude is preserved** - $b_m \propto 1/(\rho h)$, so peak-normalising destroys the only cue to $\mu$;
IRs were therefore distributed as `.npz` with absolute scale plus a normalised `.wav` (listening check only). Metric:
NMSE on the six range-normalised parameters, with log-magnitude spectral MSE as an auxiliary. Baselines: PSO (50
particles $\times$ 20 iterations) on a three-resolution multi-scale spectral loss, about 33 min per IR; and a constant
predictor.

## Task B: modal triples
Recover $\{\Omega_m,\sigma_m,b_m\}$ for an **unknown** number of modes. Identified and true modes are matched
one-to-one by **Hungarian assignment on log-frequency distance** (so confusing 100 with 110 Hz costs the same as 1
with 1.1 kHz), accepted only within half an octave; unmatched true modes get estimate zero and error 1, per-component
errors clipped at 1:
$$\mathrm{RE}_\theta = \frac{1}{M}\sum_m \min\!\left(1,\frac{|\theta_m^{\rm est}-\theta_m^{\rm ref}|}{\theta_m^{\rm ref}}\right),\;
\mathrm{RE}_0 = \tfrac13(\mathrm{RE}_\Omega+\mathrm{RE}_\sigma+\mathrm{RE}_b),\;
\mathrm{RE} = \mathrm{RE}_0 + \min\!\left(1,\tfrac{\Delta M}{M}\right)\in[0,2].$$
Normalising $\Delta M$ by $M$ keeps the count mismatch on the same scale as $\mathrm{RE}_0$ (raw $\Delta M$ reaches
thousands). Baseline: peak picking with parabolic frequency refinement, half-power-bandwidth damping
$\sigma_m\approx\Delta\omega_m/2$, and the single-mode gain approximation $H(e^{j\Omega_mT})\approx -j b_m/(2\sigma_m
T\sin\Omega_mT)$.

## Final rankings
Task A, by mean NMSE (Table 3): 1. Marttila 13-A2 (QMUL) $1.8\times10^{-13}$; 2. Park & Yi 10-A $1.9\times10^{-11}$;
3. Lee 9-A $1.0\times10^{-4}$; 4. Sechet 5-A $4.7\times10^{-4}$; 5. Marttila 13-A1 $1.1\times10^{-3}$; 6. Heminway
7-A; 7. Guo 4-A; 8. Lipkin 8-A; 9. Lu 2-A; 10. Kim 11-A; 11. Garofalo 6-A (mean 0.018, **median $6.1\times10^{-6}$**);
12. PSO baseline 0.048; 13. Yang 1-A 0.056; 14. constant predictor 0.120.

Task B, by mean RE (Table 4), with the frequency-domain rank; mean true count $\bar M = 5303$:

| Rank | Entry | RE | $\mathrm{RE}_\Omega$ | $\mathrm{RE}_\sigma$ | $\mathrm{RE}_b$ | $\Delta M$ | $L_1$ on $\log\lvert H\rvert$ (rank) |
|---|---|---|---|---|---|---|---|
| 1 | Marttila 13-B1 (U-Net) | 0.328 | 0.013 | 0.058 | 0.847 | 135 | 0.882 (3) |
| 2 | Marttila 13-B2 (cplx transformer) | 0.337 | 0.016 | 0.023 | 0.925 | 125 | 2.983 (10) |
| 3 | Lu 2-B | 0.539 | 0.025 | 0.569 | 0.838 | 278 | **0.625 (1)** |
| 4 | Heminway 7-B | 0.643 | 0.201 | 0.268 | 0.868 | 1738 | 0.651 (2) |
| 5 | Bittner 3-B | 0.743 | 0.249 | 0.760 | 0.970 | 509 | 1.561 (7) |
| 6 | Zhang 4-B | 0.862 | 0.272 | 0.499 | 0.913 | 2108 | 1.905 (9) |
| 7 | Franchino 9-B | 0.957 | 0.324 | 0.800 | 0.937 | 1546 | 1.646 (8) |
| 8-9 | Jung 12-B2 / 12-B1 | 1.066 / 1.102 | 0.184 / 0.349 | 0.530 / 0.665 | 0.881 | 2725 / 2853 | 1.125 / 1.051 |
| 10 | Cogliati 8-B | 1.485 | 0.650 | 0.935 | 0.906 | 4166 | 1.160 (6) |
| - | Baseline | 1.968 | 0.983 | 0.985 | 0.973 | 5242 | 2.463 (11) |

## Lessons
- **Task A is solved inside the training range, by opposite routes.** The winner is an Audio Spectrogram Transformer conditioning a continuous normalizing flow, whose samples seed PSO plus gradient polishing; on a 100-IR holdout, refinement cuts waveform and parameter errors by more than three orders of magnitude over the raw neural output - neural nets work best as *initialisers*[^2]. Second place uses **no training at all**: CMA-ES over seven raw parameters under an amplitude-normalised loss (which is robust but destroys the cue to $\mu$), then a 50-iteration ternary search recovering $\mu$ alone; 49 of 50 validation IRs improve and the median NMSE falls by eleven orders of magnitude, at a median 32.6 s (Stage 1) plus 0.62 s (Stage 2) per IR. An ablation shows a unified one-stage CMA-ES is slightly worse and about an hour per IR[^3].
- **Dataset size, not architecture.** QMUL trained on 327,680 IRs, five times the next-largest set; a uniform 8-point grid over six parameters would be only 262,144 points, so the network has learned to interpolate a deterministic simulator in-distribution, and the benchmark cannot tell that from a general inverse solver. Both QMUL Task B entries share one formulation (per-bin mode density) and differ only in backbone, scoring almost identically - the formulation and training set drive the result, not the architecture.
- **Mode count is most of the score.** $E\{\mathrm{RE}\}$ and $E\{\Delta M\}$ rise almost in lockstep; the exception is 3-B, whose Matrix Pencil stage gets the count right but pays with $\mathrm{RE}_\sigma = 0.76$.
- **Gains are unrecoverable.** No Task B entry gets $\mathrm{RE}_b$ below 0.83. Two causes: in dense regions many modes lie within a fraction of a hertz, so their damped-sinusoid atoms are nearly linearly dependent and least squares recovers a cluster's joint amplitude, not individual gains; and $\mathrm{RE}_b$ normalises by $b_m^{\rm ref}$ and saturates at 1.
- **Most of the metric lives where the problem is ill-posed.** Modal overlap $\mu = (\sigma_m/\pi)/\Delta f$ crosses unity between 252 Hz and 1434 Hz across the 16 test plates (mean near 1 kHz), and only 9.5% of ground-truth modes lie below 1 kHz. Above the crossover no unique set of triples exists, and the half-octave matching threshold rewards predicting the right modal *density* rather than locating poles.
- **Frequency-domain re-ranking.** Comparing $\log|H(f)|$ on a 4096-point log grid over 20 Hz-10 kHz reorders everything: 2-B wins by consistency, 9-B is nearly exact above 1 kHz but overshoots at low frequency, and 13-B2 falls to last - its gains are uniformly about 30 dB low (median $\log_{10}|b_m|$ near $-12.6$ against $-11.0$ for 13-B1), an offset the saturating per-mode metric cannot see.
- **Portability.** Task B methods estimate a biquad bank, the standard reduced-order form of any LTI modal system, so classical and hybrid entries (3-B, 7-B, 9-B) would carry over to other geometries or measured plates almost unchanged, while the QMUL entries would need retraining. Task A methods estimate the parameters of one specific PDE. A future edition intends to reserve test conditions nobody can sample in advance: out-of-range parameters, measurement noise, free rather than simply supported edges, and if possible a real plate.

[^1]: [[entities/source-papers#paper-gabrielli-dafx-challenge-overview-2026]] - Gabrielli & Ducceschi, "The 1st DAFx Challenge: Physical and Modal Parameter Estimation for Plate Reverberation," DAFx26.
[^2]: [[entities/source-papers#paper-marttila-transformer-pso-taska-2026]] - Marttila, Diaz, Tablas De Paula, Ibnyahya & Yu, "Transformer-Based Plate Parameter Estimation with Differentiable and Particle-Swarm Refinement," DAFx26.
[^3]: [[entities/source-papers#paper-park-two-stage-evolutionary-taska-2026]] - Park, Yi, Kim & Kim, "Accurate Plate Reverb Parameter Estimation Using Two-Stage Evolutionary Search," DAFx26.

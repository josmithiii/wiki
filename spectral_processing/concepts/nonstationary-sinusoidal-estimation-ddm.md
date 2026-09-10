---
title: Nonstationary Sinusoidal Estimation with the Distribution Derivative Method
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [sinusoidal, qifft, peak-detection, sms, residual, gauss, stft]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_34.pdf
  - spectral_processing/raw/DAFx26_paper_34.txt
---

# Nonstationary Sinusoidal Estimation with the Distribution Derivative Method

Quasi-stationary sinusoidal analysis (peak picking plus
[[qifft-peak-estimation]]) assumes partials are stable *inside* the
frame. Attack transients violate that. The **distribution derivative
method** (DDM, Betser 2009) estimates **polynomial modulation
sinusoids** (PMS) of arbitrary order directly from two windowed DFTs,
putting the AM and FM *inside* the frame instead of between frames.[^caetano-2026]

## Polynomial modulation sinusoid (PMS) model

One partial (index dropped) over the analysis frame:
$$x(t) \;=\; \exp\!\Big\{\sum_{q=0}^{Q}\alpha_q t^q\Big\}
        \;=\; \exp\!\Big\{\alpha_0 + \sum_{q=1}^{Q}\alpha_q t^q\Big\},
\qquad \alpha_q = a_q + j\,b_q \in \mathbb{C}$$
- $\mathrm{Re}$ part = log-amplitude polynomial, $\mathrm{Im}$ part = phase polynomial, so AM and FM share one parametric form.
- $Q=1$: stationary ($a_1=0$) or exponentially damped sinusoid. $Q=2$: linear chirp (cf. [[gaussian-and-chirp-windows]]). $Q=3$: cubic phase, the case used here.
- The sinusoidal component is $s(t)=\sum_k \exp\{A_k(t)+j\Phi_k(t)\}$, and $y(t)=s(t)+r(t)$ as in [[sms-sines-plus-noise]].

## The DDM identity

With a test function $\psi$ of compact support $U_\psi$, differentiable
at least once, and inner product $\langle x,\psi\rangle=\int x\bar\psi\,dt$,
integration by parts over $U_\psi$ (where $\psi$ vanishes at the borders) gives
$$\langle \dot x,\psi\rangle \;=\; -\,\langle x,\dot\psi\rangle .$$
Differentiating the PMS model gives $\dot x(t)=\sum_{q=1}^{Q}\alpha_q\,q\,t^{q-1}x(t)$,
which depends only on $t$ and $q$. Substituting yields the **DDM estimation equation**
$$\sum_{q=1}^{Q}\alpha_q\,\langle q\,t^{q-1}x,\;\psi\rangle \;=\; -\,\langle x,\dot\psi\rangle,$$
**linear in the unknown $\alpha_q$** - the derivative of the unknown
signal has been replaced by the derivative of the known window.

## Window-derivative form and the DFT system

For the windowed Fourier transform $\psi(t)=w(t)e^{j\omega t}$,
$\dot{\bar\psi}(t)=[\dot w(t)-j\omega w(t)]e^{-j\omega t}$, so
$$\langle x,\dot\psi\rangle \;=\; \langle x,\tau\rangle - j\omega\,\langle x,\psi\rangle,
\qquad \tau(t)=\dot w(t)e^{j\omega t}.$$
Only **two** windowed transforms are needed: one with $w$, one with
$\dot w$ (analytic for the usual windows; not for rectangular, which is
discontinuous, nor for the Slepian/DPSS window, which has no closed form).

Stacking $R$ DFT bins $\psi_k=w(n)e^{j\omega_k n}$ around a spectral peak
gives an $R\times Q$ linear system in $(\alpha_1,\dots,\alpha_Q)$:
- Solvable for $R\ge Q$; larger $R$ **reduces bias** provided the bins stay in the main lobe.
- Zero padding therefore buys accuracy cheaply via the FFT - the same argument as [[zero-padding-and-interpolation]].
- $R$ is chosen per peak from the peak's shape, so estimation is per-peak.
- $\alpha_0$ (constant amplitude and initial phase) is *not* in the derivative system; it is recovered afterwards from $\langle\bar x,\psi\rangle e^{\alpha_0}=\langle x,\psi\rangle$ by least squares (pseudo-inverse) over the same bins.

## Model order and peak selection

- DDM raises $Q$ "effortlessly" (one more column); earlier work reached $Q=5$ but estimation accuracy did not justify the cost. Caetano uses $Q=3$.
- Peaks are screened by four constant thresholds before estimation: absolute level $\rho_a=-110$ dB, relative level $\rho_r=-80$ dB, average peak-to-trough difference $\bar\varepsilon = 7$ dB, and main-lobe bandwidth $\rho_B$ (troughs left/right, $0.8\,\frac{N}{M}B_\mathrm{mlw}$, $B_\mathrm{mlw}=4$ bins for Hann).
- **Peak selection is named as the major remaining source of modeling error**: estimating from a peak that is not a sinusoid poisons the whole system.

| Model | Analysis amp | Analysis phase | Synthesis amp | Synthesis phase |
|---|---|---|---|---|
| SM+ | constant | linear | linear | cubic |
| eaQHM | adaptive | adaptive | linear | cubic |
| DDM | (log) cubic | cubic | (log) cubic | cubic |

DDM resynthesis here is plain OLA of each frame built from the PMS
formula; polynomial phase interpolation across frames
([[sinusoidal-parameter-interpolation]]) gave no audible difference.

## Comparison protocol and results

- 39 sounds (VSL and SOL), forte/fortissimo, mostly C4: 13 sustained (ordinario), 13 percussive (incl. plucked), 13 modulated (vibrato, sforzando, pizzicato, staccato).
- Common settings: zero-phase noncausal Hann, $M=6T_0f_s$ samples, 50% overlap, $f_s=44.1$ kHz, $K=100$ partials max.
- Frequency-domain measures on $V(\theta)=\ln|Y(\theta)|^2-\ln|S(\theta)|^2$: RMS log spectral measure (the $L_2$ norm of $V$, in dB) and Itakura-Saito divergence $D=\frac{1}{2\pi}\int(e^{V}-1-V)\,d\theta$; both medians across frames, lower is better.
- Time-domain measure: signal-to-residual ratio $\mathrm{SRR}=10\log_{10}(\langle y,y\rangle/\langle r,r\rangle)$ over the full waveform, higher is better; strict, since even an $\alpha_0$ error raises residual energy.
- **SRR for DDM is higher than SM+ and eaQHM for every sound except marimba** (eaQHM failed to converge on glockenspiel). RMS-LSM/ISD differences versus eaQHM are attributed mainly to peak selection: eaQHM fits its harmonic template even to noise, which lowers its spectral distances without raising SRR.
- MUSHRA (18 sounds, 6 per technique; 13 took the test, 5 kept after BS.1534-3 post-screening): significant main effect of model, $F(4,16)=40.98$, $p=3.2\times10^{-8}$; **no** main effect of playing technique, $F(2,8)=0.263$, $p=0.775$; significant model x technique interaction, $F(8,32)=10.94$, $p=2.8\times10^{-7}$. Pairwise (Holm-Bonferroni): DDM > eaQHM ($p=2.7\times10^{-9}$) > SM+ ($p=2.0\times10^{-3}$) > anchor; REF > DDM only weakly ($p=9.1\times10^{-3}$), i.e. DDM is nearly transparent. Playing technique affected eaQHM and SM+ ratings but not DDM.

## Limitations

- Only 5 listeners survived screening, so the perceptual result is thin.
- Higher $Q$ means more parameters per partial per frame; no rate/quality trade-off is reported.
- Window choice is untested (main-lobe concentration drives the bias); speech and polyphonic audio untried.

## Related Concepts
- [[sinusoidal-modeling]] - the quasi-stationary pipeline this replaces at the frame level
- [[qifft-peak-estimation]] - the QSS estimator used by the SM+ baseline
- [[sinusoidal-parameter-interpolation]] - intra-frame modulation versus cubic-phase continuation
- [[entities/source-papers#paper-caetano-ddm-polynomial-amfm-2026]] - catalog entry

[^caetano-2026]: Marcelo Caetano, "Using the Distribution Derivative Method to Model Acoustic Musical Instrument Sounds with Polynomial AM-FM Sinusoids," *Proc. DAFx26*, Cambridge MA, Sept. 2026, pp. 274-281. Distilled in [[entities/source-papers#paper-caetano-ddm-polynomial-amfm-2026]].

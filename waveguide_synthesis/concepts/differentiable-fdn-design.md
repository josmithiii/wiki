---
title: Differentiable FDN Design
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [fdn, reverb, room, differentiable, ml, optimization, faust]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_10.pdf
  - /l/dttd/DAFx26/DAFx26_demo_61.pdf
  - raw/DAFx26_paper_10.txt
  - raw/DAFx26_demo_61.txt
---

# Differentiable FDN Design

Fitting a feedback delay network to a measured room impulse response by gradient
descent, and getting the trained network out as real-time code.

## Making a recursive network differentiable

Backprop through an IIR loop sample by sample is impractical, so the
**frequency-sampling method** (Rabiner; Lee et al.; FLAMO) evaluates
$$H(z) = \mathbf{c}^{\!\top}\!\left(D_{\mathbf{m}}(z)^{-1} - U\Gamma(z)\right)^{-1}\mathbf{b} + d$$
on an $N_{\text{FFT}}$-point grid, turning the recursion into an FIR approximation with a
time-domain anti-aliasing decay envelope at the window edge. Integer delays become
differentiable as fractional delays in the same parameterisation, and an orthogonal
mixing matrix stays lossless by being written as $\exp$ of a skew-symmetric matrix.

## Parameter-efficient attenuation (Ibnyahya & Reiss)

The key economy is Jot's proportionality condition. On the unit circle
$$|\Gamma_n(z)| = |\Gamma_{\text{prot}}(z)|^{m_n},
\qquad \gamma_{\text{dB}}(k) = \frac{-60}{f_s\,T_{30}(k)},
\qquad G_{i,n} = \frac{-60}{f_s\,\gamma_i}\,m_n .$$
One **prototype PEQ** of $B$ bands is shared by all $N$ delay lines and per-line gains
follow by the linear scaling above, so the attenuation stage has $3B$ trainable
parameters **independent of $N$** - versus $B \times N$ gains for a per-line graphic EQ
(160 at octave resolution, 480 at third-octave for $N = 16$). Each band's
$(f_i, Q_i, \gamma_i)$ is an unconstrained real mapped through a sigmoid into
$[20\,\text{Hz}, 20\,\text{kHz}]$, $[0.2, 2.0]$ and $[0.05, 100]$ s; gains are clamped to $[-30,0)$ dB.

Architecture: $N = 16$ lines at 48 kHz; branch A = FDN loop + post-loop tone PEQ,
branch B = 64-tap sparse early-reflection delay line ($g_p, \tau_p$ trainable, taps at
the target's largest peaks, 50 ms span); summed, then a trainable Butterworth bandpass.

Loss: composite, centred on the **energy decay relief**
$\mathrm{EDR}(t,k) = \sum_{\tau \ge t}|X(\tau,k)|^2$, normalised to 0 dB, masked softly to the
$[-35,-5]$ dB range used by $T_{30}$, with $1/k$ weighting so each octave contributes about
equally. Eight further terms - band-$T_{30}$, linear EDC, band energy, power spectrum,
early-energy ratios at 5/50/80 ms, DRR, echo density, and a Gaussian-smoothed
time-domain $L_1$ which is what actually gives the delays and ER taps a gradient - each
normalised by its value at initialisation, weight-capped at 20.

## Reported numbers

Nine OpenAIR RIRs (studio $T_{30}\approx0.2$ s to cathedral/sports hall $\approx6$ s), Adam
at $10^{-2}$, up to 300 epochs, RTX 4070 Super, under two minutes per short RIR.

| Model | $T_{30}$ MAE (s) | DRR (dB) | $E_{50}$ | EDR (dB) | MRSTFT | mults/sample |
|---|---|---|---|---|---|---|
| NoiseShaper baseline | 0.311 | 5.28 | 7.49 | **7.78** | 80.4 | conv. |
| Mezza-style diff. FDN (16 kHz) | 1.382 | 8.08 | 5.87 | 28.87 | 194.2 | 490 |
| RIR2FDN analysis-synthesis | 0.444 | 15.15 | 16.70 | 15.95 | 273.7 | 1175 |
| Proposed, all differentiable | **0.261** | 0.52 | 2.10 | 17.60 | 52.6 | 1222 |

- PEQ-10 beats third-octave GEQ on $T_{30}$ with **2.8x fewer** multiplications (966 vs
  2751) and trains about **6x faster** (2.8 vs 17.2 min).
- Early-reflection taps cut $E_{50}$ from 5.93 to 2.10; training delays and matrix
  cuts $T_{30}$ MAE 0.315 -> 0.261 s and $D_{50}$ 7.27 -> 4.86 pp.
- Cost is comparable to partitioned convolution of a 3 s RIR (~1222 vs ~1155
  mults/sample) at roughly **11x less** state memory (100.85 kB vs ~1143 kB).
- Caveat: fully trained delay lengths drift toward near-commensurate values and add
  metallic ringing, so the fixed-delay, fixed-Hadamard variant is the safer
  deployment; the noise-shaped baseline still wins on EDR.

## Export and tooling

- **ADAC** (Franchino & Schlecht) walks a trained PyTorch graph into a framework-agnostic
  JSON IR (Series / Parallel / Recursion nodes with parameterised leaves) and emits FAUST.
  FAUST's `~` adds one implicit sample, so in-loop lines are emitted as $z^{-(m_i-1)}$ with a
  single $z^{-1}$ outside, giving the exact loop period; impulse responses match the source
  model to $7 \times 10^{-5}$ of peak. Macro-controls are reverberation time
  ($g_i = 10^{-3m_i/(f_s\,\mathrm{RT})}$, measured 0.5000 s for a 0.5 s setting), dry/wet and
  pre-delay. A **small-gain stability certificate**
  $\sup_\omega \prod_k \sigma_{\max}(E_k(e^{j\omega})) < 1$ is computed on the emitted single-precision
  values (a trained orthogonal matrix measured $\sigma_{\max} = 1.000000170$ after the cast),
  and the exporter refuses an unstable or unproven model; a lossless prototype is only
  "marginally stable" until the RT control attenuates the loop. Cost is $\Theta(N^2 + NS)$;
  a 32-line FDN runs ~90x real time on an Apple M2, and the running plug-in
  hot-reloads the model in under 10 ms per gradient step.
- **sfFDN / FDN Sandbox** (St-Onge & Scavone) takes the non-differentiable route -
  see [[entities/sffdn-library]].

## See also
- [[artificial-reverberation]] - the FDN being fitted
- [[waveguide-parameter-optimization]] - the wider optimization taxonomy
- [[entities/source-papers#paper-ibnyahya-differentiable-fdn-rir-2026]] and [[entities/source-papers#paper-franchino-adac-differentiable-to-faust-2026]] - catalog entries[^src]

[^src]: I. Ibnyahya & J. D. Reiss, "Gradient Descent Optimization of Room Impulse Responses with Parameter-Efficient Differentiable Feedback Delay Networks"; F. Franchino & S. J. Schlecht, "Compiling Differentiable Audio Graphs to Real-Time DSP"; A. St-Onge & G. Scavone, "FDN Sandbox," all DAFx26.

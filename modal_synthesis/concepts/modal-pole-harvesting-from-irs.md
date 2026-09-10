---
title: Modal Pole Harvesting from IRs
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [modal, eigenmode, resonator, dsp, impulse-response, ml, neural, inference, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_challenge_88.pdf
  - /l/dttd/DAFx26/DAFx26_challenge_87.pdf
  - /l/dttd/DAFx26/txt/DAFx26_challenge_88.txt
  - /l/dttd/DAFx26/txt/DAFx26_challenge_87.txt
---

# Modal Pole Harvesting from IRs

How do you pull $10^3$-$10^4$ modal triples $(f_m,\sigma_m,b_m)$ out of a single
dense impulse response when the mode count is unknown? Task B of the DAFx26 plate
challenge produced two answers worth keeping: a pure-signal-processing pole
harvester and a neural reformulation that regresses mode *density* instead of
picking peaks. See [[plate-reverb-parameter-estimation-challenge]] for the task,
metric and rankings, [[modal-analysis-measurement]] for the classical family, and
[[state-space-models-as-modal-resonator-banks]] for the third approach
(matrix-pencil-initialised state space models with closed-form least-squares gains).

## The target
Each mode is a damped biquad atom,
$$H_m(z)=\frac{b_m z^{-1}}{1-2r_m\cos(\Omega_m T)z^{-1}+r_m^2 z^{-2}},
\qquad h_m[k]=b_m r_m^{k-1}\frac{\sin(k\Omega_m T)}{\sin(\Omega_m T)},\;k\ge1 .$$
Two facts shape every method here. First, the scoring is asymmetric: a **missed**
mode costs the maximum in all three components *and* in the count term, while a
**spurious** mode costs only the count term - so when in doubt, output too many.
Second, when many modes sit within a fraction of a hertz, their atoms are nearly
linearly dependent, so least squares recovers a cluster's joint amplitude but not
the individual gains, no matter the window length or regularisation.

## Multi-view subband AR pole harvesting (Franchino et al.)
The organising insight: **linear filtering changes residues but never moves
poles**[^1]. So the raw IR $x[n]$, its first difference $\Delta x[n]$ and its second
difference $\Delta^2x[n]$ are three *views* of the same pole set, each making a
different subset easy to see (the differences attenuate low frequencies). Pipeline:

1. **Matching-pursuit anchor stage.** Eight residual-subtraction iterations of an FFT peak picker; after each pass the joint anchor atom set is refit by ridge least squares and subtracted, so the next pass sees lower-prominence modes. Output: an anchor set $A=\{(f_a,\sigma_a)\}$ of several hundred entries per plate.
2. **Subband AR on each view.** Each view is split into eight log-spaced bands with 25% overlap; within a band the signal is shifted to baseband, lowpassed and decimated to just above the band width, and a complex AR (Prony/ESPRIT lineage) fit gives a polynomial whose roots are pole candidates - kept if inside the band, magnitude $<1$, positive decay. AR order is proportional to the expected count in the band, capped at 1800.
3. **Recursive band splitting.** A band is flagged **saturated** when the order cap is reached and the core still yields at least 50 stable poles. Saturated bands with log-frequency ratio $>1.20$ are split log-evenly in two and re-run, to recursion depth 2 - capacity goes where mode density is, without inflating cost on sparse low bands.
4. **Merge, de-duplicate, complete.** Candidates merge by log-gap $\Delta\log_2 f<0.0008$, each cross-view merge incrementing a support counter. An affine predictor $M_{\rm lin}=a\,n_a+b$ with $(a,b)=(10.10,-4437)$ turns the anchor count $n_a$ into an initial target; the **deficit ratio** $\rho=(M_{\rm lin}-n_{\rm AR})/\max(M_{\rm lin},1)$ is a per-IR saturation indicator, and the target is raised conservatively, $M_{\rm tgt}=\max(M_{\rm lin},\,n_{\rm AR}+\beta(\rho)\max(0,M_{\rm lin}-n_{\rm AR}))$ with $\beta = 1.05, 1.10, 1.20, 1.35$ as $\rho$ crosses 0.10, 0.30, 0.45. If the pool already exceeds $1.12M_{\rm tgt}$, candidates with the weakest cross-view support are dropped; otherwise the remaining slots get log-spaced placeholder frequencies.
5. **Gains.** One global ridge least squares in the atom convention above, $n=44100$ samples, per-column ridge $\lambda_m=10^{-8}\|a_m\|^2$ to balance low- and high-frequency modes whose column norms differ by orders of magnitude. The least-squares weight for mode $m$ *is* $b_m$.

The pipeline is non-iterative at the top level (no outer search, no restarts) and
reads only the unnormalised IR - no plate parameters, no analytical modal-frequency
or decay laws, no `.wav` files, no Task A information. Cost: about 6 h wall time for
the 16 test IRs on an M2 laptop with three-way parallelism. It ranked 7th of 10 on
the per-mode metric (RE 0.957) but is **nearly exact above 1 kHz** in the organizers'
frequency-domain re-evaluation, overshooting at low frequencies. Gains stay the
limitation; the authors suggest fitting each gain locally in the frequency domain,
or jointly refining frequency, decay and gain in a small neighbourhood.

## Count-density networks (Diaz et al.)
The winning reformulation drops peak picking entirely: **jointly infer a per-bin
mode density** on a 1/20-octave log-frequency grid from 20 Hz to 10 kHz, together
with per-bin decay and gain slots, so the unknown mode count is part of the
regression rather than a preprocessing decision[^2].

- **Inputs.** Peak-normalised waveform $\tilde x = x/g_x$ *plus* the stored peak $g_x$: the `.wav` files alone lack the absolute scale needed to restore gains. Downsampled to 22.05 kHz (no modes above 10 kHz), FFT bins kept to 10 kHz, gain targets expressed as $b_m/g_x$.
- **Loss.** All count terms in $\log(1+\cdot)$ space so dense bins do not dominate: Huber losses on per-bin, global-total, cumulative and multi-resolution counts (aggregated by 2, 5, 10) plus a cross-entropy aligning predicted with normalised target density; slot-wise Huber for decay and gain, masked to occupied slots. $L = L_{\rm count}+\lambda_\sigma L_\sigma + \lambda_b L_b$.
- **Decoding (shared).** Round the global count to $\tilde M$, rescale the per-bin density to sum to $\tilde M$, floor, and assign the remainder to the bins with the largest fractional parts - a **sum-preserving allocation** giving integer per-bin counts. Frequencies are then placed deterministically inside each occupied bin.
- **B1**: real-valued 1D U-Net (4 encoder stages 32-256, 512 bottleneck, skips) on row-normalised log magnitude plus sin/cos phase, mean-pooled into 1/120-octave intervals, with a strided time-domain CNN over the first 0.75 s and $\log g_x$ conditioning the bottleneck; global heads predict total count and the gain RMS scale $b_{\rm RMS}$; 3.1 M parameters, 26 epochs, about 24 h on one A100.
- **B2**: complex-valued Transformer - phase-preserving log compression of the full-resolution complex spectrum, a five-layer complex CNN tokeniser into 64 complex tokens, then six complex Transformer layers (model dim 320, 8 heads); about 99.6 M real parameters, 83.9 M of them in the dense bottleneck.

On an independently generated 100-IR set, B1 scores RE **0.318**
($\mathrm{RE}_\Omega = 0.0077$, $\mathrm{RE}_\sigma = 0.0508$, $\mathrm{RE}_b = 0.853$,
$\min(1,\Delta M/M)=0.014$) and B2 0.330, against 1.098 for the best classical
baseline evaluated there (Fast Burg) and 1.515-1.548 for band-wise ESPRIT, Matrix
Pencil and Root-MUSIC. Inference is 1-3 ms per IR on an A100 versus 17-442 s for
the classical estimators on 24 CPU cores. Frequencies are essentially perfect and
decays good; **gains are not**, the same wall every entry hit. And the overview's
frequency-domain check exposes what the per-mode metric hides: B2 reproduces the
right spectral shape about 30 dB too low.

[^1]: [[entities/source-papers#paper-franchino-subband-ar-pole-harvesting-2026]] - Franchino, Chowdhury, Lee, Kim & Rau, "Multi-View Subband Autoregressive Pole Harvesting for Modal Plate Identification," DAFx26 challenge report.
[^2]: [[entities/source-papers#paper-diaz-count-density-networks-2026]] - Diaz, Tablas De Paula, Marttila, Ibnyahya & Yu, "Count-Density Networks for Modal Plate Parameter Estimation," DAFx26 challenge report.

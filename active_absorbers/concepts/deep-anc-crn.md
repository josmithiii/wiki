---
title: Deep ANC — CRN End-to-End Anti-Noise Prediction
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [anc, feedforward, secondary-path, loudspeaker, causality, comparison]
sources:
  - raw/DeepANC-nihms-1690502.txt
  - raw/DeepANC-SpeechPreserving-Reverberant-2604.10979.txt
---

# Deep ANC (CRN-Based)

"Deep ANC" (Zhang & Wang, *Neural Networks* 141, 2021[^zhang21]) is the
canonical **end-to-end neural ANC** architecture: a convolutional recurrent
network takes the reference signal as input and outputs the anti-noise
waveform directly. There is no explicit FxLMS loop and no explicit
$\hat{S}(z)$ — both are subsumed into the learned mapping. Classical
feedforward ANC structure is preserved (reference → controller → secondary
path → error mic), but the "controller" is a CRN.

## Architecture

- **Input:** short-time STFT of the reference signal $x(n)$.
- **Encoder:** stack of 2-D convolutions with stride, reducing time-frequency
  resolution while widening the channel dimension.
- **Bottleneck:** LSTM across time frames (the "recurrent" in CRN) — gives
  the model a finite memory of reference-signal context.
- **Decoder:** mirror of the encoder with transposed convolutions, skip
  connections from the encoder (U-Net style).
- **Output head:** two real feature maps representing the real and imaginary
  parts of the anti-noise STFT, $\tilde{Y}(t,f) = \tilde{Y}_r + j\tilde{Y}_i$.
- Time-domain anti-noise is reconstructed by inverse STFT and driven through
  the physical secondary path to the error mic.

## Training objective

The loss is the squared magnitude of the residual at the error mic, computed
on a **simulated** secondary path during training:
$$
\mathcal{L} = \sum_{t,f}\big|\,D(t,f) - S(t,f)\tilde{Y}(t,f)\,\big|^2
$$
where $D(t,f)$ is the primary-path STFT at the error mic and $S(t,f)$ is the
(simulated) secondary-path transfer function. Because $S$ enters the loss
directly, the network **learns to pre-compensate the secondary path** — this
is the role played by the filtered-reference in classical [[fxlms-algorithm]].

## Multi-condition training and generalization

Training is performed over a large pool of noise types, SNRs, and simulated
rooms, so the CRN generalizes to **unseen noise categories** at test time. The
paper reports wideband reduction on noise types not present in training —
a long-standing weak point of linear FxLMS when the reference is broadband
and non-stationary.

## Nonlinear secondary paths

Because the secondary path in training can include an arbitrary nonlinear
loudspeaker model (saturation, hysteresis), Deep ANC **implicitly** solves
the nonlinear-FxLMS problem. Classical filtered-x assumes a linear plant; when
the plant is nonlinear, the filtered-reference correction is no longer an
unbiased gradient estimate (see [[fxlms-algorithm]] stability section).
Deep ANC simply inherits the correct backprop gradient through the
(differentiable) nonlinear plant model.

## Delay compensation / causality

Feedforward ANC requires that the electrical path be faster than the
acoustic path between reference mic and error mic. Zhang & Wang handle this
by deliberately aligning the training-time secondary-path delay with the
reference-vs-primary delay, so the network learns a **causal** mapping
under the realistic delay budget. The same causality constraint discussed
on [[lms-algorithm]] (Appendix B of Widrow 1975) and [[fxlms-algorithm]]
still applies — the network does not magically get future samples.

## Strengths

- Handles **nonlinear** secondary paths natively.
- **Generalizes** across noise types via multi-condition training.
- No online secondary-path identification — everything is baked in offline.
- Implementation is a standard neural-inference pipeline; no adaptive
  bookkeeping at runtime.

## Weaknesses and open questions

- **Static plant assumption.** Training bakes in a fixed (family of) secondary
  paths; if the physical $S(z)$ drifts significantly (temperature, wind,
  ear-cup fit), performance degrades until the network is retrained. This
  is the motivation for [[neural-secondary-path]] and for combining Deep ANC
  with online adaptation.
- **Latency.** STFT framing adds algorithmic delay. For applications like
  active [[headphones]] with tight causality budgets, frame size and hop
  size dominate feasibility.
- **No adaptation.** Unlike [[fxlms-algorithm]], Deep ANC does not
  self-correct if deployment conditions deviate from training. Latent FxLMS
  (Sarkar et al. 2025, see [[fxlms-algorithm]]) offers one path to
  *adaptive* neural ANC by keeping the online gradient step.

## Follow-up: speech-preserving Deep ANC in reverberant environments

A 2026 thesis from Dai Shuning (advisor Gan Woon Seng)[^dai26] extends
Zhang & Wang 2021 in two directions relevant to real deployments:

- **Reverberant-environment training.** The Image Source Method (ISM)
  generates training rooms with configurable geometry and $RT_{60}$,
  directly addressing the "trained on anechoic, deployed in rooms" gap
  in the original Deep ANC.
- **Speech-preservation loss.** A selective-retention term identifies
  speech-like time-frequency regions and penalizes their suppression
  while still cancelling environmental noise. Framing: "semantic
  separation," not pure power minimization. For hearing-aid and
  communication-headset applications this is critical — you want the
  fan noise gone *and* the voice untouched.
- **Architecture.** Still a CRN with LSTM, but using complex spectrum
  mapping (CSM) that processes STFT real and imaginary channels jointly
  rather than estimating a magnitude mask.
- **Metrics.** Beyond NR (dB), the evaluation includes PESQ (speech
  quality) and STOI (intelligibility), confirming that the preservation
  loss actually preserves speech.
- **Scenarios.** Pure noise, speech+noise, transients — all on ESC-50 and
  a custom dataset.

This is the clearest published evidence that end-to-end neural ANC can
*simultaneously* suppress broadband non-stationary noise and preserve
speech better than linear FxLMS — the gap the Gaikwad 2021 hearing-aid
paper claimed but did not rigorously demonstrate. See `raw/SUMMARIES.md`
for the per-paper distillation.

## Relation to other AI-ANC approaches

See [[ai-anc-overview]] for the full taxonomy. Deep ANC sits in category 1
("NN replaces the adaptive filter"); Latent FxLMS sits in category 2 and is a
complementary rather than competing idea.

[^zhang21]: Zhang, H., Wang, D., "Deep ANC: A Deep Learning Approach to Active Noise Control," *Neural Networks*, vol. 141, pp. 1–10, Sep 2021. See `raw/DeepANC-nihms-1690502.txt`.
[^dai26]: Dai, S., "Speech-preserving Active Noise Control: a Deep Learning Approach in Reverberant Environments," thesis (advisor: Gan, W. S.), arXiv:2604.10979, 2026. See `raw/DeepANC-SpeechPreserving-Reverberant-2604.10979.txt`.

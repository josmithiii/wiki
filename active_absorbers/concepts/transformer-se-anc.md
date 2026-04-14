---
title: Transformer-Based Speech Enhancement and Selective Noise Cancellation
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [anc, headphones, microphone, comparison, tutorial, reference]
sources:
  - raw/DeepLearningSelectiveNoiseCancellation-2507.07043v2.txt
---

# Transformer-Based SE / Selective Noise Cancellation

Transformer (and related attention-based) architectures dominate modern
speech enhancement and selective noise cancellation, with state-of-the-art
results reported in the Khan et al. 2025 review[^khan25]:
CRN real-time inference below 10 ms and Transformer architectures reaching
approximately 18.3 dB SI-SDR on reverberant benchmarks. This page is a brief
orientation; most of this literature is **open-loop speech enhancement**,
not the closed-loop feedforward ANC of [[fxlms-algorithm]] — but the
underlying acoustic-scene models transfer directly to neural ANC pipelines
such as [[deep-anc-crn]].

## Speech enhancement vs ANC — don't conflate

| | Speech enhancement / selective NC | Active noise control |
| --- | --- | --- |
| Goal | Output a cleaned *signal* for a listener's ear | Output an *anti-sound* that cancels the noise in a physical volume |
| Loop | Open-loop: one-shot mapping from noisy to clean | Closed-loop: error mic drives adaptation / reward |
| Secondary path | Not modeled | Central concern (see [[fxlms-algorithm]]) |
| Causality | Often acausal (algorithmic latency OK) | Strictly causal; acoustic delay budget |
| Use case | Hearing aids, phones, broadcast, captioning | Headphones, ducts, rooms, industrial enclosures |

Much of the "deep learning for hearing aids" literature reviewed in the
Khan paper and in Andersen et al. 2021 is actually SE; only the parts that
go through a physical loudspeaker and an error microphone are genuine ANC.
The wiki keeps both under this umbrella because the acoustic scene
modeling transfers between them.

## Architectural families covered by Khan et al.

- **CRN / U-Net.** Encoder–decoder with skip connections; typically the
  bottleneck is an LSTM. Real-time capable; easy to deploy. The base
  architecture of [[deep-anc-crn]] sits here.
- **Transformer encoder-only.** Self-attention across time-frequency tokens.
  Strong on long-range dependencies, weaker on streaming (context window
  latency).
- **Conformer.** Convolution + self-attention hybrid; currently the
  state-of-the-art across most SE benchmarks.
- **Mamba / SSM.** Linear-time sequence models; early results match
  Conformer at lower inference cost, but not yet broadly deployed for SE.
- **Diffusion-based enhancement.** Train a diffusion model on clean
  speech, condition on noisy input; excellent quality but latency and
  cost make it unsuitable for live ANC loops (today).

## Why SE papers matter to AI-ANC

Three transfer points:

1. **Encoder features.** The STFT / learned-filterbank front ends developed
   for SE are directly reusable as the reference-signal encoder in a
   Deep ANC–style controller.
2. **Scene-aware gating.** Selective-cancellation models (leave speech,
   remove fan) can be retrained to produce the *anti-noise* rather than the
   *residual speech*, recovering an ANC architecture.
3. **Benchmarks.** SE benchmarks (VoiceBank-DEMAND, WHAMR!, DNS-Challenge)
   provide acoustic-scene variation that no current ANC benchmark matches.
   We should port one of them as a training distribution for neural ANC.

## Limitations when dropped into an ANC loop

- **Latency.** Attention-based models need context; for headphone ANC the
  budget is a few milliseconds and most transformers do not fit without
  aggressive pruning or streaming hacks.
- **No secondary path.** SE models do not pre-compensate for the
  loudspeaker–error-mic channel. Deep ANC's training loss (see
  [[deep-anc-crn]]) shows how to add this.
- **Offline evaluation.** SI-SDR, PESQ, STOI do not measure cancellation
  in a physical room; the gap between SE metrics and ANC metrics is
  large and under-studied.

## Reading map

- Start at [[ai-anc-overview]] for the taxonomy.
- Deep dive on the closed-loop end-to-end flavor: [[deep-anc-crn]].
- For classical-loop approaches that *could* use a Transformer front end,
  see the Latent FxLMS variant on [[fxlms-algorithm]] and
  [[neural-system-identification]].

[^khan25]: Khan, H., Asif, S., Nasir, H., Bhatti, K. A., Sheikh, S. A., "Advances in Intelligent Hearing Aids: Deep Learning Approaches to Selective Noise Cancellation," arXiv:2507.07043, 2025. See `raw/DeepLearningSelectiveNoiseCancellation-2507.07043v2.txt`.

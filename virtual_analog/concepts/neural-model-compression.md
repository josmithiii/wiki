---
title: Neural Model Compression for Audio
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [pruning, wavenet, neural-va, ios, real-time, amplifier, plugin]
sources:
  - /l/dttd/DAFx26/DAFx26_demo_67.pdf
  - raw/DAFx26_demo_67.txt
---

# Neural Model Compression for Audio

The other lever on the callback budget: instead of a faster runtime (see
[[real-time-neural-inference-deployment]]), shrink the model. Iterative magnitude
pruning plus a sparsity-aware engine puts a WaveNet-style guitar amp model on an
iPhone CPU where the dense model cannot run at all.[^1]

## Model

- WaveNet-style causal feedforward stack of dilated convolutional residual blocks,
  learning $x[n] \mapsto \hat{y}[n]$ directly from raw guitar audio. Skip connections
  aggregate intermediate representations.
- Wright et al. configuration: $C = 16$ channels, kernel size 3, 18 layers with
  dilation pattern $d_k = \{1,2,4,\dots,256,\,1,\dots,256\}$, 1500 epochs. Plain
  $\tanh$ rather than gated $\tanh \times \sigma$, to cut C++ deployment cost.
- 21,913 total parameters, of which 21,152 are prunable.
- Trained with MSE on a pre-emphasized target, $H(z) = 1 - 0.95 z^{-1}$ (MSE converged
  faster and more stably than ESR here); evaluated with the error-to-signal ratio
  $E_\text{ESR} = \sum (y_p - \hat{y}_p)^2 / \sum y_p^2$, which normalizes for output
  loudness.

## Iterative magnitude pruning

- Each prunable tensor $W$ carries a binary mask $M$; the layer uses $W \odot M$ in
  both forward and backward passes.
- The mask is updated **every mini-batch** on a sparsity schedule ramping $s$ from 0 to
  the target $s_t$ between epochs $e_\text{start}$ and $e_\text{end}$, so the network
  adapts to sparsity *during* training.
- Grid over {local, global} magnitude x {linear, exponential} schedule, with
  $e_\text{start} = 10$ and $e_\text{end} \in \{250,500,750,1000,1250\}$: **iterative
  local pruning with an exponential schedule, $e_\text{end} = 750$** gave the lowest
  validation ESR.
- At 90 % sparsity, 19,074 of the 21,152 prunable weights are removed. Iterative
  pruning tracks the target waveform closely at that level; **one-shot** pruning at the
  same sparsity collapses well before it.

## Quality

- Four in-house captures - Vox AC15, Fender Deluxe Reverb, a Fender Tweed-style amp,
  and a Dunlop Fuzz Face pedal - recorded with a structured three-minute excitation
  signal. All ESR values below $3.4 \times 10^{-4}$ with no audible degradation in
  informal listening.
- Long-reverb settings gave the largest errors (tails exceed the model's receptive
  field); the directly recorded Fuzz Face gave the lowest ESR despite its strong
  nonlinearity.
- Residual limitation of a deterministic model: it cannot reproduce input-uncorrelated
  noise and hum, most visible for the high-gain Fuzz Face.

## Sparse inference engine on iOS

- CPU only. Metal (GPU) and Core ML (Neural Engine) were rejected because their public
  interfaces' per-block dispatch latency, plus the absence of low-level Neural Engine
  access, is impractical for a 256-sample block - the same conclusion as
  [[real-time-neural-inference-deployment]] and [[mobile-gpu-neural-audio]].
- The engine stores and iterates over **only the nonzero weights** in a compact,
  cache-friendly layout rather than masking a dense kernel, so *unstructured* sparsity
  becomes real compute savings. This is why the dilated-convolution stack is
  hand-written instead of using RTNeural, which operates on dense kernels.
- Fixed-size blocks at 48 kHz, configurable 64-512 samples, default 256 (about 5.3 ms).
  Fixed-point I/O, float internally. Against a Python reference with the same exported
  weights, the C++ engine matches to within **int16/float conversion quantization**
  after startup.
- Real-time factor falls roughly **linearly with sparsity** on an iPhone 16 Pro at
  block 256: the dense model is well above the RT threshold and intractable, about
  70 % sparsity is the boundary into real-time operation, and 90 % leaves comfortable
  margin at RTF $\approx 0.6$.
- Block sweep {64,128,256,512} on iPhone 16 Pro and 15 Pro: 256 is the smallest block
  sustaining real time on the 16 Pro; older devices need a larger block or higher
  sparsity.
- The app adds amp/pedal selection, 0 to -24 dB input attenuation for loudness
  matching, and a partitioned overlap-add convolution reverb with measured impulse
  response - the reverb is only about 3 % of per-block DSP time.

**Limitations:** demo paper - "no perceptible loss" rests on informal listening, not a
formal perceptual evaluation; the sparse engine's advantage depends on the achievable
sparsity pattern; profiling covers two iPhone models; vectorizing the dilated-conv
stack and pointwise $\tanh$ with Accelerate/vDSP is future work. Code at
`https://github.com/ryos17/wavenet-imp`.

## See also

[[real-time-neural-inference-deployment]] - [[mobile-gpu-neural-audio]] -
[[virtual-analog-overview]]

## References

[^1]: [[entities/source-papers#paper-sato-wavenet-pruning-ios-2026]] - Sato & Silverstein, "WaveNet-Style Guitar Amplifier Model Pruning for Real-Time iOS Deployment", DAFx26 demo.

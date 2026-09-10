---
title: Neural VA Architectures
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [neural-va, rnn, stability, time-varying, dataset]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_26.pdf
  - raw/DAFx26_paper_26.txt
---

# Neural VA Architectures

Black-box VA models learn the input/output map from measurements. Two structural
problems remain once accuracy is adequate: artifacts under *time-varying* control
conditioning, treated here,[^1] and dependence on the *training sample rate*, treated
in [[fourier-neural-operators-va]].

## Deep regularized RNNs and the gammatone loss

Control values (distortion, filter, volume, attack...) are recorded as static metadata
and fed to the network as conditioning. The simplest and most common scheme is
**concatenation** with the audio input; hyper-networks that modulate weights or hidden
features are the alternative. When the conditioning is moved at runtime, LSTMs and
GRUs emit an audible crackle even with zero audio input.[^1]

**Stability regularization.** For a control-conditioned LSTM with input, hidden and
conditioning weight matrices $W_*, U_*, C_*$, the constraints shown to guarantee
asymptotic stability under zero audio input are

$$C_g = O, \quad b_g = 0, \quad \|U_g\|_\infty < 1, \quad \|f_t + i_t\|_\infty \le 1$$

- Enforced by **reparameterization**, so they hold during and after training:
  $U_g \leftarrow \overline{U}_g \cdot \tau/\|U_g\|$ when $\|U_g\| \ge \tau$ (with
  $\tau < 1$), and the input gate mirrors the forget gate,
  $U_i = -U_f,\ C_i = -C_f,\ b_i = -b_f$, so that $i_t = 1 - f_t$.
- A looser variant replaces the induced $L_\infty$ norm on $U_g$ by the **spectral
  norm** $\|U_g\|_2 < 1$. It has no formal guarantee but uses model capacity better and
  in practice suppresses control noise just as well.

**Deep concatenation conditioning.** Extend concatenation conditioning to depth: layer
1 takes $[x_t, p_t]$, every later layer takes $[h_t^{(\ell-1)}, p_t]$, and a linear
layer produces the output. Notation `LSTM_norm depth x width`. Not LSTM-specific -
GRUs work with the corresponding constraints.

**Gammatone filterbank (GFB) loss.** Instead of mixing a time-domain and an MR-STFT
loss (two scales, two convergence rates, one more hyperparameter), filter the *error*
$e_t = y_t - \hat{y}_t$ through a 32-channel gammatone bank spaced on the ERB scale
from 100 Hz (up to about 10 kHz), add a residual channel
$\mathrm{GFB}(e)_{t,\text{res}} = e_t - \sum_c \mathrm{GFB}(e)_{t,c}$ for energy
outside the bank, and average the summed absolute channel errors:

$$\mathcal{L}_\text{GFB} = \frac{1}{N}\sum_{t=1}^{N}\Big(|\mathrm{GFB}(e)_{t,\text{res}}| + \sum_{c=1}^{C}|\mathrm{GFB}(e)_{t,c}|\Big)$$

This keeps phase (important when a distortion or compressor model is blended with a
dry path) while weighting error perceptually.

**Results.** Trained on the ProCo RAT, Darkglass Duality Fuzz and Boss CS-3 subsets of
the "asymptotically stable RNN" dataset (48 kHz, 1 s clips, PyTorch, Adam $10^{-3}$,
TBPTT truncation 2048, batch 32, 1000 epochs, three seeds).

| Loss / model | RAT ESR (dB) | DFZ ESR (dB) | CS-3 ESR (dB) | control noise |
|---|---|---|---|---|
| MAE, LSTM 4x64 (unregularized) | -18.9 | -20.3 | -21.4 | -65 to -58 dBFS |
| MAE, LSTM$_\infty$ 4x64 | -17.5 | -19.8 | -23.9 | ~0 (below noise floor) |
| GFB, LSTM$_\infty$ 4x64 | -18.0 | -19.9 | -23.2 | ~0 |
| GFB, LSTM$_2$ 4x64 | -19.2 | -20.8 | -26.5 | $\le -157$ dBFS |

- Regularization costs accuracy at matched size; the spectral-norm variant narrows the
  gap, and the GFB loss closes most of what remains - regularized models reach
  MAE-trained unregularized performance while control noise stays practically zero.
- **Regularized models prefer depth to width.** On DFZ, LSTM$_\infty$ went from
  -12.8 dB ESR at 1x64 to -17.4 dB at 4x8, while the unregularized LSTM went the other
  way (-18.9 to -15.5). Parameters scale quadratically with width but linearly with
  depth, so 4x8 has roughly an order of magnitude fewer parameters than 1x64
  (2,336 versus 17,664 on RAT; ~2,400 versus ~18,000 flops/sample).
- Limitation: no listening test (the Bark-smoothed error-residual spectrum is the
  proxy); no dataset with genuinely time-varying control trajectories exists, so
  whether the artifacts are an overfitting effect is untested.

## See also

[[fourier-neural-operators-va]] - [[virtual-analog-overview]] -
[[real-time-neural-inference-deployment]] - [[neural-model-compression]] -
[[time-varying-filter-stability]] (the same stability question for white-box filters)

## References

[^1]: [[entities/source-papers#paper-kallinen-deep-regularized-rnn-va-2026]] - Kallinen, Juvela, Sherson, "Deep Regularized RNNs for Virtual Analog Modeling", DAFx26.

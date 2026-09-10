---
title: Fourier Neural Operators for VA
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [fno, neural-va, differentiable, antialiasing, oversampling]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_27.pdf
  - raw/DAFx26_paper_27.txt
---

# Fourier Neural Operators for VA

An RNN absorbs the training time step into its learned parameters, so changing $f_s$
changes the realized dynamics. **Neural operators** learn maps between function spaces
instead of between fixed-length vectors, so the same operator evaluates on any uniform
discretization of the same interval.[^1] An FNO layer is

$$z_{\ell+1} = \sigma\big(W z_\ell + \mathcal{F}^{-1}(R\,\mathcal{F}_{1:\kappa}(z_\ell))\big)$$

with $R$ acting only on the $\kappa$ lowest Fourier modes. Because $\kappa$ is fixed
independently of the FFT length, the parameter shapes do not depend on the grid - that
is the sample-rate invariance.

**Adaptations for VA.** (i) *Frame-based*: define the operator on a fixed support
$T = 20$ ms with root-Hann analysis/synthesis windows, 75 % overlap (5 ms hop), and
overlap-add reconstruction; latency can be made arbitrarily small by zero-filling the
first frame. Unlike an RNN, no state crosses frames, so only within-frame dependencies
are captured. (ii) *Modified layer*: move the skip branch into the frequency domain,
$z_{\ell+1} = \sigma(\mathcal{F}^{-1}(\uparrow_{\varrho_\ell}(W\mathcal{F}_{1:\tilde N}(z_\ell) + \tilde R\,\mathcal{F}_{1:\tilde\kappa}(z_\ell))))$,
exploiting Hermitian symmetry (only $\tilde\kappa = \lfloor\kappa/2\rfloor + 1$ modes)
and implementing internal oversampling as spectral zero-padding, which saves a factor
$\varrho_\ell$ in flops and keeps the skip branch bounded to the input Nyquist limit.
The pointwise nonlinearity stays in the time domain, preserving the block-oriented
(Wiener-Hammerstein-like) separation of linear dynamics from static nonlinearity.
(iii) Brick-wall lowpass, channelwise MLP $Q$, then downsample by $\varrho_0$.

**Results.** Big Muff Pi input stage (2N5089 BJT), Simscape-simulated, ~130 s, trained
at 48 kHz. FNO: $L = 3$ layers, 8 channels, $\tilde\kappa = 64$, SiLU, 17,785
parameters, training $\varrho_0 = 2$. Baseline: LIDL-RNN (GRU 64, 12,929 parameters),
which reinterprets the unit delay on the new grid with fractional-delay interpolation.

| Metric | 24 kHz | 48 kHz | 88.2 kHz | 96 kHz |
|---|---|---|---|---|
| MAE ($\times 10^{-3}$), LIDL-RNN | N/A | 2.173 | 2.319 | 2.333 |
| MAE ($\times 10^{-3}$), FNO | 2.894 | 2.897 | 2.898 | 2.898 |
| SC ($\times 10^{-2}$), LIDL-RNN | N/A | 3.852 | 3.920 | 3.932 |
| SC ($\times 10^{-2}$), FNO | 2.932 | 3.237 | 3.408 | 3.431 |

- Comparable in up-sampling (MAE favors the RNN slightly, spectral convergence favors
  the FNO), but the LIDL-RNN is **not applicable to downsampling** at all - its delay
  reinterpretation becomes non-causal - while the FNO runs at 24 kHz with metrics of
  the same order.
- At 24 kHz the lower Nyquist limit folds new harmonics back; setting inference-time
  $\varrho_0 = 2$ visibly removes the fold-back in the spectrogram and raises SNRA in
  the upper part of a 100 Hz - 8 kHz sweep, at the cost of FFT/IFFT and nonlinearity
  work on the expanded grid.
- Limitations: one circuit; no study of how accuracy scales as parameters shrink; the
  effect of training-time internal upsampling on the learned weights is unexplored.

## See also

[[neural-va-architectures]] - [[virtual-analog-overview]] -
[[antiderivative-antialiasing]] (the other route to alias control)

## References

[^1]: [[entities/source-papers#paper-massi-fno-sample-rate-independent-va-2026]] - Massi, Mezza, Bernardini, "Fourier Neural Operators for Sample-Rate-Independent Virtual Analog Modeling", DAFx26.

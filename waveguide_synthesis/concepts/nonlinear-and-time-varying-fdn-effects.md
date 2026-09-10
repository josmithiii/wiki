---
title: Nonlinear and Time-Varying FDN Effects
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [reverb, fdn, nonlinear, dsp, realtime]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_05.pdf
  - raw/DAFx26_paper_05.txt
---

# Nonlinear and Time-Varying FDN Effects

Shimmer reverb - pitch-shifted, "ethereal" feedback in the ValhallaShimmer sense -
built by putting nonlinear or time-varying blocks **inside** the FDN feedback loop
rather than after the reverberator.[^dalsanto]

## Placement and the stability criterion

With FDN state $\mathbf{s}(n+\mathbf{m}) = U\Gamma(n)\mathbf{s}(n) + \mathbf{b}x(n)$, the nonlinearity NL
is inserted per delay line before the mixing matrix $U$, so $U$ spreads its output
across all channels. The design constraint is **near energy preservation**
$$\sum_{n=0}^{L}|\mathrm{NL}(x(n))|^2 \;\approx\; \sum_{n=0}^{L}|x(n)|^2 .$$
With orthogonal $U$ and $|\Gamma_i| < 1$ the system is stable; near-preservation is
what keeps the *decay* controllable. Because the NL recursively moves energy
between bins, the $T_{60}$ profile set by $\Gamma$ is no longer strictly preserved,
and aliasing can appear. All experiments run at $f_s = 96$ kHz.

## The five operations

| Operation | Mechanism | Spectrum | Mults/sample |
|---|---|---|---|
| Controllable full-wave rectifier (CFWR) | $y = g_{\text{cfwr}}\big((1-\alpha)x + \alpha|x|\big)$, $g_{\text{cfwr}} = \sqrt{2-2|\alpha-1/2|}$ | all even harmonics, then odd by recursion; strong DC | 8 |
| Signal-dependent fractional delay (SDFD) | half-wave rectify, delay $+$ part by $\approx 1+d$ and $-$ part by $\approx 1-d$, sum | even harmonics, weaker; distortion at zero crossings | 4 |
| Ring modulation (RM) | $y = g_{\text{rm}}\, x \sin(2\pi f_{\text{rm}} n)$, $g_{\text{rm}} = \sqrt{2}$ | sidebands at $\pm f_{\text{rm}}$, carrier suppressed | 2 |
| Time compression/expansion | one ring buffer, two read pointers offset by half the modulation period, equal-power crossfade, cubic interpolation; pointer advances by $2^{T_{st}/12}$ | true octave transposition | 12 |
| Granular time compression | same buffer, read index re-drawn every $L_w$ samples from $\mathcal{U}(L_w, L_{\text{ring}})$, windowed grains | diffuse, "blooming", stochastic | 12 |

Defaults: $L_w = 2048$, $L_{\text{ring}} = 8192$.

## Keeping it bounded

- **Antialiasing.** CFWR gets first-order antiderivative antialiasing,
  $|x(n)| \approx \tfrac12\,\dfrac{x(n)|x(n)| - x(n-1)|x(n-1)|}{x(n)-x(n-1)}$,
  falling back to $|x(n)+x(n-1)|/2$ when the denominator is near zero.
- **DC blocking.** CFWR and the ring-buffer methods produce DC that would
  accumulate in the loop, so each is followed by
  $y(n) = g_{\text{env}}(n)\big(x(n) - x(n-1) + R\,y(n-1)\big)$ with $R = 0.995$ (76 Hz cutoff),
  plus a slow adaptive gain $g_{\text{env}}$ tracking $x^2/y^2$ with $\tau = 50$ ms to
  restore the energy the highpass removes (2 more mults/sample).
- **Measured energy ratios** over 100 ms windows of 336 minutes of MoisesDB stems:
  concentrated near 1; time compression has the widest spread (delay and
  instantaneous-energy mismatch), SDFD skews below 1 (high-frequency loss), CFWR
  peaks near **0.87**, i.e. the DC-blocker compensation is not yet exact.
- Energy preservation for CFWR is exact only at $\alpha = 0$ and $\alpha = 1$; power dips
  quadratically to a minimum at $\alpha = 0.5$, which $g_{\text{cfwr}}$ corrects.
  RM at $g_{\text{rm}} = \sqrt{2}$ preserves average power but can still blow up with short,
  strongly recirculating lines and a diagonally dominant $U$.

## Behaviour and sound design

Test FDN: $N = 8$, random orthogonal $U$, delays 71-400 ms ascending, first-order
lowpass attenuation prototype ($f_c = 10$ kHz, $T_{60}(0) = 2$ s, $T_{60}(\pi) = 0.5$ s);
octave-up time compression on the four longest lines only.

- CFWR/SDFD: even harmonics appear after $2m_1$ samples, odd after $3m_1$.
- Large $N$ and a dense $U$ excite the nonlinearity hard (distortion-like); longer
  delays and sparser $U$ give slow, evolving textures. A diagonally dominant
  (Householder) $U$ reduces inharmonicity on sustained input.
- $\alpha = 0.5$ makes CFWR a half-wave rectifier - mechanical/"helicopter" on percussive
  input; $\alpha < 0.5$ is subtler. RM below ~10 Hz reads as tremolo; higher $f_{\text{rm}}$
  gives metallic inharmonic echoes.
- Pitch shifting is the most musical: octaves are safest, longer read-pointer
  modulation periods reduce reset distortion at the cost of latency, and delay
  length sets the onset time of each shifted layer.
- Nonlinearities compose (chain them, or apply different ones to different lines).
- Open problem named by the authors: an adaptive attenuation filter that holds a
  target $T_{60}$ despite nonlinear energy redistribution, e.g. via a differentiable
  nonlinear FDN.

## See also
- [[artificial-reverberation]] - the linear FDN this modifies
- [[fdn-kronecker-feedback-matrices]] - lossless time-varying mixing, the other route to animation
- [[delay-line-techniques]] - the ring-buffer pitch shifting and fractional delay used here
- [[entities/source-papers#paper-dalsanto-nonlinear-shimmer-fdn-2026]] - catalog entry

[^dalsanto]: G. Dal Santo, X. Pi, K. Prawda, S. J. Schlecht, V. Valimaki, "Shimmer Reverberation with Nonlinear Feedback Delay Networks," DAFx26. See [[entities/source-papers#paper-dalsanto-nonlinear-shimmer-fdn-2026]].

---
title: Corpus-Driven Parametric Modal Reverb
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [modal, modal-synthesis, resonator, room, damping, impulse-response, ml, dataset]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_06.pdf
  - /l/dttd/DAFx26/DAFx26_demo_72.pdf
  - /l/dttd/DAFx26/txt/DAFx26_paper_06.txt
  - /l/dttd/DAFx26/txt/DAFx26_demo_72.txt
---

# Corpus-Driven Parametric Modal Reverb

Nobody can set thousands of per-mode frequencies, dampings and residues by hand.
Ducceschi, Gabrielli, Simionato and Russo learn that mapping from a corpus of measured
room IRs: six perceptual controls in, thousands of modal parameters out[^1]. See
[[resonator-bank-implementation]], [[damping-models]] and [[stochastic-modal-synthesis]].

## Modal representation
$$H(j\omega)=\sum_{k=1}^{M}\left(\frac{r_k}{j\omega-\lambda_k}+\frac{r_k^*}{j\omega-\lambda_k^*}\right),\quad
h(t)=\sum_{k=1}^{M}2e^{-\sigma_k t}\left(a_k\cos\omega_{d,k}t - b_k\sin\omega_{d,k}t\right)$$
with $\lambda_k=-\sigma_k+j\omega_{d,k}$ and $r_k=a_k+jb_k$, plus a 256-tap FIR $h_{\rm FIR}$ (about 5.8 ms at 44.1 kHz) carrying the direct sound and first reflections, which the modal sum does not resolve.

## Corpus and decomposition
About 1500 IRs from Logic Pro and Ableton bundles, MeldaProduction factory content,
OpenAIR and the authors' own measurements, all at 44.1 kHz, decomposed by sub-band peak
picking over 40-12000 Hz: $\sigma_k$ from the $-3$ dB bandwidth rule ($\sigma_k=\pi\Delta f_{-3\rm dB}$)
combined with sub-band Schroeder integration, residues by linear least squares against
the measured response, $h_{\rm FIR}$ by time-domain least squares on the residual. Resynthesised IRs are scored by nRMSE and
rejected above a threshold - mostly IRs saturated, compressed or spectrally shaped
(violating LTI) - plus manual removal of springs and plates. **N = 1151** survive.

## The 50-variable feature table
Computed on the **resynthesised** signal, so every descriptor refers to the same modal representation. Five bands throughout: sub-bass 40-125, bass 125-500, mid 500-2k, presence 2k-8k, brilliance 8k-12k Hz.

| Group | Variables |
|---|---|
| Acoustic indices (ISO 3382-1) | $T_{30,\rm mid}$, centre time $T_s$, bass ratio BR, treble ratio TR, $C_{80,\rm mid}$; per-octave $T_{30}$ and $C_{80}$ at 125 Hz-4 kHz |
| Damping | per-band mean $\sigma_b$; global mean, median, std |
| Spacing and density | mode count $M$; $\mathrm{CV}_\Delta=\mathrm{std}(\Delta f)/\mathrm{mean}(\Delta f)$; per-band density $\rho_b$ |
| Amplitude | per-band mean $\lvert r_k\rvert$; global mean, median, std; OLS slope of $\log\lvert r_k\rvert$ on $\log\lvert f_k\rvert$ |
| FIR | energy, peak value, temporal centroid |

Here $T_s = T\sum_n n h^2/\sum_n h^2$ and $C_{80}=10\log_{10}\big(\sum_{n\le n_{80}}h^2/\sum_{n>n_{80}}h^2\big)$, $n_{80}=\lfloor0.08/T\rfloor$. PCA on the full 50-feature matrix as the reduction strategy was **rejected**: 18 components for 95% of the variance, no physical meaning.

## Six user controls, orthogonalised
| Control | Range | Dataset parameter |
|---|---|---|
| T60 | 0.1-6 s | $T_{30,\rm mid}$ |
| warmth | 0.5-2.0 | BR |
| brightness | 0.3-2.0 | TR |
| roomSize | 0-1 | $T_s$ (volume proxy) |
| diffusion | 0-1 | $\mathrm{CV}_\Delta$ (spacing regularity) |
| earlyLate | 0-1 | $C_{80,\rm mid}$ |

These are conceptually distinct but **not** statistically independent ($T_{30}$-$T_s$:
$r=0.83$; $T_s$-$C_{80}$: $r=-0.64$), and direct regression on the raw vector was unstable. The controls are therefore robustly standardised,
$z_j=(p_j-\tilde p_j)/(\mathrm{IQR}_j/1.349)$, then rotated by PCA into an orthogonal
basis $V$ - all six components kept so each control keeps a unique invertible
direction, off-diagonal PC-score correlations below $7\times10^{-16}$. Design vector
$x=[1,\mathrm{PC}_1,\dots,\mathrm{PC}_6]^{\!\top}\in\mathbb{R}^7$.

## Regressions and physics
- **Damping and density**, ten per-band models in log space, fitted by IRLS with bisquare weights: $\log\hat\sigma_b = x^{\!\top}\beta^{\sigma,b}$ and $\log\hat\rho_b = x^{\!\top}\beta^{\rho,b}$, $b=1..5$. The log guarantees positivity. Band-centre values are interpolated to per-mode frequencies in $(\log_{10}f,\log\sigma)$ space, then anchored: $\hat\sigma(f_k)\leftarrow\hat\sigma(f_k)\cdot(3\ln10/T_{60})/\overline{\hat\sigma}_{500-1k}$, with a log-linear taper dividing by BR below 500 Hz and TR above 1 kHz.
- **Mode count** $M_{\rm raw}=\sum_b\hat\rho_b\Delta f_b$, remapped linearly into $[1000,8000]$ and allocated per band by largest-remainder rounding. Within a band modes sit on a uniform grid jittered by the diffusion control, $f_k\leftarrow f_k+\xi_k\,d\,0.9\overline{\Delta f}_b$ with $\xi_k\sim U[-\tfrac12,\tfrac12]$: $d=0$ gives a metallic comb, $d=1$ the quasi-random spacing of real rooms.
- **Residues from physics, not regression.** No useful predictor of $|r_k|$ exists in the corpus. Instead, diffuse-field equipartition (each mode carries equal energy $E_k=|r_k|^2/2\sigma_k$) forces $|r_k|\propto\sqrt{\sigma_k}$; the corpus median $\kappa=\mathrm{median}(|r_i|/\sqrt{\sigma_i})\approx4.86$ (std $\approx7.07$) fixes an overall gain absorbed by normalisation. Phases are random, $a_k=|r_k|\cos\phi_k$, $b_k=|r_k|\sin\phi_k$.
- **Early reflections from the $C_{80}$ definition.** Rearranged, $E_{\rm early}=E_{\rm late}\,10^{C_{80}/10}$ with $E_{\rm late}=\sum_k|r_k|^2/2\hat\sigma_k$; the corpus-mean FIR template is simply rescaled to that energy.

## Diagnostics and limits
Damping fits: robust $R^2$ from 0.747 (brilliance) to 0.937 (bass); density fits
looser, 0.497 to 0.717, with only 1-4% of IRs rejected as outliers. Three presets
spanning a 7.5:1 range of decay times project inside the corpus cloud; settings outside
the $p_5$-$p_{95}$ envelope extrapolate beyond the training distribution. The MATLAB
prototype generates parameters in well under a second per IR and runs in real time at
44.1 kHz inside a host convolver. **Validation is statistical, not perceptual**: no
listening test against measured spaces or FDN methods.

## Spatial extension: Bunkervik
The companion demo walks the same machinery through a space[^2]: a 30 m WWII tunnel
in Brescia, swept at three receiver positions (8, 10, 25 m from the source), the
loudspeaker summed over six orientations to fake omnidirectionality. Fitting each
position independently puts the same physical mode at slightly different
frequencies, so residue interpolation is ill-defined. The fix is a **common modal basis**:
the three pole sets are concatenated, clustered along frequency with a frequency-dependent
tolerance and merged per cluster by a residue-magnitude-weighted average - 6300 shared
poles over 70 Hz-12 kHz. Per-position residues and 256-tap
FIRs are re-fitted against that shared set by joint alternating least squares
(time-domain nRMSE below 3.5% everywhere, two to three times better than modal-only),
so at run time only residue weights and FIR taps are interpolated (linear; cubic
Lagrange for the fractional delay carrying source-receiver distance), recomputed
every eighth sample. Further controls stretch mode frequencies above a
cutoff to render content up to 20 kHz ("Aura" brilliance), plus damping and mic
rotation, all LFO-modulatable. State update and sum reduction is about 90% of the cost,
hand-vectorised (SSE/AVX/NEON); single-core use stays under 25% on an M2 Pro.

[^1]: [[entities/source-papers#paper-ducceschi-corpus-driven-modal-reverberator-2026]] - Ducceschi, Gabrielli, Simionato & Russo, "A Corpus-Driven Parametric Modal Reverberator," DAFx26. Code: github.com/Nemus-Project/DAFx26_ModalReverb
[^2]: [[entities/source-papers#paper-ducceschi-bunkervik-spatial-reverb-2026]] - Ducceschi & Webb, "Bunkervik Spatial Reverb Demo," DAFx26.

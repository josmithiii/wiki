---
title: Extrema-Sampling Time Stretching
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [tsm, ola, modifications, applications, downsampling]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_21.pdf
  - spectral_processing/raw/DAFx26_paper_21.txt
---

# Extrema-Sampling Time Stretching

Time-scale modification for low-power embedded audio, where the FFT of
a phase vocoder or the cross-correlation of WSOLA does not fit the
budget. The signal is reduced to timestamped local extrema
("keyframes"); their **spacing** is a free per-sample estimate of local
bandwidth, and it drives an overlap-add engine whose crossfade
duration adapts sample by sample.[^nielsen-2026]

## The extrema representation

- A uniform sampler spends the same samples per second on a bass note and a cymbal crash. Keeping only local extrema $(n_m, v_m)$ gives a sparse buffer whose local rate follows instantaneous bandwidth: few widely spaced points for a bass note, many tightly packed ones for a crash.
- Extrema (with zero crossings) are the classic information-rich locations in the reconstruction literature; here the novelty is using the *spacing itself* as a control signal rather than for compression.
- **Bandlimited derivative**: a plain difference $x[n]-x[n-1]$ peaks at Nyquist and reports spurious extrema from noise and quantization. A cubic B-spline kernel, implemented as a 4-tap FIR with data-defined coefficients, has a zero at Nyquist (at the cost of HF rolloff) and is differentiated analytically to give the detector.
- **Difference thresholding**: a candidate extremum is kept only if it differs from the last *saved* extremum by more than $\epsilon$ - a state-dependent hysteresis deadband. $\epsilon = 0.001$ ($-60$ dB) gives faithful reconstruction; raising it acts as an amplitude-dependent lowpass, since high frequencies usually carry lower amplitude.
- **Subsample location** by reverse linear interpolation of the derivative $d[n]$:
$$\alpha=\frac{|d[n-1]|}{|d[n-1]|+|d[n]|},\qquad n_m=(n-1)+\alpha,\qquad v_m=B(n_m).$$
Grid snapping instead of this aliases badly; a second refinement or quadratic root find adds little.

## Reconstruction without division

Non-uniform cubic Hermite interpolation between keyframes,
$p(t)=v_m h_{00}(t)+T_0h_{01}(t)+v_{m+1}h_{10}(t)+T_1h_{11}(t)$,
normally needs tangents $T_0,T_1$ from neighbouring spacings (four
divisions, two extra keyframes). But **every saved point is an
extremum, so its derivative is zero**: set $T_0=T_1=0$ and
$$p(t) \;=\; v_m\,h_{00}(t) + v_{m+1}\,h_{10}(t),\qquad
h_{00}=2t^3-3t^2+1,\; h_{10}=-2t^3+3t^2,$$
which is the graphics *smoothstep*: $C^1$ continuity from two points,
no division, less than half the multiplies, and spacing drops out.

## The adaptive-crossfade OLA engine

Three playheads over the sparse buffer: a reference $\phi_\mathrm{ref}$
advancing at the time rate $\tau$, a playing head $\phi_\mathrm{play}$
at the pitch rate $\sigma$, and a temporary head used during a splice.

- "Jogger and leashed dog": the leash is $K$ **keyframes** long, so its length in *time* stretches with the signal. Sparse passages let the playhead roam; approaching a transient the keyframes crowd, the leash shortens, the splice fires sooner.
- Splice triggers when the keyframe-index distance exceeds $K$; its duration is the span of the next $K$ keyframes, $L = n_{w_\mathrm{ref}.m+K}-n_{w_\mathrm{ref}.m}$, and the crossfade completes in $L/\sigma$ output samples.
- Output is produced sample by sample with **no block latency**; block processing is only needed live, by forcing a keyframe at each block boundary (e.g. 512 samples).
- $K$ is a real-time macro over splice duration, and $\tau,\sigma$ modulate freely.

## Cost

Per-output-sample estimates (Cortex-M7 cycle model; TSM-toolbox
defaults $N_w=1024$, $H_s=512$, $\Delta_\mathrm{max}=512$, $N_f=2048$):

| Method | MUL | ADD | Cycles |
|---|---|---|---|
| OLA | 2 | 2 | ~4 |
| WSOLA (time-domain corr.) | 2050 | 2052 | ~4100 |
| WSOLA (FFT corr.) | 280 | 407 | ~690 |
| Phase vocoder | 190 | 275 | ~850 |
| This method, offline | 15 | 19 | ~34 |
| This method, live | 21 | 26 | ~61 |

An order of magnitude below PV and FFT-WSOLA. The gap narrows on
desktop CPUs with vectorized FFTs; on the target hardware the per-bin
$\arctan$ of the phase vocoder (roughly 200 of its ~850 cycles)
resists tabulation.

## Evaluation

Hardware: Electrosmith Daisy Patch SM (480 MHz STM32H7, 48 kHz).
Corpus: the 10 TSM-toolbox stress clips.

- **Passthrough** (unity rate, $\epsilon=-60$ dB): mean STOI 0.91, mean log-attack-time deviation 0.09, mean spectral contrast loss 3.08 dB. Glockenspiel (STOI 0.75, LAT dev 0.41) and singing voice (contrast loss 4.54 dB) sparsify worst; dense mixes best.
- **Spline distortion**: THD of a 1 kHz sine is $-38.1$ dB odd, $-85.8$ dB even (a unity-gain $\tanh$ saturator is $-25$ dB odd) - hence "added saturation" as the characteristic artifact.
- **Listening test** (webMUSHRA, $N=15$, 5 clips, stretch 0.5/1.2/1.8, no hidden reference since the time scale changes): WSOLA wins overall (4 of 5 clips); PV good on harmonic, poor on transient material; OLA excellent on pure percussion, very poor on harmonic. This method rates "fair" overall, "poor" only on singing voice. Crucially the ranking **tracks sparsification fidelity, not stretch quality**: the two clips with the worst passthrough contrast loss are the two lowest-rated.
- **Transient preservation** (LAT deviation, lower better, averaged over 10 clips): best of all four at 1.8x (0.502 vs WSOLA 0.531, OLA 0.575, PV 0.648), close second at 1.2x, worst at 0.5x.

## Limits

- Time compression (0.5x) underperforms: longer splices were chosen there to avoid robotic inharmonic distortion, at the cost of timing scores.
- Spectral contrast loss is inherent to the representation, independent of stretching - a noise-like haze filling the valleys between partials.
- Silence or very sparse passages before a transient give very long splices and audible repeats; mitigated by capping splice duration at a few hundred ms.
- No pitch-shifting or formant control is claimed, and the authors note that frame-aligned or perceptual spectral metrics assume an alignment that TSM itself destroys.

## Related Concepts
- [[phase-vocoder-and-tsm]] - the expensive, phasey alternative
- [[overlap-add-stft]] - OLA in its usual STFT setting
- [[entities/source-papers#paper-nielsen-keyframe-extrema-tsm-2026]] - catalog entry

[^nielsen-2026]: Matthew Nielsen, "Keyframe Time Stretching via Extrema Sampling," *Proc. DAFx26*, Cambridge MA, Sept. 2026, pp. 168-175. Distilled in [[entities/source-papers#paper-nielsen-keyframe-extrema-tsm-2026]].

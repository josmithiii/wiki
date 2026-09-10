---
title: Moog Ladder Filter Models
created: 2026-09-10
updated: 2026-09-10
type: concept
tags: [ladder-filter, va-filters, tpt-zdf, spice, nonlinear, benchmark, comparison, history]
sources:
  - /l/dttd/DAFx26/DAFx26_paper_29.pdf
  - raw/DAFx26_paper_29.txt
---

# Moog Ladder Filter Models

The transistor ladder VCF is the canonical VA filter target. Its musical
identity is *nonlinear* - self-oscillation, drive-dependent cutoff motion,
input-dependent harmonic coloration - yet digital ladders are usually compared
by linear frequency response, which hides exactly what matters.[^1]

## Topology

- Four cascaded one-pole lowpass sections (see [[tpt-zdf-filters]]) with global
  feedback gain $k$ (emphasis / resonance). Linearized state-space form and
  time-varying stability ranges: [[time-varying-filter-stability]].
- Each circuit stage is an emitter-coupled NPN pair, so saturation is
  $2V_T\tanh(v/2V_T)$; cutoff is set by tail current
  $I_\text{control} = 8\pi V_T C f_c$, $V_T = 26$ mV.
- With the input differential pair there are **five** saturation points ("1+4"),
  not the same as the four poles. Which of them stay nonlinear is the central
  design variable.

## Lineage

| Work | Contribution |
|---|---|
| Moog 1965 | the analog voltage-controlled LP/HP filter |
| Rossum 1992 | saturation *inside* the feedback path makes a digital filter overload like analog |
| Stilson & Smith 1996 | the ladder framed as a digital implementation problem |
| Huovilainen 2004 | nonlinear cascade formulation (1+4 tanh, 2x oversampling) |
| Fontana 2007 | structure-preserving digital reformulation of the Moog VCF |
| Zavalishin 2012 | TPT / zero-delay-feedback framework (the practitioner standard) |
| D'Angelo & Valimaki 2014 | explicit nonlinear model via a delay-free-loop method, SPICE-compared |

## SPICE-referenced metrics

Reference: ngspice 46 ladder circuit with idealized NPN devices (saturation is
the emitter-coupled tanh alone), max step 1/8 of the sample period. One boundary
layer normalizes only I/O scale and resonance range (onset at $k \approx 4$);
internal DSP untouched. Each test reduces to one observable versus SPICE:[^1]

- **Linear** - dB magnitude RMSE, 1 s log sweep, 0.01 V, $k = 2$, 96 kHz.
- **Self-oscillation** - RMS of the final 0.5 s after a 1 s, 1570.8 Hz, 1 V
  excitation is removed; cutoff 1000 Hz, $k = 4.3$.
- **Cutoff shift** - fitted resonance peak frequency and gain versus drive
  (0.001-0.104 V).
- **Harmonics** - Farina swept-sine deconvolution at 384 kHz, H2-H9 normalized
  to each run's own H1, then RMSE; also under a cutoff sweep (C3 sawtooth,
  $k=3.5$) and a drive sweep (C2 sawtooth, $k=0$, so feedback does not confound).

## Cross-implementation comparison

| Model | Linear (dB) | Spectra (%H1) | Cutoff (%H1) | Drive (%H1) |
|---|---|---|---|---|
| Huovilainen 2004 | 0.116 | 0.04 | 0.17 | 0.05 |
| D'Angelo 2014 | 0.363 | 0.06 | 0.22 | 0.18 |
| Csound 6.18.1 `moogladder` | 0.403 | 0.06 | 0.19 | 0.09 |
| VCV Rack 2.6.4 Fundamental VCF | 0.162 | 0.10 | 0.33 | 0.24 |
| JUCE 8.0.13 `LadderFilter` | 0.304 | 0.65 | 3.39 | 3.03 |

- Linear agreement is nearly uninformative: JUCE is competitive linearly yet an
  order of magnitude off in every nonlinear view.
- The four **distributed 1+4** models cluster at 0.04-0.10 %H1; JUCE's
  **boundary saturation** (tanh at signal input and feedback path only, four
  sections linear) sits at 0.65 %.
- Cutoff shift: the four track SPICE within about 20 cents and 0.11 dB; JUCE
  departs by 427 cents and 0.70 dB.
- Self-oscillation: SPICE sustains 4.803 mV; D'Angelo, Csound, VCV Rack are
  close; Huovilainen is lower (4.262 mV, its omitted resonance-correction factor
  $a_\text{cr} \approx 1.016$); JUCE goes silent, its tanh-limited loop gain
  reaching threshold only at $k = 4.5$.

## Ablation and design guidance

The controlled common-core ablation that explains *why* these implementations
diverge - saturator function versus placement, and which ladder stages must stay
nonlinear - is on its own page:
[[ladder-nonlinearity-ablation]].

## See also

[[virtual-analog-overview]] - [[antiderivative-antialiasing]] for the aliasing
axis this benchmark excludes.

## References

[^1]: [[entities/source-papers#paper-oyama-moog-ladder-nonlinearity-2026]] - Oyama, "Quantifying Nonlinear Behavior in Digital Moog Ladder Filters", DAFx26.

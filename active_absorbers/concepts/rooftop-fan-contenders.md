---
title: Rooftop-Fan Noise — Out-of-Scope Contenders (pointer page)
created: 2026-04-17
updated: 2026-04-18
type: concept
tags: [fan-noise, passive, metamaterial, industrial, reference]
sources:
  - raw/Brooks-Pope-Marcolini-NASA-RP1218-1989.txt
  - raw/Sutliff-ANC-LowSpeedFan-TM107458-1997.txt
  - raw/Sutliff-ANCF-20Year-Retrospective-2019.txt
---

# Rooftop-Fan Noise — Out-of-Scope Contenders

**Scope disclaimer.** This wiki is about **active** noise control /
active absorbers (see SCHEMA.md). This page exists as a **pointer** so
that a rooftop-fan practitioner has the complete landscape even though
most entries below will never get deeper treatment here. The covered-
in-wiki methods are cross-linked; everything else is one bullet.

Use this page as a checklist: before committing to an ANC solution
for data-center rooftop fan hum (primary concern: ~118 Hz BPF), verify
that the cheaper / simpler contenders in §1–§4 are either already in
place or ruled out on engineering grounds.

## 1. Source modifications (attack the fan)

Cheapest dB-per-dollar for rotating machinery. Often saturates before
ANC becomes economically worthwhile.

- **Larger, slower fans** — BPF ∝ RPM × blade count. Doubling
  diameter and halving RPM at the same flow usually moves BPF below
  the annoyance band and cuts radiated power.
- **Non-uniform blade spacing** — spreads the BPF line into a comb,
  reduces tonality penalty (see [[psychoacoustic-anc]]) without
  touching total energy.
- **Skewed / swept blades** — staggers blade-pass events, reduces
  peak radiated pressure.
- **Serrated trailing edges** — reduces broadband trailing-edge noise
  (Howe 1991 / owl-wing inspired).
- **Rotor-stator spacing and vane counts** — chosen to cut off the
  rotor-stator interaction tone (Tyler-Sofrin mode counts); standard
  aeroacoustic design practice.
- **Tip treatments** — shrouds, winglets, tip-gap seals reduce
  tip-vortex noise.
- **Variable-speed control with dither** — operate off BPF resonance
  with small RPM modulation; smears the tone.

## 2. Operational / multi-unit strategies

Free once you have multiple fans.

- **Staggered RPMs** — detune $N$ fans by a few percent so their BPFs
  don't coincide; the community-received spectrum becomes broadband
  rather than a reinforced line.
- **Phase scheduling (Abali 2007, US 7,282,873)** — deliberate
  mechanical phase offset between fans; already in the wiki as
  `paper-abali-fan-phase-cancellation-patent`.
- **Demand-based speed control** — run fewer fans at higher RPM, or
  more fans at lower RPM, whichever is quieter for the current load.
  Commonly limited by compressor / cooling constraints.

## 3. Path treatments (between fan and community)

### 3.1 Barriers and enclosures

- **Acoustic barriers** — limited at 118 Hz (λ ≈ 2.9 m), insertion
  loss typically 5–10 dB for a rooftop barrier of practical size.
  Still standard first line of defense.
- **Partial enclosures with interior lining** — wrap the fan discharge
  in absorptive panels; effective 10–15 dB for BPF when sized
  properly.
- **Louvers / shielded openings** — directivity shaping rather than
  absorption.

### 3.2 Silencers

- **Reactive mufflers** (expansion chambers, quarter-wave side-
  branches, Helmholtz side-branches) — tuned narrowband attenuation;
  can deliver 15–25 dB at design frequency with modest size.
- **Dissipative silencers** (parallel-baffle, lined ducts) — broadband
  attenuation above ~250 Hz; weak at BPF.
- **Hybrid reactive+dissipative** — standard HVAC practice.

### 3.3 Passive narrowband absorbers

The class most directly useful at 118 Hz.

- **Helmholtz resonator arrays** — tuned to BPF; can achieve near-
  perfect absorption at the design frequency in a compact (~10 cm)
  package if quality factor is matched to source bandwidth.
  Detunes ±2% on the way to ±15% temperature swing — see
  [[hybrid-active-passive]] for the active-tuning fix.
- **Panel / membrane absorbers** — tuned bass traps; λ/20 thickness
  possible. Broader-band than Helmholtz but lower peak absorption.
- **Acoustic metamaterials** (Fang 2006, Mei 2012, Ma & Sheng 2014,
  Yang 2015) — locally-resonant membrane AMs; perfect absorption at
  100–200 Hz in λ/50 packages. The "dark acoustic metamaterial"
  lineage is the strongest passive option at 118 Hz for a rooftop
  geometry. See [[hybrid-active-passive]] for the active / tunable
  extensions.
- **Ventilated sound-insulation metamaterials** — allow airflow
  through while blocking sound; relevant for fan discharge paths
  (Ghaffarivardavagh 2019 and follow-ups).

### 3.4 Distance and siting

- Geometric spreading is 6 dB per doubling of distance; often
  cheaper to relocate the intake/discharge than to add treatment.
- Tall stacks direct noise upward; ground reflection favours
  horizontal paths to community receivers.

## 4. Receiver-side mitigation

Last resort, but occasionally cheapest.

- **Façade upgrades** at complainant residences — secondary glazing,
  low-frequency wall bracing.
- **Masking** — deliberate low-level shaped noise at the receiver
  (rare in community settings, common indoors).
- **Regulatory / schedule change** — noise-sensitive hours
  curtailment.

## 4.5 NASA fan-noise literature (now distilled)

NASA's Advanced Noise Control Fan (ANCF) is the closest publicly-
documented aeroacoustic analog of the rooftop-fan problem — 4-ft ducted
low-speed fan, BPF ≈ 500 Hz, documented ANC + liner + source-modification
outcomes over two decades.

- **Broadband-noise floor reference** — Brooks, Pope & Marcolini 1989
  NASA RP-1218: canonical BPM airfoil self-noise prediction with 5
  mechanisms (TBL-TE, separation-stall, LBL-VS, tip-vortex,
  TE-bluntness). Sets the broadband floor that tonal ANC cannot
  reduce. See [paper-brooks-pope-marcolini-airfoil-selfnoise-1989](../entities/source-papers.md#paper-brooks-pope-marcolini-airfoil-selfnoise-1989).
- **In-duct modal ANC benchmark** — Sutliff, Hu, Pla, Heidelberg 1997
  NASA TM-107458: modal-control ring-array drove (6,0) to zero at
  920 Hz; (4,0)+(4,1) gave 15 dB modal PWL; **9.4 dB** total 2BPF
  farfield PWL reduction. Benchmark for a multi-actuator in-duct
  solution on a rooftop fan. See [paper-sutliff-ancf-ge-anc-1997](../entities/source-papers.md#paper-sutliff-ancf-ge-anc-1997).
- **20-year programmatic retrospective** — Sutliff 2019:
  ANCF 1994–2016 at NASA Glenn, ~100 publications, Rotating Rake +
  CFANS diagnostic toolset, Over-the-Rotor Foam Metal Liner path to
  flight (FJ44, 737 MAX). Single best entry point into the NASA
  fan-noise literature. See [paper-sutliff-ancf-20yr-retrospective-2019](../entities/source-papers.md#paper-sutliff-ancf-20yr-retrospective-2019).

## 5. Covered in this wiki (cross-links)

- **Active noise control (all variants)** — [[classical-anc-overview]],
  [[ai-anc-overview]]
- **Narrowband / tonal ANC (the BPF case)** — [[tonal-periodic-anc]]
- **Hybrid active + passive treatments** — [[hybrid-active-passive]]
- **Psychoacoustic / tonality reshaping** — [[psychoacoustic-anc]]
- **Virtual sensing (quiet zone 30 m away)** — [[pinn-virtual-sensing]]
- **Multi-fan mechanical-phase cancellation** — Abali 2007 patent in
  `entities/source-papers.md#paper-abali-fan-phase-cancellation-patent`
- **Tonal fan ANC (early patent)** — Guerci 1995 in
  `entities/source-papers.md#paper-guerci-fan-anc-patent`

## 6. Recommended ordering for a rooftop-fan project

1. Specify the actual community-noise metric (§1 of
   [[psychoacoustic-anc]]) — tonality-weighted, not raw dB(A).
2. Quantify contribution of BPF fundamental vs harmonics vs
   broadband on *received* spectrum, not source spectrum.
3. Exhaust cheap source / operational mitigations (§1–§2).
4. Add passive narrowband absorption sized for BPF (§3.3).
5. If residual is still dominated by BPF → add tonal ANC
   ([[tonal-periodic-anc]]) — probably as a hybrid cell
   ([[hybrid-active-passive]]).
6. If residual is dominated by community-direction leakage → add
   directional / beam-steered ANC and virtual sensing
   ([[pinn-virtual-sensing]]).

## Pending sources (no distillation planned here)

- Beranek & Vér, *Noise and Vibration Control Engineering*, Wiley
  — standard reference for §1–§4.
- ISO 3744 / ISO 9613 — measurement and propagation standards.
- Neise, W., Koopmann, G. H., "Reduction of centrifugal fan noise..."
  *JSV* 1980 — classic fan-noise source treatment.
- Ghaffarivardavagh, R. et al., "Ultra-open metamaterial silencer,"
  *Phys. Rev. B* 2019.
- Tyler, J. M. & Sofrin, T. G., "Axial Flow Compressor Noise Studies,"
  *SAE Trans.* 70:309, 1962 — rotor-stator interaction mode cutoff
  theory underlying the NASA ANCF modal-control work (§4.5).

See also: [[classical-anc-overview]], [[tonal-periodic-anc]],
[[hybrid-active-passive]], [[psychoacoustic-anc]].

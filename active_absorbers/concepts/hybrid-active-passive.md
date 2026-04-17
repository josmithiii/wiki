---
title: Hybrid Active + Passive Absorbers
created: 2026-04-17
updated: 2026-04-17
type: concept
tags: [active-absorber, active-impedance, hybrid-passive, metamaterial, anc, feedback, industrial, reference]
sources: []
---

# Hybrid Active + Passive Absorbers

**Scaffold page — sources pending.** Hybrid absorbers combine a
**passive acoustic element** (porous liner, Helmholtz resonator array,
membrane, locally-resonant metamaterial) with an **active controller**
(loudspeaker + sensor + feedback/feedforward law) so that each does
what it is good at:

- Passive element: broadband high-frequency absorption + mechanical
  robustness, no power required.
- Active element: low-frequency / narrowband / tunable absorption,
  compensates passive detuning from temperature, humidity, or ageing.

Directly relevant to rooftop fan-hum control because passive bass
absorption at 100–200 Hz is physically bulky (λ/4 ≈ 0.7 m at 118 Hz),
while a thin active layer can synthesize the missing low-frequency
impedance in a much shallower package. Contrast with pure ANC in
[[classical-anc-overview]] and with pure passive methods listed in
[[rooftop-fan-contenders]].

## 1. Active impedance control

Goal: make the boundary surface present a prescribed acoustic
impedance $Z_s(\omega)$ — typically $Z_s = \rho c$ (anechoic) or a
specified frequency profile.

- **Olson & May (1953)** — earliest electronic sound absorber; error
  mic in front of a driver, feedback synthesizes a pressure-release
  boundary locally.
- **Guicking (1980s–90s)** — formalised *active impedance control*;
  pressure + velocity sensing pair, feedback law sets $p/v$ at the
  surface.
- **Hybrid Fahy / Guicking cells** — porous layer in front of a driver
  with an in-layer microphone; passive layer does the HF work, active
  loop pins the LF impedance.
- **Beyene & Burdisso (1997), Smith (1999), Furstoss (1997)** — hybrid
  passive-active liners for duct silencers; significant LF extension
  of the absorption band for modest driver cost.

## 2. Active liners in ducts and plena

The natural habitat of hybrid absorption: lined duct for mid/high
frequencies + active actuator array for the low-frequency band that
passive lining cannot reach.

- Aircraft engine inlet liners (NASA / Rolls-Royce prototypes) —
  driver array behind perforated facing-sheet replaces / augments
  Helmholtz cells.
- HVAC silencer retrofits — loudspeaker in the splitter plenum,
  microphone downstream, feedback FxLMS.
- Rooftop-fan application: active layer sized for the BPF + first two
  harmonics only; passive fibrous lining handles everything above
  ~400 Hz.

## 3. Active / tunable acoustic metamaterials

Locally-resonant metamaterials (Fang 2006, Mei 2012, Ma 2014)
achieve λ/50 sub-wavelength absorption at design frequencies — but
are *narrowband* and *fixed-tuned*. Active / tunable variants
address both limits.

- **Piezo-coupled membrane metamaterials** — shunt circuit on a piezo
  back-plate adjusts the effective membrane mass/stiffness, retunes
  the absorption peak.
- **Electro-mechanical shunt damping** — resistive + inductive + active
  shunts turn the piezo impedance into a frequency-dependent negative
  capacitance, broadening the band.
- **Actively-controlled Helmholtz resonators** — a secondary speaker
  modifies the effective neck impedance; tuning frequency becomes a
  control parameter rather than a geometric constant.
- **Programmable metasurfaces** — voltage-addressable local cells; can
  shape wavefronts and create steerable absorption zones (early-stage
  research).

## 4. Semi-active absorbers

MEMS or relay-switched elements change the passive element's
parameters slowly (sub-Hz); the acoustic loop remains passive at every
instant. Not real-time ANC but useful when the disturbance spectrum
drifts slowly (seasonal temperature affecting fan RPM, etc.).

- Switched-neck Helmholtz: mechanical valve changes the neck cross-section.
- Tunable membrane: DC magnetic bias changes tension.
- Variable-porosity facing sheet.

## 5. Why hybrid is attractive for rooftop fan hum

| Sub-problem | Passive alone | Active alone | Hybrid |
|---|---|---|---|
| BPF 118 Hz tone | needs 70 cm thickness | small driver suffices | active on top of thin passive |
| HF broadband (turb. inflow) | 5 cm porous works fine | wastes driver authority | passive does the work |
| Fan-RPM drift | detunes fixed resonator | trivially tracks | active compensates |
| Power failure | still absorbs HF | fails open | degrades to passive-only |
| Size | bulky | thin | thin + robust |
| Cost | low material / high volume | moderate | moderate |

The *fail-safe* property (§row 4) is often the decisive factor for
rooftop installations: a power outage in the ANC system must not
produce a step increase in community noise.

## 6. Open design questions

- **Sensor placement** in a hybrid cell — pressure-only vs.
  pressure-velocity pair; error-mic survivability in rooftop weather.
- **Driver survivability** — UV, ice, salt fog on a rooftop; sealed
  moving-coil vs. piezo actuators.
- **Co-design of passive + active layers** — currently designed
  sequentially (pick passive, then add active); joint optimisation is
  open.
- **Integration with virtual sensing** — the hybrid cell's error
  mic is local, but the quiet-zone target is 30 m downwind.
  ([[pinn-virtual-sensing]])

## Pending sources

- Guicking, D., "Active control of sound and vibration — history, fundamentals, state of the art." (tutorial).
- Beyene, S. & Burdisso, R., *JASA* 1997 — hybrid passive-active absorber.
- Furstoss, M., Thenail, D., Galland, M.-A., *JSV* 1997 — active duct liner.
- Ma, G., Sheng, P., "Acoustic metamaterials: from local resonances to broad horizons," *Science Adv.* 2016.
- Fang, N. et al., "Ultrasonic metamaterials with negative modulus," *Nature Materials* 2006.

See also: [[classical-anc-overview]] §2–3 (adaptive filters and
secondary-path modeling that still apply to the active layer),
[[tonal-periodic-anc]] (narrowband control used in hybrid cells),
[[rooftop-fan-contenders]] (the passive side catalogued for the
fan-hum application).

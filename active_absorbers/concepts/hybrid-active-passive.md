---
title: Hybrid Active + Passive Absorbers
created: 2026-04-17
updated: 2026-04-17
type: concept
tags: [active-absorber, active-impedance, hybrid-passive, metamaterial, anc, feedback, industrial, reference]
sources:
  - raw/Galland-HybridPassiveActive-FlowDuct-AppAcoust2005.txt
  - raw/Betgen-Galland-HybridLiner-AppAcoust2012.txt
  - raw/Guicking-ActiveControl-Patents-Overview.txt
  - raw/Mei-DarkAcousticMetamaterial-NatComm2012.txt
  - raw/Ghaffarivardavagh-VentilatedMetamaterial-arxiv1801.03613.txt
  - raw/Ma-Sheng-AcousticMetamaterials-SciAdv2016.txt
---

# Hybrid Active + Passive Absorbers

Hybrid absorbers combine a **passive acoustic element** (porous liner,
Helmholtz resonator array, membrane, locally-resonant metamaterial)
with an **active controller** (loudspeaker + sensor +
feedback/feedforward law) so that each does what it is good at:

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
  surface. Guicking's 2009 patent overview[^guicking-patents-2009]
  catalogues the full patent lineage around this idea (§2 algorithms,
  §9 ASAC, §17 transducers), including the Guicking & Karcher 1984
  experimental work cited by Galland.
- **Hybrid Fahy / Guicking cells** — porous layer in front of a driver
  with an in-layer microphone; passive layer does the HF work, active
  loop pins the LF impedance.
- **Beyene & Burdisso (1997), Smith (1999), Furstoss (1997)** — hybrid
  passive-active liners for duct silencers; significant LF extension
  of the absorption band for modest driver cost.
- **Galland, Mazeaud & Sellen 2005**[^galland-2005] formalise the full
  5-step design procedure for a flow-duct hybrid cell (§2 below);
  Betgen, Galland, Piot & Simon 2012[^betgen-2012] extend to a
  **complex** variant controlling arbitrary frequency-dependent
  impedance (two mics instead of one).

## 2. Active liners in ducts and plena (Galland / Betgen design procedure)

The natural habitat of hybrid absorption: lined duct for mid/high
frequencies + active actuator array for the low-frequency band that
passive lining cannot reach. The ECL Lyon group's work is the
canonical treatment.

Galland et al. 2005[^galland-2005] 5-step design recipe:

1. **Target impedance** — compute frequency-dependent optimal $Z_s(\omega)$
   for the duct geometry (Tester 1970: weak LF resistance, increasing
   negative reactance; purely passive and purely active each fall short).
2. **Passive design** — pick porous material and cut-off $f_c$ above
   which active control turns off and classical $\lambda/4$ tuning takes
   over.
3. **Active design** — actuator + controller.
4. **Single-cell validation** in a standing-wave tube.
5. **Multi-cell duct test** — predicted vs measured on the ECL MATISSE
   laboratory flow duct with anechoic termination.

Architecture highlights:

- **Cell-by-cell feedback FxLMS** (rear-face microphone behind a
  porous screen, digital adaptive loop on each cell independently) —
  trivial surface scaling by adding cells, no global MIMO coupling.
- **Piezoelectric actuators + wire-mesh porous layers** yield hybrid
  cells **<0.03 m thick** with approximately real and constant
  surface impedance up to 2500 Hz.
- Basic cell[^betgen-2012] — 1 rear mic → pressure cancelled → purely
  real $Z_s$ = screen resistance. Error mic shielded from grazing
  flow; fast convergence, excellent stability.
- Complex cell[^betgen-2012] — 2 mics (front + rear) → controls
  arbitrary complex target impedance. Front-face mic exposed to flow,
  so flow-induced turbulence adds noise; more capability at stability
  cost. Laser-Doppler velocimetry at ONERA: without flow, the
  multi-cell array acts as a near-homogeneous liner (global
  duct-mode effect); with grazing flow, each cell's influence becomes
  local — the homogeneous-impedance picture breaks down, explaining
  the measured TL drop with increasing Mach. TL up to 20 dB without
  flow.
- Complementary approaches cited by Betgen 2012: **Kanev & Mironov
  2008** (passive-electrical shunt tuning the secondary source) and
  **Lissek et al. 2011** (unified electroacoustic-absorber theory)
  achieve active-impedance control without an external sensor.

Application targets:

- Aircraft engine inlet liners (NASA / Rolls-Royce prototypes) —
  driver array behind perforated facing-sheet replaces / augments
  Helmholtz cells.
- HVAC silencer retrofits — loudspeaker in the splitter plenum,
  microphone downstream, feedback FxLMS.
- Rooftop-fan application: active layer sized for the BPF + first two
  harmonics only; passive fibrous lining handles everything above
  ~400 Hz.

## 3. Active / tunable acoustic metamaterials

Locally-resonant metamaterials achieve sub-wavelength absorption at
design frequencies — but are *narrowband* and *fixed-tuned* — so
tunable and active variants are the frontier for rooftop-scale
deployment. Ma & Sheng 2016[^ma-sheng-2016] is the canonical
cross-cutting review; it surveys the trajectory from locally-resonant
units through negative-parameter regimes to actively-controllable
metamaterials and non-Hermitian loss-gain designs.

**Canonical fixed-tuned milestones:**

- **Mei et al. 2012**[^mei-2012] — *dark acoustic metamaterial*:
  200 µm elastic membrane + asymmetric iron platelets. Near-unity
  absorption at resonances in 100–1000 Hz band with
  wavelength-to-thickness ratio $\gtrsim 10^3$ (λ ≈ 2 m at 172 Hz).
  Mechanism: asymmetric-platelet flapping concentrates **elastic
  curvature energy** at platelet perimeters; these modes couple only
  weakly to radiation, so internal energy density runs 2–3 orders
  above incident — effectively an open cavity. Sample A peaks at
  172 / 340 / 813 Hz; Sample B (8-platelet arrays) reaches near-unity
  at multiple peaks.
- **Fang et al. 2006** — negative modulus (pending PDF ingest).
- **Ma et al. 2014** — hybrid-resonance metasurface (pending).

**Ventilated variants (critical for rooftop fans — airflow must flow
through the absorber):**

- **Wu et al. 2018**[^wu-2018] — *ventilated metamaterial absorber*
  (VMA): two oppositely-oriented split-tube resonators whose
  degenerate eigenmodes hybridize. Breaks the 50% upper bound on
  reflector-free symmetric absorption; **>90% absorption** <500 Hz
  with only two layers, ventilation preserved through gaps between
  units. Purely passive, so more practical than CPA schemes (which
  need dynamically-generated counter-incident beams) and more robust
  than prestress-sensitive membrane absorbers. (Filename staged as
  "Ghaffarivardavagh" but arXiv 1801.03613 is Wu et al.;
  Ghaffarivardavagh 2019 is a different, closely related group.)
- **Ghaffarivardavagh et al. 2019** — final ultra-open silencer
  (*Phys. Rev. B*). Pending PDF.

**Tunable-active families:**

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
  research; surveyed in Ma & Sheng 2016[^ma-sheng-2016]).

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

## Sources ingested

- **Galland, Mazeaud & Sellen 2005** — flow-duct hybrid liner 5-step
  design; MATISSE test rig; cell-by-cell FxLMS. See
  `entities/source-papers.md#paper-galland-hybrid-flowduct-2005`.
- **Betgen, Galland, Piot & Simon 2012** — basic vs complex hybrid
  cells; LDV non-intrusive characterization with grazing flow. See
  `entities/source-papers.md#paper-betgen-galland-hybrid-liner-2012`.
- **Guicking 2009** — 1740-patent overview of ANVC (use as patent
  index). See `entities/source-papers.md#paper-guicking-patents-overview`.
- **Mei et al. 2012** — dark acoustic metamaterial, foundational
  sub-wavelength LF super-absorber. See
  `entities/source-papers.md#paper-mei-dark-metamaterial-2012`.
- **Wu et al. 2018** (arXiv 1801.03613) — ventilated metamaterial
  absorber with airflow preserved. See
  `entities/source-papers.md#paper-wu-ventilated-metamaterial-2018`.
- **Ma & Sheng 2016** (*Sci. Adv.*) — 15-year metamaterials review
  (use as citation hub). See
  `entities/source-papers.md#paper-ma-sheng-metamaterials-review-2016`.

## Pending sources

- Olson & May, *JASA* 1953 — electronic sound absorber (pre-digital).
- Guicking, D., "Active control of sound and vibration — history, fundamentals, state of the art." (tutorial article separate from the patents overview).
- Beyene, S. & Burdisso, R., *JASA* 1997 — hybrid passive-active absorber.
- Furstoss, M., Thenail, D., Galland, M.-A., *JSV* 1997 — earlier active duct liner.
- Fang, N. et al., "Ultrasonic metamaterials with negative modulus," *Nature Materials* 2006.
- Ma, Yang, Xiao, Yang & Sheng, *Nature Materials* 13:873, 2014 — hybrid-resonance metasurface.
- Ghaffarivardavagh et al. 2019 (*Phys. Rev. B*) — final ultra-open silencer (the 2018 arXiv preprint ingested is Wu et al.).

See also: [[classical-anc-overview]] §2–3 (adaptive filters and
secondary-path modeling that still apply to the active layer),
[[tonal-periodic-anc]] (narrowband control used in hybrid cells),
[[rooftop-fan-contenders]] (the passive side catalogued for the
fan-hum application).

[^galland-2005]: M.-A. Galland, B. Mazeaud & N. Sellen, "Hybrid passive/active absorbers for flow ducts," *Applied Acoustics* 66:691–708, 2005. Distilled in `entities/source-papers.md#paper-galland-hybrid-flowduct-2005`.
[^betgen-2012]: B. Betgen, M.-A. Galland, E. Piot & F. Simon, "Implementation and non-intrusive characterization of a hybrid active–passive liner with grazing flow," *Applied Acoustics* 73:624–638, 2012. Distilled in `entities/source-papers.md#paper-betgen-galland-hybrid-liner-2012`.
[^guicking-patents-2009]: D. Guicking, *Patents on Active Control of Sound and Vibration — an Overview*, 2nd ed., Göttingen, May 2009. Distilled in `entities/source-papers.md#paper-guicking-patents-overview`.
[^mei-2012]: J. Mei, G. Ma, M. Yang, Z. Yang, W. Wen & P. Sheng, "Dark acoustic metamaterials as super absorbers for low-frequency sound," *Nature Communications* 3:756, 2012. Distilled in `entities/source-papers.md#paper-mei-dark-metamaterial-2012`.
[^wu-2018]: X. Wu, K. Y. Au-Yeung, X. Li, R. C. Roberts, J. Tian, C. Hu, Y. Huang, S. Wang, Z. Yang & W. Wen, "High-efficiency Ventilated Metamaterial Absorber at Low Frequency," arXiv 1801.03613 / *APL* 2018. Distilled in `entities/source-papers.md#paper-wu-ventilated-metamaterial-2018`.
[^ma-sheng-2016]: G. Ma & P. Sheng, "Acoustic metamaterials: from local resonances to broad horizons," *Science Advances* 2:e1501595, 2016. Distilled in `entities/source-papers.md#paper-ma-sheng-metamaterials-review-2016`.

---
title: WDF Applications
created: 2026-04-11
updated: 2026-11-25
type: concept
tags: [waveguide, dsp, physical-modeling, nonlinear, guitar, string]
sources:
  - /l/wgr/Sections/HistoricalBackground.tex
  - /l/dttd/WDF
  - /l/dttd/SMC_2022_Diff_WDFs.pdf
  - /l/dttd/WDF-NeuralK-Benardini-IEEE-OpenSigProc-2025.pdf
  - /l/dttd/PyWDF-DAFx23.pdf
  - /l/dttd/Automatic_Generation_of_Virtual_Analog_Audio_Plug_ins_based_on_WDFs_RG.pdf
  - https://ccrma.stanford.edu/~jos/pasp/Wave_Digital_Modeling_Examples.html
  - /l/dttd/DAFx26/ - DAFx26 papers catalogued in entities/source-papers.md
---

# WDF Applications

Wave digital filters bridge lumped-element circuit modeling with
real-time audio synthesis and effects processing. Key applications
span musical acoustics, analog audio circuit emulation, and modern
differentiable/neural extensions.

## Musical Instrument Components

### Piano Hammer (Van Duyne & Smith, 1994)[^1]
- Hammer-string contact modeled as nonlinear mass-spring WDF
- Passive reformulation: Bilbao, Smith, Bensa & Kronland-Martinet (2002)
- Felt compression characteristic: power-law or piecewise
- WDF provides modularity: change felt stiffness without re-deriving string
- Connects to digital waveguide string at a scattering junction

### Tonehole (Van Walstijn, 2000)
- Woodwind tonehole modeled as WDF shunt element
- Open/closed tonehole impedance connects via T-junction adaptor
- Radiation impedance at open hole included
- Integrates with the DWG [[bore-modeling|bore model]] seamlessly

## Analog Audio Circuit Emulation

A major modern application: real-time emulation of vintage audio gear.

### Diode Clippers (Werner et al., 2015)
- Diode V-I characteristic as WDF nonlinear element
- Solved explicitly at root of WDF tree
- Warm analog distortion in real time

### Tube Amplifiers
- Triode stage with cross-control model (Karjalainen & Pakarinen, 2006)
- Fender Bassman 5F6-A preamplifier (Dunkel et al., 2016)
- Triode/pentode stages as nonlinear WDF elements
- Tone stack as passive WDF network

### VIOLA — Automatic SPICE-to-Plugin (Giampiccolo et al., 2025)
- End-to-end: SPICE netlist → WDF → MATLAB Audio Toolbox → VST/AU
- Builds on Werner's MNA scattering; adds numerical port adaptation
- Diode consolidation often reduces to explicit single-NL solution
- SIM + DSR as table-free solver for irreducible multi-NL circuits
- See [[viola-wdf-plugin-generator]] for details

### General Approach
1. Draw the analog circuit schematic
2. Identify series/parallel connections → WDF tree topology
3. Digitize each element: R,L,C → WDF one-ports; nonlinear at root
4. Connect via adaptors
5. Run in real time

## Software Implementations

### RT-WDF (Rest, Dunkel, Werner & Smith, DAFx 2016)
- Modular C++ library; arbitrary topologies (R-type) and multiple nonlinearities
- Run-time polymorphism: flexible but slow (see [[wdf-code-generation]])

### Faust `wdmodels`
- WDF adaptors and elements in the Faust libraries; topology fixed at compile time

### `chowdsp_wdf` and `wdf_compiler` (Chowdhury)
- Template-metaprogramming C++ library, and its code-generating successor

### PyWDF (Anthon, Lizarraga-Seijas & Font, DAFx23)
- Python framework for prototyping and simulating WDF circuits
- Differentiable WDFs are listed as future work, not implemented

## Modern Extensions

### Differentiable WDFs (SMC 2022)
- Backpropagate through WDF computation graph
- Optimize circuit parameters to match target audio
- Bridge to DDSP / neural audio synthesis

### Explicit Neural Multiport Junctions (Giampiccolo, Gafencu & Bernardini, 2025)
- An MLP learns the explicit wave mapping of the (multiport) nonlinear junction
  in vector-wave form, replacing K-method lookup tables and iterative solvers
- DAFx26 follow-up compares KANs with MLPs in this role

### Lipschitz-Bounded Neural WDFs (DAFx24)
- Constrain neural nonlinearity to be Lipschitz-bounded
- Guarantees passivity / stability of the neural WDF element

### Multiple Nonlinearities
- Werner et al. (2015)[^2]: SPQR-tree + R-type root + K-method framework —
  see [[wdf-multiple-nonlinearities]] for details
- Olsen et al. (2016): iterative techniques for grouped nonlinearities
- Yeh et al. (2010, 2012): general NLSS (nodal DK) formulation for complicated topologies
- Reciprocal multiport junctions in general: Bernardini et al. (2019)[^3]

## Comparison: WDF vs. Direct Circuit Simulation

| Aspect | WDF | SPICE-like | Nodal DK |
|--------|-----|-----------|----------|
| Modularity | High (element-level) | Low | Medium |
| Stability guarantee | Yes (passivity) | No | Conditional |
| Real-time | Yes | Rarely | Yes |
| Nonlinear support | One per tree (or iterative) | Any | Any |
| Frequency accuracy | Warped (bilinear) | Step-size controlled | Warped (trapezoidal) |

## Related Concepts
- [[wave-digital-filters]] — the foundational theory
- [[wdf-elements]] — the building blocks
- [[wdf-adaptors]] — how elements connect
- [[waveguide-parameter-optimization]] — DDSP techniques applied to WDFs
- [[reed-and-bow-models]] — DWG models that interface with WDF components
- **DAFx26 page:** [[wdf-code-generation]] - the declarative circuit DSL, compiler and benchmarks
- **DAFx26 additions (Sept 2026):** compiled abstraction-free WDF code generation, an explicit CPWL wave digital model of the Fulltone OCD pedal, and KANs vs MLPs as the learned nonlinear-junction solver - see [[entities/source-papers#wave-digital-filters-and-circuit-emulation]]
- [[virtual_analog/concepts/virtual-analog-overview|virtual analog overview]] — the wider VA context (state-space, TPT, neural)

## JOS online books
- [[jos_books/entities/pasp-book|PASP]]: [Wave Digital Modeling Examples](https://ccrma.stanford.edu/~jos/pasp/Wave_Digital_Modeling_Examples.html), [Piano Hammer Modeling](https://ccrma.stanford.edu/~jos/pasp/Piano_Hammer_Modeling.html), [Tonehole Modeling](https://ccrma.stanford.edu/~jos/pasp/Tonehole_Modeling.html), [Wave Digital Mass-Spring Oscillator](https://ccrma.stanford.edu/~jos/pasp/Wave_Digital_Mass_Spring_Oscillator.html), ["Piano hammer in flight"](https://ccrma.stanford.edu/~jos/pasp/_Piano_hammer_flight.html)

## References
[^1]: Van Duyne, S. & Smith, J.O. (1994). "The Wave Digital Hammer: A Computationally Efficient Traveling Wave Model of the Piano Hammer and the Felt Mallet." JASA 96(5).
[^2]: Werner, K.J., Nangia, V., Smith, J.O. & Abel, J.S. (2015). "Resolving Wave Digital Filters with Multiple/Multiport Nonlinearities." DAFx-15.
[^3]: Bernardini, A., Werner, K.J., Smith, J.O. & Sarti, A. (2019). "Generalized Wave Digital Filter Realizations of Arbitrary Reciprocal Connection Networks." IEEE TCAS-I 66(2).

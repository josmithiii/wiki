---
title: WDF Applications
created: 2026-04-11
updated: 2026-04-15
type: concept
tags: [waveguide, dsp, physical-modeling, nonlinear, guitar, string]
sources:
  - /l/wgr/Sections/HistoricalBackground.tex
  - /l/dttd/WDF
  - /l/dttd/SMC_2022_Diff_WDFs.pdf
  - /l/dttd/WDF-NeuralK-Benardini-IEEE-OpenSigProc-2025.pdf
  - /l/dttd/PyWDF-DAFx23.pdf
  - /l/dttd/Automatic_Generation_of_Virtual_Analog_Audio_Plug_ins_based_on_WDFs_RG.pdf
---

# WDF Applications

Wave digital filters bridge lumped-element circuit modeling with
real-time audio synthesis and effects processing. Key applications
span musical acoustics, analog audio circuit emulation, and modern
differentiable/neural extensions.

## Musical Instrument Components

### Piano Hammer (Van Duyne & Smith, 1994)
- Hammer-string contact modeled as nonlinear mass-spring WDF
- Felt compression characteristic: power-law or piecewise
- WDF provides modularity: change felt stiffness without re-deriving string
- Connects to digital waveguide string at a scattering junction

### Tonehole (Van Walstijn, 2000)
- Woodwind tonehole modeled as WDF shunt element
- Open/closed tonehole impedance connects via T-junction adaptor
- Radiation impedance at open hole included
- Integrates with DWG bore model seamlessly

### Lip Reed (Bilbao, 2002)
- Mass-spring lip model digitized as WDF
- Nonlinear coupling to bore pressure via K-method
- One- and two-mass models

## Analog Audio Circuit Emulation

A major modern application: real-time emulation of vintage audio gear.

### Diode Clippers (Werner et al., 2015)
- Diode V-I characteristic as WDF nonlinear element
- Solved explicitly at root of WDF tree
- Warm analog distortion in real time

### Tube Amplifiers
- Fender Bassman 5F6-A preamplifier (Dunkel et al., 2016)
- Triode/pentode stages as nonlinear WDF elements
- Tone stack as passive WDF network

### VIOLA — Automatic SPICE-to-Plugin (Giampiccolo et al., 2025)
- End-to-end: SPICE netlist → WDF → MATLAB Audio Toolbox → VST/AU
- General junction-port adaptation formula (closes WDF literature gap)
- Diode consolidation + SIM + DSR for multi-nonlinearity circuits
- See [[viola-wdf-plugin-generator]] for details

### General Approach
1. Draw the analog circuit schematic
2. Identify series/parallel connections → WDF tree topology
3. Digitize each element: R,L,C → WDF one-ports; nonlinear at root
4. Connect via adaptors
5. Run in real time

## Software Implementations

### STK (Cook & Scavone)
- Early WDF-based instrument models in C++

### Faust
- WDF primitives in Faust libraries
- Composable physical modeling via block diagrams

### PyWDF (DAFx23)
- Python framework for prototyping wave digital filters
- Supports automatic differentiation for parameter optimization

### RT-WDF (Bernardini et al., 2018)
- C++ library for real-time WDF simulation
- Handles reciprocal connection networks

## Modern Extensions

### Differentiable WDFs (SMC 2022)
- Backpropagate through WDF computation graph
- Optimize circuit parameters to match target audio
- Bridge to DDSP / neural audio synthesis

### Neural K-Method (Bernardini et al., 2025)
- Replace lookup-table K-method with neural network
- Learns nonlinear scattering from data
- Handles multiple nonlinearities more flexibly

### Lipschitz-Bounded Neural WDFs (DAFx24)
- Constrain neural nonlinearity to be Lipschitz-bounded
- Guarantees passivity / stability of the neural WDF element

### Multiple Nonlinearities
- Werner et al. (2015): SPQR-tree + R-type root + K-method framework —
  see [[wdf-multiple-nonlinearities]] for details
- Olsen et al. (2016): iterative techniques for grouped nonlinearities
- Yeh et al. (2010, 2012): general NLSS formulation for complicated topologies

## Comparison: WDF vs. Direct Circuit Simulation

| Aspect | WDF | SPICE-like | Nodal DK |
|--------|-----|-----------|----------|
| Modularity | High (element-level) | Low | Medium |
| Stability guarantee | Yes (passivity) | No | Conditional |
| Real-time | Yes | Rarely | Yes |
| Nonlinear support | One per tree (or iterative) | Any | Any |
| Frequency accuracy | Warped (bilinear) | Exact (small step) | Exact |

## Related Concepts
- [[wave-digital-filters]] — the foundational theory
- [[wdf-elements]] — the building blocks
- [[wdf-adaptors]] — how elements connect
- [[waveguide-parameter-optimization]] — DDSP techniques applied to WDFs
- [[reed-and-bow-models]] — DWG models that interface with WDF components

## References
[^1]: Van Duyne, S. & Smith, J.O. (1994). "A Simplified Approach to Modeling Dispersion..." ICMC.
[^2]: Werner, K.J. et al. (2015). "Wave Digital Filter Modeling of Circuits with Multiple Nonlinearities." DAFx.
[^3]: Bernardini, A. et al. (2018). "Reciprocal Connection Networks in WDFs." IEEE TCAS-I.

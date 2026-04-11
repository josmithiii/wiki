---
title: Waveguide Parameter Optimization
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [waveguide, optimization, ml, differentiable, dsp, physical-modeling]
sources:
  - /l/wgr/Sections/Parameter Optimization/ParameterOptimisation.tex
---

# Waveguide Parameter Optimization

Calibrating a digital waveguide model to match a target sound requires
estimating physical or filter parameters. Multiple strategies have been
developed over four decades, from physics-based measurement to modern
differentiable DSP.

## Physics-Based

- Estimate modal parameters (A_n, omega_n, alpha_n) from impulse response
- Design loop filter from measured viscothermal losses and dispersion
- Does not guarantee realism on its own (Guillemain 1997, Ystad 1998)
- Best as anchor/constraint combined with other methods
- Example: Smyth & Abel — clarinet bell reflection filter from measurement,
  then estimate reed pulse by inverse filtering

## Filter Design

- From (A_n, omega_n, alpha_n), derive poles/zeros of H(z)
- Fundamental frequency: autocorrelation, harmonic spacing, or lowest harmonic
- Body response: inverse-filter string to obtain pluck response
- Body resonator: Warped-IIR captures non-harmonic modes (Helmholtz resonance)
  and can be shared across strings (Tolonen & Välimäki)
- See [[commuted-synthesis]] for the body separation technique

## System Identification

- Precompute input-output mappings, use lookup at runtime
- K-L model: area → formant table; nearest-neighbor match (Kestian & Smyth 2010)
- Saxophone fingering: maximize time-domain cosine similarity (Smyth & Wang 2014)
- Bowed string: LPC + PCA features → GMM mapping (Serafin et al. 2001)
- Limited generalizability; task-specific

## Genetic Algorithms

- Random search; successful parameter sets survive
- First applied to flute model (Vuori & Välimäki, 1993)
- Psychoacoustic weighting in fitness function (Riionheimo & Välimäki, 2003)
- Scaled to 2D waveguide mesh vocal tract (Cooper et al., 2006)
- Modern: Pink Trombone optimization competes with neural methods (Cámara, 2023-25)
- Tradeoff: quality depends on population size; slower than neural inference

## Neural — Black-Box

Controller network predicts DWG parameters from audio:
- Casey (1994): first neural DWG inversion (bowed string), parameter loss
- Cemgil & Erkut (1997): perceptual loss from listening tests
- Sinclair (2018): adversarial autoencoder for bowed string
- Gabrielli et al. (2017-19): CNN for flue-organ DWG (patented)
- Xu & Reiss (2025): Transformer for Pink Trombone vocal tract

Synthesizer networks predict output waveform (teacher for controller):
- Drioli (1998), Uncini (2002): predict reed excitation signal
- Data-hungry; quality depends on dataset size

## Neural — White-Box (DDSP)

DWG embedded within neural network; backprop through differentiable DSP:
- Su, Liang et al. (1997-2006): RNN ↔ IIR filter equivalence;
  neuron weights = scattering coefficients
- Engel et al. (2020): DDSP framework — native differentiable operations
- Hayes et al.: FDL decay optimized via multi-scale spectral loss (L_MSS)
- Tablas de Paula et al. (2025): time-variant FDL with pluck position,
  dynamics, timbre, and decay optimized separately
- Sudholt et al. (2023): DDSP on K-L vocal tract; beats genetic + black-box
- Mezza et al. (2025): DDSP applied to SDN reverb; matches room RIR features

### Current Challenges
- L_MSS yields poor gradients for sinusoidal frequency (f_0) prediction
- Permutation symmetry in mode ordering degrades point-based regressors
- Generative, symmetry-equivariant architectures showing promise (Hayes, 2025)
- Combining physically interpretable control with neural audio (Zong, 2025)

## Comparison Summary

| Method | Strengths | Weaknesses |
|--------|-----------|-----------|
| Physics-based | Interpretable, no data needed | Limited realism alone |
| Filter design | Precise freq-dep. control | Restricted to LTI FDLs |
| System ID | Fast at runtime | Task-specific, low generalizability |
| Genetic | No data needed, flexible | Slow, quality ∝ population size |
| Neural black-box | Real-time inference, generalizes | Data-hungry |
| Neural white-box | Less data, physical structure | Requires differentiable implementation |

## Related Concepts
- [[waveguide-overview]] — the models being optimized
- [[string-modeling]] — primary target for FDL optimization
- [[commuted-synthesis]] — body separation enables independent optimization
- [[waveguide-vocal-models]] — vocal tract as optimization target

## References
[^1]: Tablas de Paula, Smith, Välimäki & Reiss (2025). "Four Decades of Digital Waveguides." JAES.
[^2]: Engel, J. et al. (2020). "DDSP: Differentiable Digital Signal Processing." ICLR.

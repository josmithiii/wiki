---
title: ML Modal Parameter Estimation
created: 2026-04-10
updated: 2026-04-10
type: concept
tags: [modal-synthesis, ml, neural, differentiable, dsp, inference]
sources:
  - /l/dttd/DifferentiableModalSynthPlanarString-2407.05516v1.pdf
  - /l/dttd/DiffImpact-294_diffimpact_differentiable_rend.pdf
  - /l/dttd/SynthMatch-DDSP-Diaz-Hayes-RigidBodyModal-ICASSP23.pdf
  - ~/wiki/modal_synthesis/raw/papers/DiffSound-2409.13486v1.pdf
---

# ML Modal Parameter Estimation

Machine learning approaches to modal synthesis fall into two categories:
(1) learning to predict modal parameters (frequencies, damping, gains) from
object properties, and (2) differentiable modal synthesizers trained end-to-end
from audio.

## Neural Mode Prediction

### NeuralSound (Jin et al. 2020, 2022)
- Neural network predicts eigenvalues and eigenvectors from voxelized 3D shapes
- Circumvents expensive FEM eigensolve
- Adaptive scaling for different sizes and materials
- Limitation: discrete voxel positions, post-processing needed for material transfer
- Extended in 2022 with acoustic transfer functions for radiation

### DiffSound (Jin, Xu et al., SIGGRAPH 2024)[^1]
- Fully differentiable pipeline: mesh → FEM → eigensolve → audio
- Hybrid shape representation: implicit neural + explicit tetrahedral mesh
- High-order FEM module (not just linear elements) — better accuracy
- Differentiable audio synthesizer with hybrid loss (spectral + log-spectral)
- Inverse rendering tasks: infer material, thickness, shape, impact position from sound
- First to estimate object thickness and geometric shape purely from audio

## Differentiable Modal Synthesizers

### DiffImpact (Clarke et al., CoRL 2021)[^2]
- Fully differentiable generative model for rigid-body impact sounds
- Components: impact force profile + modal impulse response + noise + reverb
- Modal IR: K decaying sinusoids with learnable (f_k, g_k, d_k)
- Force profile: Gaussian approximation of Hertz half-sine contact
- Gradient-based joint inference of acoustic properties and impact characteristics
- Can be plugged as decoder of an autoencoder for self-supervised learning
- Tested on real YouTube ASMR videos and robotic manipulation audio

### DDSP Rigid-Body Modal (Diaz, Hayes et al., ICASSP 2023)[^3]
- End-to-end framework: neural network generates modal resonator bank
- Input: 2D rasterized shape + material parameters
- Output: differentiable IIR filter bank (biquad coefficients)
- Trained with audio-domain loss — no explicit eigenvalue supervision
- No post-processing for material/size adaptation (unlike NeuralSound)
- Arbitrary coordinate input for excitation position

### Differentiable Modal Synth for Strings (Lee et al., NeurIPS 2024)[^4]
- DMSP: differentiable modal synthesis for physical modeling
- Encodes string physical properties (tension, stiffness, damping) → displacement
- Outputs spatio-temporal string motion solving the nonlinear string PDE
- Integrates modal decomposition with spectral modeling in a neural framework
- Dynamic control: pitch glide, vibrato, material changes in real time
- Superior accuracy vs. baseline architectures for string motion simulation

## Comparison of Approaches

| Method | Input | Output | Training Signal | Real-time? |
|--------|-------|--------|----------------|-----------|
| NeuralSound | Voxelized 3D | Eigenvalues/vectors | FEM ground truth | Inference only |
| DiffSound | Tet mesh | Audio waveform | Audio (spectral loss) | No (optimization) |
| DiffImpact | Audio spectrogram | Modal params + force | Audio (spectral loss) | Inference only |
| DDSP Rigid-Body | 2D shape + material | IIR filter bank | Audio (spectral loss) | Yes |
| DMSP Strings | Physical properties | String displacement | PDE solution | Yes |

## Key Insights

- **Audio-domain losses** (multi-scale spectral + log-spectral) outperform
  parameter-space losses for perceptual quality
- **Physics-based inductive bias** (modal structure) dramatically reduces data
  needs vs. generic neural audio synthesis
- **Differentiability** enables analysis-by-synthesis: optimize physical parameters
  to match a target recording
- **Trade-off**: full physical accuracy (DiffSound/FEM) vs. real-time speed
  (DDSP/DiffImpact inference)

## Related Concepts
- [[modal-synthesis-overview]] — classical modal synthesis
- [[fem-bem-for-modal-synthesis]] — the FEM solvers these methods aim to replace
- [[resonator-bank-implementation]] — the DSP structure being learned
- [[gpu-modal-synthesis]] — GPU acceleration for large mode counts
- [[rigid-body-sound-synthesis]] — application domain

## References
[^1]: Jin, Xu, Gao, Wu, Wang & Li (2024). "DiffSound." SIGGRAPH Conference Papers.
[^2]: Clarke, Heravi, Rau, Gao, James, Wu & Bohg (2021). "DiffImpact." CoRL.
[^3]: Diaz, Hayes, Saitis, Fazekas & Sandler (2023). "Rigid-Body Sound Synthesis with Differentiable Modal Resonators." ICASSP.
[^4]: Lee, Choi, Park & Lee (2024). "Differentiable Modal Synthesis for Physical Modeling of Planar String Sound and Motion Simulation." NeurIPS.

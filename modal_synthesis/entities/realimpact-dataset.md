---
title: RealImpact Dataset
created: 2026-04-09
updated: 2026-11-25
type: entity
tags: [dataset, impact, modal-synthesis, acoustics, measurement, ml]
sources:
  - https://arxiv.org/abs/2306.09944
  - https://samuelpclarke.com/realimpact/
---

# RealImpact Dataset

## Overview
RealImpact is a large-scale dataset of real impact sound fields recorded from physical objects
under controlled conditions, designed for audio-visual learning and for calibrating the
sim-to-real gap of modal impact-sound simulation.

## Citation
Clarke, Gao, Wang, Rau, Xu, Wang, James, & Wu (2023):
"RealImpact: A Dataset of Impact Sound Fields for Real Objects"
CVPR 2023 (highlight) / arXiv:2306.09944

## Contents
- ~150,000 impact sound recordings
- 50 everyday objects with material labels
- Each object: struck at several positions × recorded at many microphone positions
- Annotations: impact locations, microphone locations, contact force profiles, material labels
- RGBD images of each object

## Recording Setup
- Recorded under controlled conditions (room, gantry and hammer details are in the paper)
- Instrumented impacts: a contact force profile is recorded for each strike
- Microphone positions distributed around the object, sampling its radiated sound field

## Unique Features
- **Position-labeled impacts**: know exactly where object was struck
- **Microphone position sweep**: captures directional radiation patterns
- **Calibrated force input**: enables normalization and FRF estimation
- **Physical diversity**: spans orders of magnitude in damping and stiffness

## Intended Use Cases
1. Training ML models to predict mode parameters from geometry + material
2. Evaluating modal synthesis algorithms against real recordings
3. Learning acoustic transfer functions (listener position dependence); see [[radiation-and-directivity]]
4. The paper's two benchmark tasks: listener location classification and visual acoustic matching

## Related Work
- **Visually Indicated Sounds** (Owens et al., CVPR 2016): predict impact sound from video ("Greatest Hits" dataset)
- **Generative model of rigid-body contact sounds** (Traer, Cusimano & McDermott, DAFx 2019): perceptually motivated impact synthesis
- **ObjectFolder** (Gao et al., 2021-2023): simulated and measured multisensory object datasets
- **DiffImpact** (Clarke et al., 2021): differentiable impact model from the same group; see [[ml-modal-parameter-estimation]]

## Access
Project page: https://samuelpclarke.com/realimpact/ · code and download scripts: https://github.com/samuel-clarke/RealImpact

## Limitations
- 50 objects is small by ML standards; diversity limited
- Only impact excitation (no friction/rolling)
- Real objects have imperfections and material variation that idealized geometry misses → FEM mismatch

## Related Concepts
- [[modal-analysis-measurement]] — techniques used to process this data
- [[impact-synthesis]] — what this dataset enables and benchmarks
- [[modal-synthesis-overview]] — broader context

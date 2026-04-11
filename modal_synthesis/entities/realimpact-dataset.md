---
title: RealImpact Dataset
created: 2026-04-09
updated: 2026-04-09
type: entity
tags: [dataset, impact, modal-synthesis, acoustics, measurement, ml]
sources: []
---

# RealImpact Dataset

## Overview
RealImpact is a large-scale dataset of real impact sounds recorded from physical objects,
designed to support ML-based modal synthesis and audio-visual sound generation research.

## Citation
Clarke, Gao, Wang, Rau, Xu, Wang, James, & Wu (2023):
"RealImpact: A Dataset of Impact Sound Fields for Real Objects"
ICCV 2023 / arXiv:2306.09944

## Contents
- ~150,000 impact sound recordings
- 50 unique objects (diverse materials: metal, wood, ceramic, plastic, rubber)
- Each object: struck at many positions × recorded at many microphone positions
- Synchronized video + audio
- 3D geometry scans (point clouds) for each object
- Impact position annotations

## Recording Setup
- Anechoic or semi-anechoic chamber
- Objects suspended by thin threads (minimizes boundary damping)
- Impact hammer with force sensor (calibrated force measurement)
- Microphone array at multiple distances/angles
- High-speed camera for contact visualization

## Unique Features
- **Position-labeled impacts**: know exactly where object was struck
- **Microphone position sweep**: captures directional radiation patterns
- **Calibrated force input**: enables normalization and FRF estimation
- **Physical diversity**: spans orders of magnitude in damping and stiffness

## Intended Use Cases
1. Training ML models to predict mode parameters from geometry + material
2. Evaluating modal synthesis algorithms against real recordings
3. Learning acoustic transfer functions (pickup position dependence)
4. Audio-visual sound synthesis (predict sound from video + object identity)

## Related Work
- **SoundingNet** (Owens et al., 2016): predict impact sound from video frames
- **Impact Sound Synthesis** (Traer & McDermott, 2016): perceptual study of impact stats
- **DCASE Challenge**: RealImpact used in some editions for physical audio modeling tasks

## Access
Available at: https://github.com/microsoft/RealImpact (as of 2022)
License: Creative Commons BY 4.0

## Limitations
- 50 objects is small by ML standards; diversity limited
- Only impact excitation (no friction/rolling)
- Real objects have surface imperfections not in 3D scan → FEM mismatch

## Related Concepts
- [[modal-analysis-measurement]] — techniques used to process this data
- [[impact-synthesis]] — what this dataset enables and benchmarks
- [[modal-synthesis-overview]] — broader context

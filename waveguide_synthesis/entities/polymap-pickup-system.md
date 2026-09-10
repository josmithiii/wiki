---
title: PolyMap Pickup System
created: 2026-09-10
updated: 2026-09-10
type: entity
tags: [guitar, string, dsp, realtime, reference]
sources:
  - /l/dttd/DAFx26/DAFx26_demo_73.pdf
  - raw/DAFx26_demo_73.txt
---

# PolyMap Pickup System

A 64-channel polyphonic electric-guitar pickup array from ETH Zurich - eight
strings sensed individually at eight positions each - useful here as a
**measurement platform** for string vibration and pickup-position effects.[^wieland]

Open-source design files: <https://github.com/IIP-Group/polymap>

## What it measures

- An **8 x 8 grid** of small directional active pickups (Cycfi Nu Capsules, strong
  neodymium magnets plus a preamp under the coil, wider bandwidth than typical
  guitar pickups) on a custom eight-string guitar: one pickup per string per
  position, eight positions between bridge and neck.
- Every channel is buffered, impedance-matched and bandwidth-limited, then
  digitised by eight 8-channel ADCs (Cirrus CS5308P) at **48 kHz / 24 bit**. Each
  channel has its own converter and all channels on a chip sample simultaneously,
  so signals from different positions along one string stay time-aligned - a
  precondition for blending or for measuring propagation along the string.

## Transport

An FPGA (SystemVerilog RTL: ADC buffer, subframe assembler, 4B5B encoder, clock-
domain-crossing FIFO, sync-symbol insertion, serialiser plus NRZI) formats the 64
channels into an **AES10 / MADI** stream at a fixed 125 Mbit/s over one coaxial
cable, which also carries power into the instrument. An off-the-shelf USB MADI
interface (RME MADIFace) exposes it to the DAW, delegating USB handling to proven
hardware.

- End-to-end latency **259 samples = 5.4 ms** at a 32-sample buffer and 48 kHz;
  the PolyMap hardware contributes about 5 samples and MADI another 27, the rest
  being DAW and OS buffering. A conventional USB interface measured 6.1 ms.
- Channel RMS noise **$-73$ to $-67$ dBFS**, dominated by the active pickups
  themselves (unpowered, the floor is $-90$ dBFS), largely coupled supply noise.
  Countermeasures are a moving-average filter plus a noise gate below $-55$ dBFS,
  blended with the dry signal up to $-32$ dBFS, and a resonant bandpass on output.

## What it enables

- **Post-hoc pickup placement.** The `PolyMap Studio` plug-in offers a manual mode
  (per pickup: enable, level, invert, pan, delay) and a virtual-pickup mode where a
  continuous position per string is chosen and neighbouring pickups are blended
  proportionally. Confirmed working in Reaper, which allows arbitrary channel counts.
- **Per-string processing**: strings panned across the stereo field, routed to
  separate amplifiers or effects, delayed or phase-inverted independently.
- **Controlled string-vibration measurement.** Because all pickups are identical
  and the position is chosen after the fact, position is the only variable. The
  paper's spectrum of an open A string shows the fundamental is not the strongest
  partial; the neck-most pickup is strongest for the fundamental and first
  harmonic, with the maximum moving bridge-ward for higher harmonics, and dips at
  particular harmonics where a standing-wave node sits near a pickup - the
  **comb-filter** model standardly used for guitar pickups. That makes the rig a
  direct instrument for validating pickup and string models (see
  [[string-modeling]]).

Limitation: a demo paper. Noise is pickup-limited, host support for 64-channel
tracks is narrow, and no modelling work is done with the captured data.

## See also
- [[string-modeling]] - the string models this can measure against
- [[commuted-synthesis]] - pickup and body response as a separable filter
- [[entities/source-papers#paper-wieland-polymap-pickups-2026]] - catalog entry

[^wieland]: D. Wieland, J. Roth, C. Studer, "PolyMap: A 64-Channel Polyphonic Guitar Pickup System," DAFx26 demo. See [[entities/source-papers#paper-wieland-polymap-pickups-2026]].

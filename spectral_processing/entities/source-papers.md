---
title: Source Papers -- Distilled Catalog
created: 2026-05-04
updated: 2026-05-04
type: entity
tags: [reference, phase-vocoder, tsm]
sources:
  - spectral_processing/raw/Improved_phase_vocoder_time-scale_modification_of_audio.txt
  - /l/dttd/Improved_phase_vocoder_time-scale_modification_of_audio.pdf
  - https://doi.org/10.1109/89.759041
---

# Source Papers -- Distilled Catalog

One section per ingested source. Each heading matches the `paper-<slug>` ID
used in `index.md`, so inbound links like
`[paper-laroche-dolson-improved-pv-1999](entities/source-papers.md#paper-laroche-dolson-improved-pv-1999)`
resolve inside this page. Blocks are distilled from text extractions in `raw/`
(gitignored); see `raw/MANIFEST.md` for the filename-to-PDF mapping.

When any single paper needs deeper treatment than the bullet summary supports,
promote it to a dedicated `entities/paper-<slug>.md` file and leave the section
here as a cross-link.

---

## Phase-vocoder TSM references

### paper-laroche-dolson-improved-pv-1999

**"Improved Phase Vocoder Time-Scale Modification of Audio"** -- Jean Laroche & Mark Dolson · *IEEE Transactions on Speech and Audio Processing* 7(3):323-332, May 1999 · DOI [10.1109/89.759041](https://doi.org/10.1109/89.759041) · `raw/Improved_phase_vocoder_time-scale_modification_of_audio.txt` · distilled at [[phase-vocoder-and-tsm]]

- Canonical paper explaining why classical phase-vocoder TSM sounds "phasy": standard bin-wise phase propagation preserves **horizontal** coherence over time but can destroy **vertical** coherence across neighboring STFT channels.
- Phase analysis shows that synthesis phases depend on current analysis phase, initial phase, time-scale factor, and accumulated phase-unwrapping integers. Integer factors can avoid the problem with the right initial phases; noninteger factors usually accumulate cross-bin phase errors when sinusoids cross bins or bins are temporarily noise-dominated.
- Introduces an STFT consistency measure adapted from Griffin-Lim. Useful diagnostic, but not a full perceptual predictor: PSOLA can score worse yet sound less reverberant on monophonic speech.
- Reviews two older alternatives: magnitude-only reconstruction avoids phase-unwrapping errors but is too iterative for real-time use; Puckette loose phase locking is cheap but signal-dependent.
- **Identity phase locking:** detect spectral peaks, propagate only peak-bin phases, and rotate the surrounding region of influence so synthesis-bin phase offsets match the analysis-frame offsets.
- **Scaled phase locking:** track corresponding peaks between frames and scale local offsets, improving perceived naturalness over identity locking in the authors' informal listening tests.
- Important implementation payoff: peak-only unwrapping makes 50% overlap practical for Hann/Hamming windows instead of the usual 75%, giving at least a factor-of-two cost reduction.
- Caveats: phase locking does not solve transient smearing, chirp-dependent magnitude reshaping, or harmonic shape-invariance; PSOLA remains better for monophonic pitched speech.
- Tags: phase-vocoder, tsm, stft, phase-unwrap, modifications, reference

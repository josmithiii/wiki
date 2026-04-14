# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-04-14] create | Wiki initialized
- Domain: Active absorbers and active noise control (ANC)
- Structure created: SCHEMA.md, index.md, log.md
- Directories: raw/, concepts/, entities/, comparisons/, queries/
- Source corpus to ingest: /l/dttd/ANC-Stuff/ (symlinks into /l/dttd/)

## [2026-04-14] ingest | pdf2txt.py extraction of 12 ANC/active-absorber PDFs
- Tool: pdf2txt.py (pdfminer.six)
- Source: /l/dttd/ANC-Stuff/*.pdf (12 papers/patents)
- Output: raw/*.txt + raw/MANIFEST.md (text-file ↔ original-PDF mapping)
- Note: DeepLearningHearingAids-2507.07043v2.txt and
  DeepLearningSelectiveNoiseCancellation-2507.07043v2.txt are the same arxiv paper
- Next: distill into concepts/entities pages with BBBot

## [2026-04-14] create | concepts/fxlms-algorithm.md
- Source: raw/ANC-Widrow-j1975adaptivenoise.txt (LMS foundation)
- Content: FxLMS update, stability/phase-error constraint, variants (NLMS, leaky, modified, multichannel, freq-domain), causality note
- Notes: Widrow 1975 introduces LMS but not FxLMS itself — attributed Morgan 1980 / Burgess 1981
- Index bumped: Concepts count 0 → 1

## [2026-04-14] split | concepts/fxlms-algorithm.md → +concepts/lms-algorithm.md
- Reason: original page conflated Widrow 1975 (LMS) with Morgan/Burgess (FxLMS). Scoped each page to its actual source.
- New page concepts/lms-algorithm.md: distillation of Widrow 1975 — architecture, Widrow–Hoff update, convergence time constants, tapped-delay FIR rules, 1975 application list (ECG, antenna sidelobe, fetal ECG, speech-in-noise), causality caveat from Appendix B.
- Trimmed concepts/fxlms-algorithm.md: removed "Standard LMS" section and Widrow footnote; now cites Morgan 1980 + Burgess 1981 (pending ingestion); links to lms-algorithm.
- Frontmatter sources updated on both pages.

## [2026-04-14] research | locate Morgan 1980 / Burgess 1981 source PDFs
- Checked /l/dttd/ and /l/dttd/ANC-Stuff/ — neither paper present.
- Both are paywalled (IEEE TASSP and JASA respectively); cannot fetch autonomously.
- Added placeholder entries in concepts/fxlms-algorithm.md footnotes and an "Pending ingestion" block in index.md + raw/SUMMARIES.md documenting the standard pdf2txt.py ingestion procedure.

## [2026-04-14] create | raw/SUMMARIES.md (12 papers + 2 pending)
- Delegated reading of all 12 raw extractions to an Explore subagent; compiled dense 4–6 bullet summaries keyed to planned entity pages.
- Confirmed DeepLearningHearingAids-2507.07043v2.txt and DeepLearningSelectiveNoiseCancellation-2507.07043v2.txt are byte-identical duplicates of arXiv 2507.07043 (Khan et al. 2025) — collapsed into a single pending entity.
- Flagged 3 internal project documents (Active_Noise_Control_for_Data_Center_Rooftop_Fan_Hum, Experiment_1_Neural_ANC_Controller_vs_Classical_Methods, ML_Opportunities_for_ANC_of_Data_Center_Fan_Noise) as unpublished working docs dated ~2026-03-29.

## [2026-04-14] update | index.md — draft initial entity stubs
- Added 11 entity entries under Entities (grouped: Published references / Patents / Internal project documents), each marked [pending] and pointing at raw/SUMMARIES.md for the actual content.
- Added Concepts entry for lms-algorithm; updated total count to "2 concepts + 12 pending entities".
- Added Pending-ingestion section listing Morgan 1980 and Burgess 1981.

## [2026-04-14] ingest | LatentFxLMS (Sarkar et al. 2025, arXiv 2507.03854)
- PDF: /l/dttd/LatentFxLMS-2507.03854v1.pdf (symlinked in ANC-Stuff/)
- Extracted: raw/LatentFxLMS-2507.03854v1.txt (1190 lines via pdf2txt.py)
- MANIFEST.md updated.
- SUMMARIES.md: added dense block (latent-space FxLMS update, VAE vs mixup decoders, latent-normalized step, bounded-primary-region caveat).
- concepts/fxlms-algorithm.md: added Latent FxLMS bullet under "Variants" and a [^latent] footnote; frontmatter sources list updated.
- index.md: added paper-sarkar-latent-fxlms entity stub; pending count 12 → 9 after internal-doc removals below.

## [2026-04-14] cleanup | remove duplicate extraction
- JOS deleted /l/dttd/DeepLearningHearingAids-2507.07043v2.pdf (canonical copy is DeepLearningSelectiveNoiseCancellation-2507.07043v2.pdf).
- Removed raw/DeepLearningHearingAids-2507.07043v2.txt.
- MANIFEST.md row collapsed; SUMMARIES.md duplicate note rewritten as single entry.

## [2026-04-14] scope | exclude internal project documents from distillation
- Per JOS: omit the three rooftop-fan internal working documents from wiki distillation (they are project state, not research sources).
- Removed "Internal project documents" section from index.md.
- Removed corresponding summary blocks from raw/SUMMARIES.md.
- Added an "Excluded from wiki distillation" list to raw/MANIFEST.md so the .txt extractions remain present as raw context but are explicitly not given entity pages:
  - Active_Noise_Control_for_Data_Center_Rooftop_Fan_Hum.txt
  - Experiment_1_Neural_ANC_Controller_vs_Classical_Methods.txt
  - ML_Opportunities_for_ANC_of_Data_Center_Fan_Noise.txt
- Morgan 1980 / Burgess 1981 remain pending; JOS will obtain later.

## [2026-04-14] create | 8 new concept pages for AI-based ANC (project focus)
- Context: research project will focus on AI-extensions of ANC; scaffold the concept layer so future source ingestion drops into clear slots.
- Organizing axis: *where the neural network sits in the ANC loop*, not architecture family. Seven categories in the overview.
- New pages under concepts/:
  - ai-anc-overview.md — umbrella / map of the territory (7 categories, reading map)
  - deep-anc-crn.md — Zhang & Wang 2021 end-to-end CRN; architecture, loss, multi-condition training, nonlinear plant handling, causality
  - neural-system-identification.md — NNSI framework (Helwani ICASSP 2023), parent of Latent FxLMS; generic update, instantiation table, open questions
  - meta-learning-anc.md — learned optimizer for FxLMS; training protocol, strengths/weaknesses, contrast with NNSI
  - neural-secondary-path.md — implicit / explicit / generative / physics-informed secondary-path modeling [stub]
  - pinn-virtual-sensing.md — Helmholtz-constrained neural fields for virtual error signals [stub]
  - deep-rl-anc.md — policy learning with hard constraints and perceptual rewards [stub]
  - transformer-se-anc.md — Conformer/Transformer/Mamba SE architectures and what transfers to ANC
- Index updated: Concepts section reorganized into "Classical adaptive filtering" + "AI-based ANC approaches (project focus)"; total 2 → 10 concepts.
- Every new page wikilinks to ai-anc-overview and at least one other concept page (SCHEMA ≥2 outbound links rule satisfied).
- Pages marked [stub] have sources:[] or [pending] footnotes and candidate-source lists to guide future ingestion.

## [2026-04-14] download | 13 free PDFs staged for /l/dttd/
- New staging directory: incoming-pdfs/ (to be deleted after JOS moves files into /l/dttd/)
- Downloaded in parallel via curl from arxiv.org and cdn.amazon.science; all verified as real PDFs (file(1) confirms).
- Contents grouped by target concept page:
  - NNSI (Helwani et al. ICASSP 2023) — 1 file → neural-system-identification.md
  - PINN virtual sensing — 6 files (canonical Zhang 2309.10605 + survey + volumetric + 1D + region-to-region + point-neuron) → pinn-virtual-sensing.md
  - Meta-learning ANC — 3 files (delayless subband / SFANC-ResNet / co-init) → meta-learning-anc.md (+ neural-secondary-path.md for the co-init paper)
  - Deep ANC follow-up — 1 file (speech-preserving reverberant) → deep-anc-crn.md
  - DRL-ANC-adjacent — 2 files (GFANC + DRL-in-control survey) → deep-rl-anc.md
- README.md in incoming-pdfs/ has the full file-to-page mapping + move-and-ingest bash recipe.
- Morgan 1980 and Burgess 1981 remain paywalled; no legitimate free source surfaced. Recommended secondary citations: Kuo & Morgan 1996, Elliott 2001.

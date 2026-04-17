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

## [2026-04-14] doc | PDF ingestion convention for future agents
- Top-level ~/wiki/README.md: added "PDF ingestion convention (all wikis)" section documenting /l/dttd/ host location, raw/ gitignore policy, MANIFEST.md / SUMMARIES.md conventions, Read-a-PDF prohibition, and the incoming-pdfs/ staging protocol (commit README only, not binaries).
- active_absorbers/SCHEMA.md: rewrote "Source Attribution" to point at the README section plus document this wiki's specific details (raw/ contents, staging, excluded-from-distillation list in MANIFEST.md).

## [2026-04-14] ingest | AI-ANC batch of 13 PDFs
- JOS moved incoming-pdfs/ contents to /l/dttd/ and created symlinks in /l/dttd/ANC-Stuff/.
- Ran pdf2txt.py in parallel on all 13, producing raw/*.txt extractions (738–2110 lines each, 41720 lines total).
- Delegated per-paper distillation to an Explore subagent; applied taxonomy-compliant tags.
- MANIFEST.md: appended 13 rows with arXiv IDs and short provenance notes.
- SUMMARIES.md: added new "AI-ANC Ingestion Batch (2026-04-14)" section grouped by target concept page (NNSI / PINN / meta-learning / deep ANC / deep RL); dense bullet summaries with architecture, loss, experimental setup, and key numeric results where reported.
- index.md: added "AI-ANC ingestion batch" subsection under Entities with 12 pending entity stubs, grouped by the same concept-page clusters. Pending-entities count 9 → 21.
- Decision: **DRL-Control-Survey-2507.08196** does NOT get an entity page — verified extraction contains no ANC/acoustic content. Flagged for use as inline background reference only in concepts/deep-rl-anc.md.
- **Promotion of stub concept pages deferred** to a separate pass. This commit is scoped purely to ingestion; the concept pages still carry their [stub] markers and sources:[] lists until they're rewritten from the new primary sources.
- Deleted active_absorbers/incoming-pdfs/ staging directory (PDFs now in /l/dttd/, README's job is done).

## [2026-04-15] promote | AI-ANC stub concept pages rewritten from primary sources
- **neural-system-identification.md**: added concrete Helwani 2023 section — topology-aware VAE with DIP-VAE-II disentanglement + Kirchhoff-Helmholtz simplicial-complex topology constraint, retraction-based adaptation (Euler + Newton variants), RLS / ℓ1-RLS baselines on 200-RIR shoebox dataset. Removed [pending ingestion] markers. sources: now includes NNSI-Helwani-ICASSP2023.txt.
- **pinn-virtual-sensing.md**: full rewrite from stub. Zhang 2023 as canonical primary (8-mic sphere, 300/400/500 Hz tones, MCFxLMS on virtual error signals, -13 dB vs multi-point). Added sections for Point Neuron Learning (Bi 2024), permutation-invariant deep-set PINN (Chen 2025), volumetric time-domain speech PINN (Olivieri 2024), Borrel 2021 historical, Koyama 2024 survey. 6 sources cited.
- **meta-learning-anc.md**: added 3-paper comparison table; Feng & So 2024 section (attention-RNN gradient predictor, delayless subband with downsampling D, loudspeaker saturation in training distribution); Xiao 2025 MAML-SFANC with ResNet classifier section; Yang 2026 co-init cross-reference. Removed Sources-pending stub. sources: 4 files.
- **neural-secondary-path.md**: removed stub banner. Added Yang 2026 co-init as category 2 (meta-learned FIR initialization preserving classical runtime algorithm — clearest conservative-deployment story). Original Deep ANC implicit approach retained as category 1. Pure online neural ID and generative priors remain stubs. sources: now includes MetaLearning-CoInit.
- **deep-anc-crn.md**: added Dai 2026 speech-preserving reverberant follow-up section (ISM-based reverberant training, selective-retention speech-preservation loss, CSM complex-spectrum mapping, PESQ/STOI evaluation). sources: 2 files.
- **deep-rl-anc.md**: downgraded from pure [stub] to [partial stub]. Added GFANC-as-contrast section explicitly distinguishing "classifier over filters" from a true RL policy; added Agyei 2025 DRL-in-control survey as background-only reference (no ANC content). The core design prospectus for genuine DRL-ANC remains aspirational — no primary source yet.
- **index.md**: updated concept-section blurbs to reflect promoted content; removed [stub] markers from 4 pages; kept [partial stub] on deep-rl-anc. Updated date header 2026-04-14 → 2026-04-15.
- **Still pending**: pure online neural secondary-path identification paper, true DRL-ANC paper (PPO/SAC/TD3/TD-MPC2 applied to an acoustic plant).

## [2026-04-15] ingest+promote | DRL-ANC batch of 4 papers
- JOS downloaded GFANC-RL and Li/Wu/Bai PDFs via browser (Cloudflare blocked curl); I moved all 4 (plus the 2 previously-staged Shi 2023 review and Wang 2024 metric-learning VS) into /l/dttd/ with cleaner filenames, symlinked into ANC-Stuff/, and extracted with pdf2txt.py in parallel.
- Delegated distillation to Explore subagent (4 papers, ~1450 words total).
- **MANIFEST.md**: appended 4 rows with venue/DOI/positioning notes.
- **SUMMARIES.md**: added new "DRL-ANC Batch (2026-04-15)" section grouped by target concept page. Flagged GFANC-RL's γ=0 contextual-bandit framing as a key caveat and Li/Wu/Bai's GRPO as the earliest known head-to-head PPO-vs-DDPG-vs-DQN comparison on an ANC task. Wang 2024 clarified as NOT a PINN (cosine-similarity classifier over Moreau-style auxiliary filters). Shi 2023 review flagged as pre-dating all AI-ANC work in the wiki.
- **concepts/deep-rl-anc.md**: promoted from [partial stub] to real concept page. Added "Primary sources ingested" section with detailed GFANC-RL MDP formulation (state/action/reward/transition/γ) and the Li/Wu/Bai RL-algorithm comparison table (DQN 89.40% / DDPG 92.04% / PPO 89.36% / **GRPO 87.02%**). GRPO's periodic-prediction auxiliary module explained. The 2023 supervised GFANC section rewritten as a contrast to its 2024 RL successor. "Still missing" section updated: continuous-drive DRL remains the open frontier; Ryu-Lim-Lee 2024 DDPG paper noted as paywalled Springer.
- **concepts/neural-secondary-path.md**: added category 3 "Explicit nonlinear neural identification — Li, Wu, Bai 2025" with full MDP formulation, the 4-algorithm comparison, closed-loop ZSL-92 deployment results (6.5-8.8 dB NR), and explicit gaps. Previously-empty "explicit online neural ID" slot now filled.
- **concepts/pinn-virtual-sensing.md**: added "Non-PINN neural alternative: metric-learning selective VS" section with Wang 2024 details, "metric learning" nomenclature clarification (not a triplet loss — just cosine similarity in a learned embedding space), and a table directly contrasting Zhang 2023 PINN vs Wang 2024 metric learning across 6 axes (underlying sensor, network job, physics prior, compute, FxLMS integration, transferability).
- **concepts/ai-anc-overview.md**: added a 2023-context citation block referencing the Shi review as canonical classical-ANC survey, with a warning not to use it as an up-to-date AI-ANC source.
- **index.md**: added "DRL-ANC ingestion batch (2026-04-15)" subsection under Entities with 4 new pending stubs; deep-rl-anc.md blurb updated to reflect its promoted status (no more [partial stub]); pending-entities count 21 → 25.
- Deleted incoming-pdfs/ staging directory.

## [2026-04-15] catalog | replace 25 [pending] entity stubs with single source-papers.md catalog
- Rationale: 25 broken entity links in the published HTML build (raw/SUMMARIES.md is gitignored so its content never reached the build). Creating 25 individual entity pages was the "proper" option but would be ~25 files of mechanical transcription.
- Chose option 1: one `entities/source-papers.md` file with H2 headings keyed to the `paper-<slug>` IDs already used in index.md, so every existing link in the form `[paper-foo](entities/source-papers.md#paper-foo)` resolves via a GitHub-flavored-markdown anchor.
- Content: all 25 distilled blocks copied verbatim from raw/SUMMARIES.md plus a short intro explaining the "promote to dedicated entity page on demand" protocol. DRL-Control-Survey-2507.08196 intentionally excluded (no ANC content). Added a "Pending ingestion" section listing Morgan 1980, Burgess 1981, Ryu 2024.
- index.md: rewrote Entities section; every [paper-foo](entities/paper-foo.md) [pending] link now points at entities/source-papers.md#paper-foo. Header bumped to "Concepts: 10 · Source papers in catalog: 25" — pending-entity count retired.
- Stub promotions later: when a concept page needs deeper treatment of one paper, promote that section to its own entities/paper-<slug>.md file and leave a cross-link in the catalog.

## [2026-04-16] ingest | Classical ANC reviews batch — Kuo & Morgan 1999 + Lu et al. 2021
- PDFs: `/l/dttd/ANC-Tutorial-Review-1999-2010913102917710.pdf` (Kuo & Morgan, *Proc. IEEE* 1999) and `/l/dttd/ANC-Survey-Part1-1-s2.0-S0165168421000785-main.pdf` (Lu et al., *Signal Processing* 2021).
- Extracted via pdf2txt.py: `raw/ANC-Tutorial-Review-1999-2010913102917710.txt` (4556 lines) and `raw/ANC-Survey-Part1-1-s2.0-S0165168421000785-main.txt` (3693 lines).
- MANIFEST.md: appended 2 rows.
- SUMMARIES.md: added "Classical ANC Reviews Batch (2026-04-16)" section with dense summaries for both papers.
- entities/source-papers.md: added "Classical ANC Reviews (2026-04-16)" section with `paper-kuo-morgan-anc-tutorial-1999` and `paper-lu-anc-survey-part1-2021`.
- index.md: added "Classical ANC reviews batch (2026-04-16)" subsection under Entities; paper count 25 → 27; date bumped to 2026-04-16.
- **Kuo & Morgan 1999:** THE canonical ANC tutorial; Morgan co-derived FxLMS; covers broadband/narrowband feedforward, feedback, multichannel, online secondary-path modeling, lattice/freq-domain/subband/RLS, applications. Complements existing Widrow 1975 (LMS foundation) and Shi 2023 (modern review).
- **Lu et al. 2021:** Decade survey (2009–2020) of linear ANC; three filter families (FxLMS/FeLMS/FuLMS), 21 online secondary-path methods, and novel methods (psychoacoustic, sparse, convex combination, fractional-order, 3-D, selective ANC, distributed). Bridges Kuo & Morgan 1999 and Shi 2023 temporally. Selective ANC (Sec. 4.6) is the direct precursor to SFANC/GFANC.
- No concept-page updates needed — these are classical reference papers that strengthen the citation foundation; existing concept pages already cover the relevant algorithms.

## [2026-04-16] ingest | Lu et al. 2021 Part II — nonlinear ANC decade survey
- PDF: `/l/dttd/ANC-Survey-Part2-NonlinearSystems-2110.09672v2.pdf` (arXiv 2110.09672v2 / *Signal Processing* 181:107929, 2021)
- Extracted via pdf2txt.py: `raw/ANC-Survey-Part2-NonlinearSystems-2110.09672v2.txt` (3996 lines)
- Note: initial PDF (`ANC-Survey-Part2-NonlinearSystems-2021.pdf`) was only 1 page (a summary table image); second attempt (`2110.00531v1`) was Part I mislabeled; third attempt correct.
- MANIFEST.md: appended 1 row.
- SUMMARIES.md: added "Nonlinear ANC Survey Batch (2026-04-16)" section with dense summary covering NLANC algorithm families (Volterra, FLANN, Hammerstein, bilinear, Chebyshev/Legendre), heuristic methods (GA/PSO/BFO/BSA/FF/FWA), novel methods (spline, kernel, distributed), implementations (DSP/FPGA/VLSI), and applications (fMRI, headphones, vehicle, transformer, open-window, spatial ANC). Updated Part I cross-reference.
- entities/source-papers.md: added `paper-lu-anc-survey-part2-2021` section; updated Part I entry to cross-reference Part II.
- index.md: added entry under "Classical ANC reviews batch"; paper count 27 → 28.
- No concept-page updates needed — this is a classical-era survey; the nonlinear algorithms it covers (Volterra, FLANN, etc.) predate the AI-ANC concept pages. The paper's coverage window (2009–2020) ends before the deep-learning ANC wave.

## [2026-04-17] update+stage | tonal-periodic-anc §8 robustness; 8 free PDFs staged
- **tonal-periodic-anc.md:** added §8 "Robustness: Doppler, amplitude fluctuation, lock loss" per JOS's rooftop-specific requirement that a mis-locked tonal canceller must mute rather than radiate uncorrelated anti-sound (first-do-no-harm rule).
  - §8.1 sources of frequency drift/modulation table — VFD, mean-wind convective shift, turbulent scintillation, gust-driven FM, multi-fan BPF beating — with timescales and typical magnitudes at 118 Hz. Notes that classical Doppler is not the mechanism (source & receiver are both stationary); it's propagation through a moving turbulent medium (Ostashev & Wilson 2015).
  - §8.2 tacho-ref is immune to VFD drift but path FM/AM still requires continuous error-mic-driven adaptation.
  - §8.3 lock-loss indicators: coherence $\gamma^2_{xe}$ below threshold, residual-power ratio >1, weight-norm runaway, tacho dropout, ADC clipping, sideband dominance.
  - §8.4 graceful mute: 30-100 ms ramp of $(w_c, w_s)\to 0$, sustained good-lock window before re-engage, leaky FxLMS as continuous fail-safe bias, hard output-authority cap, independent watchdog supervisor with amp-relay cutout.
  - §8.5 AM tracking via FxNLMS; distinguish amplitude fade from lock loss by coherence.
  - Cross-reference to `paper-wise-leventhall-lf-anc` (coherence bound).
- **Pending sources block** updated with Ostashev & Wilson 2015, Kajikawa moving-source ANC literature.
- **Staged 8 free-to-download PDFs** in `incoming-pdfs/` (downloaded in parallel via curl; all verified as real PDFs with `file`):
  - tonal-periodic-anc: Kuo & Tsai APSIPA 2011 quick-review, Elliott & Nelson IEEE SPM 1993.
  - hybrid-active-passive: Galland 2005 flow-duct hybrid, Betgen & Galland 2012 hybrid liner, Guicking patents overview, Mei 2012 *Nat Commun* dark acoustic metamaterial, Ghaffarivardavagh arXiv 1801.03613 ventilated metamaterial preprint.
  - psychoacoustic-anc: Rivera, Papantoni & Zölzer ICSV25 2018 Zwicker-weighted hybrid ANC.
- **NASA NTRS download failed** (504 Gateway Timeout on 3 retries for Brooks 1989, Sutliff 1997, Sutliff 2019). Moved to "JOS to fetch by browser" list in `incoming-pdfs/README.md`.
- **`incoming-pdfs/README.md` committed** with full file→page mapping, move-and-extract bash recipe, and an expanded "Still pending — grab via Stanford proxy" list covering Kuo & Morgan 1996 book, Elliott 2001 book, Swinbanks 1973, Chaplin 1983, Bodson/Sacks/Khosla 1994, Hara 1988, Olson & May 1953, Guicking 1984 papers, Furstoss 1997, Beyene & Burdisso 1997, Fang 2006, Ma 2014, Ma & Sheng 2016, Ghaffarivardavagh 2019 final, Zwicker & Fastl book, Aures 1985, Kuo & Tsai SPL, Rees & Elliott 2004, Zhou & DeBrunner 2007, ISO 1996-2 / DIN 45681 / ISO 532-1 / ANSI S12.9 Pt 3 standards, Beranek & Vér book, Hansen-Snyder book, Tyler & Sofrin 1962, Neise 1976, Neise & Koopmann 1980, Howe 1991.
- Next: after JOS fetches remaining PDFs and moves everything into `/l/dttd/`, run `pdf2txt.py` and promote the four scaffold pages from primary sources.

## [2026-04-17] stage | Ma & Sheng 2016 Science Advances (9th free PDF)
- Delegated follow-up search for free-to-download versions of paywalled items to an Explore subagent.
- Net win: Ma, G. & Sheng, P., "Acoustic metamaterials: from local resonances to broad horizons," *Science Advances* 2:e1501595, 2016 — author-hosted copy at HKUST Sheng-group page (Sci Adv is OA by policy).
- Downloaded: `incoming-pdfs/Ma-Sheng-AcousticMetamaterials-SciAdv2016.pdf` (2.06 MB, verified real PDF).
- README.md updated: new staged row under hybrid-active-passive, and "Still pending" entry struck through.
- All other paywalled items confirmed paywalled (no legitimate open copy found for Fang 2006, Ma 2014, Ghaffarivardavagh 2019 PRB, Bodson/Sacks/Khosla 1994, Furstoss 1997, Zhou & DeBrunner 2007, Kuo & Tsai 1994, Hansen/Snyder/Qiu 2012, Rees & Elliott 2004). JOS to fetch via Stanford proxy.
- NASA NTRS download retried with longer timeouts, still returned 504 HTML stubs. Stubs deleted; NTRS trio remains on "JOS to fetch by browser" list.

## [2026-04-17] create | 4 rooftop-fan ANC scaffold pages
- Context: JOS asked whether the wiki was missing major contenders for data-center rooftop fan noise reduction (primary concern ~118 Hz BPF). Identified four topic gaps and created scaffold concept pages (sources: [] to be filled as primary literature is ingested).
- New pages under concepts/:
  - `tonal-periodic-anc.md` — BPF-tonal ANC: tacho-referenced synchronous reference generation, single-frequency FxLMS-SF, adaptive notch, Internal-Model Principle / Repetitive Control / ILC, harmonic ANC (BPF + k·BPF), AI-era extensions (meta-learning, RL, selective).
  - `hybrid-active-passive.md` — Active impedance control (Olson 1953, Guicking), hybrid active duct liners (Beyene/Burdisso, Furstoss), tunable / piezo-coupled metamaterials (Fang/Mei/Ma lineage), semi-active Helmholtz. Motivation: passive λ/4 ≈ 0.7 m at 118 Hz vs thin active layer.
  - `psychoacoustic-anc.md` — Tonality and loudness cost functions: ISO 1996-2 $K_T$, DIN 45681, ANSI S12.9 Pt 3, Zwicker loudness, Aures sharpness, roughness. Tonal-to-broadband reshaping. Differentiable perceptual losses for deep ANC.
  - `rooftop-fan-contenders.md` — Explicit **out-of-scope pointer page**: source mods (uneven blade spacing, sweep, serrations), operational (staggered RPM, Abali 2007 phasing), passive (Helmholtz arrays, membrane AMs, metamaterials), silencers, distance/siting, receiver-side mitigation. Cross-linked to all four new in-scope pages and the existing Abali/Guerci entity entries.
- SCHEMA.md taxonomy updated: added tags `hybrid-passive`, `tonal`, `repetitive-control` (Core ANC) and `fan-noise`, `psychoacoustic`, `passive` (Applications).
- index.md: new subsection "Rooftop-fan / tonal ANC (project focus — scaffolds)" listing the 4 pages above; Concepts count 11 → 15; date 2026-04-16 → 2026-04-17.
- No source ingestion this pass — pages are scaffolds with "Pending sources" blocks listing the primary literature to pursue (Kuo & Morgan 1996 book, Elliott 2001, Guicking tutorial, Beyene/Burdisso 1997, Furstoss 1997, Ma & Sheng 2016 Science Adv., Zwicker & Fastl textbook, Beranek & Vér, Neise 1980, Ghaffarivardavagh 2019, etc.).

## [2026-04-16] create | concepts/classical-anc-overview.md
- New concept page: companion to ai-anc-overview.md covering all classical (non-AI) ANC methods.
- Organizing axis: what type of model sits in the control path (linear FIR/IIR, nonlinear expansion, heuristic optimizer).
- Sections: control topologies (feedforward/feedback/hybrid), linear algorithms (FxLMS family + FeLMS + FuLMS + lattice/convex/sparse/fractional), secondary-path modeling (21 methods), NLANC algorithms (Volterra, FLANN, Hammerstein, orthogonal polynomials, bilinear, spline, KAF), heuristic optimization (GA/PSO/BSA/BFO/FF/FWA), distributed ANC, novel 2010s methods (selective ANC, psychoacoustic, 3-D ZoQ, IoT), applications (10 domains), hardware implementations (DSP/FPGA/VLSI), open challenges.
- Sources: all four ingested survey papers (Kuo & Morgan 1999, Lu Part I 2021, Lu Part II 2021, Shi 2023).
- Index updated: Concepts 10 → 11; new entry at top of "Classical adaptive filtering" section.
- Wikilinks: links to ai-anc-overview, lms-algorithm, fxlms-algorithm, neural-secondary-path, deep-rl-anc (≥2 outbound links satisfied).

## [2026-04-17] ingest+promote | Classical ANC & hybrid-absorber batch of 9 papers
- JOS moved the 10 staged PDFs from `incoming-pdfs/` into `/l/dttd/` and symlinked into `/l/dttd/ANC-Stuff/`. On extraction, `Sutliff-AdvancedNoiseControlFan-20yrRetro-NASA-2019.pdf` turned out to be a 504 Gateway Time-out HTML error page (NTRS endpoint failed again, curl wrote the error body under the .pdf name); removed the bogus file, its symlink, and its empty .txt extraction. All three NASA NTRS items (Brooks 1989, Sutliff 1997, Sutliff 2019) remain pending — updated pending blocks accordingly.
- Extracted the remaining 9 PDFs via pdf2txt.py (431–10363 lines each).
- **Filename corrections made visible in MANIFEST + catalog:**
  - `Kuo-Tsai-FxLMS-QuickReview-APSIPA2011.pdf` is actually **Ardekani & Abdulla** (University of Auckland, APSIPA 2011). Staged README had wrong author attribution. Slug used: `paper-ardekani-fxlms-quickreview`.
  - `Ghaffarivardavagh-VentilatedMetamaterial-arxiv1801.03613.pdf` is actually **Wu, Au-Yeung et al. 2018** (HKUST/Chongqing/HKU). arXiv 1801.03613 resolves to Wu et al.; Ghaffarivardavagh 2019 *Phys. Rev. B* is the better-known canonical reference for the ultra-open silencer family. Slug used: `paper-wu-ventilated-metamaterial-2018`. Ghaffarivardavagh 2019 remains pending.
- **MANIFEST.md:** appended 9 rows with author/venue notes + the two filename-vs-authors caveats highlighted inline.
- **SUMMARIES.md:** added "Classical ANC & Hybrid-Absorber Ingestion Batch (2026-04-17)" section with 9 dense blocks. Pending-ingestion block updated to flag the NASA NTRS trio.
- **entities/source-papers.md:** added "Classical ANC & Hybrid Absorbers (2026-04-17 batch)" section with 9 paper entries; Pending-ingestion section expanded to include the NASA NTRS trio with explicit note on the Sutliff 504 artifact.
- **concepts/tonal-periodic-anc.md:** scaffold banner removed; sources: list populated with Elliott-Nelson 1993, Ardekani-Abdulla 2011, Widrow 1975, Wise-Leventhall 2010. Intro rewritten to cite Elliott-Nelson + Ardekani-Abdulla. §3 (FxLMS-SF / adaptive notch) augmented with the Ardekani-Abdulla exact-sinusoidal-input convergence result and the Elliott-Nelson ±0.6 dB / ±5° precision benchmark. New "Sources ingested" section; "Pending sources" retained but narrowed. Two named footnotes added.
- **concepts/hybrid-active-passive.md:** scaffold banner removed; sources: list populated with Galland 2005, Betgen 2012, Guicking 2009, Mei 2012, Wu 2018, Ma-Sheng 2016. §1 (active impedance control) expanded with Guicking patents context + Galland/Betgen reference. §2 rewritten as the canonical 5-step Galland design procedure with basic-vs-complex cell details, LDV grazing-flow result, and TL<20 dB ceiling. §3 (metamaterials) rewritten with Ma-Sheng 2016 as citation hub, Mei 2012 as fixed-tuned milestone, Wu 2018 as ventilated variant (flagged the Ghaffarivardavagh filename mismatch). New "Sources ingested" section; Pending-sources retained for Olson 1953, Beyene 1997, Furstoss 1997, Fang 2006, Ma 2014, Ghaffarivardavagh 2019 PRB. Six named footnotes added.
- **concepts/psychoacoustic-anc.md:** scaffold banner removed; sources: Rivera-Zoelzer 2018. New §5 "Primary source: Rivera Benois, Papantoni & Zölzer 2018" added — FeLMS-psy + MVC architecture details, closed-form transfer function, FPGA implementation, Zwicker/Aures numeric results (loudness 11.06 sone, roughness 0.13 asper, pleasantness 0.140), 6300 Hz artifact note, leaky-FeLMS + online $\hat S$ re-estimation remediation. §6 "AI-era" and §7 "Why this matters for rooftop fans" renumbered. One named footnote added.
- **concepts/rooftop-fan-contenders.md:** unchanged — remains a scaffold pending the NASA NTRS trio.
- **index.md:** Source-papers count 28 → 37; new "Classical ANC & hybrid-absorber batch (2026-04-17)" subsection under Entities, grouped by target concept page (tonal-periodic / hybrid-active-passive / psychoacoustic-anc). Rooftop-fan section heading renamed from "(project focus — scaffolds)" to "(project focus)" since 3 of 4 pages are now promoted; scaffold marker kept only on `rooftop-fan-contenders`. Pending-ingestion block expanded with NASA NTRS trio.
- Deleted `incoming-pdfs/` staging directory (PDFs live in `/l/dttd/`, README served its git-history role).
- JOS's personal working doc `REFERENCES_WE_STILL_WANT.md` was in the staging dir (untracked) — moved to `active_absorbers/REFERENCES_WE_STILL_WANT.md` so it survives the staging-dir deletion; emacs `.md~` backup discarded.

## [2026-04-17] create | pending-sources.md — consolidated wishlist
- Moved JOS's `incoming-pdfs/REFERENCES_WE_STILL_WANT.md` (which was about to be nuked with the staging dir) to a permanent home at top-level `pending-sources.md`.
- Added SCHEMA-compliant frontmatter (type: summary; tags: reference, anc), wikilinks to each target concept page (tonal-periodic-anc, hybrid-active-passive, psychoacoustic-anc, rooftop-fan-contenders, fxlms-algorithm, deep-rl-anc), and a self-contained "how to contribute a PDF" bash recipe (since incoming-pdfs/README is gone).
- Updated `index.md` "Pending ingestion" block to a one-line pointer at pending-sources.md (absorbs Morgan 1980, Burgess 1981, Ryu/Lim/Lee 2024, NASA NTRS trio, plus the scaffold-page shopping lists previously only tracked inside each scaffold page's "Pending sources" block).
- Saved just in time — the other-terminal ingestion agent deleted `incoming-pdfs/` shortly after.
- Dedup: deleted `REFERENCES_WE_STILL_WANT.md` (other agent's rescue copy of JOS's plain-text list); `pending-sources.md` is the canonical wiki form (frontmatter, wikilinks, index.md pointer).

## [2026-04-17] rename | fix two misfiled PDFs to correct author attributions
- **`Kuo-Tsai-FxLMS-QuickReview-APSIPA2011.pdf` → `Ardekani-Abdulla-FxLMS-QuickReview-APSIPA2011.pdf`** — actual authors are Iman Tabatabaei Ardekani & Waleed H. Abdulla (Univ. of Auckland); original staging README misattributed. Renamed PDF in `/l/dttd/`, recreated `/l/dttd/ANC-Stuff/` symlink to the new name, renamed `raw/*.txt` extraction.
- **`Ghaffarivardavagh-VentilatedMetamaterial-arxiv1801.03613.pdf` → `Wu-VentilatedMetamaterial-arxiv1801.03613.pdf`** — arXiv 1801.03613 is actually Wu, Au-Yeung et al. 2018 (HKUST/Chongqing/HKU); Ghaffarivardavagh's 2019 *Phys. Rev. B* ultra-open silencer is a closely-related but distinct paper that remains pending. Same rename procedure.
- Reference updates:
  - `raw/MANIFEST.md` — both rows updated; kept "Renamed 2026-04-17 from `<old>`" notes inline for history.
  - `raw/SUMMARIES.md` — both "File:" lines updated; "Filename caveat" blocks rewritten as "Filename history" with the rename note.
  - `entities/source-papers.md` — both paper sections updated (File: path + Filename history note).
  - `concepts/tonal-periodic-anc.md` — frontmatter `sources:` list + footnote cleaned (removed "misfiled as Kuo-Tsai" aside; real filename in use).
  - `concepts/hybrid-active-passive.md` — frontmatter `sources:` list + §3 Wu 2018 bullet simplified (parenthetical about the mismatch removed now that filename matches authorship); §Pending sources entry for Ghaffarivardavagh 2019 reworded to reflect it's a distinct paper, not just "the published version" of Wu 2018.
  - `index.md` — removed "(staged as Kuo-Tsai)" / "(staged as Ghaffarivardavagh)" annotations from the 2026-04-17 batch entries.
- Paper slugs (`paper-ardekani-fxlms-quickreview`, `paper-wu-ventilated-metamaterial-2018`) unchanged — they already reflect the correct authors.
- Left `log.md` historical entries verbatim (original attributions in earlier 2026-04-17 entries preserved — renaming is documented here, not retroactively in prior log entries).

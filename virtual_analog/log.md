# Activity Log

## [2026-09-08] create | virtual_analog sub-wiki scaffold + DAFx26 pass-1 ingestion
- Created SCHEMA.md (domain, 32k context budget, LaTeX math rule, frontmatter spec, VA tag taxonomy), index.md, log.md, and entities/ concepts/ comparisons/ queries/ raw/.
- Rationale: VA filters, ADAA, oscillators and neural VA are not waveguide material, so they get their own wiki; wave digital filters stay in waveguide_synthesis (wdf-* pages) and are cross-linked, not duplicated.
- Added virtual_analog to the "Active Wikis" list in ~/wiki/README.md and to SUBWIKIS in ~/wiki/Makefile.
- Ingested 16 DAFx26 sources (pass 1, catalog only) from /l/dttd/DAFx26/:
  paper_28 (McClellan, time-varying VA filter stability), paper_29 (Oyama, Moog ladder nonlinearity),
  paper_31 (Zea & Rivera, adaptive multi-rate QP), paper_47 (Gabrielli & Squartini, PolyADAA),
  paper_45 (Fontana et al., allpass clipping prevention), paper_26 (Kallinen et al., deep regularized RNNs),
  paper_27 (Massi et al., Fourier neural operators), paper_30 (Thompson & Heilemann, compressor control voltage),
  paper_49 (Roth et al., alias-free oscillator sync), paper_32 (Argentieri & Scagliola, arbitrary polygon oscillator),
  paper_37 (Tabata et al., FM parameter estimation), paper_33 (Braun & Finkelstein, FM shared embeddings),
  paper_16 (Balasubramaniam et al., Apple Silicon benchmarks), paper_18 (Huang et al., Snapdragon iGPU benchmarks),
  demo_67 (Sato & Silverstein, WaveNet pruning for iOS), demo_60 (Dittmar et al., pulsetable synthesis).
- Created entities/source-papers.md with those 16 catalog entries plus cross-reference-only entries for the three DAFx26 WDF papers (paper_23, paper_24, paper_25) that live in waveguide_synthesis.
- Created concepts/virtual-analog-overview.md (98 lines) orienting the method families.
- Copied the 16 text extractions into raw/ (gitignored) and wrote raw/MANIFEST.md and raw/SUMMARIES.md.
- Pass 2 (deep distillation of the three-star papers into dedicated concept pages) is pending.

# Projects Wiki — Log

## 2026-04-10
- Created projects wiki with SCHEMA.md, index.md, project-state.md, decisions-log.md
- Motivation: cross-agent shared state inspired by Alex Finn's Obsidian memory layers
- Added modal-synthesis-wiki as active project (14 pages, ongoing)
- Updated hermes-agent status (model-switch fix, make targets, shared state)
- Added project lifecycle convention to SCHEMA.md

## 2026-09-08
- Added dafx26-wiki-ingestion to project-state.md: DAFx26 pass-1 (catalog only) ingestion of the selected papers from /l/dttd/DAFx26/ into virtual_analog (new), waveguide_synthesis, modal_synthesis and spectral_processing
- Logged the decision to create a new virtual_analog sub-wiki rather than folding VA into waveguide_synthesis
- Pass 2 (deep distillation of the three-star papers into concept pages) is pending

## 2026-09-10 - DAFx26 pass 2 complete
- Four parallel agents distilled 37 DAFx26 papers into concept pages across virtual_analog, waveguide_synthesis, modal_synthesis and spectral_processing; project-state.md updated; make rebuild clean (0 errors, no broken wikilinks)

## 2026-09-16
- dafx26-wiki-ingestion: mirrored the neural/differentiable subset of DAFx26 into the Music 423 GitLab repo (/w/music423-2023): 41 PDFs, 46 source pages, 3 concept pages, cross-links; modal-synthesis export re-synced (sync-to-423gl.bash fixed for anchored wikilinks, code-span literals, cross-sub-wiki links)


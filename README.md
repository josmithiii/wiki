# LLM Wiki

Each subdirectory is an independent wiki with its own SCHEMA.md, index.md, and log.md.

## Active Wikis

- `waveguide_synthesis/` -- Digital waveguide modeling: traveling waves, scattering junctions, instrument models, reverb
- `modal_synthesis/` -- Physics-based synthesis using measured or computed modes of vibration
- `spectral_processing/` -- Spectral audio signal processing (JOS SASP book): STFT, windows, OLA/FBS, sinusoidal/SMS modeling, phase vocoder, filter banks
- `active_absorbers/` -- Active absorbers and active noise control (ANC): adaptive filters, feedforward/feedback control, active impedance, ANC headphones
- `projects/` -- Cross-agent shared project state, decisions, and coordination

## PDF ingestion convention (all wikis)

Research PDFs are **not stored in this repo**. They live on the host machine
at `/l/dttd/` and are surfaced to sub-wikis via curated symlinks in
`/l/dttd/ANC-Stuff/` (or analogous per-wiki directories). This applies
uniformly to every sub-wiki that cites papers.

Each sub-wiki has a `raw/` directory containing **text extractions** of those
PDFs, produced by `pdf2txt.py` (pdfminer.six). `raw/` is globally
`.gitignore`d — extractions are local-only and never committed. The canonical
mapping from extraction file to original PDF lives in `raw/MANIFEST.md`, and
short distillation notes per source live in `raw/SUMMARIES.md`. Both of
those markdown files *are* part of the wiki's local state but are still
gitignored along with the rest of `raw/`.

**Never use the `Read` tool on a PDF directly** — always convert with
`pdf2txt.py` first and read the `.txt` instead. This is enforced by the
[PDF convert first](~/.claude/projects/-Users-jos-wiki/memory/feedback_pdf_convert_first.md)
feedback memory.

### Staging downloaded PDFs

When an agent downloads free-to-access PDFs (e.g., from arXiv or
author-hosted copies) on JOS's behalf, the canonical staging location is
`<wiki>/incoming-pdfs/` inside the relevant sub-wiki. Rules for staging:

- Include an `incoming-pdfs/README.md` mapping each filename to its source
  URL **and** to the concept/entity page it feeds. This README *is*
  committed; the PDFs themselves are not.
- Binary PDFs in `incoming-pdfs/` must not be added to git. Treat them as
  the same class as `raw/` contents.
- JOS moves files from `incoming-pdfs/` into `/l/dttd/`, creates symlinks
  into the curated per-wiki subdirectory, runs `pdf2txt.py` to populate
  `raw/`, and then deletes the `incoming-pdfs/` staging directory.
- Agents may pre-stage, but must not push binaries, rename files after
  staging (the README maps by filename), or delete other agents' staging
  directories.

### Failure modes to avoid

- Committing a PDF to git (fix: `git reset HEAD <file>` before commit; the
  PDF will appear as untracked, matching the `raw/` policy).
- Reading a PDF with the `Read` tool instead of running `pdf2txt.py`.
- Placing text extractions outside `raw/` (they will not be gitignored).
- Distilling a source into a wiki page without adding a `sources:` entry
  to that page's YAML frontmatter and a row to `raw/MANIFEST.md`.

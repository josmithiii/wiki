# Incoming PDFs — staging for /l/dttd/

Downloaded 2026-04-14 as free-to-download companions to the AI-ANC concept
pages in `../concepts/`. When JOS moves them to `/l/dttd/`, symlink each into
`/l/dttd/ANC-Stuff/`, run `pdf2txt.py` to produce the `.txt` in `../raw/`,
and append a row to `../raw/MANIFEST.md`. Then remove this directory.

| File | Source URL | Feeds wiki page |
| --- | --- | --- |
| `NNSI-Helwani-ICASSP2023.pdf` | https://cdn.amazon.science/52/76/a228a6534068937d7c29ad478ac0/generative-modeling-based-manifold-learning-for-adaptive-filtering-guidance.pdf | `concepts/neural-system-identification.md` (parent NNSI framework — Helwani, Smaragdis, Goodwin, ICASSP 2023) |
| `PINN-ANC-Zhang-2309.10605.pdf` | https://arxiv.org/pdf/2309.10605 | `concepts/pinn-virtual-sensing.md` (**canonical PINN-for-ANC** — Zhang, Ma, Abhayapala et al. 2023, mics outside ROI, Helmholtz-constrained interpolation + FxLMS) |
| `PINN-SoundField-Survey-2408.14731.pdf` | https://arxiv.org/pdf/2408.14731 | `concepts/pinn-virtual-sensing.md` (invited SPM survey on physics-informed ML for sound-field estimation) |
| `PINN-Volumetric-2403.09524.pdf` | https://arxiv.org/pdf/2403.09524 | `concepts/pinn-virtual-sensing.md` (volumetric sound-field reconstruction of speech signals) |
| `PINN-1D-ParamSources-2109.11313.pdf` | https://arxiv.org/pdf/2109.11313 | `concepts/pinn-virtual-sensing.md` (1-D sound field with parameterized sources + impedance boundaries — early PINN-acoustics paper) |
| `PINN-PermutationInvariant-2601.19491.pdf` | https://arxiv.org/pdf/2601.19491 | `concepts/pinn-virtual-sensing.md` (permutation-invariant PINN for region-to-region reconstruction) |
| `PINN-PointNeuron-2408.16969.pdf` | https://arxiv.org/pdf/2408.16969 | `concepts/pinn-virtual-sensing.md` (Point Neuron Learning — embeds wave-equation fundamental solution directly) |
| `MetaLearning-DelaylessSubband-2412.19471.pdf` | https://arxiv.org/pdf/2412.19471 | `concepts/meta-learning-anc.md` (**strongest match to Sarkar et al. ref [5]** — Luo et al., complex self-attention RNN as learned gradient predictor) |
| `MetaLearning-SFANC-ResNet-2504.19173.pdf` | https://arxiv.org/pdf/2504.19173 | `concepts/meta-learning-anc.md` (Shi et al., meta-learning SFANC with ResNet classifier, MAML variant) |
| `MetaLearning-CoInit-2601.13849.pdf` | https://arxiv.org/pdf/2601.13849 | `concepts/meta-learning-anc.md` **and** `concepts/neural-secondary-path.md` (joint meta-init of control filter and secondary-path model — relevant to both pages) |
| `DeepANC-SpeechPreserving-Reverberant-2604.10979.pdf` | https://arxiv.org/pdf/2604.10979 | `concepts/deep-anc-crn.md` (follow-up to Zhang & Wang; speech-preserving Deep ANC in reverberant environments) |
| `GFANC-Luo-2303.05788.pdf` | https://arxiv.org/pdf/2303.05788 | `concepts/deep-rl-anc.md` (Deep Generative Fixed-filter ANC — closest "policy over filters" paper to a DRL-ANC framing; not strictly PPO/SAC) |
| `DRL-Control-Survey-2507.08196.pdf` | https://arxiv.org/pdf/2507.08196 | `concepts/deep-rl-anc.md` (general DRL-in-applied-control survey: DDPG/TD3/PPO/TD-MPC2 on benchmark + real systems — background reference only, no direct ANC content) |

## Still paywalled (not in this directory)

- **Morgan 1980** — IEEE TASSP 28(4) — 10.1109/TASSP.1980.1163430 — primary FxLMS source, cited by `concepts/fxlms-algorithm.md`.
- **Burgess 1981** — JASA 70(3) — 10.1121/1.386908 — primary duct-ANC source, cited by `concepts/fxlms-algorithm.md`.

Secondary-source fallback for both: Kuo & Morgan, *Active Noise Control Systems*,
Wiley 1996; Elliott, *Signal Processing for Active Control*, Academic Press 2001.

## Suggested move + ingest procedure

```bash
# from this directory
mv *.pdf /l/dttd/
cd /l/dttd/ANC-Stuff/
for f in NNSI-Helwani-ICASSP2023.pdf PINN-ANC-Zhang-2309.10605.pdf \
         PINN-SoundField-Survey-2408.14731.pdf PINN-Volumetric-2403.09524.pdf \
         PINN-1D-ParamSources-2109.11313.pdf PINN-PermutationInvariant-2601.19491.pdf \
         PINN-PointNeuron-2408.16969.pdf MetaLearning-DelaylessSubband-2412.19471.pdf \
         MetaLearning-SFANC-ResNet-2504.19173.pdf MetaLearning-CoInit-2601.13849.pdf \
         DeepANC-SpeechPreserving-Reverberant-2604.10979.pdf GFANC-Luo-2303.05788.pdf \
         DRL-Control-Survey-2507.08196.pdf; do
  ln -s ../$f .
  pdf2txt.py -o ~/wiki/active_absorbers/raw/${f%.pdf}.txt ../$f
done
# then: append rows to ../raw/MANIFEST.md and update ../raw/SUMMARIES.md + index.md
# finally: rm -r ~/wiki/active_absorbers/incoming-pdfs
```

Tell Claude "ingest the incoming-pdfs batch" and I'll run `pdf2txt.py`,
distill each into `raw/SUMMARIES.md`, promote the three stub concept pages
(`pinn-virtual-sensing`, `meta-learning-anc`, `neural-secondary-path`) from
stubs to real pages, and update `index.md` + `log.md`.

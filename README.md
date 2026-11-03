# Phage–Antibiotic Coevolution (exploratory mathematical model)

**Status: conceptual proof of concept, not validated against experiments. Not for clinical decisions or laboratory protocol design.**

An abstract, dimensionless two-bacterial-strategy / two-phage-strategy evolutionary game. Adjustable antibiotic exposure, replication-output proxy, mutation transitions, and mechanism weights from 0 to 1. `simple` and `extended` configurations share a common core. All parameter values are illustrative and **must not be interpreted as organism-specific**.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run.py
python -m pytest -q
```

The two CSV outputs contain frequencies, mean susceptibility and exposure. A higher mean susceptibility means a lower resistant share *in this stylized two-type model*, not a clinical outcome.

## Initial verification (synthetic)

- Four automated tests passed on 2026-11-04.
- Simple scenario final mean susceptibility: **0.58171**
- Extended scenario final mean susceptibility: **0.60984**

These are **illustrative calculations**, not empirical findings. Run `python run.py` to regenerate the full trajectories in `results/`.

## Limitations

The `burst` parameter enters as a saturating proxy in phage payoff; it is **not** an absolute count of phage progeny or a physical population equation. Mutation parameters are phenotype transition rates, not per-base mutation probabilities. No genomes, real pathogens, infections, biofilm, immunity, HGT, spatial gradients, pharmacokinetics or population bottlenecks are simulated. These remain proposed extensions, not implemented toggles. No model calibration or empirical validation has been performed. Do not extrapolate results to clinical settings.

## Authorship and transparency

Research concept and direction: project owner. Model drafting and software assistance: OpenAI ChatGPT (AI tool, not a human co-author). Contributors and external reviewers welcome after publication.

## Feedback

Open an issue with model assumptions, test failures, reproducible synthetic comparisons or references to published aggregate data. Do not upload identifiable patient data.

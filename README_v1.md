# Phage–Antibiotic Coevolution: v1.0 exploratory release

**Research software, not a validated clinical, experimental, or dosing predictor.**

This release adds a six-state bacterial population (S/I/R antibiotic phenotype × F+/F− phage phenotype) coupled to two independent free-phage populations. A host-range matrix and a species/strain-specific bacterial defense matrix independently modify infection. A further bacterial independent-resistance vector can be varied separately. A single `free_phage_loss` coefficient (0–1 per simulation step) aggregates natural and non-natural loss; it is not inferred from experiments.

Every declared mechanism has an independent **model switch** in [0,1]: phage, defense, independent resistance, biofilm, immunity, horizontal gene transfer (HGT), epistasis, metabolic cost, bottleneck, mutation and antibiotic. These are interpolation weights, **not biological probabilities**. Experimentalists must supply and validate coefficients. The defaults are artificial numerical illustrations, not parameter estimates.

## Reproduce

```bash
python -m pip install numpy pytest
python -m pytest -q test_v1.py
python run_v1.py
```

The script writes `results_v1.csv` with eight illustrative scenarios (no therapy, phage-only, antibiotic-only and combinations). This is a synthetic smoke test, not a biological validation or therapy comparison.

## Core update and limitations

- Infection probability: `1 - exp(-sum_j pressure_ij)` where pressure is a function of phage population, adsorption proxy, host range, bacterial defense, independent resistance, biofilm and epistasis.
- Infection counts are bounded by bacterial counts and available free phage; infected bacteria are removed and burst output added to the corresponding free-phage pool.
- Surviving bacteria undergo abstract density-limited growth, antibiotic-associated attenuation, column-stochastic HGT/mutation transitions and a bottleneck multiplier.
- Free phage is depleted by infection, aggregate environmental loss and optional immune pressure.
- All quantities are dimensionless. Time steps are not seconds or generations; antibiotic input is **not molarity or a clinical dose**. The simulation does not establish phage–antibiotic synergy, antagonism, PK/PD, host immunity kinetics, biofilm spatial structure, gene transfer biology or treatment efficacy.
- HGT, mutation, immunity, biofilm, epistasis and bottleneck are **simplified abstract effect operators**, not mechanistic submodels. The two phage strains are generic, not actual phage isolates.
- Calibration, uncertainty bounds, external datasets, experimental validation and safety assessment remain the responsibility of qualified investigators.

## Authorship

Concept and research direction: Altug Kuran. OpenAI ChatGPT assisted with model formulation, code drafting, testing and manuscript drafting; it is not a scientific co-author. No independent biological or clinical peer review is claimed.

## License and feedback

See repository LICENSE. Feedback is welcome through GitHub Issues, especially on falsifiable assumptions, mass-balance semantics, reproducibility, and published non-identifiable aggregate datasets. Do not upload patient data or infer clinical recommendations.
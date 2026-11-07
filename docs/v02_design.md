# v0.2 — Abstract comparison matrix

**Status:** exploratory computational prototype. No pathogen strains, genomic sequences, laboratory conditions, antimicrobial concentrations, clinical dosing, or experimental optimization instructions.

The original v0.1 model in `models/model.py` is preserved. This version adds `models/v02.py` and a reproducible 20-scenario comparison script.

## Experimental-design abstraction

Five baselines: (1) one initially compatible bacterium/phage strategy; (2) low-diversity related bacterial strategies with a single phage strategy; (3) high-diversity related strategies with a single phage strategy; (4) low diversity with a phage mixture; (5) high diversity with a phage mixture. Each is crossed with four **dimensionless** antibiotic settings: none, low, medium, high.

Diversity and antibiotic exposure are **independent axes**; higher diversity may be examined at higher exposure, but this is not confounded by default. `diversity_override="medium"` enables intermediate diversity without changing antibiotic level. `relatedness` controls an abstract mixing of a fixed compatibility matrix; it is not genetic distance and does not imply host range.

## Interpretation and limitations

All population states are **frequencies**, not absolute cell or virion counts. Antibiotic labels are illustrative coefficients, **not** doses, MICs or predicted efficacy. The fixed compatibility matrix is not inferred from relatedness and does not evolve. The phage 'cocktail' is an abstract distribution of three strategies, not a formulation. There is no phage infection cycle, resistance gene evolution, HGT, biofilm, immunity, pharmacokinetics, spatial effects, or bottleneck process. The simple mutation mixing is not per-base mutation. Mechanism weights in [0,1] switch abstract payoff contributions; they are not biological probabilities. Results cannot be used to guide clinical or laboratory decisions.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run_v02.py
python -m pytest -q
```

Output: `results/v02_summary.csv`, containing final abstract indices from all 20 scenarios. No biological claims follow from differences in these indices.

## Next phase

1. Check numerical convergence and seed sensitivity.
2. Add separate synthetic control comparisons that isolate diversity and antibiotic exposure.
3. Review assumptions with domain experts before considering empirical aggregate data.
4. Document limitations and failure cases; preserve neutral results.

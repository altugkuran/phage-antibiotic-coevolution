# v0.4 design — Mathematical core and researcher layer

**Status:** conceptual specification only. No v0.4 implementation or experimental validation yet. The existing v0.1–v0.3 files are preserved. This project is not a clinical predictor or laboratory protocol.

## Confirmed principles

1. Keep bacterial and phage **absolute counts**, **densities** and **relative frequencies** conceptually distinct. A frequency-only model cannot infer absolute abundance.
2. Distinguish antibiotic **mol/L**, **mg/L** and **MIC-normalized** representations. Conversions require substance identity, molecular mass, and an appropriate susceptibility reference. Numeric inputs are not meaningful efficacy predictions without calibration.
3. Every evidence-based parameter should record its source, measurement method, units, uncertainty, and applicable context.
4. Permit user-defined hypothetical parameters as well as literature-derived ones. Label each as measured, literature-derived, inferred, or hypothetical. Researchers retain freedom to explore assumptions; unverified assumptions must never be reported as empirical results.
5. Treat external mutagenic chemicals, added high-energy ionizing radiation, and other uncontrolled environmental mutagens as **outside the baseline model**. This does not imply zero background mutation or zero naturally occurring DNA damage. Antibiotic-associated stress effects must not be confused with external mutagens.
6. Genetic relatedness and phage-host compatibility are separate variables; neither determines the other.
7. Every optional mechanism has an independently documented weight in [0,1]. These weights scale model contributions and **are not biological probabilities**. Setting a weight to zero must remove all pathways of that mechanism, not merely one payoff term.
8. Antibiotic exposure and initial bacterial diversity are independent scenario axes, including in high-exposure comparisons.
9. The 3-of-5 agreement heuristic is an exploratory screen only. Define an outcome metric and tolerance in advance; assess convergence, sensitivity, uncertainty, and independent repeatability before making stronger claims.

## Core model: conceptual decomposition

The next mathematical revision should separate:
- **State representation:** absolute abundance versus normalized frequencies, with explicit reference volume for densities.
- **Selection and mutation:** distinguish deterministic selection from stochastic drift; neutral, harmful, and beneficial changes are not assumed to have equal effects.
- **Interactions:** an independently specified compatibility matrix and explicit distinction between adsorption/attachment and successful infection.
- **Antibiotic representation:** external exposure as a time-dependent input, separate from drug response and bacterial susceptibility.
- **Optional mechanisms:** cost, trade-off, epistasis, spatial effects, immunity, biofilm, horizontal transfer, and bottlenecks, each separately documented and gated.
- **Observation layer:** distinguish model latent states from measurable quantities and report uncertainty.

No real pathogen-specific infection kinetics, drug concentrations, irradiation conditions, experimental cultivation settings or optimization procedures are prescribed here.

## Researcher layer

Record inputs in a machine-readable schema with:
`parameter_name`, `value`, `unit`, `source_type`, `source_reference`, `measurement_method`, `uncertainty`, `notes`.
Support both literature-grounded and clearly labeled hypothetical values.
Include a list of omitted environmental factors in each generated report.

## Validation roadmap

1. Review dimensional consistency and identifiability before connecting physical units to dynamics.
2. Establish invariants and numerical convergence tests.
3. Run independent sensitivity analysis for antibiotic exposure, diversity, compatibility and mechanism weights.
4. Evaluate repeatability across independent random seeds, with predeclared metrics.
5. Compare predictions against appropriately licensed published aggregate evidence only after the model's observation layer is defined.
6. Invite independent microbiology and mathematical-modeling review under appropriate biosafety and institutional oversight.

## Version status

- **v0.1:** two-strategy abstract frequency game.
- **v0.2:** three-strategy, twenty-scenario abstract frequency comparison.
- **v0.3:** numeric counts/molarity accepted as **metadata**, not active dynamics; exploratory repeatability screen.
- **v0.4:** this design document; mathematical implementation pending.

## Next decision

Prioritize a **dimensionally coherent mathematical state specification** and independent validation of its assumptions. Do not treat a numeric count or molar input as calibrated simply because it carries a physical unit.

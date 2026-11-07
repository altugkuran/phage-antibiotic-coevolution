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


## Approved six-state intersection specification (design, not implemented)

Antibiotic response is partitioned into three **mutually exclusive operational states** for a given drug, exposure and measurement context: susceptible (S), intermediate/transition (I), resistant (R). The proposed small overlap of susceptible and resistant sets is represented by **I**, not by counting the same cell twice. The transition state is a modeling abstraction; its interpretation (intermediate susceptibility, heterogeneous response, or an uncertain phenotype) must be documented and not conflated with a particular clinical breakpoint.

For a **specified phage–host pairing**, define F+ (susceptible to productive phage infection under model assumptions) and F− (not productively infected). The six bacterial compartments are:
`B_S,F+`, `B_S,F−`, `B_I,F+`, `B_I,F−`, `B_R,F+`, `B_R,F−`.
These six categories are disjoint and their populations sum to the total bacterial population. F+ / F− is **pair-specific**, not an intrinsic global property of a phage or bacterium. Binding, productive infection and phage replication must remain conceptually distinct.

**Reference initial condition:** bacteria numerically predominate over phages; antibiotic-resistant bacterial variants are already present; the mutation process is not presumed negligible. Initial abundance, resistance distribution, mutation assumptions and uncertainty ranges remain researcher-configurable. Pre-existing resistance **does not imply** a high mutation rate. Phage abundance can be uncertain; rapid increase is possible only conditional on compatible hosts and productive replication.

## Transition catalog and interpretation

| User case | Conceptual model transition | Interpretation and qualification |
|---|---|---|
| 1.1 | R ↔ I ↔ S without antibiotic | Resistance loss or selection of susceptible variants; not guaranteed |
| 1.2 | S ↔ I ↔ R with antibiotic | Genetic change, transfer, or differential selection; do not equate selection with individual transformation |
| 2.1, 2.2 | Productively infecting phage variants ↔ nonproductive variants | May arise under either antibiotic condition; distinguish particle defect from host mismatch |
| 3.1, 3.2 | R ↔ I ↔ S with antibiotic and phage | Both directions permitted as hypotheses; no predetermined favorable outcome |
| 4.1, 4.2 | Phage infectivity phenotype may change in either direction | Requires an explicit mechanism; genes do not spontaneously become phage particles |
| 5.1 | Phage-associated horizontal gene transfer may change bacterial traits | Optional and separately gated; not presumed to occur in every system |
| 5.2 | Phage → bacterium | **Excluded**: viruses do not transform into bacteria. If intended as phage-mediated trait transfer, it belongs under 5.1 |
| 6.1, 6.3 | Emergence of bacterial/phage variants with uncharacterized effects | Mark **uncertain**, not neutral; do not assume zero effect |

The six bacterial compartments are **phenotypic states**; new genetic variants may exist within each compartment and need not be a new species. Antibiotic-resistant bacteria need not be completely unaffected by antibiotic exposure.

## Uncertain outcomes: explicit treatment

Use the status **uncertain** (`belirsiz`) for uncharacterized effects. Do **not** automatically assign zero selection effect, a beneficial effect, or a harmful effect. Keep an explicit `unknown` marker, document the reason, and distinguish missing knowledge from a genuinely measured neutral effect. An exploratory model may use labeled hypothetical sensitivity cases, but cannot claim that a selected value is experimentally established. No probability distribution is implied without a stated assumption and evidence.

## Conceptual state accounting and quality gates

For six nonnegative bacterial state populations `B_k(t)`, total bacteria is `N_B(t)=sum_k B_k(t)`. If `N_B>0`, frequencies are `x_k=B_k/N_B` and sum to one; when `N_B=0`, frequencies are **undefined**, not zero by fiat. Conceptually separate (a) growth/loss, (b) mutation and trait transitions, (c) antibiotic/phage selection, (d) optional transfer and environmental mechanisms. Any transition-only operator must conserve bacterial counts across the six compartments; birth/death and infection loss are accounted for separately. The phage population has its own state and is never a bacterial state.

Quality gates before a code release: nonnegative states, conservation under transition-only dynamics, no double counting in overlap, explicit handling of extinction, independent mechanism toggles, reproducibility, numerical convergence and uncertainty reporting. No mechanistic rates are asserted in this design.

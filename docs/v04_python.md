# v0.4 Python matrix engine

**Status:** abstract, synthetic and uncalibrated mathematical implementation. It is not a biological, laboratory or clinical prediction model.

Files: `models/v04.py`, `tests/test_v04.py`.

## State order

`S_Fplus, S_Fminus, I_Fplus, I_Fminus, R_Fplus, R_Fminus`.

S = susceptible to specified antibiotic; I = intermediate/transition state; R = resistant. Fplus/Fminus are defined **for a particular phage–host pairing**, not universal attributes.

## Mathematical rule

Given a six-entry nonnegative population vector `n`, a 6×6 nonnegative **column-stochastic** transition matrix `T`, and six nonnegative population multipliers `g`:

`flow[i,j] = T[i,j] * n[j]`

`moved[i] = sum_j flow[i,j]`

`next[i] = g[i] * moved[i]`

`frequency[i] = next[i] / sum(next)` if the total is positive; otherwise frequencies are undefined.

Optional `volume` yields `transition_density[i,j] = flow[i,j] / volume` in the user's count/volume units.

Transition and population effects are independent inputs; order is **transition first, multiplier second**. Transition-only operations conserve total population, but multipliers need not.

## Explicit uncertainty

All 36 matrix entries must be specified and each column must sum to 1. Missing values, NaN, negative entries and unnormalized columns are rejected. A value of zero means an **explicitly excluded transition**, not an unknown effect. For uncertain parameters, researchers should supply documented alternative matrices and compare outputs. No unknown effect is automatically assumed neutral.

## Example: software-only identity test

```python
import numpy as np
from models.v04 import step

initial = np.array([6., 5., 4., 3., 2., 1.])
transition = np.eye(6)
multipliers = np.ones(6)
result = step(initial, transition, multipliers, volume=2)
print(result.after_growth)
print(result.transition_flows)
print(result.frequencies)
```

These are synthetic software-test values, not biological parameter recommendations.

## Boundaries

No dynamic phage population, infection cycle, empirical mutation rates, drug response or pathogen-specific calibration is implemented. F+ and F− are phenotype labels in this first matrix version. A separate phage model and an observation/calibration layer would require new specifications and tests.

Run tests with `python -m pytest -q tests/test_v04.py`.

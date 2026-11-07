# Version comparison: v0.1 → v0.2 → v0.3

**All versions are exploratory and unvalidated. No clinical or laboratory use.**

| Feature | v0.1 | v0.2 | v0.3 |
|---|---|---|---|
| Main file | `models/model.py` | `models/v02.py` | `models/v03.py` |
| Mathematical state | 2 bacterial and 2 phage strategy **frequencies** | 3 bacterial and 3 phage strategy **frequencies** | v0.2 frequency engine + numeric-input interface |
| Scenario comparison | Simple / extended | 5 baseline cases × 4 abstract antibiotic settings = 20 | Replicate comparison with numeric input metadata |
| Bacterial diversity | Two fixed strategies | Low/medium/high abstract distributions | Same distributions, selected explicitly |
| Phage choice | Two-strategy mixture | Single vs abstract mixture | Same |
| Antibiotic | Dimensionless schedule | None/low/medium/high abstract exposure | User enters nonnegative mol/L **as metadata only** |
| Bacteria/phage count | Not modeled | Not modeled | Integer inputs **as metadata only** |
| Repeatability | Seeded stochastic term | Seeded stochastic term | Multiple seeds, mean/std, exploratory 3-of-5 screen |
| Real infection / birth-death | No | No | No |
| Calibrated drug response | No | No | No |
| Empirical validation | No | No | No |

## Why v0.3 is an interface milestone, not a biological simulation upgrade

The request for actual bacterial/phage counts and antibiotic molarity is captured by typed inputs, validation and reproducible outputs. However, **entering units does not create a dimensionally consistent biological model**. The current underlying v0.2 frequency game has no absolute population dynamics, volume, drug identity, pharmacodynamics, adsorption, lysis or burst equations. Consequently v0.3 deliberately does **not** feed these physical quantities into the frequency dynamics. They are recorded as metadata; changing them does not change predictions. This is tested explicitly.

The 3-of-5 check counts outcomes near the median within a user-specified absolute tolerance. It is a preliminary repeatability flag, **not** evidence of statistical significance, predictive accuracy or biological validity. Five runs alone cannot establish validity. If noise weight is zero, repeated runs are deterministic and the screen is trivial.

## Next phase

1. Test sensitivity to numerical step size, stochastic seeds and dimensionless weights.
2. Independently assess whether an absolute-population model is identifiable from published aggregate data.
3. Only after appropriate external validation, consider whether any physical units can be mapped to model variables.
4. Keep genetic relatedness separate from phage-host compatibility; never infer one from the other.

## Reproduce

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python run_v03.py --bacteria-count 100 --phage-count 50 --antibiotic-mol-per-liter 0 --replicates 5
```

The numbers in this command are **software test placeholders**, not laboratory settings or biological recommendations.

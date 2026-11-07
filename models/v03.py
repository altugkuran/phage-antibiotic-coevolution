"""v0.3 numerical-input interface for a SYNTHETIC comparison model.

Inputs use counts and an optional mol/L label, but no calibrated biological
dynamics, antibiotic efficacy, pharmacokinetics or pathogen-specific parameters.
This module must not be used for clinical or laboratory decisions.
"""
from dataclasses import dataclass
import numpy as np
from models.v02 import Scenario, simulate_v02, COLUMNS

@dataclass(frozen=True)
class Inputs:
    bacteria_count: int
    phage_count: int
    antibiotic_mol_per_liter: float
    replicates: int = 5
    diversity: str = "medium"
    phages: str = "cocktail"

def validate(inputs):
    if type(inputs.bacteria_count) is not int or inputs.bacteria_count < 0:
        raise ValueError("bacteria_count must be a nonnegative integer")
    if type(inputs.phage_count) is not int or inputs.phage_count < 0:
        raise ValueError("phage_count must be a nonnegative integer")
    if not np.isfinite(inputs.antibiotic_mol_per_liter) or inputs.antibiotic_mol_per_liter < 0:
        raise ValueError("antibiotic_mol_per_liter must be finite and nonnegative")
    if type(inputs.replicates) is not int or inputs.replicates < 1:
        raise ValueError("replicates must be a positive integer")
    if inputs.diversity not in ("low", "medium", "high"):
        raise ValueError("invalid diversity")
    if inputs.phages not in ("single", "cocktail"):
        raise ValueError("invalid phages")

def compare(inputs, seed=7, weights=None):
    """Produce repeatability diagnostics without claiming biological calibration.

    v0.2 frequency trajectories are computed independently of absolute counts
    and molarity. These values are retained as input metadata ONLY.
    """
    validate(inputs)
    s = Scenario("numeric_inputs", inputs.diversity, inputs.phages, "none")
    results = []
    for i in range(inputs.replicates):
        trajectory = simulate_v02(s, weights=weights, seed=seed+i)
        results.append({"seed": seed+i,
                        "final_mean_susceptibility": float(trajectory[-1, 7]),
                        "final_compatibility_index": float(trajectory[-1, 9])})
    vals = np.array([r["final_mean_susceptibility"] for r in results])
    return {"inputs": vars(inputs).copy(), "replicates": results,
            "mean": float(vals.mean()), "std": float(vals.std()),
            "warning": "Counts and molarity are metadata, NOT active model drivers; "
                       "results are synthetic frequency-game outputs."}

def consistency_screen(values, tolerance=0.05):
    """Descriptive screen: count values near median; not a validity test."""
    a = np.asarray(values, dtype=float)
    if a.ndim != 1 or len(a) == 0 or not np.all(np.isfinite(a)):
        raise ValueError("finite nonempty values required")
    if tolerance < 0 or not np.isfinite(tolerance):
        raise ValueError("invalid tolerance")
    median = float(np.median(a))
    matches = int(np.count_nonzero(np.abs(a - median) <= tolerance))
    return {"matches": matches, "total": len(a),
            "at_least_three_of_five": len(a) == 5 and matches >= 3,
            "note": "Exploratory repeatability screen only, not validation."}

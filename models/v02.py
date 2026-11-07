"""v0.2: abstract, dimensionless comparison engine; not a pathogen predictor.

The 'relatedness' and 'compatibility' arrays are illustrative mathematical
structures, not genome sequences or measured infection probabilities.
"""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Scenario:
    name: str
    diversity: str
    phages: str
    antibiotic: str

DIVERSITY = ("low", "medium", "high")
ANTIBIOTIC = ("none", "low", "medium", "high")
# Five baseline comparisons, crossed with four antibiotic conditions.
BASELINES = (
    ("reference", "low", "single"),
    ("low_single", "low", "single"),
    ("high_single", "high", "single"),
    ("low_cocktail", "low", "cocktail"),
    ("high_cocktail", "high", "cocktail"),
)
WEIGHT_NAMES = ("selection", "phage", "mutation", "cost", "tradeoff", "noise")

def scenarios():
    return [Scenario(n, d, p, a)
            for a in ANTIBIOTIC for n, d, p in BASELINES]

def simulate_v02(scenario, steps=200, dt=0.02, weights=None, seed=7,
                 diversity_override=None, relatedness=0.75):
    """Return abstract trajectories, with no organism- or drug-specific units.

    Antibiotic level and diversity are independently controlled. 'High'
    diversity changes the initial distribution, not an antibiotic response.
    """
    if steps < 1 or dt <= 0 or not 0 <= relatedness <= 1:
        raise ValueError("invalid numerical parameters")
    if scenario.diversity not in DIVERSITY or scenario.antibiotic not in ANTIBIOTIC:
        raise ValueError("unknown scenario category")
    if scenario.phages not in ("single", "cocktail"):
        raise ValueError("unknown phage category")
    d = diversity_override or scenario.diversity
    if d not in DIVERSITY:
        raise ValueError("invalid diversity override")
    w = dict.fromkeys(WEIGHT_NAMES, 1.0)
    w["noise"] = 0.0
    if weights:
        if set(weights) - set(w):
            raise ValueError("unknown mechanism weight")
        w.update(weights)
    if any(not np.isfinite(v) or not 0 <= v <= 1 for v in w.values()):
        raise ValueError("mechanism weights must be in [0,1]")
    rng = np.random.default_rng(seed)
    # Three abstract variants, never specific bacterial species or resistance genes.
    initial = {"low": [0.92, 0.06, 0.02],
               "medium": [0.65, 0.25, 0.10],
               "high": [0.40, 0.35, 0.25]}
    b = np.array([1., 0., 0.]) if scenario.name == "reference" else np.array(initial[d], float)
    p = np.array([1., 0., 0.]) if scenario.phages == "single" else np.array([0.40, 0.35, 0.25])
    # Fixed, illustrative compatibility matrix: relatedness does not determine host range.
    h = np.array([[0.80, 0.12, 0.08],
                  [0.10, 0.75, 0.12],
                  [0.08, 0.15, 0.70]])
    h = relatedness * h + (1.0 - relatedness) * np.full((3, 3), 0.33)
    susceptibility = np.array([0.85, 0.45, 0.20])
    exposure = dict(zip(ANTIBIOTIC, (0.0, 0.15, 0.35, 0.55)))[scenario.antibiotic]
    rows = []
    for k in range(steps + 1):
        rows.append([k * dt, *b, *p, float(b @ susceptibility), exposure,
                     float(b @ h @ p)])
        if k == steps:
            break
        # Frequency-selection game, NOT absolute birth/death, lysis, or drug kinetics.
        pressure = h @ p
        fb = 1.0 - w["selection"] * exposure * susceptibility
        fb -= w["phage"] * 0.30 * pressure
        fb -= w["cost"] * np.array([0.0, 0.04, 0.08])
        fb += w["tradeoff"] * 0.03 * (pressure - pressure.mean())
        fp = (b @ h) * w["phage"]
        db = b * (fb - b @ fb)
        dp = p * (fp - p @ fp)
        db += w["mutation"] * 0.004 * (np.roll(b, 1) + np.roll(b, -1) - 2*b)
        dp += w["mutation"] * 0.004 * (np.roll(p, 1) + np.roll(p, -1) - 2*p)
        if w["noise"]:
            db += w["noise"] * 0.01 * rng.normal(size=3)
            dp += w["noise"] * 0.01 * rng.normal(size=3)
        b = np.maximum(b + dt * db, 0)
        p = np.maximum(p + dt * dp, 0)
        b /= b.sum()
        p /= p.sum()
    return np.asarray(rows)

COLUMNS = ("time", "b1", "b2", "b3", "p1", "p2", "p3",
           "mean_susceptibility", "antibiotic_exposure", "compatibility_index")

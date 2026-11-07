"""v0.4: six-state abstract transition/population matrix engine.

Purely mathematical, synthetic and uncalibrated. Not a clinical or laboratory
prediction tool. Unknown coefficients must be specified, not silently set to 0.
"""
from dataclasses import dataclass
import numpy as np

STATES = ("S_Fplus", "S_Fminus", "I_Fplus", "I_Fminus", "R_Fplus", "R_Fminus")
N = len(STATES)

@dataclass(frozen=True)
class StepResult:
    before: np.ndarray
    transition_flows: np.ndarray
    after_transition: np.ndarray
    after_growth: np.ndarray
    frequencies: np.ndarray | None
    total: float
    transition_density: np.ndarray | None

def _finite_nonnegative(name, value, shape):
    a = np.asarray(value, dtype=float)
    if a.shape != shape or not np.all(np.isfinite(a)) or np.any(a < 0):
        raise ValueError(f"{name} must have shape {shape}, finite nonnegative entries")
    return a

def validate_transition(transition, tolerance=1e-10):
    """Column j represents fractions leaving state j, including its self-loop."""
    t = _finite_nonnegative("transition", transition, (N, N))
    if not np.allclose(t.sum(axis=0), 1.0, atol=tolerance, rtol=0):
        raise ValueError("each transition matrix column must sum to one")
    return t

def step(population, transition, multipliers, volume=None):
    """One step: transition first, then per-target-state multipliers.

    flow[i,j] = transition[i,j] * population[j].
    Density is a modeled count divided by a user-supplied reference volume.
    Missing volume leaves density undefined; missing transitions raise errors.
    """
    n = _finite_nonnegative("population", population, (N,))
    t = validate_transition(transition)
    g = _finite_nonnegative("multipliers", multipliers, (N,))
    if volume is not None and (not np.isfinite(volume) or volume <= 0):
        raise ValueError("volume must be finite and positive")
    flow = t * n[np.newaxis, :]
    moved = flow.sum(axis=1)
    result = g * moved
    total = float(result.sum())
    freq = result / total if total > 0 else None
    density = flow / volume if volume is not None else None
    return StepResult(n.copy(), flow, moved, result, freq, total, density)

def simulate(initial, transitions, multipliers, volume=None):
    """Run a sequence of independently supplied transition/multiplier pairs."""
    if len(transitions) != len(multipliers):
        raise ValueError("transitions and multipliers must have equal lengths")
    history = []
    current = _finite_nonnegative("initial", initial, (N,))
    for t, g in zip(transitions, multipliers):
        result = step(current, t, g, volume=volume)
        history.append(result)
        current = result.after_growth
    return history

def make_transition(entries):
    """Construct a 6x6 matrix from a COMPLETE 6x6 numeric array.

    No default identity, no inferred zero, no automatic normalization.
    """
    return validate_transition(entries)

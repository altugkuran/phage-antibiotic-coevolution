import numpy as np
from models.v02 import Scenario, scenarios, simulate_v02

def test_twenty_scenarios():
    s = scenarios()
    assert len(s) == 20
    assert len(set((x.name, x.antibiotic) for x in s)) == 20

def test_frequency_invariants():
    for s in scenarios():
        a = simulate_v02(s)
        assert a.shape == (201, 10)
        assert np.all(np.isfinite(a))
        assert np.all(a[:, 1:7] >= 0)
        assert np.allclose(a[:, 1:4].sum(axis=1), 1)
        assert np.allclose(a[:, 4:7].sum(axis=1), 1)

def test_antibiotic_and_diversity_independent():
    a = Scenario("low_single", "low", "single", "none")
    b = Scenario("low_single", "low", "single", "high")
    x = simulate_v02(a)
    y = simulate_v02(b)
    assert np.allclose(x[0, 1:7], y[0, 1:7])
    assert x[0, 8] != y[0, 8]
    z = simulate_v02(a, diversity_override="high")
    assert z[0, 8] == x[0, 8]
    assert not np.allclose(z[0, 1:4], x[0, 1:4])

def test_seed_and_weight_validation():
    s = scenarios()[1]
    x = simulate_v02(s, weights={"noise": 0.5}, seed=9)
    assert np.array_equal(x, simulate_v02(s, weights={"noise": 0.5}, seed=9))
    try:
        simulate_v02(s, weights={"phage": 1.1})
    except ValueError:
        pass
    else:
        raise AssertionError("invalid weight accepted")

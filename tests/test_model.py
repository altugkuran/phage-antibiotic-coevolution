import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from models.model import simulate

def test_frequencies():
    a=simulate()
    assert np.all(np.isfinite(a))
    assert np.allclose(a[:,1]+a[:,2],1)
    assert np.allclose(a[:,3]+a[:,4],1)
    assert np.all(a[:,1:5]>=0)

def test_reproducibility():
    assert np.array_equal(simulate(seed=4,weights={'noise':0.5}),simulate(seed=4,weights={'noise':0.5}))

def test_switches_change_results():
    a=simulate(weights={'phage':0})
    b=simulate(weights={'phage':1})
    assert not np.allclose(a,b)

def test_reject_bad_weights():
    try: simulate(weights={'noise':1.1})
    except ValueError: return
    raise AssertionError('bad weight accepted')

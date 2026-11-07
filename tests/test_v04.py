import numpy as np
import pytest
from models.v04 import STATES, step, simulate, make_transition

def test_identity():
    n = np.array([6.,5.,4.,3.,2.,1.])
    r = step(n,np.eye(6),np.ones(6),volume=2)
    assert np.allclose(r.after_growth,n)
    assert np.isclose(r.frequencies.sum(),1)
    assert np.isclose(r.transition_flows.sum(),n.sum())
    assert np.isclose(r.transition_density.sum(),n.sum()/2)

def test_transition_and_growth_are_separate():
    n = np.array([10.,0,0,0,0,0])
    t = np.eye(6)
    t[0,0]=0.75
    t[2,0]=0.25
    g = np.array([1.,1.,2.,1.,1.,1.])
    r = step(n,t,g)
    assert np.allclose(r.after_transition,[7.5,0,2.5,0,0,0])
    assert np.allclose(r.after_growth,[7.5,0,5,0,0,0])
    assert r.transition_flows[2,0]==2.5

def test_missing_or_invalid_coefficients_rejected():
    for bad in (np.full((6,6),np.nan), np.zeros((6,6)), np.ones((5,5))):
        with pytest.raises(ValueError):
            make_transition(bad)

def test_extinction_frequency_undefined():
    r=step(np.zeros(6),np.eye(6),np.ones(6))
    assert r.total==0 and r.frequencies is None

def test_multi_step_and_validation():
    h=simulate([1,0,0,0,0,0],[np.eye(6)]*2,[np.ones(6)]*2)
    assert len(h)==2
    with pytest.raises(ValueError):
        simulate([1]*6,[np.eye(6)],[])

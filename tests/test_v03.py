import pytest
from models.v03 import Inputs, validate, compare, consistency_screen

def test_numeric_inputs_are_metadata_not_calibration():
    a = compare(Inputs(100, 10, 0.0), weights={"noise":0.2})
    b = compare(Inputs(100000, 10000, 0.001), weights={"noise":0.2})
    assert a["replicates"] == b["replicates"]
    assert "NOT active model drivers" in a["warning"]

def test_reproducibility_and_repeat_count():
    a = compare(Inputs(100, 50, 0.0, replicates=5),weights={"noise":0.5},seed=3)
    assert a == compare(Inputs(100, 50, 0.0, replicates=5),weights={"noise":0.5},seed=3)
    assert len(a["replicates"]) == 5

def test_validation():
    for item in (Inputs(-1, 3, 0), Inputs(3, -1, 0),
                 Inputs(3, 3, -0.1), Inputs(3, 3, 0, replicates=0)):
        with pytest.raises(ValueError):
            validate(item)

def test_three_of_five_is_screen_only():
    a = consistency_screen([0.1,0.11,0.12,0.8,0.9],tolerance=0.03)
    assert a["at_least_three_of_five"]
    assert a["matches"] == 3

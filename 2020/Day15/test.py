import pytest
from day15 import *


@pytest.mark.parametrize("inp, exp", [
    ("0,3,6", 436),
    ("1,3,2", 1),
    ("2,1,3", 10),
    ("1,2,3", 27),
    ("2,3,1", 78),
    ("3,2,1", 438),
    ("3,1,2", 1836),
])
def test_one(inp, exp):
    res = part_one(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    ("0,3,6", 175594),
    ("1,3,2", 2578),
    ("2,1,3", 3544142),
    ("1,2,3", 261214),
    ("2,3,1", 6895259),
    ("3,2,1", 18),
    ("3,1,2", 362),
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


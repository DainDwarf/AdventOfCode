import pytest
from day18 import *


@pytest.mark.parametrize("inp, exp", [
    ("1 + 2 * 3 + 4 * 5 + 6", 71),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51),
    ("2 * 3 + (4 * 5)", 26),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
    ("1 + 2 * 3 + 4 * 5 + 6\n1 + (2 * 3) + (4 * (5 + 6))\n2 * 3 + (4 * 5)", 71+51+26),
])
def test_one(inp, exp):
    res = part_one(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


import pytest
from day13 import *


inp = """939
7,13,x,x,59,x,31,19"""


def test_one():
    res = part_one(inp)
    assert res == 295


@pytest.mark.parametrize("inp, exp", [
    (inp, 1068781),
    ("1\n17,x,13,19", 3417),
    ("1\n67,7,59,61", 754018),
    ("1\n67,x,7,59,61", 779210),
    ("1\n67,7,x,59,61", 1261476),
    ("1\n1789,37,47,1889", 1202161486),
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


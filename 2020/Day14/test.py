import pytest
from day14 import *


inp = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

@pytest.mark.parametrize("inp, exp", [
    (11, 73),
    (101, 101),
    (0, 64),
])
def test_mask(inp, exp):
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    assert apply_mask(mask, inp) == exp

def test_one():
    res = part_one(inp)
    assert res == 165


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


import pytest
from day14 import *


@pytest.mark.parametrize("inp, exp", [
    (11, 73),
    (101, 101),
    (0, 64),
])
def test_mask(inp, exp):
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    assert apply_mask(mask, inp) == exp


@pytest.mark.parametrize("mask, addr, exp", [
    ("000000000000000000000000000000X1001X", 42, "000000000000000000000000000000X1101X"),
    ("00000000000000000000000000000000X0XX", 26, "00000000000000000000000000000001X0XX"),
])
def test_mask_v2(mask, addr, exp):
    assert apply_mask_v2(mask, addr) == exp


@pytest.mark.parametrize("inp, exp", [
    ("000000000000000000000000000000000001", set((1,))),
    ("00000000000000000000000000000000000X", set((0, 1))),
    ("00000000000000000000000000000000001X", set((2, 3))),
    ("000000000000000000000000000000X1101X", set((26, 27, 58, 59))),
    ("00000000000000000000000000000001X0XX", set((16, 17, 18, 19, 24, 25, 26, 27))),
])
def test_x_gen(inp, exp):
    assert set(x_gen(inp)) == exp


def test_one():
    inp = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
    res = part_one(inp)
    assert res == 165


def test_two():
    inp = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
    res = part_two(inp)
    assert res == 208


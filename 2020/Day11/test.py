import pytest
from day11 import *


inp = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


def test_one():
    res = part_one(inp)
    assert res == 37


def test_two():
    res = part_two(inp)
    assert res == 26


import pytest
from day17 import *


inp=""".#.
..#
###"""


def test_one():
    res = part_one(inp)
    assert res == 112


def test_two():
    res = part_two(inp)
    assert res == 848

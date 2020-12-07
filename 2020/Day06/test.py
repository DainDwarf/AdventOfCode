import pytest
from day06 import *


inp = """abc

a
b
c

ab
ac

a
a
a
a

b"""


def test_one():
    res = part_one(inp)
    assert res == 11


def test_two():
    res = part_two(inp)
    assert res == 6

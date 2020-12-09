import pytest
from day09 import *


inp = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""


def test_one():
    res = part_one(inp, preamble=5)
    assert res == 127


def test_two():
    res = part_two(inp, preamble=5)
    assert res == 62


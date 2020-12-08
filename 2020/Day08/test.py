import pytest
from day08 import *


inp = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


def test_one():
    res = part_one(inp)
    assert res == 5


def test_two():
    res = part_two(inp)
    assert res == 8


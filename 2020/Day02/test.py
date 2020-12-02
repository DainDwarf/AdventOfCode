from day02 import *
import pytest


"""That's handy, the Advent of Code gives unittests."""


@pytest.mark.parametrize("inp, exp", [
    ("1-3 a: abcde", True),
    ("1-3 b: cdefg", False),
    ("2-9 c: ccccccccc", True),
])
def test_line_is_valid(inp, exp):
    res = line_is_valid(PasswordPolicy, inp)
    assert res == exp


def test_one():
    inp = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
    assert part_one(inp) == 2


@pytest.mark.parametrize("inp, exp", [
    ("1-3 a: abcde", True),
    ("1-3 b: cdefg", False),
    ("2-9 c: ccccccccc", False),
])
def test_new_line_is_valid(inp, exp):
    res = line_is_valid(NewPasswordPolicy, inp)
    assert res == exp


def test_two():
    inp = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
    assert part_two(inp) == 1


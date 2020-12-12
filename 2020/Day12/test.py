import pytest
from day12 import *


inp = """F10
N3
F7
R90
F11"""


def test_one_step_by_step():
    ship = Ship()
    expected = [(10, 0), (10, 3), (17, 3), (17, 3), (17, -8)]
    for line, exp in zip(inp.split('\n'), expected):
        ship.navigate(line)
        assert ship.pos == exp


def test_one():
    res = part_one(inp)
    assert res == 25


def test_two_step_by_step():
    ship = WaypointShip()
    expected = [(100, 10), (100, 10), (170, 38), (170, 38), (214, -72)]
    for line, exp in zip(inp.split('\n'), expected):
        ship.navigate(line)
        assert ship.pos == exp


def test_two():
    res = part_two(inp)
    assert res == 286


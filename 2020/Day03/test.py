import pytest
from day03 import *


"""That's handy, the Advent of Code gives unittests."""


test_map = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""


def test_one():
    res = part_one(test_map)
    assert res == 7


def test_two():
    res = part_two(test_map)
    assert res == 336




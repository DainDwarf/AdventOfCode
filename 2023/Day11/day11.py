#!/usr/bin/python3
from itertools import combinations
import pytest


# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".strip()

@pytest.mark.parametrize("inp, exp", [
    (((6, 1), (11, 5)), 9),
    (((0, 4), (10, 9)), 15),
    (((2, 0), (7, 12)), 17),
    (((11, 0), (11, 5)), 5),
])
def test_distance(inp, exp):
    assert distance(*inp) == exp

@pytest.mark.parametrize("expansion, result", [
    (2, 374),
    (10, 1030),
    (100, 8410),
])
def test_expansion(expansion, result):
    assert compute_distances(TEST_EXAMPLE, expansion) == result


class SpaceMap:
    mapping = None
    expansion = 1
    _empty_lines = None
    _empty_columns = None

    def __init__(self, inp):
        self.mapping = [l for l in inp.split('\n')]
        self._empty_lines = []
        for i, line in enumerate(self.mapping):
            if all(c == '.' for c in line):
                self._empty_lines.append(i)
        self._empty_columns = []
        for j in range(len(self.mapping[0])):
            if all(line[j] == '.' for line in self.mapping):
                self._empty_columns.append(j)

    def search_all(self, char):
        ret = []
        for i, line in enumerate(self.mapping):
            for j, c in enumerate(line):
                if c == char:
                    expand_i = sum(self.expansion if x in self._empty_lines else 1 for x in range(i+1))
                    expand_j = sum(self.expansion if x in self._empty_columns else 1 for x in range(j+1))
                    ret.append((expand_i, expand_j))
        return ret


def distance(p1, p2):
    """Measured in Manhattan distance."""
    return abs(p2[0]-p1[0])+abs(p2[1]-p1[1])


def compute_distances(inp, expansion):
    space = SpaceMap(inp)
    space.expansion = expansion
    galaxies = space.search_all('#')
    return sum(distance(g1, g2) for g1, g2 in combinations(galaxies, 2))

def part_one(inp):
    return compute_distances(inp, 2)


def part_two(inp):
    return compute_distances(inp, 1000000)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))

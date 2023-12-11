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

def test_one():
    assert part_one(TEST_EXAMPLE) == 374


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


class SpaceMap:
    mapping = None

    def __init__(self, inp):
        self.mapping = [list(l) for l in inp.split('\n')]

    def line(self, i):
        return self.mapping[i][:]

    def column(self, j):
        return [line[j] for line in self.mapping]

    def len_lines(self):
        return len(self.mapping[0])

    def len_columns(self):
        return len(self.mapping)

    def iter_lines(self):
        for i in range(len(self.mapping)):
            yield self.line(i)

    def iter_columns(self):
        for j in range(len(self.mapping[0])):
            yield self.column(j)

    def insert_line(self, i, new_line):
        assert len(new_line) == len(self.mapping[0])
        self.mapping.insert(i, list(new_line))

    def insert_column(self, j, new_column):
        assert len(new_column) == len(self.mapping)
        for line, char in zip(self.mapping, new_column):
            line.insert(j, char)

    def search_all(self, char):
        ret = []
        for i, line in enumerate(self.mapping):
            for j, c in enumerate(line):
                if c == char:
                    ret.append((i, j))
        return ret

    def __str__(self):
        return '\n'.join(''.join(l) for l in self.mapping)


def expand_space(space):
    empty_lines = []
    for i, line in enumerate(space.iter_lines()):
        if all(c == '.' for c in line):
            empty_lines.append(i)

    empty_columns = []
    for j, col in enumerate(space.iter_columns()):
        if all(c == '.' for c in col):
            empty_columns.append(j)

    # TODO: Remove that bad hack: to avoid inserting in the wrong index,
    # since all index after insertion are moved,
    # insert them in reverse order.
    for i in reversed(empty_lines):
        space.insert_line(i, '.'*space.len_lines())
    for j in reversed(empty_columns):
        space.insert_column(j, '.'*space.len_columns())


def distance(p1, p2):
    """Measured in Manhattan distance."""
    return abs(p2[0]-p1[0])+abs(p2[1]-p1[1])


def part_one(inp):
    space = SpaceMap(inp)
    expand_space(space)
    galaxies = space.search_all('#')
    return sum(distance(g1, g2) for g1, g2 in combinations(galaxies, 2))


def part_two(inp):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))

#!/usr/bin/python3
from enum import Enum
import pytest


# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE_1 = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF""".strip()

TEST_EXAMPLE_2 = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ""".strip()

@pytest.mark.parametrize("inp, exp", [
    (TEST_EXAMPLE_1, 4),
    (TEST_EXAMPLE_2, 8),
])
def test_one(inp, exp):
    res = part_one(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


class Direction(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4,

    def move(self, pos):
        i, j = pos
        if self == Direction.UP:
            return (i-1, j)
        elif self == Direction.DOWN:
            return (i+1, j)
        elif self == Direction.LEFT:
            return (i, j-1)
        elif self == Direction.RIGHT:
            return (i, j+1)

    def through(self, pipe):
        if pipe == '|':
            if self == Direction.UP:
                return Direction.UP
            elif self == Direction.DOWN:
                return Direction.DOWN
        elif pipe == '-':
            if self == Direction.LEFT:
                return Direction.LEFT
            elif self == Direction.RIGHT:
                return Direction.RIGHT
        elif pipe == '7':
            if self == Direction.UP:
                return Direction.LEFT
            elif self == Direction.RIGHT:
                return Direction.DOWN
        elif pipe == 'F':
            if self == Direction.UP:
                return Direction.RIGHT
            elif self == Direction.LEFT:
                return Direction.DOWN
        elif pipe == 'J':
            if self == Direction.RIGHT:
                return Direction.UP
            elif self == Direction.DOWN:
                return Direction.LEFT
        elif pipe == 'L':
            if self == Direction.LEFT:
                return Direction.UP
            elif self == Direction.DOWN:
                return Direction.RIGHT
        else:
            raise RuntimeError(f"Cannot move through {pipe} with direction {self}")


class Pipes:
    mapping = None

    def __init__(self, inp):
        self.mapping = ['.' + l + '.' for l in inp.split('\n')]
        self.mapping.append('.'*len(self.mapping[0]))
        self.mapping.insert(0, '.'*len(self.mapping[0]))

    def index(self, char):
        for i, p in enumerate(self.mapping):
            if char in p:
                return (i, p.index(char))

    def __getitem__(self, pos):
        i, j = pos
        return self.mapping[i][j]


def part_one(inp):
    pipes = Pipes(inp)
    start_pos = pipes.index('S')

    if pipes[Direction.UP.move(start_pos)] in ['|', '7', 'F']:
        direction = Direction.UP
    elif pipes[Direction.DOWN.move(start_pos)] in ['|', 'J', 'L']:
        direction = Direction.DOWN
    elif pipes[Direction.LEFT.move(start_pos)] in ['-', 'L', 'F']:
        direction = Direction.LEFT
    elif pipes[Direction.RIGHT.move(start_pos)] in ['-', '7', 'J']:
        direction = Direction.RIGHT

    i = 1
    pos = direction.move(start_pos)

    while pos != start_pos:
        print(pos, direction)
        direction = direction.through(pipes[pos])
        pos = direction.move(pos)
        i += 1

    return i


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

#!/usr/bin/python3
from enum import Enum
import pytest


# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""".strip()

def test_one():
    assert part_one(TEST_EXAMPLE) == 136

@pytest.mark.skip
def test_two():
    assert part_two(TEST_EXAMPLE) == 64

def test_cycles():
    plat = Platform(TEST_EXAMPLE)
    for d in CYCLE:
        plat.tilt(d)
    assert plat.load(Direction.UP) == 87
    for d in CYCLE:
        plat.tilt(d)
    assert plat.load(Direction.UP) == 69
    for d in CYCLE:
        plat.tilt(d)
    assert plat.load(Direction.UP) == 69


class Position(tuple):
    """Tuple subclass to allow for position-wise operations rather than concatenation."""
    def __add__(self, other):
        return self.__class__(s+o for s, o in zip(self, other))
    def __sub__(self, other):
        return self.__class__(s-o for s, o in zip(self, other))


class Direction(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4,

    def __neg__(self):
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        elif self == Direction.LEFT:
            return Direction.RIGHT
        elif self == Direction.RIGHT:
            return Direction.LEFT

    @property
    def to_pos(self):
        if self == Direction.UP:
            return Position((-1, 0))
        elif self == Direction.DOWN:
            return Position((1, 0))
        elif self == Direction.LEFT:
            return Position((0, -1))
        elif self == Direction.RIGHT:
            return Position((0, 1))


CYCLE = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]


class Platform:
    board = None

    def __init__(self, inp):
        # Adding a border to avoid limit checking
        self.board = [['#']+list(l)+['#'] for l in inp.split('\n')]
        self.board.append(['#']*len(self.board[0]))
        self.board.insert(0, ['#']*len(self.board[0]))

    def __str__(self):
        return '\n'.join(''.join(l) for l in self.board)

    def __getitem__(self, pos):
        i, j = pos
        return self.board[i][j]

    def __setitem__(self, pos, x):
        i, j = pos
        self.board[i][j] = x

    @property
    def length(self):
        return len(self.board[0])

    @property
    def height(self):
        return len(self.board)

    def iter_position(self, direction = Direction.RIGHT):
        """Iterate through the board positions excluding borders.

        direction is used to choose the way of iterating.
        Default is the usual european writing left-to-right."""
        if direction == Direction.DOWN:
            for j in range(1, self.length-1):
                for i in range(1, self.height-1):
                    yield Position((i, j))
        elif direction == Direction.UP:
            for j in range(1, self.length-1):
                for i in range(self.height-1, 0, -1):
                    yield Position((i, j))
        elif direction == Direction.RIGHT:
            for i in range(1, self.height-1):
                for j in range(1, self.length-1):
                    yield Position((i, j))
        elif direction == Direction.LEFT:
            for i in range(1, self.height-1):
                for j in range(self.length-1, 0, -1):
                    yield Position((i, j))

    def tilt(self, direction):
        for pos in self.iter_position(-direction):
            if self[pos] == 'O':
                self[pos] = '.'
                new_pos = pos
                while self[new_pos] == '.':
                    new_pos += direction.to_pos
                self[new_pos - direction.to_pos] = 'O'

    def load(self, direction):
        ret = 0
        if direction == Direction.UP:
            for weight, line in enumerate(self.board[::-1]):
                ret += line.count('O')*weight
        return ret


def part_one(inp):
    plat = Platform(inp)
    plat.tilt(Direction.UP)
    print(plat)
    return plat.load(Direction.UP)


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

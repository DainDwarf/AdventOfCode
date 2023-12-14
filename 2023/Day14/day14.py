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


class Direction(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4,

    def to_pos(self):
        if self == Direction.UP:
            return (-1, 0)
        elif self == Direction.UP:
            return (1, 0)
        elif self == Direction.LEFT:
            return (0, -1)
        elif self == Direction.RIGHT:
            return (0, 1)


class Platform:
    board = None

    def __init__(self, inp):
        self.board = [['#']+list(l)+['#'] for l in inp.split('\n')]
        self.board.append(['#']*len(self.board[0]))
        self.board.insert(0, ['#']*len(self.board[0]))

    def __str__(self):
        return '\n'.join(''.join(l) for l in self.board)

    def tilt(self, direction):
        if direction == Direction.UP:
            for j in range(len(self.board[0])):
                for i in range(len(self.board)):
                    if self.board[i][j] == 'O':
                        self.board[i][j] = '.'
                        new_i = i
                        while self.board[new_i][j] == '.':
                            new_i += -1
                        self.board[new_i+1][j] = 'O'

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

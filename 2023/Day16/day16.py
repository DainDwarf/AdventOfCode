#!/usr/bin/python3
from enum import Enum
import pytest


# That's handy, the Advent of Code gives unittests.
TEST_EXAMPLE = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""".strip()

def test_beam():
    assert Position((4, 5)) == Position((4, 5))
    assert Direction.UP == Direction.UP
    assert Beam(Position((4, 5)), Direction.UP) == Beam(Position((4, 5)), Direction.UP)

def test_one():
    assert part_one(TEST_EXAMPLE) == 46


class Position(tuple):
    """Tuple subclass to allow for position-wise operations rather than concatenation."""
    def __add__(self, other):
        return self.__class__(s+o for s, o in zip(self, other))
    def __sub__(self, other):
        return self.__class__(s-o for s, o in zip(self, other))


class Beam:
    position = None
    direction = None
    
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def __eq__(self, other):
        return (self.position == other.position
            and self.direction == other.direction
        )
    
    def __hash__(self):
        return hash((self.position, self.direction))


class Direction(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4,

    @property
    def pos(self):
        if self == Direction.UP:
            return Position((-1, 0))
        elif self == Direction.DOWN:
            return Position((1, 0))
        elif self == Direction.LEFT:
            return Position((0, -1))
        elif self == Direction.RIGHT:
            return Position((0, 1))

    @property
    def sym_slash(self):
        if self == Direction.UP:
            return Direction.RIGHT
        elif self == Direction.LEFT:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.LEFT
        elif self == Direction.RIGHT:
            return Direction.UP

    @property
    def sym_backslash(self):
        if self == Direction.UP:
            return Direction.LEFT
        elif self == Direction.RIGHT:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.RIGHT
        elif self == Direction.LEFT:
            return Direction.UP


class Contraption:
    cells = None

    def __init__(self, inp):
        # Adding a border to avoid limit checking
        self.cells = ['#'+l+'#' for l in inp.split('\n')]
        self.cells.append('#'*len(self.cells[0]))
        self.cells.insert(0, '#'*len(self.cells[0]))

    def __getitem__(self, pos):
        i, j = pos
        return self.cells[i][j]

    def pass_beam(self, beam):
        """Returns the set of beams coming out from the input beam."""
        pos = beam.position
        direct = beam.direction
        ret = set()

        if self[pos] == '#': # Border absorbs beams
            pass
        elif self[pos] == '.':
            ret.add(Beam(pos+direct.pos, direct))
        elif self[pos] == '/':
            ret.add(Beam(pos+direct.sym_slash.pos, direct.sym_slash))
        elif self[pos] == '\\':
            ret.add(Beam(pos+direct.sym_backslash.pos, direct.sym_backslash))
        elif self[pos] == '-':
            if direct in (Direction.LEFT, Direction.RIGHT):
                ret.add(Beam(pos+direct.pos, direct))
            else:
                ret.add(Beam(pos+direct.sym_slash.pos, direct.sym_slash))
                ret.add(Beam(pos+direct.sym_backslash.pos, direct.sym_backslash))
        elif self[pos] == '|':
            if direct in (Direction.UP, Direction.DOWN):
                ret.add(Beam(pos+direct.pos, direct))
            else:
                ret.add(Beam(pos+direct.sym_slash.pos, direct.sym_slash))
                ret.add(Beam(pos+direct.sym_backslash.pos, direct.sym_backslash))
        else:
            raise RuntimeError(f"Unrecognized cell {self[pos]} at position {pos}")
        return ret

    def print_charges(self, charged_positions):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[0])):
                if (i, j) in charged_positions:
                    print('C', end='')
                else:
                    print(self[i, j], end='')
            print()


def part_one(inp):
    contraption = Contraption(inp)
    contraption.print_charges({})
    print()
    start = Beam(Position((1, 1)), Direction.RIGHT)

    to_propagate = set()
    to_propagate.add(start)
    visited = set()
    while to_propagate:
        beam = to_propagate.pop()
        visited.add(beam)
        new_beams = contraption.pass_beam(beam)
        for b in new_beams:
            if b not in visited and contraption[b.position] != '#':
                to_propagate.add(b)

    positions = set(b.position for b in visited)
    contraption.print_charges(positions)
    return len(positions)



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

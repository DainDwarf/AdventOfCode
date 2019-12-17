import pytest
import re
from enum import Enum, unique, auto
from itertools import product

from intcode.simulator import Simulator, ParamMode


# That's handy, the Advent of Code gives unittests.
def test_calibrate():
    full_map = """
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^.."""
    res = calibrate(full_map)
    assert res == 76, full_map


def test_full_path():
    full_map = """
#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......"""
    res = full_path(full_map)
    assert res == "R8R8R4R4R8L6L2R4R4R8R8R8L6L2"


def test_factorize():
    full_path = "R8R8R4R4R8L6L2R4R4R8R8R8L6L2"
    main, a, b, c = factorize(full_path)
    assert len(main) <= 20
    assert len(a) <= 20
    assert len(b) <= 20
    assert len(c) <= 20
    reconstruct = ''
    for fun in main:
        if fun == 'A':
            reconstruct += a
        if fun == 'B':
            reconstruct += b
        if fun == 'C':
            reconstruct += c
    assert reconstruct == full_path

def test_encode_route():
    main = "ABCBAC"
    a = "R8R8"
    b = "R4R4R8"
    c = "L6L2"
    code = encode(main, a, b, c)
    assert code == [65, 44, 66, 44, 67, 44, 66, 44, 65, 44, 67, 10, 82, 44, 56, 44, 82, 44, 56, 10, 82, 44, 52, 44, 82, 44, 52, 44, 82, 44, 56, 10, 76, 44, 54, 44, 76, 44, 50, 10]


@unique
class Direction(Enum):
    NORTH = auto(),
    SOUTH = auto(),
    WEST = auto(),
    EAST = auto(),

    @classmethod
    def from_cell(cls, cell):
        if cell == '^':
            return cls.NORTH
        elif cell == 'v':
            return cls.SOUTH
        elif cell == '<':
            return cls.WEST
        elif cell == '>':
            return cls.EAST
        else:
            raise RuntimeError(f"Unrecognized robot direction {cell}")

    def move(self, pos):
        if self is Direction.NORTH:
            return (pos[0]  , pos[1]-1)
        elif self is Direction.SOUTH:
            return (pos[0]  , pos[1]+1)
        elif self is Direction.WEST:
            return (pos[0]-1, pos[1]  )
        elif self is Direction.EAST:
            return (pos[0]+1, pos[1]  )

    @property
    def right(self):
        """Returns the move that corresponds to the right of current direction."""
        if self is Direction.NORTH:
            return Direction.EAST
        elif self is Direction.EAST:
            return Direction.SOUTH
        elif self is Direction.SOUTH:
            return Direction.WEST
        elif self is Direction.WEST:
            return Direction.NORTH

    @property
    def left(self):
        """Returns the move that corresponds to the left of current direction."""
        if self is Direction.NORTH:
            return Direction.WEST
        elif self is Direction.WEST:
            return Direction.SOUTH
        elif self is Direction.SOUTH:
            return Direction.EAST
        elif self is Direction.EAST:
            return Direction.NORTH


def to_dict(full_map):
    mamap = dict()
    for y, line in enumerate(full_map.strip().split('\n')):
        for x, cell in enumerate(line.strip()):
            mamap[x, y] = cell
    return mamap


def calibrate(full_map):
    mamap = to_dict(full_map)
    sum = 0
    for pos, cell in mamap.items():
        x, y = pos
        if cell == '#':
            if all(mamap.get(neighbor, '') == '#' for neighbor in [
                (x-1, y  ),
                (x+1, y  ),
                (x  , y+1),
                (x  , y-1),
            ]):
                sum += x*y
    return sum


def full_path(full_map):
    mamap = to_dict(full_map)
    pos = None
    direction = None
    for map_pos, cell in mamap.items():
        if cell in ('^', 'v', '<', '>'):
            pos = map_pos
            direction = Direction.from_cell(cell)
            break
    path = []
    while True:
        if mamap.get(direction.left.move(pos), '.') == '#':
            path.append('L')
            direction = direction.left
        elif mamap.get(direction.right.move(pos), '.') == '#':
            path.append('R')
            direction = direction.right
        else:
            break
        move = 0
        while mamap.get(direction.move(pos), '.') == '#':
            pos = direction.move(pos)
            move += 1
        path.append(str(move))
    return ','.join(path)


def factorize(full_path):
    full_path = full_path.replace(',', '')
    for size_a, size_b, size_c in product(range(1, 15), repeat=3):
        a = full_path[:size_a]
        b = full_path[size_a:size_b+size_a]
        c = full_path[size_a+size_b:size_a+size_b+size_c]
        try_match = re.match(f"^({c}|{b}|{a})*$", full_path)
        if try_match:
            def _fun(matchobj):
                if matchobj.group(0) == a:
                    return 'A'
                if matchobj.group(0) == b:
                    return 'B'
                if matchobj.group(0) == c:
                    return 'C'
            main = re.sub(f"({c}|{b}|{a})", _fun, full_path)
            return [main, a, b, c]


def encode(*args):
    ret = []
    full_string = '\n'.join(','.join(arg) for arg in args)+'\n'
    return list(map(ord, full_string))


def part_one(code):
    simulator = Simulator(code)
    simulator.run()
    full_map = ''.join(map(chr, simulator.output()))
    return calibrate(full_map)


def part_two(code):
    simulator = Simulator(code)
    simulator.run()
    full_map = ''.join(map(chr, simulator.output()))
    path = full_path(full_map)
    print(full_map)
    print(path)
    manual = "A,B,A,C,B,A,C,B,A,C\n" \
             "L,6,L,4,R,12\n" \
             "L,6,R,12,R,12,L,8\n" \
             "L,6,L,10,L,10,L,6\n" \
             "n\n"
    print(manual)
    encoded = list(map(ord, manual))
    real_run = Simulator(code)
    real_run[0] = 2
    real_run.add_input(encoded)
    real_run.run()
    print(real_run.output())
    print(''.join(map(chr, simulator.output())))
    return real_run.output()[-1]


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    code = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(code)))
    print("Answer for part two is : {res}".format(res=part_two(code)))

#!/usr/bin/python3
from enum import Enum
from itertools import pairwise
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

TEST_EXAMPLE_3 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""".strip()

TEST_EXAMPLE_4 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""".strip()

TEST_EXAMPLE_5 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""".strip()

@pytest.mark.parametrize("inp, exp", [
    (TEST_EXAMPLE_1, 4),
    (TEST_EXAMPLE_2, 8),
])
def test_one(inp, exp):
    res = part_one(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    (TEST_EXAMPLE_1, 1),
    (TEST_EXAMPLE_2, 1),
    (TEST_EXAMPLE_3, 4),
    (TEST_EXAMPLE_4, 8),
    (TEST_EXAMPLE_5, 10),
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

    @property
    def max_pos(self):
        return (len(self.mapping)-1, len(self.mapping[0])-1)

    def index(self, char):
        for i, p in enumerate(self.mapping):
            if char in p:
                return (i, p.index(char))

    def __getitem__(self, pos):
        i, j = pos
        return self.mapping[i][j]


def get_main_loop(pipes):
    start_pos = pipes.index('S')

    if pipes[Direction.UP.move(start_pos)] in ['|', '7', 'F']:
        direction = Direction.UP
    elif pipes[Direction.DOWN.move(start_pos)] in ['|', 'J', 'L']:
        direction = Direction.DOWN
    elif pipes[Direction.LEFT.move(start_pos)] in ['-', 'L', 'F']:
        direction = Direction.LEFT
    elif pipes[Direction.RIGHT.move(start_pos)] in ['-', '7', 'J']:
        direction = Direction.RIGHT

    path = [start_pos]
    pos = direction.move(start_pos)

    while pos != start_pos:
        path.append(pos)
        direction = direction.through(pipes[pos])
        pos = direction.move(pos)

    return path


def part_one(inp):
    pipes = Pipes(inp)
    path = get_main_loop(pipes)

    return len(path) // 2


def part_two(inp):
    pipes = Pipes(inp)
    path = get_main_loop(pipes)

    #Close the loop
    path.append(pipes.index('S'))

    # Once we have the path coordinates, we don't need the pipes map anymore.
    # To deal with squeezable spaces, add half numbers to the pile
    def neighbors(pos):
        i, j = pos
        ret = set()
        if i > 0:
            ret.add((i-0.5, j))
        if i < pipes.max_pos[0]:
            ret.add((i+0.5, j))
        if j > 0:
            ret.add((i, j-0.5))
        if j < pipes.max_pos[1]:
            ret.add((i, j+0.5))
        return ret

    double_path = set(path)
    for p1, p2 in pairwise(path):
        double_path.add(( (p1[0]+p2[0])/2, (p1[1]+p2[1])/2 ))

    to_search = {(0.0, 0.0)}
    found = set()
    
    while to_search:
        searching = to_search.pop()
        for neigh in neighbors(searching):
            if neigh not in found and neigh not in double_path:
                to_search.add(neigh)
        found.add(searching)

    ret = 0
    for i in range(pipes.max_pos[0]):
        for j in range(pipes.max_pos[1]):
            if (i, j) not in found and (i, j) not in path:
                ret += 1

    return ret



if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))

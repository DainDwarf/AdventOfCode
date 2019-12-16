import pytest
import random
from time import sleep
from intcode.simulator import Simulator, ParamMode
from enum import IntEnum, unique


# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
])
def testOne(inp, exp):
    res = partOne(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
])
def testTwo(inp, exp):
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")
    assert res == exp


@unique
class Move(IntEnum):
    NORTH = 1,
    SOUTH = 2,
    WEST = 3,
    EAST = 4,

    def move(self, pos):
        if self is Move.NORTH:
            return (pos[0]  , pos[1]-1)
        elif self is Move.SOUTH:
            return (pos[0]  , pos[1]+1)
        elif self is Move.WEST:
            return (pos[0]-1, pos[1]  )
        elif self is Move.EAST:
            return (pos[0]+1, pos[1]  )

    @property
    def right(self):
        """Returns the move that corresponds to the right of current direction."""
        if self is Move.NORTH:
            return Move.EAST
        elif self is Move.EAST:
            return Move.SOUTH
        elif self is Move.SOUTH:
            return Move.WEST
        elif self is Move.WEST:
            return Move.NORTH

    @property
    def left(self):
        """Returns the move that corresponds to the left of current direction."""
        if self is Move.NORTH:
            return Move.WEST
        elif self is Move.WEST:
            return Move.SOUTH
        elif self is Move.SOUTH:
            return Move.EAST
        elif self is Move.EAST:
            return Move.NORTH


@unique
class Tile(IntEnum):
    UNKNOWN = -1,
    WALL = 0,
    CORRIDOR = 1,
    OXYGEN = 2,

    def __str__(self):
        if self is self.UNKNOWN:
            return ' '
        elif self is self.WALL:
            return '#'
        elif self is self.CORRIDOR:
            return '.'
        elif self is self.OXYGEN:
            return 'O'


class Maze:
    def __init__(self):
        self._maze = {(0, 0): Tile.CORRIDOR}

    def display(self, robot=None):
        minx = min(p[0] for p in self._maze.keys())
        maxx = max(p[0] for p in self._maze.keys())
        miny = min(p[1] for p in self._maze.keys())
        maxy = max(p[1] for p in self._maze.keys())
        display = ""
        for y in range(miny, maxy+1):
            for x in range(minx, maxx+1):
                if robot is not None and (x, y) == robot:
                    display += '@'
                else:
                    display += str(self[x, y])
            display += '\n'
        return display

    def __getitem__(self, pos):
        return self._maze.get(pos, Tile.UNKNOWN)

    def __setitem__(self, pos, tile):
        assert pos not in self._maze or self._maze[pos] is Tile.UNKNOWN or self._maze[pos] is tile
        self._maze[pos] = tile


class Explorer(Simulator):
    def __init__(self, *args, **kwargs):
        self._pos = (0, 0)
        self._try_dir = None
        self._current_dir = Move.NORTH
        self._maze = Maze()
        super().__init__(*args, **kwargs)

    def _ai(self):
        right_dir = self._current_dir.right
        right_pos = right_dir.move(self._pos)
        if self._maze[right_pos] is not Tile.WALL:
            print(f"Going on the unknown right {right_pos}")
            return right_dir
        elif self._maze[self._current_dir.move(self._pos)] is not Tile.WALL:
            print(f"Going forward, full speed!")
            return self._current_dir
        elif self._maze[self._current_dir.left.move(self._pos)] is not Tile.WALL:
            print(f"Cannot go right nor in front. Going left.")
            self._current_dir = self._current_dir.left
            return self._current_dir
        else:
            print(f"Last try, behind?")
            self._current_dir = self._current_dir.left.left
            return self._current_dir

    def _input(self, *args, **kwargs):
        if not self._input_values:
            self._try_dir = self._ai()
            self.add_input([self._try_dir.value])
        super()._input(*args, **kwargs)

    def _output(self, *args, **kwargs):
        super()._output(*args, **kwargs)
        feedback = Tile(self._output_values.pop(0))
        if feedback is Tile.WALL:
            wall_pos = self._try_dir.move(self._pos)
            self._maze[wall_pos] = feedback
        elif feedback is Tile.CORRIDOR:
            self._pos = self._try_dir.move(self._pos)
            self._maze[self._pos] = feedback
            if self._try_dir is not self._current_dir:
                # We tried the right position, and it was not a wall, continue on that direction.
                self._current_dir = self._try_dir
        elif feedback is Tile.OXYGEN:
            self._pos = self._try_dir.move(self._pos)
            self._maze[self._pos] = feedback
            if self._try_dir is not self._current_dir:
                # We tried the right position, and it was not a wall, continue on that direction.
                self._current_dir = self._try_dir
            self._finished = True

        print(self._maze.display(self._pos))
        print(f"I did try {self._try_dir.name}")
        print(f"Now navigating {self._current_dir.name}")
        sleep(0.01)


def partOne(code):
    explore = Explorer(code)
    explore.run()


def partTwo(code):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    code = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(code)))
    print("Answer for part two is : {res}".format(res=partTwo(code)))

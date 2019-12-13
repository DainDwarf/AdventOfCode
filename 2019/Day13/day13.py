import pytest
from enum import IntEnum, unique

import progressbar

from intcode.simulator import Simulator, ParamMode


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


@unique
class Tile(IntEnum):
    EMPTY = 0,
    WALL = 1,
    BLOCK = 2,
    PADDLE = 3,
    BALL = 4,

    def __str__(self):
        if self is Tile.EMPTY:
            return ' '
        elif self is Tile.WALL:
            return '|'
        elif self is Tile.BLOCK:
            return 'X'
        elif self is Tile.PADDLE:
            return '-'
        elif self is Tile.BALL:
            return 'o'
        else:
            raise RuntimeError(f"Unknown tile {tile}")


class Screen:
    def __init__(self):
        self._screen = dict()
        self._score = 0
        self._minx = self._maxx = None
        self._miny = self._maxy = None
        self._acc = []

    def __setitem__(self, pos, value):
        if pos == (-1, 0):
            self._score = value
        else:
            self._screen[pos] = Tile(value)

    def input(self, val):
        self._acc.append(val)
        if len(self._acc) == 3:
            x, y, tile = self._acc
            self[x, y] = tile
            self._acc = []

    @property
    def block_count(self):
        return sum(1 if t is Tile.BLOCK else 0 for t in self._screen.values())

    @property
    def ball_position(self):
        for pos, tile in self._screen.items():
            if tile is Tile.BALL:
                return pos

    @property
    def paddle_position(self):
        for pos, tile in self._screen.items():
            if tile is Tile.PADDLE:
                return pos


class Arcade(Simulator):
    def __init__(self, *args, bar=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._screen = Screen()
        self._bar = bar

    def mini_ai(self):
        bp = self._screen.ball_position
        pp = self._screen.paddle_position
        return sign(bp[0] - pp[0])

    def _input(self, *args, **kwargs):
        if not self._input_values:
            inp = self.mini_ai()
            self.add_input([int(inp)])
        if self._bar is not None:
            self._bar.update(self._bar.max_value-self.block_count)
        super()._input(*args, **kwargs)

    def _output(self, *args, **kwargs):
        super()._output(*args, **kwargs)
        self._screen.input(self._output_values.pop(0))

    def auto_play(self):
        self[0] = 2
        self.run()

    @property
    def block_count(self):
        return self._screen.block_count

    @property
    def score(self):
        return self._screen._score


def partOne(code):
    arcade = Arcade(code)
    while not arcade.finished:
        arcade.run()
    return arcade.block_count


def partTwo(code, block_count):
    bar = progressbar.ProgressBar(max_value=block_count)
    arcade = Arcade(code, bar=bar)
    arcade.auto_play()
    bar.update(bar.max_value-arcade.block_count)
    return arcade.score


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    code = options.input.read().strip()
    res1=partOne(code)
    res2=partTwo(code, res1)
    print()
    print(f"Answer for part one is : {res1}")
    print(f"Answer for part two is : {res2}")

#!/usr/bin/python3
import itertools


class InfiniteND:
    def __init__(self, dimension):
        self._dim = dimension
        self.reset()

    def __getitem__(self, pos):
        return pos in self._grid

    def __setitem__(self, pos, value):
        if value:
            self._grid.add(pos)
        else:
            self._grid.discard(pos)

    def __iter__(self):
        return iter(self._grid)

    def __len__(self):
        return len(self._grid)

    @property
    def minpos(self):
        return tuple(min((t[d] for t in self._grid), default=0) for d in range(self._dim))

    @property
    def maxpos(self):
        return tuple(max((t[d] for t in self._grid), default=0) for d in range(self._dim))

    def reset(self):
        self._grid = set()


class GameOfLifeND:
    def __init__(self, dimension):
        self._dim = dimension
        self._grid = InfiniteND(self._dim)

    def __getitem__(self, pos):
        return self._grid[pos]

    def __setitem__(self, pos, value):
        self._grid[pos] = value

    def parse(self, inp):
        for x, line in enumerate(inp.split('\n')):
            for y, char in enumerate(line):
                pos = (x, y) + (0,)*(self._dim-2)
                self[pos] = (char=='#')
        return self

    def neighbors_active_count(self, pos):
        count = 0
        for dpos in itertools.product(range(-1, 2), repeat=self._dim):
            if dpos != (0,)*self._dim:
                count += int(self[tuple(x+dx for x, dx in zip(pos, dpos))])
        return count

    def next_state(self, pos):
        count = self.neighbors_active_count(pos)
        if self[pos]:
            return count in (2, 3)
        else:
            return count == 3

    def cycle(self):
        new_grid = InfiniteND(self._dim)
        for pos in itertools.product(*(range(mind-1, maxd+2) for mind, maxd in zip(self._grid.minpos, self._grid.maxpos))):
            new_grid[pos] = self.next_state(pos)
        self._grid = new_grid
        return self

    def run(self, cycles):
        for _ in range(cycles):
            self.cycle()
        return self

    def count(self):
        return len(self._grid)


def part_one(inp):
    return GameOfLifeND(3).parse(inp).run(6).count()


def part_two(inp):
    return GameOfLifeND(4).parse(inp).run(6).count()


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))

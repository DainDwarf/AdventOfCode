#!/usr/bin/python3


class InfiniteND:
    def __init__(self, dimension):
        self._dim = dimension
        self.reset()

    def __getitem__(self, pos):
        assert len(pos) == self._dim
        if pos in self._grid:
            return '#'
        else:
            return '.'

    def __setitem__(self, pos, value):
        assert len(pos) == self._dim
        if value == '#':
            self._grid.add(pos)
        else:
            self._grid.discard(pos)

    def __iter__(self):
        return iter(self._grid)

    def __len__(self):
        return len(self._grid)

    @property
    def minpos(self):
        return tuple(min(t[d] for t in self._grid) for d in range(self._dim))

    @property
    def maxpos(self):
        return tuple(max(t[d] for t in self._grid) for d in range(self._dim))

    def reset(self):
        self._grid = set()


class GameOfLife3D:
    def __init__(self):
        self._grid = InfiniteND(3)

    def __getitem__(self, pos):
        return self._grid[pos]

    def __setitem__(self, pos, value):
        self._grid[pos] = value

    def parse(self, inp):
        for x, line in enumerate(inp.split('\n')):
            for y, char in enumerate(line):
                self[x, y, 0] = char

    def neighbors(self, pos):
        x, y, z = pos
        ret = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    if (dx, dy, dz) != (0, 0, 0):
                        ret.append(self[x+dx, y+dy, z+dz])
        return ret

    def next_state(self, pos):
        count = len([n for n in self.neighbors(pos) if n == '#'])
        if self[pos] == '#':
            if count in (2, 3):
                return '#'
            else:
                return '.'
        else:
            if count == 3:
                return '#'
            else:
                return '.'

    def cycle(self):
        new_grid = InfiniteND(3)
        minx, miny, minz = self._grid.minpos
        maxx, maxy, maxz = self._grid.maxpos
        for x in range(minx-1, maxx+2):
            for y in range(miny-1, maxy+2):
                for z in range(minz-1, maxz+2):
                    new_grid[x, y, z] = self.next_state((x, y, z))

        self._grid = new_grid

    def run(self, cycles):
        for _ in range(cycles):
            self.cycle()

    def count(self):
        return len(self._grid)


class GameOfLife4D():
    def __init__(self):
        self._grid = InfiniteND(4)

    def __getitem__(self, pos):
        return self._grid[pos]

    def __setitem__(self, pos, value):
        self._grid[pos] = value

    def parse(self, inp):
        for x, line in enumerate(inp.split('\n')):
            for y, char in enumerate(line):
                self[x, y, 0, 0] = char

    def neighbors(self, pos):
        x, y, z, w = pos
        ret = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    for dw in range(-1, 2):
                        if (dx, dy, dz, dw) != (0, 0, 0, 0):
                            ret.append(self[x+dx, y+dy, z+dz, w+dw])
        return ret

    def next_state(self, pos):
        count = len([n for n in self.neighbors(pos) if n == '#'])
        if self[pos] == '#':
            if count in (2, 3):
                return '#'
            else:
                return '.'
        else:
            if count == 3:
                return '#'
            else:
                return '.'


    def cycle(self):
        new_grid = InfiniteND(4)
        minx, miny, minz, minw = self._grid.minpos
        maxx, maxy, maxz, maxw = self._grid.maxpos
        for x in range(minx-1, maxx+2):
            for y in range(miny-1, maxy+2):
                for z in range(minz-1, maxz+2):
                    for w in range(minw-1, maxw+2):
                        new_grid[x, y, z, w] = self.next_state((x, y, z, w))

        self._grid = new_grid

    def run(self, cycles):
        for _ in range(cycles):
            self.cycle()

    def count(self):
        return len(self._grid)


def part_one(inp):
    game = GameOfLife3D()
    game.parse(inp)
    game.run(6)
    return game.count()


def part_two(inp):
    game = GameOfLife4D()
    game.parse(inp)
    game.run(6)
    return game.count()


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))

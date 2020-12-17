#!/usr/bin/python3


class Infinite3D:
    def __init__(self):
        self.reset()

    def __getitem__(self, pos):
        if pos in self._grid:
            return '#'
        else:
            return '.'

    def __setitem__(self, pos, value):
        if value == '#':
            self._grid.add(pos)
        else:
            self._grid.discard(pos)

    def __iter__(self):
        return iter(self._grid)

    @property
    def minx(self):
        return min(t[0] for t in self._grid)

    @property
    def maxx(self):
        return max(t[0] for t in self._grid)

    @property
    def miny(self):
        return min(t[1] for t in self._grid)

    @property
    def maxy(self):
        return max(t[1] for t in self._grid)

    @property
    def minz(self):
        return min(t[2] for t in self._grid)

    @property
    def maxz(self):
        return max(t[2] for t in self._grid)

    def reset(self):
        self._grid = set()


class GameOfLife3D(Infinite3D):
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
        new_grid = Infinite3D()
        for x in range(self.minx-1, self.maxx+2):
            for y in range(self.miny-1, self.maxy+2):
                for z in range(self.minz-1, self.maxz+2):
                    new_grid[x, y, z] = self.next_state((x, y, z))

        self.reset()
        for pos in new_grid:
            self[pos] = new_grid[pos]

    def run(self, cycles):
        for _ in range(cycles):
            self.cycle()

    def count(self):
        return len(self._grid)


class Infinite4D:
    def __init__(self):
        self.reset()

    def __getitem__(self, pos):
        if pos in self._grid:
            return '#'
        else:
            return '.'

    def __setitem__(self, pos, value):
        if value == '#':
            self._grid.add(pos)
        else:
            self._grid.discard(pos)

    def __iter__(self):
        return iter(self._grid)

    @property
    def minx(self):
        return min(t[0] for t in self._grid)

    @property
    def maxx(self):
        return max(t[0] for t in self._grid)

    @property
    def miny(self):
        return min(t[1] for t in self._grid)

    @property
    def maxy(self):
        return max(t[1] for t in self._grid)

    @property
    def minz(self):
        return min(t[2] for t in self._grid)

    @property
    def maxz(self):
        return max(t[2] for t in self._grid)

    @property
    def minw(self):
        return min(t[3] for t in self._grid)

    @property
    def maxw(self):
        return max(t[3] for t in self._grid)

    def reset(self):
        self._grid = set()


class GameOfLife4D(Infinite4D):
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
        new_grid = Infinite3D()
        for x in range(self.minx-1, self.maxx+2):
            for y in range(self.miny-1, self.maxy+2):
                for z in range(self.minz-1, self.maxz+2):
                    for w in range(self.minw-1, self.maxw+2):
                        new_grid[x, y, z, w] = self.next_state((x, y, z, w))

        self.reset()
        for pos in new_grid:
            self[pos] = new_grid[pos]

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

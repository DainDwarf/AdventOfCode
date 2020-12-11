#!/usr/bin/python3


class GameOfSeat:
    _tolerance = 4

    def __init__(self, inp):
        self._grid = inp.split('\n')
        self._height = len(self._grid)
        self._length = len(self._grid[0])

    @property
    def grid(self):
        return self._grid

    def display(self):
        return '\n'.join(self._grid)

    def __getitem__(self, pos):
        x, y = pos
        if x < 0 or y < 0:
            return ' '
        try:
            return self._grid[x][y]
        except IndexError:
            return ' '

    def get_neighborhood(self, x, y):
        return [self[x-1, y-1], self[x-1, y], self[x-1, y+1],
                self[x  , y-1],               self[x  , y+1],
                self[x+1, y-1], self[x+1, y], self[x+1, y+1]]

    def new_state(self, x, y):
        if self[x, y] == '.':
            return '.'
        elif self[x, y] == 'L':
            return '#' if self.get_neighborhood(x, y).count('#') == 0 else 'L'
        elif self[x, y] == '#':
            return 'L' if self.get_neighborhood(x, y).count('#') >= self._tolerance else '#'
        else:
            raise RuntimeError(f"Unknown state {self[x, y]} at position ({x}, {y})")

    def step(self):
        new_grid = []
        for x in range(self._height):
            new_line = ""
            for y in range(self._length):
                new_line += self.new_state(x, y)
            new_grid.append(new_line)
        self._grid = new_grid


class GameOfSight(GameOfSeat):
    _tolerance = 5

    def get_neighborhood(self, x, y):
        neigh = []
        for v_x, v_y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            i = 1
            while (cell := self[x+i*v_x, y+i*v_y]) == '.':
                i += 1
            neigh.append(cell)
        return neigh



def part_one(inp):
    game = GameOfSeat(inp)
    old_grid = []
    new_grid = game.grid
    while old_grid != new_grid:
        game.step()
        old_grid = new_grid
        new_grid = game.grid
    return sum(l.count('#') for l in new_grid)


def part_two(inp):
    game = GameOfSight(inp)
    old_grid = []
    new_grid = game.grid
    while old_grid != new_grid:
        game.step()
        old_grid = new_grid
        new_grid = game.grid
    return sum(l.count('#') for l in new_grid)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))

#!/usr/bin/python3
from __future__ import print_function

class GameOfLife(object):
    def __init__(self, display):
        # List of lists, indexed line first, columns second, starting top-left.
        self.grid = []
        for line in display.split('\n'):
            self.grid.append(list(map(lambda c: 1 if c == '#' else 0, line)))

    def __str__(self):
        return '\n'.join(''.join(map(lambda n: '#' if n==1 else '.', line)) for line in self.grid)

    def __getitem__(self, pos):
        try:
            line, col = pos
            if line >= 0 and col >= 0:
                return self.grid[pos[0]][pos[1]]
            else:
                return 0
        except IndexError:
            return 0

    def getNeighborsLitCount(self, pos):
        line, col = pos
        return ( self[(line-1, col-1)]
               + self[(line-1, col  )]
               + self[(line-1, col+1)]
               + self[(line  , col-1)]
               + self[(line  , col+1)]
               + self[(line+1, col-1)]
               + self[(line+1, col  )]
               + self[(line+1, col+1)]
        )

    def getLitCount(self):
        return sum(map(sum, self.grid))


    def step(self):
        new_grid = []
        for line_num, line in enumerate(self.grid):
            new_line = []
            for col_num, cell in enumerate(line):
                if cell == 1:
                    if 3 >= self.getNeighborsLitCount((line_num, col_num)) >= 2:
                        new_line.append(1)
                    else:
                        new_line.append(0)
                else:
                    if self.getNeighborsLitCount((line_num, col_num)) == 3:
                        new_line.append(1)
                    else:
                        new_line.append(0)
            new_grid.append(new_line)
        self.grid = new_grid

class StuckCorners(GameOfLife):
    def __init__(self, display):
        super().__init__(display)
        self.grid[ 0][ 0] = 1
        self.grid[ 0][-1] = 1
        self.grid[-1][ 0] = 1
        self.grid[-1][-1] = 1

    def step(self):
        super().step()
        self.grid[ 0][ 0] = 1
        self.grid[ 0][-1] = 1
        self.grid[-1][ 0] = 1
        self.grid[-1][-1] = 1



# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = ".#.#.#\n...##.\n#....#\n..#...\n#.#..#\n####.."

    g = GameOfLife(ex)
    print("Unit test for Part One.")
    print("Initial state:\n{g}".format(g=g))

    g.step()
    print("\nAfter 1 step:\n{g}".format(g=g))

    g.step()
    print("\nAfter 2 step:\n{g}".format(g=g))

    g.step()
    print("\nAfter 3 step:\n{g}".format(g=g))

    g.step()
    print("\nAfter 4 step:\n{g}".format(g=g))

    print("\nAfter 4 steps, example has {res} lights on.".format(res = partOne(ex, 4)))


    g2 = StuckCorners(ex)
    print("")
    print("Unit test for Part Two.")
    print("Initial state:\n{g}".format(g=g2))

    g2.step()
    print("\nAfter 1 step:\n{g}".format(g=g2))

    g2.step()
    print("\nAfter 2 step:\n{g}".format(g=g2))

    g2.step()
    print("\nAfter 3 step:\n{g}".format(g=g2))

    g2.step()
    print("\nAfter 4 step:\n{g}".format(g=g2))

    g2.step()
    print("\nAfter 5 step:\n{g}".format(g=g2))

    print("\nAfter 5 steps, example has {res} lights on.".format(res = partTwo(ex, 5)))


def partOne(inp, steps=100):
    g = GameOfLife(inp)
    for step in range(steps):
        g.step()
    return g.getLitCount()

def partTwo(inp, steps=100):
    g = StuckCorners(inp)
    for step in range(steps):
        g.step()
    return g.getLitCount()

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))

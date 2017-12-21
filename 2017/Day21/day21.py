#!/usr/bin/python3
from __future__ import print_function

def display(grid):
    """Display as a grid, whether it used '/' notation or '\n'."""
    print(grid.replace('/', '\n'))

def flip(slashed_grid):
    """Returns the slashed_grid, flipped left/right."""
    return '/'.join(s[::-1] for s in slashed_grid.split('/'))

def rotateL(slashed_grid):
    """Returns the left-rotation of the slashed_grid."""
    return '/'.join(''.join(s[-i-1] for s in slashed_grid.split('/')) for i in range(len(slashed_grid.split('/'))))

def genAllMatches(slashed_grid):
    """Generates all slashed_grids that can match an input slashed_grid.
    
    You will get some matches several times, but who cares, right?"""
    rotation = slashed_grid
    for i in range(4):
        rotation = rotateL(rotation)
        yield rotation
    rotation = flip(slashed_grid)
    for i in range(4):
        rotation = rotateL(rotation)
        yield rotation

def getAllRules(inp):
    rules = dict()
    for rule in inp.split('\n'):
        head, res = rule.split(' => ')
        for h in genAllMatches(head):
            rules[h] = res
    return rules

class Grid(object):
    def __init__(self, desc):
        self.grid = []
        for line in desc.split('\n'):
            self.grid.append(list(line))

    def __getitem__(self, row, col):
        if row < 0 or col < 0:
            raise IndexError
        else:
            return self.grid[row][col]

    def __str__(self):
        return '\n'.join(''.join(line) for line in self.grid)

    def __repr__(self):
        return str(self)
        

    def enhance(self, rules):
        if len(self.grid) % 2 == 0:
            new_grid = []
            for i in range(len(self.grid)//2*3):
                new_grid.append([' ']*(len(self.grid)//2*3))
            for i in range(len(self.grid)//2):
                for j in range(len(self.grid)//2):
                    subsquare = self.grid[i*2][j*2]+self.grid[i*2][j*2+1]+'/'+self.grid[i*2+1][j*2]+self.grid[i*2+1][j*2+1]
                    new_subsquare = rules[subsquare].split('/')
                    new_grid[i*3  ][j*3  ] = new_subsquare[0  ][0  ]
                    new_grid[i*3  ][j*3+1] = new_subsquare[0  ][0+1]
                    new_grid[i*3  ][j*3+2] = new_subsquare[0  ][0+2]
                    new_grid[i*3+1][j*3  ] = new_subsquare[0+1][0  ]
                    new_grid[i*3+1][j*3+1] = new_subsquare[0+1][0+1]
                    new_grid[i*3+1][j*3+2] = new_subsquare[0+1][0+2]
                    new_grid[i*3+2][j*3  ] = new_subsquare[0+2][0  ]
                    new_grid[i*3+2][j*3+1] = new_subsquare[0+2][0+1]
                    new_grid[i*3+2][j*3+2] = new_subsquare[0+2][0+2]
            self.grid = new_grid
        else:
            new_grid = []
            for i in range(len(self.grid)//3*4):
                new_grid.append([' ']*(len(self.grid)//3*4))
            for i in range(len(self.grid)//3):
                for j in range(len(self.grid)//3):
                    subsquare = self.grid[i*3][j*3]+self.grid[i*3][j*3+1]+self.grid[i*3][j*3+2]+'/'+self.grid[i*3+1][j*3]+self.grid[i*3+1][j*3+1]+self.grid[i*3+1][j*3+2]+'/'+self.grid[i*3+2][j*3]+self.grid[i*3+2][j*3+1]+self.grid[i*3+2][j*3+2]
                    new_subsquare = rules[subsquare].split('/')
                    new_grid[i*4  ][j*4  ] = new_subsquare[0  ][0  ]
                    new_grid[i*4  ][j*4+1] = new_subsquare[0  ][0+1]
                    new_grid[i*4  ][j*4+2] = new_subsquare[0  ][0+2]
                    new_grid[i*4  ][j*4+3] = new_subsquare[0  ][0+3]
                    new_grid[i*4+1][j*4  ] = new_subsquare[0+1][0  ]
                    new_grid[i*4+1][j*4+1] = new_subsquare[0+1][0+1]
                    new_grid[i*4+1][j*4+2] = new_subsquare[0+1][0+2]
                    new_grid[i*4+1][j*4+3] = new_subsquare[0+1][0+3]
                    new_grid[i*4+2][j*4  ] = new_subsquare[0+2][0  ]
                    new_grid[i*4+2][j*4+1] = new_subsquare[0+2][0+1]
                    new_grid[i*4+2][j*4+2] = new_subsquare[0+2][0+2]
                    new_grid[i*4+2][j*4+3] = new_subsquare[0+2][0+3]
                    new_grid[i*4+3][j*4  ] = new_subsquare[0+3][0  ]
                    new_grid[i*4+3][j*4+1] = new_subsquare[0+3][0+1]
                    new_grid[i*4+3][j*4+2] = new_subsquare[0+3][0+2]
                    new_grid[i*4+3][j*4+3] = new_subsquare[0+3][0+3]
            self.grid = new_grid

    def count(self, c):
        return sum(l.count(c) for l in self.grid)

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#""".strip()

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex1, res=partOne(ex1, steps=2)))

    print("")
    print("Unit test for Part Two.")


def partOne(inp, steps=5):
    grid = Grid(""".#.
..#
###""".strip())
    rules = getAllRules(inp)
    for i in range(steps):
        grid.enhance(rules)
    return grid.count('#')

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
        print("Answer for part two is : {res}".format(res=partOne(inp, steps=18)))

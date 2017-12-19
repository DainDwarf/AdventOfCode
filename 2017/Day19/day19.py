#!/usr/bin/python3
from __future__ import print_function

class Maze(object):
    def __init__(self, inp):
        self.grid = inp.split('\n') #list of list, access through [line][col], 0,0 at top-left.
        self.max_line = len(self.grid)
        self.max_col = max(len(line) for line in self.grid)

    def __getitem__(self, pos):
        line, col = pos
        if line < 0 or col < 0:
            raise IndexError("Position out of range")
        else:
            line, col = pos
            return self.grid[line][col]

    def __str__(self):
        return '\n'.join(self.grid)

    def __repr__(self):
        return str(self)

    def getStart(self):
        return (0, self.grid[0].index('|'))

    def isPath(self, line, col):
        try:
            return self[line, col] != ' '
        except IndexError:
            return False

class LettersCollector(object):
    def __init__(self, maze):
        self.maze = maze
        self.line, self.col = maze.getStart()
        self.direction = 'down'
        self.letters = ''

    def __str__(self):
        def genWithSelf():
            for line_num, line in enumerate(self.maze.grid):
                if line_num == self.line:
                    yield line[:self.col] + '@' + line[self.col+1:]
                else:
                    yield line
        return '\n'.join(genWithSelf())

    def __repr__(self):
        return str(self)

    def goDown(self):
        newline = self.line+1
        if self.maze.isPath(newline, self.col):
            self.line = newline
        else:
            raise RuntimeError("Walking out of the maze!")

    def goUp(self):
        newline = self.line-1
        if self.maze.isPath(newline, self.col):
            self.line = newline
        else:
            raise RuntimeError("Walking out of the maze!")

    def goRight(self):
        newcol = self.col+1
        if self.maze.isPath(self.line, newcol):
            self.col = newcol
        else:
            raise RuntimeError("Walking out of the maze!")

    def goLeft(self):
        newcol = max(0, self.col-1)
        if self.maze.isPath(self.line, newcol):
            self.col = newcol
        else:
            raise RuntimeError("Walking out of the maze!")

    def turn(self):
        if self.direction == 'down' or self.direction == 'up':
            if self.maze.isPath(self.line, self.col-1):
                self.direction = 'left'
            elif self.maze.isPath(self.line, self.col+1):
                self.direction = 'right'
            else:
                raise RuntimeError("Cannot turn anymore!")
        else:
            if self.maze.isPath(self.line-1, self.col):
                self.direction = 'up'
            elif self.maze.isPath(self.line+1, self.col):
                self.direction = 'down'
            else:
                raise RuntimeError("Cannot turn anymore!")

    def autoStep(self):
        try:
            if self.direction == 'up':
                self.goUp()
            elif self.direction == 'down':
                self.goDown()
            elif self.direction == 'right':
                self.goRight()
            elif self.direction == 'left':
                self.goLeft()
        except RuntimeError:
            self.turn()

        if self.maze[self.line, self.col].isalpha():
            self.letters += self.maze[self.line, self.col]


    def autoWalk(self):
        try:
            while True:
                self.autoStep()
        except RuntimeError as e:
            print("Finished due to {err}".format(err=str(e)))

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = """     |         
     |  +--+   
     A  |  C   
 F---|----E|--+
     |  |  |  D
     +B-+  +--+""".strip('\n')

    print("Unit test for Part One.")
    print("Testing on maze\n{inp}\ngives {res}".format(inp=ex, res=partOne(ex)))

    print("")
    print("Unit test for Part Two.")
    print("Test on maze\n{inp}\ngives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    maze = Maze(inp)
    walk = LettersCollector(maze)
    walk.autoWalk()
    return walk.letters

def partTwo(inp):
    pass

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.read().strip('\n')
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))

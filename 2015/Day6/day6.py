#!/usr/bin/python3
from __future__ import print_function
import re

class Grid(object):
    def __init__(self, lines=1000, columns=1000):
        self.grid = list([0]*columns for i in range(lines))

    def getLitCount(self):
        return sum(map(sum, self.grid))

    def turnOn(self, start_col, end_col, start_line, end_line):
        for i in range(start_col, end_col+1):
            for j in range(start_line, end_line+1):
                self.grid[j][i] = 1

    def turnOff(self, start_col, end_col, start_line, end_line):
        for i in range(start_col, end_col+1):
            for j in range(start_line, end_line+1):
                self.grid[j][i] = 0

    def toggle(self, start_col, end_col, start_line, end_line):
        for i in range(start_col, end_col+1):
            for j in range(start_line, end_line+1):
                self.grid[j][i] = 1 - self.grid[j][i]

    def parseInstruction(self, inp):
        instruction_re = r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)"
        action, start_col_s, start_line_s, end_col_s, end_line_s = re.match(instruction_re, inp).groups()

        start_col, end_col = min(int(start_col_s), int(end_col_s)), max(int(start_col_s), int(end_col_s))
        start_line, end_line = min(int(start_line_s), int(end_line_s)), max(int(start_line_s), int(end_line_s))

        if action == "turn on":
            self.turnOn(start_col, end_col, start_line, end_line)
        elif action == "turn off":
            self.turnOff(start_col, end_col, start_line, end_line)
        elif action == "toggle":
            self.toggle(start_col, end_col, start_line, end_line)


    def __str__(self):
        return '\n'.join(map(lambda line: ''.join(map(lambda c: '.' if c == 0 else 'X', line)), self.grid))

    def __repr__(self):
        return str(self)

class Grid2(Grid):
    def turnOn(self, start_col, end_col, start_line, end_line):
        for i in range(start_col, end_col+1):
            for j in range(start_line, end_line+1):
                self.grid[j][i] += 1

    def turnOff(self, start_col, end_col, start_line, end_line):
        for i in range(start_col, end_col+1):
            for j in range(start_line, end_line+1):
                self.grid[j][i] -= 1 if self.grid[j][i] > 0 else 0

    def toggle(self, start_col, end_col, start_line, end_line):
        for i in range(start_col, end_col+1):
            for j in range(start_line, end_line+1):
                self.grid[j][i] += 2

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = "turn on 0,0 through 999,999"
    ex2 = "toggle 0,0 through 999,0"
    ex3 = "turn off 499,499 through 500,500"

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex1, res=partOne(ex1)))
    print("Test {inp} gives {res}".format(inp=ex2, res=partOne(ex2)))
    print("Test {inp} gives {res}".format(inp=ex3, res=partOne(ex3)))
    print("Test all three gives {res}".format(res=partOne('\n'.join([ex1, ex2, ex3]))))

    ex4 = "turn on 0,0 through 0,0"
    ex5 = "toggle 0,0 through 999,999"

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex4, res=partTwo(ex4)))
    print("Test {inp} gives {res}".format(inp=ex5, res=partTwo(ex5)))


def partOne(inp):
    g = Grid(1000, 1000)
    for i in inp.split('\n'):
        g.parseInstruction(i)
    return g.getLitCount()


def partTwo(inp):
    g = Grid2(1000, 1000)
    for i in inp.split('\n'):
        g.parseInstruction(i)
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

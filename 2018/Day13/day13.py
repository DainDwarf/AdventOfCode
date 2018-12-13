#!/usr/bin/python3
from __future__ import print_function


class CrashCart(Exception):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.message = f"Carts crashing at position ({x},{y})"


class Cart(object):
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction
        self.inter_choice = "left"

    def frontPos(self):
        if self.dir == "<":
            return (self.x-1, self.y)
        elif self.dir == ">":
            return (self.x+1, self.y)
        elif self.dir == "^":
            return (self.x, self.y-1)
        elif self.dir == "v":
            return (self.x, self.y+1)
        else:
            raise RuntimeError(f"Unknown cart direction {self.dir} at position ({self.x}, {self.y})")

    def newPos(self, x, y, tile):
        # assert self.frontPos() == (x, y)
        self.x = x
        self.y = y
        if tile == "/":
            if self.dir == "<":
                self.dir = "v"
            elif self.dir == ">":
                self.dir = "^"
            elif self.dir == "^":
                self.dir = ">"
            elif self.dir == "v":
                self.dir = "<"
        elif tile == "\\":
            if self.dir == "<":
                self.dir = "^"
            elif self.dir == ">":
                self.dir = "v"
            elif self.dir == "^":
                self.dir = "<"
            elif self.dir == "v":
                self.dir = ">"
        elif tile == "+": # Hmmm
            if self.inter_choice == "left":
                self.inter_choice = "straight"
                if self.dir == "<":
                    self.dir = "v"
                elif self.dir == ">":
                    self.dir = "^"
                elif self.dir == "^":
                    self.dir = "<"
                elif self.dir == "v":
                    self.dir = ">"
            elif self.inter_choice == "straight":
                self.inter_choice = "right"
            elif self.inter_choice == "right":
                self.inter_choice = "left"
                if self.dir == "<":
                    self.dir = "^"
                elif self.dir == ">":
                    self.dir = "v"
                elif self.dir == "^":
                    self.dir = ">"
                elif self.dir == "v":
                    self.dir = "<"
            else:
                raise RuntimeError(f"Unknown intersection choice {self.inter_choice}")
        # Did you read it all? That was boring as hell...


class Tracks(object):
    def __init__(self, desc):
        self.carts = []
        self.grid = []
        for y, line in enumerate(desc.split('\n')):
            grid_line = []
            for x, char in enumerate(line):
                if char not in "<>^v":
                    grid_line.append(char)
                elif char in "^v":
                    grid_line.append('|')
                    self.carts.append(Cart(x, y, char))
                elif char in "<>":
                    grid_line.append('-')
                    self.carts.append(Cart(x, y, char))
                else:
                    raise RuntimeError(f"Unrecognized track character {char}")
            self.grid.append(grid_line)

        # Transpose to get x-coordinates first
        self.grid = list(map(list, zip(*self.grid)))

    def cellDisplay(self, x, y):
        for c in self.carts:
            if c.x == x and c.y == y:
                return c.dir
        return self.grid[x][y]

    def display(self):
        for y in range(len(self.grid[0])):
            print("".join(self.cellDisplay(x, y) for x in range(len(self.grid))))

    def tick(self, raising=True):
        for cart in sorted(self.carts, key=lambda c:(c.x, c.y)):
            x, y = cart.frontPos()
            cart.newPos(x, y, self.grid[x][y])
            if any(c.x == x and c.y == y for c in self.carts if c is not cart):
                self.carts = [c for c in self.carts if not (c.x == x and c.y == y)]
                if raising:
                    raise CrashCart(x, y)


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    line = '\n'.join("|v|||^|")
    res1 = partOne(line, display=True)
    print(f"Crash occured at position {res1}")

    example = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """
    res2 = partOne(example.strip('\n'), display=True)
    print(f"Crash occured at position {res2}")


def testTwo():
    print("Unit test for Part Two.")

    example = r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""
    res1 = partTwo(example.strip('\n'), display=True)
    print(f"Last car standing is at position {res1}")


def partOne(inp, display=False):
    track = Tracks(inp)
    try:
        while True:
            if display:
                track.display()
                print()
            track.tick()
    except CrashCart as e:
        return f"{e.x},{e.y}"


def partTwo(inp, display=False):
    track = Tracks(inp)
    while len(track.carts) > 1:
        if display:
            track.display()
            print()
        track.tick(raising=False)
    if display:
        track.display()
        print()
    c = track.carts[0]
    return f"{c.x},{c.y}"


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print()
        testTwo()
        print()
    if options.input:
        inp = options.input.read().strip('\n')
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))

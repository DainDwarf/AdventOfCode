import re
import networkx as nx


class Ground(object):
    def __init__(self):
        self.clay = set()
        self.spring = (500, 0)
        self.flow = nx.DiGraph()
        self.flow.add_node(self.spring)

    @classmethod
    def fromDescription(cls, desc):
        num_re = r"(-?\d+)"
        self = cls()
        for line in desc.split("\n"):
            if line.startswith("x"):
                x, ymin, ymax = list(map(int, re.findall(num_re, line)))
                self.addVerticalClay(x, ymin, ymax)
            elif line.startswith("y"):
                y, xmin, xmax = list(map(int, re.findall(num_re, line)))
                self.addHorizontalClay(y, xmin, xmax)
            else:
                raise RuntimeError(f"Unable to parse line {line}")
        return self

    def addVerticalClay(self, x, ymin, ymax):
        for y in range(ymin, ymax+1):
            self.clay.add((x, y))

    def addHorizontalClay(self, y, xmin, xmax):
        for x in range(xmin, xmax+1):
            self.clay.add((x, y))

    def __getitem__(self, pos):
        x, y = pos
        if (x, y) in self.clay:
            return '#'
        elif (x, y) == self.spring:
            return '+'
        elif (x, y) in self.flow:
            return '|'
        else:
            return '.'

    def display(self):
        minx = min(t[0] for t in self.clay)
        maxx = max(t[0] for t in self.clay)
        miny = 0
        maxy = max(t[1] for t in self.clay)
        for y in range(miny, maxy+1):
            print("".join(self[(x, y)] for x in range(minx, maxx+1)))

# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    inp = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""
    gr = Ground.fromDescription(inp)
    gr.display()
    # print(f"Test {inp} gives {res}")


def testTwo():
    print("Unit test for Part Two.")

    inp = "toto"
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")


def partOne(inp):
    pass


def partTwo(inp):
    pass


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
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))

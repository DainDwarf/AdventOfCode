#!/usr/bin/python3
from __future__ import print_function
import re


class Fabric(object):
    cut_re = re.compile(
        r"""^\#(?P<id>\d+)                                  # ID of the cut
            \ @\                                            # spacing
            (?P<start_width>\d+),(?P<start_height>\d+):\    # Start position of the cut
            (?P<cut_width>\d+)x(?P<cut_height>\d+)          # Length of the cut
            $""", re.X)
    def __init__(self, width, height):
        self.__cells = [ [[] for _ in range(width)] for _ in range(height)]
        self.__height = height
        self.__width = width

    def __getitem__(self, pos):
        h, w = pos
        return self[h][w]

    def addCut(self, cut_description):
        cut = self.cut_re.match(cut_description)
        if cut:
            cut_id = int(cut.group('id'))
            start_h = int(cut.group('start_height'))
            start_w = int(cut.group('start_width'))
            len_h = int(cut.group('cut_height'))
            len_w = int(cut.group('cut_width'))
            for h in range(start_h, start_h+len_h):
                for w in range(start_w, start_w+len_w):
                    try:
                        self.__cells[h][w] += [cut_id]
                    except IndexError:
                        print(f"Wrong index ({h}:{w})")
                        raise
        else:
            raise RuntimeError(f"Cannot parse cut description {cut_description}")

    def display(self):
        def __cell_display(c):
            if len(c) > 1:
                return 'X'
            elif len(c) == 0:
                return '.'
            elif c[0] > 9:
                return '#'
            else:
                return str(c[0])

        return "\n".join(
            "".join(__cell_display(c) for c in line
            ) for line in self.__cells
        )

    def count_overlaps(self):
        return sum(sum(len(c) > 1 for c in line) for line in self.__cells)

    def untouched_claims(self):
        claims_states = dict()
        for line in self.__cells:
            for cell in line:
                if len(cell) > 1:
                    for claim in cell:
                        claims_states[claim] = False
                elif len(cell) == 1:
                    claim = cell[0]
                    if not claim in claims_states:
                        claims_states[claim] = True
        ret = []
        for claim, free in claims_states.items():
            if free:
                ret.append(claim)
        return ret


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    ex123 = "#123 @ 3,2: 5x4"
    fabric = Fabric(11, 9)
    fabric.addCut(ex123)
    print("Fabric 11x9 for example {inp} gives\n{res}".format(inp=ex123, res=fabric.display()))
    print()

    ex1 = "#1 @ 1,3: 4x4"
    ex2 = "#2 @ 3,1: 4x4"
    ex3 = "#3 @ 5,5: 2x2"
    ex_full = "\n".join([ex1, ex2, ex3])
    fabric = Fabric(8, 8)
    fabric.addCut(ex1)
    fabric.addCut(ex2)
    fabric.addCut(ex3)
    print("Fabric 8x8 for examples\n{inp}\ngives\n{res}".format(inp=ex_full, res=fabric.display()))

    print("This has {res} overlaps".format(inp=ex_full, res=partOne(ex_full, 8, 8)))


def testTwo():
    print("Unit test for Part Two.")
    ex1 = "#1 @ 1,3: 4x4"
    ex2 = "#2 @ 3,1: 4x4"
    ex3 = "#3 @ 5,5: 2x2"
    ex_full = "\n".join([ex1, ex2, ex3])
    fabric = Fabric(8, 8)
    fabric.addCut(ex1)
    fabric.addCut(ex2)
    fabric.addCut(ex3)
    print("Fabric 8x8 for examples\n{inp}\ngives\n{res}".format(inp=ex_full, res=fabric.display()))

    print("Untouched claims are {claims}".format(claims=partTwo(ex_full, 8, 8)))


def partOne(inp, height=1000, width=1000):
    fabric = Fabric(height, width)
    for line in inp.split("\n"):
        fabric.addCut(line)
    return fabric.count_overlaps()


def partTwo(inp, height=1000, width=1000):
    fabric = Fabric(height, width)
    for line in inp.split("\n"):
        fabric.addCut(line)
    return fabric.untouched_claims()


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print("")
        testTwo()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))

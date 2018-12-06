#!/usr/bin/python3
from __future__ import print_function
from typing import List, Tuple


def manhattan(p1, p2):
    return abs(p2[0]-p1[0]) + abs(p2[1]-p1[1])


class FiniteGrid(object):
    def __init__(self, points: List[Tuple[int, int]]):
        self.points = points
        self.minx = min(p[0] for p in points)
        self.maxx = max(p[0] for p in points)
        self.miny = min(p[1] for p in points)
        self.maxy = max(p[1] for p in points)

    @classmethod
    def fromDescription(cls, desc):
        points = [tuple(map(int, l.split(", "))) for l in desc.split("\n")]
        return cls(points)

    def isBorder(self, p):
        """Tells if a point is on border of the focuses.

        Because a focus having an infinite region for part one
        is equivalent to the focus being on the border."""
        return p[0] in (self.minx, self.maxx) or p[1] in (self.miny, self.maxy)

    def closest(self, p):
        """Returns index of closest point, or None if equidistant to several points."""
        all_distances = list(map(lambda x:manhattan(p, x), self.points))
        min_distance = min(all_distances)
        if all_distances.count(min_distance) == 1:
            return all_distances.index(min_distance)

    def sumDistances(self, p):
        return sum(map(lambda x:manhattan(p, x), self.points))

    def biggestFiniteArea(self):
        """Returns, well, solution for part one..."""
        areas = {i: 0 for i, p in enumerate(self.points) if not self.isBorder(p)}
        for x in range(self.minx, self.maxx+1):
            for y in range(self.miny, self.maxy+1):
                close = self.closest((x, y))
                if close in areas:
                    areas[close] += 1
        return max(areas.values())

    def safeRegion(self, max_sum):
        """Returns, well, solution for part two..."""
        area = 0
        for x in range(self.minx, self.maxx+1):
            for y in range(self.miny, self.maxy+1):
                if self.sumDistances((x, y)) < max_sum:
                    area += 1
        return area


# That's handy, the Advent of Code gives unittests.
def testOne():
    ex = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

    print("Unit test for Part One.")
    print("Test on example gives {res}".format(inp=ex, res=partOne(ex)))


def testTwo():
    ex = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

    print("Unit test for Part Two.")
    print("Test on example gives {res}".format(inp=ex, res=partTwo(ex, 32)))


def partOne(inp):
    grid = FiniteGrid.fromDescription(inp)
    return grid.biggestFiniteArea()


def partTwo(inp, sum_distances=10000):
    grid = FiniteGrid.fromDescription(inp)
    return grid.safeRegion(sum_distances)


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

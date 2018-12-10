#!/usr/bin/python3
from __future__ import print_function
import re


class Star(object):
    def __init__(self, position, velocity):
        self.pos = position
        self.vel = velocity

    def step(self):
        self.pos = (self.pos[0]+self.vel[0], self.pos[1]+self.vel[1])


class StarsSimulator(object):
    def __init__(self):
        self.stars = []

    @classmethod
    def fromDescription(cls, desc):
        self = cls()
        star_re = re.compile(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>")
        for line in desc.split('\n'):
            p_x, p_y, v_x, v_y = map(int, star_re.match(line).groups())
            self.addStar((p_x, p_y), (v_x, v_y))
        return self

    def addStar(self, position, velocity):
        self.stars.append(Star(position, velocity))

    def step(self):
        for star in self.stars:
            star.step()

    def __getitem__(self, pos):
        x, y = pos
        for s in self.stars:
            if s.pos[0] == x and s.pos[1] == y:
                return s

    def display(self):
        minx = min(s.pos[0] for s in self.stars)
        maxx = max(s.pos[0] for s in self.stars)
        miny = min(s.pos[1] for s in self.stars)
        maxy = max(s.pos[1] for s in self.stars)
        for y in range(miny, maxy+1):
            print("".join("#" if self[(x, y)] is not None else "." for x in range(minx, maxx+1)))

    def aligned(self):
        #Find at least 4 stars aligned vertically and call it a day.
        for star in self.stars:
            if      self[(star.pos[0]-1, star.pos[1])] is not None \
                and self[(star.pos[0]-2, star.pos[1])] is not None \
                and self[(star.pos[0]-3, star.pos[1])] is not None \
                and self[(star.pos[0]-4, star.pos[1])] is not None :
                return True
        return False


# That's handy, the Advent of Code gives unittests.
def testOne():
    ex = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""

    print("Unit test for Part One.")
    # print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))
    partOne(ex)


def testTwo():
    ex = "tata"
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    stars = StarsSimulator.fromDescription(inp)
    i = 1
    while not stars.aligned():
        print(i)
        stars.step()
        i += 1
    stars.display()


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
        print("")
        testTwo()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))

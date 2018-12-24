import re
import math


def manhattan(p1, p2):
    return sum(map(lambda t: abs(t[0]-t[1]), zip(p1, p2)))


class Octahedron(object):
    """The bots define octahedrons, also called 3-ball for the L1 metric."""
    def __init__(self, pos, r):
        self.pos = pos
        self.r = r

    def intersect(self, other):
        """Intersection can simply be tested by mesuring the distance between the centers."""
        return manhattan(self.pos, other.pos) <= self.r+other.r


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    inp = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1"""

    res = partOne(inp)
    print(f"Example answer is {res}.")


def testTwo():
    print("Unit test for Part Two.")

    inp = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""
    res = partTwo(inp)
    print(f"Test {inp} gives {res}")


def partOne(inp):
    num_re = r"(-?\d+)"
    bots = []
    for line in inp.split('\n'):
        x, y, z, r = list(map(int, re.findall(num_re, line)))
        bots.append(((x, y, z), r))
    best_bot, bot_range = max(bots, key=lambda t:t[1])
    return sum(1 if manhattan(b, best_bot) <= bot_range else 0 for b, _ in bots)


def partTwo(inp):
    num_re = r"(-?\d+)"
    bots = []
    for line in inp.split('\n'):
        x, y, z, r = list(map(int, re.findall(num_re, line)))
        bots.append(Octahedron((x, y, z), r))
    max_range = max(b.r for b in bots)
    #Avoid issues by rounding to next power of 2
    max_range = 2**math.ceil(math.log2(max_range))


    #Now, some dichotomy:
    search_bots = [Octahedron((0, 0, 0), max_range)]
    current_r = max_range
    while current_r > 1:
        print("Range {r}, searching through {num} subspaces".format(r=current_r, num=len(search_bots)))
        sub_search = []
        sub_r = current_r//2
        for bot in search_bots:
            x, y, z = bot.pos
            sub_search.append(Octahedron((x+sub_r, y, z), sub_r))
            sub_search.append(Octahedron((x-sub_r, y, z), sub_r))
            sub_search.append(Octahedron((x, y+sub_r, z), sub_r))
            sub_search.append(Octahedron((x, y-sub_r, z), sub_r))
            sub_search.append(Octahedron((x, y, z+sub_r), sub_r))
            sub_search.append(Octahedron((x, y, z-sub_r), sub_r))
            #There are two missing?
        search_bots = sub_search
        current_r = sub_r
        raise NotImplementedError("Nope")


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

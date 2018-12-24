import re
import math
import heapq


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

    def __lt__(self, other):
        if self.r == other.r:
            return manhattan((0, 0, 0), self.pos) < manhattan((0, 0, 0), other.pos)
        else:
            return self.r<other.r

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
    print(f"Second example gives {res}")


def partOne(inp):
    num_re = r"(-?\d+)"
    bots = []
    for line in inp.split('\n'):
        x, y, z, r = list(map(int, re.findall(num_re, line)))
        bots.append(((x, y, z), r))
    best_bot, bot_range = max(bots, key=lambda t:t[1])
    return sum(1 if manhattan(b, best_bot) <= bot_range else 0 for b, _ in bots)


class OctaSearchQueue(object):
    """Priorty queue wrapper for the octahedron search."""
    def __init__(self, bots):
        self.__h = []
        self.bots = bots

    def add(self, octa):
        weight = sum(1 if octa.intersect(b) else 0 for b in self.bots)
        dist = manhattan((0, 0, 0), octa.pos)
        heapq.heappush(self.__h, (-weight, octa))

    def pop(self):
        """Pop the best candidate."""
        return heapq.heappop(self.__h)[1]

    def __bool__(self):
        return bool(self.__h)

        
def partTwo(inp):
    num_re = r"(-?\d+)"
    bots = []
    for line in inp.split('\n'):
        x, y, z, r = list(map(int, re.findall(num_re, line)))
        bots.append(Octahedron((x, y, z), r))
    max_x = max(abs(b.pos[0]) for b in bots)
    max_y = max(abs(b.pos[1]) for b in bots)
    max_z = max(abs(b.pos[2]) for b in bots)
    max_range = max(max_x, max_y, max_z)

    #Now, some dichotomy:
    search_bots = OctaSearchQueue(bots)
    search_bots.add(Octahedron((0, 0, 0), max_range))
    while search_bots:
        octa = search_bots.pop()
        if octa.r == 0:
            return manhattan((0, 0, 0), octa.pos)
        offset = math.floor(octa.r/3) if octa.r >= 3 else 1 if octa.r > 0 else 0
        sub_r = octa.r - offset
        x, y, z = octa.pos
        search_bots.add(Octahedron((x+offset, y, z), sub_r))
        search_bots.add(Octahedron((x-offset, y, z), sub_r))
        search_bots.add(Octahedron((x, y+offset, z), sub_r))
        search_bots.add(Octahedron((x, y-offset, z), sub_r))
        search_bots.add(Octahedron((x, y, z+offset), sub_r))
        search_bots.add(Octahedron((x, y, z-offset), sub_r))


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

#!/usr/bin/python3
from __future__ import print_function
from collections import Counter

class Particle(object):
    def __init__(self, description):
        pos, vel, acc = map(lambda s: s.split('=')[1].strip('<>').split(','), description.split(', '))
        self.pos = list(map(int, pos))
        self.vel = list(map(int, vel))
        self.acc = list(map(int, acc))

    def __str__(self):
        return "p=<{px},{py},{pz}>, v=<{vx},{vy},{vz}>, a=<{ax},{ay},{az}>".format(
              px=self.pos[0], py=self.pos[1], pz=self.pos[2]
            , vx=self.vel[0], vy=self.vel[1], vz=self.vel[2]
            , ax=self.acc[0], ay=self.acc[1], az=self.acc[2]
        )

    def __repr__(self):
        return str(self)

    def tick(self):
        self.vel = list(v+a for v, a in zip(self.vel, self.acc))
        self.pos = list(p+v for p, v in zip(self.pos, self.vel))

def distance(pos):
    return sum(map(abs, pos))

def closests(particles):
    min_dist = min(map(lambda p:distance(p.pos), particles))
    return list(particles.index(p) for p in particles if distance(p.pos) == min_dist)

def genCollides(particles):
    d = dict()
    for p in particles:
        try:
            d[tuple(p.pos)].append(p)
        except KeyError:
            d[tuple(p.pos)] = [p]
    for l in d.values():
        if len(l) > 1:
            yield from l

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = """p=<3,0,0>, v=<2,0,0>, a=<-1,0,0>
p=<4,0,0>, v=<0,0,0>, a=<-2,0,0>""".strip()

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex1, res=partOne(ex1, 4, True)))

    ex2="""p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>
p=<3,0,0>, v=<-1,0,0>, a=<0,0,0>""".strip()

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex2, res=partTwo(ex2, 4, True)))


def partOne(inp, test_ticks=1000, debug=False):
    particles = list(map(Particle, inp.split('\n')))
    for i in range(test_ticks):
        if debug:
            print("Closest particles are: {clos}".format(clos=closests(particles)))
        for p in particles:
            p.tick()
    return closests(particles)

def partTwo(inp, test_ticks=1000, debug=False):
    particles = list(map(Particle, inp.split('\n')))
    for i in range(test_ticks):
        for p in genCollides(particles):
            particles.pop(particles.index(p))
        if debug:
            print("There are {n} particles left".format(n=len(particles)))
        for p in particles:
            p.tick()
    return len(particles)

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

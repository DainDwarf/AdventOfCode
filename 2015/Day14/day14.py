#!/usr/bin/python3
from __future__ import print_function
import re

class Reindeer(object):
    def __init__(self, name, speed, speed_length, rest_length):
        self.name = name
        self.speed = speed #in km/s
        self.speed_length = speed_length #in s
        self.rest_length = rest_length

    def run(self, amount):
        distance = 0
        while amount > 0:
            distance += self.speed*min(self.speed_length, amount)
            amount -= self.speed_length + self.rest_length
        return distance

def parseToReindeer(s):
    reindeer_re = r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\."
    name, speed, speed_length, rest_length = re.match(reindeer_re, s).groups()
    return Reindeer(name, int(speed), int(speed_length), int(rest_length))

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""

    ex1 = parseToReindeer("Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.")
    ex2 = parseToReindeer("Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.")

    print("Unit test for Part One.")
    print("Running {inp} for 1000 seconds gives {res} km".format(inp=ex1.name, res=ex1.run(1000)))
    print("Running {inp} for 1000 seconds gives {res} km".format(inp=ex2.name, res=ex2.run(1000)))

    print("")
    print("Unit test for Part Two.")
    print("Best score for example is {res}".format(res=partTwo(ex.strip(), 1000)))


def partOne(inp, amount=2503):
    return max(map(lambda r: r.run(amount), map(parseToReindeer, inp.split('\n'))))

def partTwo(inp, amount=2503):
    scoring = dict((r, 0) for r in map(parseToReindeer, inp.split('\n')))
    for step in range(1, amount+1):
        best_dist = max(map(lambda r: r.run(step), scoring.keys()))
        for r in scoring.keys():
            if r.run(step) == best_dist:
                scoring[r] += 1
    return max(scoring.values())

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

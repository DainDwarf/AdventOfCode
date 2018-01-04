#!/usr/bin/python3
from __future__ import print_function

class Emulator(object):
    def __init__(self, instructions):
        self._reg = dict((l, 0) for l in 'abcdefgh')
        self._int = list(i.strip().split() for i in instructions.split('\n'))
        self._cur = 0

    def __getitem__(self, k):
        try:
            return self._reg[k]
        except KeyError:
            return int(k)

    def set(self, x, y):
        self._reg[x] = self[y]
        self._cur += 1

    def sub(self, x, y):
        self._reg[x] -= self[y]
        self._cur += 1

    def mul(self, x, y):
        self._reg[x] *= self[y]
        self._cur += 1

    def jnz(self, x, y):
        if self[x] != 0:
            self._cur += self[y]
        else:
            self._cur += 1

    def doStep(self, debug=False):
        if debug:
            print(self._int[self._cur])
            instruction = self._int[self._cur][0]
            args = self._int[self._cur][1:]
        return getattr(self, instruction)(*args)

    def partOne(self):
        ret = 0
        while len(self._int) > self._cur >=0:
            instruction = self._int[self._cur][0]
            args = self._int[self._cur][1:]
            getattr(self, instruction)(*args)
            if instruction == 'mul':
                ret += 1
        return ret

    def partTwo(self):
        self._reg['a'] = 1
        while len(self._int) > self._cur >=0:
            instruction = self._int[self._cur][0]
            args = self._int[self._cur][1:]
            getattr(self, instruction)(*args)
        return self['h']

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    print("No unit test for Part One.")
    print("")
    print("Unit test for Part Two.")


def partOne(inp):
    emu = Emulator(inp)
    return emu.partOne()


def partTwo(inp):
    emu = Emulator(inp)
    return emu.partTwo()


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

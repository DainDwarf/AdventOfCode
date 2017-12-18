#!/usr/bin/python3
from __future__ import print_function

class Emulator(object):
    def __init__(self, instructions):
        self.__reg = dict((l, 0) for l in 'abcdefghijklmnopqrstuvwxyz')
        self.__reg['sound'] = 0
        self.__int = list(i.strip().split() for i in instructions.split('\n'))
        self.__cur = 0

    def __getitem__(self, k):
        try:
            return self.__reg[k]
        except KeyError:
            return int(k)

    def snd(self, x):
        self.__reg['sound'] = self[x]
        self.__cur += 1

    def set(self, x, y):
        self.__reg[x] = self[y]
        self.__cur += 1

    def add(self, x, y):
        self.__reg[x] += self[y]
        self.__cur += 1

    def mul(self, x, y):
        self.__reg[x] *= self[y]
        self.__cur += 1

    def mod(self, x, y):
        self.__reg[x] %= self[y]
        self.__cur += 1

    def rcv(self, x):
        if self[x] != 0:
            return self.__reg['sound']
        self.__cur += 1

    def jgz(self, x, y):
        if self[x] > 0:
            self.__cur += self[y]
        else:
            self.__cur += 1

    def emulateUntilRcv(self):
        ret = None
        while True:
            instruction, *args = self.__int[self.__cur]
            ret = getattr(self, instruction)(*args)
            if ret is not None:
                break
        return ret


# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2""".strip()

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex)))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    emu = Emulator(inp)
    return emu.emulateUntilRcv()


def partTwo(inp):
    pass

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

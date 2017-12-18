#!/usr/bin/python3
from __future__ import print_function
from queue import Queue, Empty

class Emulator(object):
    def __init__(self, instructions):
        self._reg = dict((l, 0) for l in 'abcdefghijklmnopqrstuvwxyz')
        self._reg['sound'] = 0
        self._int = list(i.strip().split() for i in instructions.split('\n'))
        self._cur = 0

    def __getitem__(self, k):
        try:
            return self._reg[k]
        except KeyError:
            return int(k)

    def snd(self, x):
        self._reg['sound'] = self[x]
        self._cur += 1

    def set(self, x, y):
        self._reg[x] = self[y]
        self._cur += 1

    def add(self, x, y):
        self._reg[x] += self[y]
        self._cur += 1

    def mul(self, x, y):
        self._reg[x] *= self[y]
        self._cur += 1

    def mod(self, x, y):
        self._reg[x] %= self[y]
        self._cur += 1

    def rcv(self, x):
        if self[x] != 0:
            return self._reg['sound']
        self._cur += 1

    def jgz(self, x, y):
        if self[x] > 0:
            self._cur += self[y]
        else:
            self._cur += 1

    def doStep(self, debug=False):
        if debug:
            print(self._int[self._cur])
        instruction, *args = self._int[self._cur]
        return getattr(self, instruction)(*args)

    def emulateUntilRcv(self):
        ret = None
        while True:
            ret = self.doStep()
            if ret is not None:
                break
        return ret


class ConcurrentEmulator(Emulator):
    def __init__(self, instructions, programID, out_channel, in_channel):
        super().__init__(instructions)
        self._reg['p'] = programID
        self._reg.pop('sound')
        self.out_ch = out_channel
        self.in_ch = in_channel
        self.send_count = 0
        self._wait = False

    def snd(self, x):
        self.out_ch.put_nowait(self[x])
        self._cur += 1
        self.send_count += 1

    def rcv(self, x):
        try:
            self._reg[x] = self.in_ch.get_nowait()
            self._cur += 1
        except Empty:
            self._wait = True

    def isWaiting(self):
        return self._wait

    def getSendCount(self):
        return self.send_count

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = """set a 1
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
    print("Test {inp} gives {res}".format(inp=ex1, res=partOne(ex1)))

    ex2 = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d""".strip()

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex2, res=partTwo(ex2)))


def partOne(inp):
    emu = Emulator(inp)
    return emu.emulateUntilRcv()


def partTwo(inp):
    zeroToOne = Queue()
    oneToZero = Queue()
    emu0 = ConcurrentEmulator(inp, 0, zeroToOne, oneToZero)
    emu1 = ConcurrentEmulator(inp, 1, oneToZero, zeroToOne)
    while (not emu0.isWaiting()) or (not emu1.isWaiting()):
        emu0.doStep()
        emu1.doStep()
    return emu1.getSendCount()


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
